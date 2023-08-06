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
        Function to load data from .mat object

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
                    data = {k:copy.deepcopy(np.squeeze(mat[k][0][0])) for k in mat.dtype.names}
                    return data   
        # !TODO add functionality to load other data structures
        return None

    def __getitem__(self, key):
        if key not in self.__DATA.keys():
            raise ValueError(f"Lookup table does not contain this data")

        return self.__DATA[key]

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
        return self.look_up(out, **kwargs)

    def look_up(self, out, **kwargs):

        outkeys = out.upper().split('_')
        varkeys, vararg = next(iter((kwargs.items()))) if kwargs else (None, None)
        varkeys = str(varkeys).upper().split('_')

        # convert kwargs to upper
        kwargs = {k.upper(): v for k, v in kwargs.items()}
        # extracts parameters from kwargs
        pars = {k:kwargs.get(k, v) for k, v in self.__default.items()}
        
        try:
            mode = self._modeset(outkeys, varkeys)
        except:
            return []
        
        y = self.__modefuncmap.get(mode) (outkeys, varkeys, pars)
        
        return y

    def _SimpleLK(self, outkeys, varkey, pars):
        
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