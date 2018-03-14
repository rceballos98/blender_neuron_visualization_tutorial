import numpy as np
from mayavi import mlab
import pdb
import h5py
import pickle
import scipy
import sys
sys.path.append('/Users/rodrigo/repos/syntist')
import utils
import copy

def get_components(points):
    d = {}
    points = np.array(points)
    d['x'] = points.T[2]*voxel_size[2]
    d['y'] = points.T[1]*voxel_size[1]
    d['z'] = points.T[0]*voxel_size[0]
    return d;

def get_vectors(pre_points, post_points):
    vecs = post_points - pre_points
    locs = get_components(pre_points)
    vecs = get_components(vecs)
    return locs, vecs

def get_vectors_above_thresh(pre_points, post_points, scores, threshold):
    i = scores > threshold
    if any(i == True):
        pre_points = pre_points[i]
        post_points = post_points[i]
        return get_vectors(pre_points, post_points);
    else:
        return get_xyz_dir(), get_xyz_dir()

def get_xyz_dir():
    d = {}
    d['x'],d['y'],d['z'] = np.array([]),np.array([]),np.array([])
    return d

def get_test_synlocs(path='/Users/rodrigo/repos/neuronTracing/paper/data/synloc_600000_small.pickle'):
    with open(path, 'r') as f:
        print('loading synlocs %s' % path)
        splitted_synlocs = cPickle.load(f)
    return splitted_synlocs

def get_vectors_above_thresh_over_synlocs(synlocs, threshold):
    locs = get_xyz_dir()
    vecs = get_xyz_dir()

    for synloc in synlocs:
        pre_points = np.array(synloc.all_locs_pre)
        post_points = np.array(synloc.all_locs_post)
        scores = np.array(synloc.affinities)
        assert(len(pre_points) == len(post_points) and len(pre_points) == len(scores))
        l, v = get_vectors_above_thresh(pre_points, post_points, scores, threshold)
        # pdb.set_trace()
        locs['x'] = np.append(locs['x'], l['x'])
        locs['y'] = np.append(locs['y'], l['y'])
        locs['z'] = np.append(locs['z'], l['z'])

        vecs['x'] = np.append(vecs['x'], v['x'])
        vecs['y'] = np.append(vecs['y'], v['y'])
        vecs['z'] = np.append(vecs['z'], v['z'])

    return locs, vecs

def make_points(l, mode = 'cube', opacity = 0.9, scale = 2):
    # mlab.clf()
    opacity = l['x'].shape[0]*[opacity]
    mlab.points3d(l['x'], l['y'], l['z'], opacity, mode = mode, scale_factor = scale, transparent=True)

def make_quiver(l, v, mode = 'arrow',  opacity = 0.9, scale = 1):
    opacity = l['x'].shape[0]*[opacity]
    mlab.quiver3d(l['x'], l['y'], l['z'], v['x'], v['y'], v['z'], mode = mode, scale_factor = scale, transparent=True)

def get_test_segmentation():
    dataset_path = '/Users/rodrigo/repos/datasets/cremi/sample_C_padded_20160501.hdf'
    start = np.array([81, 60, 60])
    end = np.array([125-30, 1250-60, 1250-60])
    seg = get_segmentation(dataset_path, start, end)
    return seg

def get_segmentation(dataset_path, st, en):
    hf = h5py.File(dataset_path, 'r')
    seg = hf['volumes']['labels']['neuron_ids']
    seg = np.array(seg[...])
    cropped_seg = seg[st[0]:en[0],st[1]:en[1],st[2]:en[2]]
    return cropped_seg

# neuron id : 11102
def get_neuron_blobs(segmentation, offset =np.array([81, 60, 60]), neuron_id=11102):
    point_locs = np.array(np.where(segmentation == neuron_id))
    point_comp = get_components(point_locs.T)
    return point_comp

# def get_neuron_mesh(segmentation, offset =np.array([81, 60, 60]), neuron_id=11102):
#     point_locs = np.array(np.where(segmentation == neuron_id))
#     point_comp = get_components(point_locs.T)
#     point_locs = np.array([point_comp['x'],point_comp['y'],point_comp['z']])
#     mesh = scipy.spatial.ConvexHull(point_locs.T)
#     # point_cloud = segmentation == neuron_id
#     return mesh

