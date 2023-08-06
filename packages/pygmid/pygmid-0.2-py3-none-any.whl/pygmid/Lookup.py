import copy
import logging
import os.path
import pickle

import numpy as np
import scipy.io
from scipy.interpolate import interpn


class Lookup:
    def __init__(self, filename="MOS.mat"):
        self.__setup(filename)
        self.__modefuncmap = {1 : self._SimpleLK,
                              2 : self._SimpleLK,  
                              3 : self._RatioVRatioLK}

    def __setup(self, filename):
        """
        Setup the Lookup object

        Assigns loaded data and defaults
        to the DATA member variable

        Args:
            filename
        """
        data = self.__load(filename)
        if data is not None:
            self.__DATA = data
        else:
            raise Exception(f"Data could not be loaded from {filename}")
        self.__default = {}
        self.__default['L'] = min(self.__DATA['L'])
        self.__default['VGS'] = self.__DATA['VGS']
        self.__default['VDS'] = max(self.__DATA['VDS'])/2
        self.__default['VSB'] = 0.0
        self.__default['METHOD'] = 'pchip'
        
    def __load(self, filename):
        """
        Function to load data from file

        Loads array data from file. Currently supports .mat files only.
        .mat is parsed to convert MATLAB cell data into a dictionary of
        arrays. Data is loaded from value with first non-header key. 
        Python interprets MATLAB cell structures as 1-D nests. Nested 
        data is accessed and deep copied to member DATA variable

        Args:
            filename

        Returns:
            First MATLAB variable encountered in file as data
        """
        if filename.endswith('.mat'):
            # parse .mat file into dict object
            mat = scipy.io.loadmat(filename, matlab_compatible=True)

            for k in mat.keys():
                if not( k.startswith('__') and k.endswith('__') ):
                    mat = mat[k]
                    data = {k.upper():copy.deepcopy(np.squeeze(mat[k][0][0])) for k in mat.dtype.names}
                    return data   
        # !TODO add functionality to load other data structures
        return None

    def __getitem__(self, key):
        """
        __getitem__ dunder method overwritten to allow convenient
        pseudo array access to member data. Returns a copy of the
        member array.
        """
        if key not in self.__DATA.keys():
            raise ValueError(f"Lookup table does not contain this data")

        return np.copy(self.__DATA[key])

    def _modeset(self, outkey, varkey):
        """
        Function to set lookup mode
            MODE1: output is single variable, variable arg is single
            MODE2: output is ratio, variable arg is single
            MODE3: output is ratio, variable arg is ratio

        Args:
            outkey: keywords (list) of output argument
            varkey: keywords (list) of variable argument

        Returns:
            mode (integer). Error if invalid mode selected
        """
        out_ratio = isinstance(outkey, list) and len(outkey) > 1
        var_ratio = isinstance(varkey, list) and len(varkey) > 1
        if out_ratio and var_ratio:
            mode = 3
        elif out_ratio and (not var_ratio):
            mode = 2
        elif (not out_ratio) and (not var_ratio):
            mode = 1
        else:
            raise Exception("Invalid syntax or usage mode! Please check documentation.")
        
        return mode

    def lookup(self, out, **kwargs):
        """
        Alias for look_up() function
        """
        return self.look_up(out, **kwargs)

    def look_up(self, out, **kwargs):
        """
        Entry method for lookup functionality

        Sanitises input. Extracts the variable key as first key value pair
        in kwargs dict. Both the outkey and varkey are converted to lists.
        String is split based on _ character.

        Mode is determined and appropriate lookup function is called from
        modefuncmap dict

        Args:
            out: desired variable to be interpolated 'GM', 'ID' etc
            kwargs: keyword arguments (dict). First key-value pair is
                    variable argument

        Returns:
            y: interpolated data, [] if erroneous mode selected
        """
        outkeys = out.upper().split('_')
        varkeys, vararg = next(iter((kwargs.items()))) if kwargs else (None, None)
        varkeys = str(varkeys).upper().split('_')

        kwargs = {k.upper(): v for k, v in kwargs.items()} # convert kwargs to upper
        pars = {k:kwargs.get(k, v) for k, v in self.__default.items()} # extracts parameters from kwargs
        
        try:
            mode = self._modeset(outkeys, varkeys)
        except:
            return []
        # appropriate lookup function is called with modefuncmap dict
        y = self.__modefuncmap.get(mode) (outkeys, varkeys, pars)
        
        return y

    def _SimpleLK(self, outkeys, varkeys, pars):
        """
        Lookup for Modes 1 and 2

        Args:
            outkeys: list of keys for desired output e.g ['GM', 'ID'] for 'GM_ID'
            varkeys: unused
            pars: dict ontaining L, VGS, VDS and VSB data
        Output:
            output: interpolated data specified by outkeys Squeezed to remove extra
                    dimensions
        """
        if len(outkeys) > 1:
            num, den = outkeys
            ydata =  self.__DATA[num]/self.__DATA[den]
        else:
            outkey = outkeys[0]
            ydata = self.__DATA[outkey]

        points = (self.__DATA['L'], self.__DATA['VGS'], self.__DATA['VDS'],\
            self.__DATA['VSB'])
        xi_mesh = np.array(np.meshgrid(pars['L'], pars['VGS'], pars['VDS'], pars['VSB']))
        xi = np.rollaxis(xi_mesh, 0, 5)
        xi = xi.reshape(int(xi_mesh.size/4), 4)

        output = interpn(points, ydata, xi).reshape(len(np.atleast_1d(pars['L'])), \
            len(np.atleast_1d(pars['VGS'])), len(np.atleast_1d(pars['VDS'])),\
                 len(np.atleast_1d(pars['VSB'])) )
        # remove extra dimensions
        output = np.squeeze(output)

        return output

    def _RatioVRatioLK(self):
        pass
        
    def lookupVGS(self, **kwargs):
        return self.look_upVGS(**kwargs)

    def look_upVGS(self, **kwargs):
        pass