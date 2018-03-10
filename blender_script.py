import bpy
import sys
sys.path.append('/Users/rodrigo/miniconda3/envs/pyBlender/lib/python3.5/site-packages')
sys.path.append('/Users/rodrigo/repos/neuronTracing/paper')
import h5py
import plotting_functions as pf
from importlib import reload
import copy
import numpy as np

data = h5py.File('/Users/rodrigo/rc2529/datasets/cremi/sample_C_padded_20160501.hdf','r')
pred = h5py.File('/Users/rodrigo/rc2529/Projects/neuronTracing/paper/cremi_sample.hdf','r')


loaded_locs = pred['/annotations/locations'][...]
gt_locs = data['/annotations/locations'][...]
gt_ids = data['/annotations/ids'][...]
gt_partners = data['/annotations/presynaptic_site/partners'][...]
labels = data['/volumes/labels/neuron_ids'][...]
raw = data['/volumes/raw'][...]

id1 = 14023
id2 = 16111

pre_locs_pairs, post_locs_pairs = pf.get_locations_for_partners(gt_locs, gt_partners, gt_ids,labels, id1, id2)

# bpy.ops.object.select_pattern(pattern="Arrow.*")
# bpy.ops.object.delete(use_global=False)

scaling = (0.004,0.004,0.04)
vector_scale = 0.001

pre_syn_arrow_mesh = bpy.data.objects['Sample_PreSyn'].data

neuron_obj = bpy.data.objects['neuron-14023']

pre_syn_arr = bpy.data.objects.new( "pre_syn_arr", None )
bpy.context.scene.objects.link( pre_syn_arr)
pre_syn_arr.parent = neuron_obj

offset = np.floor((np.array(raw.shape) - np.array(labels.shape))/2).astype('int')
voxel_size = np.array([40,4,4])
offset = offset*voxel_size
xyz_offset = pf.switch_zx(offset)

scene = bpy.context.scene

for loc_pair in pre_locs_pairs:
    head = pf.switch_zx(loc_pair[0])
    tail = pf.switch_zx(loc_pair[1])
    v1, v2 = Vector((head+xyz_offset)*vector_scale), Vector((tail+xyz_offset)*vector_scale)
    obj = bpy.data.objects.new("preSyn", pre_syn_arrow_mesh)
    obj.scale = scaling
    obj.location = v2
    obj.rotation_mode = 'QUATERNION'
    obj.rotation_quaternion = (v2-v1).to_track_quat('Z','Y')
    obj.parent = pre_syn_arr
    scene.objects.link(obj)

# post_syn_arrow_mesh = bpy.data.objects['Sample_PostSyn'].data
# post_syn= bpy.data.objects.new( "post_syn", None )
# bpy.context.scene.objects.link(post_syn)
# post_syn.parent = neuron_obj

# for head, tail in zip(sel_pre_locs,sel_post_locs):
#     v1, v2 = Vector((head+xyz_offset)*vector_scale), Vector((tail+xyz_offset)*vector_scale)
#     obj = bpy.data.objects.new("postSyn", post_syn_arrow_mesh)
#     obj.scale = scaling
#     obj.location = v2
#     obj.rotation_mode = 'QUATERNION'
#     obj.rotation_quaternion = (v2-v1).to_track_quat('Z','Y')
#     obj.parent = post_syn
#     scene.objects.link(obj)