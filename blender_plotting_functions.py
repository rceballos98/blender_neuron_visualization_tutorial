import numpy as np
# from mayavi import mlab
import pdb
import h5py
import pickle
import scipy
import sys
sys.path.append('/Users/rodrigo/repos/syntist')
import utils
import copy


# from scipy.spatial import ConvexHull
voxel_size = np.array([40,4,4])

def get_locations_for_partners(locs, partners, ids, labels, neuron_id1, neuron_id2):
    # pre_post = np.where(partners == [neuron_id1, neuron_id2])
    pre = []
    post = []

    for i, partner in enumerate(partners):
        loc_1 = locs[np.where(partner[0] == ids)[0][0]]
        loc_2 = locs[np.where(partner[1] == ids)[0][0]]

        # pdb.set_trace()
        loc_voxel_1 = (np.round(loc_1/voxel_size)).astype('int')
        label_1 = labels[loc_voxel_1[0],loc_voxel_1[1],loc_voxel_1[2]]

        loc_voxel_2 = (np.round(loc_2/voxel_size)).astype('int')
        label_2 = labels[loc_voxel_2[0],loc_voxel_2[1],loc_voxel_2[2]]

        if label_1 == neuron_id1 and label_2 == neuron_id2:
            pre.append([loc_1, loc_2])

        if label_1 == neuron_id2 and label_2 == neuron_id1:
            post.append([loc_1, loc_2])

    return pre, post

def switch_zx(arr):
    arr_copy = copy.copy(arr)
    arr_copy[2] = arr[0]
    arr_copy[0] = arr[2]
    return arr_copy