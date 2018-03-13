# Neuron Visualizations

This repo contains a some scripts, sample data and explanations on how to visualize data for connectomics research in Blender and Mayavi.

This is by no means an exhaustive tutorial, but rather more like a helloworld with some examples that might help you get started.

# Blender

Blender is a very powerful open source 3D modeling and animation software. It has hunderds of features for a variety of applications. Here we'll be using a tiny fraction of those features to jointly view neurons in the form of meshes and synaptic pair locations shown as arrows. We'll also be using the Blender addon [NeuroMorph](https://neuromorph.epfl.ch/).

1. [Install Blender](https://www.blender.org/download/)
2. [Install NeuroMorph Toolbox](https://github.com/NeuroMorph-EPFL/NeuroMorph)
3. Activate the Neuromorph Add Ons and import a neuron. [(Tutorial)](https://www.youtube.com/watch?v=CVkcYjWgceM)
Be careful about the scaling option right above the import button. For the .obj sample neuron meshes provided here you need to use a scaling of 0.001.
4. If you follows these steps and import sample neuron 14023 you should be able to move around the camera to find the neuron, it should look somthing like this:
![neuron_14023](img/neuron_14023.jpg)
It might be tempting to move your neuron so that it is centered on the scene but if you are going to keep adding other data points I recommend you leave the neuron where it spanned so that your locations are consistent. To view your neuron more closely, [learn how to move](https://www.katsbits.com/tutorials/blender/learning-keyboard-mouse-navigation.php) your point of view about the scene instead.
5. Finally run blender_script.py to load and add vectors that show the synaptic pairs as arrows pointing from the pre to the post synaptic location. 
This script does a very specific procedure of loading pre/post synaptic location and spanning arrows along the pre-post vector direction. 






