# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 14:28:29 2015

@author: stvhoey
"""

import os
import sys

import numpy as np
import scipy.io as sio

def convert_ascat_to_matlab(filename, grid_point_id='all', byte2skip=208):
    """read in the .idx and .dat file combinationa dn convert data to matlab readable .mat-files

    Parameters
    -----------
    filename : str
        name (relative path or full path) of the .idx and .dat file combination
    grid_point_id : int or 'all'
        ask for a specific gridpoint or let them all convert and write in different .mat-structures
    byte2skip : int
        number of bytes to skip to leave out the header file
    """
    # provided data structures of the partner organisation
    struct_idx = np.dtype([('gpi', np.int32)])
    struct_dat = np.dtype([('jd', np.double), ('sig', np.float32), ('sig_noise', np.float32),
                           ('dir', np.dtype('S1')), ('pdb',np.ubyte), ('azcorr_flag',
                                                                       np.dtype([('f', np.ubyte),
                                                                                 ('m',np.ubyte),
                                                                                 ('a', np.ubyte)]))])
    # reading in the index file
    f = open("".join([filename, ".idx"]), "rb")  # reopen the file
    f.seek(byte2skip, os.SEEK_SET)  # seek
    idx_data = np.fromfile(f, dtype=struct_idx).astype('int32') # astype erbij om de omzetting te verzekeren

    # extract the unique indexes available in this file
    unique_idx = np.unique(idx_data)

    # reading in the data file
    f = open(''.join([filename, ".dat"]), "rb")  # reopen the file
    f.seek(byte2skip, os.SEEK_SET)  # seek
    data = np.fromfile(f, dtype=struct_dat)

    # writing a file for each gridpoint
    if grid_point_id == 'all':
        for grid_point in unique_idx:
            data_dict = {}
            indxs_point = np.where(idx_data == grid_point)
            current_selection = data[indxs_point]
            data_dict[''.join(['grid_point_', str(grid_point)])] = current_selection
            sio.savemat(''.join([filename, '_', str(grid_point)]), data_dict) #.mat is automatically appended
    else:
        if grid_point_id in unique_idx:
            grid_point = grid_point_id
            data_dict = {}
            indxs_point = np.where(idx_data == grid_point)
            current_selection = data[indxs_point]
            data_dict[''.join(['grid_point_',str(grid_point)])] = current_selection
            sio.savemat(''.join([filename, '_', str(grid_point)]), data_dict) #.mat is automatically appended
        else:
            raise Exception('grid_point id not available...')

    return data_dict


def main(argv=None):
    """
    Export all grid point data as matlab .mat file
    """
    #argv[0] is always the file name itself
    if sys.argv[2] == 'all':
        convert_ascat_to_matlab(sys.argv[1], grid_point_id='all', byte2skip=208)
    else:
        try:
            convert_ascat_to_matlab(sys.argv[1],
                                grid_point_id=int(sys.argv[2]),
                                byte2skip=208)
        except:
            raise Exception('Conversion failed...')

if __name__ == "__main__":
    sys.exit(main())