def plot_test_vectors(synlocs, threshold = 0.8):
    locs, vecs = get_vectors_above_thresh_over_synlocs(synlocs, threshold)
    make_quiver(locs, vecs, mode = 'arrow',  opacity = 0.9, scale = 1)

def plot_test_mesh():
    seg = get_test_segmentation();
    mesh = get_neuron_mesh(seg)
    pdb.set_trace(())
    # make_quiver(l, v, mode = 'arrow',  opacity = 0.9, scale = 1)


def get_locations_for_neuron(locs, labels, selected_labels):
    selected_locs = np.zeros(len(locs))
    for i, loc in enumerate(locs):
        # pdb.set_trace()
        loc_voxel = (np.round(loc/voxel_size)).astype('int')
        label = labels[loc_voxel[0],loc_voxel[1],loc_voxel[2]]
        selected_locs[i] = label in selected_labels
    return selected_locs

def get_ids(locs, labels):
    loc_ids = np.zeros(len(locs))
    for i, loc in enumerate(locs):
        # pdb.set_trace()
        loc_voxel = (np.round(loc/voxel_size)).astype('int')
        loc_ids[i] = labels[loc_voxel[0],loc_voxel[1],loc_voxel[2]]
    return loc_ids

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

    return pre, post, post_ids

def get_post_syn_ids(locs, partners, ids, labels, neuron_id1):
    # pre_post = np.where(partners == [neuron_id1, neuron_id2])
    post_ids = []

    for i, partner in enumerate(partners):
        loc_1 = locs[np.where(partner[0] == ids)[0][0]]
        loc_2 = locs[np.where(partner[1] == ids)[0][0]]

        # pdb.set_trace()
        loc_voxel_1 = (np.round(loc_1/voxel_size)).astype('int')
        label_1 = labels[loc_voxel_1[0],loc_voxel_1[1],loc_voxel_1[2]]

        loc_voxel_2 = (np.round(loc_2/voxel_size)).astype('int')
        label_2 = labels[loc_voxel_2[0],loc_voxel_2[1],loc_voxel_2[2]]

        if label_1 == neuron_id1:
            post_ids.append(label_2)

    return post_ids


def get_pre_post_vecs(pre_locs, post_locs, pre_locs_i):
    pre_locs = pre_locs[pre_loc_i]
    post_locs = post_locs[pre_loc_i]

def switch_zx(arr):
    arr_copy = copy.copy(arr)
    arr_copy[2] = arr[0]
    arr_copy[0] = arr[2]
    return arr_copy

def switch_zx_arr(arr):
    arr_copy = copy.copy(arr)
    arr_copy[:,2] = arr[:,0]
    arr_copy[:,0] = arr[:,2]
    return arr_copy

# if __name__ == '__main__':

# import bpy
# import sys
# sys.path.append('/Users/rodrigo/miniconda3/envs/pyBlender/lib/python3.5/site-packages')
# sys.path.append('/Users/rodrigo/repos/neuronTracing/paper')
# import h5py
# import plotting_functions as pf
# from importlib import reload

# data = h5py.File('/Users/rodrigo/rc2529/datasets/cremi/sample_C_padded_20160501.hdf','r')
# pred = h5py.File('/Users/rodrigo/rc2529/Projects/neuronTracing/paper/cremi0000.hdf','r')

# locs = pred['/annotations/locations'][...]
# labels = data['/volumes/labels/neuron_ids'][...]

# pre_locs = locs[::2]
# post_locs = locs[1::2]

# selected_labels = [14023]

# pre_loc_i = pf.get_locations_for_neuron(pre_locs, labels, selected_labels)
# post_loc_i = pf.get_locations_for_neuron(post_locs, labels, selected_labels)

# sel_pre_locs = pre_locs[pre_loc_i==1]
# sel_post_locs = post_locs[pre_loc_i==1]

# arrow_mesh = bpy.data.objects['ArrowObject'].data
# scene = bpy.context.scene

# for head, tail in zip(sel_pre_locs, sel_post_locs):
#     v1, v2 = Vector(head), Vector(tail)
#     obj = bpy.data.objects.new("Arrow_duplicate", arrow_mesh)
#     obj.location = v2
#     obj.rotation_mode = 'QUATERNION'
#     obj.rotation_quaternion = (v1-v2).to_track_quat('Z','Y')
#     scene.objects.link(obj)


# # def get_neuron_mesh(segmentation, neuron_id):

