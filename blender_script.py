import bpy
import sys

# Create a conda py3.5 env that you can use to manage your python packages
# and import it onto blender by adding it to the path
# sys.path.append('/Users/rodrigo/miniconda3/envs/my_env_name/lib/python3.5/site-packages')
sys.path.append('/Users/rodrigo/miniconda3/envs/pyBlender/lib/python3.5/site-packages')
sys.path.append('/Users/rodrigo/repos/neuronVisualizationScripts')

import h5py
import blender_plotting_functions as pf
from importlib import reload
import copy
import numpy as np

# get your volumetric/location data
data = h5py.File('/Users/rodrigo/rc2529/datasets/cremi/sample_C_padded_20160501.hdf','r')
pred = h5py.File('/Users/rodrigo/rc2529/Projects/neuronTracing/paper/cremi_sample.hdf','r')

loaded_locs = pred['/annotations/locations'][...]
gt_locs = data['/annotations/locations'][...]
gt_ids = data['/annotations/ids'][...]
gt_partners = data['/annotations/presynaptic_site/partners'][...]
labels = data['/volumes/labels/neuron_ids'][...]
raw = data['/volumes/raw'][...]

# IDs for relevant neurons
id1 = 14023
id2 = 16111

pre_locs_pairs, post_locs_pairs = pf.get_locations_for_partners(gt_locs, gt_partners, gt_ids,labels, id1, id2)

# arrow scaling in xyz dimension
arrow_scaling = (1,1,1)

# Failed attempt at trying to import neuron from command line, doesn't work,
# neuron is rated and translated

# # arrow scaling in xyz dimension
# neuron_scaling = (0.001,0.001,0.001)

# # Import Neuron
# file_loc = '/Users/rodrigo/repos/neuronVisualizationScripts/meshes/neuron-14023.obj'
# imported_object = bpy.ops.import_scene.obj(filepath=file_loc, use_groups_as_vgroups=False)
# obj_object = bpy.context.selected_objects[0] ####<--Fix
# obj_object.scale = neuron_scaling
# neuron = bpy.data.objects[obj_object.name].data

# this should match the scaling you used to import your neuron object
vector_scale = 0.001

# import arrow object mesh
file_loc = '/Users/rodrigo/repos/neuronVisualizationScripts/meshes/sample_arrow.obj'
imported_object = bpy.ops.import_scene.obj(filepath=file_loc)
obj_object = bpy.context.selected_objects[0] ####<--Fix
pre_syn_arrow_mesh = bpy.data.objects[obj_object.name].data

# get neuron object
neuron_obj = bpy.data.objects['neuron-14023']

# create an empty that will be parent to all arrows
# this creates a hierarchy that allows you to manipulate
# all pre_synaptic arrow object simultaneously
pre_syn_arr = bpy.data.objects.new( "pre_syn_arr", None )
bpy.context.scene.objects.link( pre_syn_arr)

# make it a child of the main neuron
pre_syn_arr.parent = neuron_obj

# Define/Calculate offsets and voxel size
offset = np.floor((np.array(raw.shape) - np.array(labels.shape))/2).astype('int')
voxel_size = np.array([40,4,4])
offset = offset*voxel_size
xyz_offset = pf.switch_zx(offset)

scene = bpy.context.scene

# for each pre-post synaptic location pair, create an arrow
# that begin at the pre synaptic location and is rotated
# to match the vector direction the post synaptic location
for loc_pair in pre_locs_pairs:

    # create vector
    head = pf.switch_zx(loc_pair[0])
    tail = pf.switch_zx(loc_pair[1])
    v1, v2 = Vector((head+xyz_offset)*vector_scale), Vector((tail+xyz_offset)*vector_scale)

    # create arrow
    obj = bpy.data.objects.new("preSyn", pre_syn_arrow_mesh)
    obj.scale = arrow_scaling
    obj.location = v2
    obj.rotation_mode = 'QUATERNION'
    obj.rotation_quaternion = (v2-v1).to_track_quat('Z','Y')
    obj.parent = pre_syn_arr
    scene.objects.link(obj)