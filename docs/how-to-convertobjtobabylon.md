# How To Convert .obj Files to .babylon files

This document provides specific information for running the SQS pipeline command in Squid Hall.

There are several ways to convert the file types, including plugins for various 3D modeling programs that export objects in .babylon format. However, this document focuses on using the Babylon.js Sandbox for the conversion.

The Sandbox is located here: https://sandbox.babylonjs.com/

There is an article on exporting here: https://medium.com/@babylonjs/exporting-3d-content-for-babylon-js-76cb71a2df01

For converting the objects there are three steps, described in detail below:

1. Drag and Drop your Object in the Sandbox

2. Display the Inspector

3. Export the Object

You can also make changes to the object in the Sandbox before exporting it. This is described in 'Modifying the Object' below.

## Drag and Drop your Object in the Sandbox

Simply navigate your browser to the Sandbox and drag and drop your .obj 3D object file onto the browser. 

## Display the Inspector

On the lower right of the Sandbox page there are three icons: 'Display Inspector', 'Select Environment', and 'Files'. The 'Display Inspector' icon is a cube with a pencil. Click it.

Two panels appear on the Sandbox page: 'Scene Explorer' on the left and 'Inspector' on the right. 

## Export the Object

The Inspector panel has five icons: 'Properties', 'Debug', 'Statistics', 'Tools', and 'Settings'. The 'Tools' icon is a wrench. Click it to open the Tools tab.

Towards the bottom of the Tools tab there is a 'Scene Export' section. Under that there is a 'Export to Babylon' button. Click it. A 'Save File' dialogue should appear allowing you to save the object as a .babylon file.

The object will be saved to your download folder as 'scene.babylon'. Simply change the name as needed.

NOTE: The export will fail for some .obj objects. No clue as to why.

NOTE: There is some cleanup to the raw .babylon data required, however Jack will take care of that.

## Modifying the Object

You can modify the object after the display inspector step and before the export step if needed. Every possible modification using the inspector is not covered here, you will need to play around with the Sandbox on your own to learn all the ins and outs.

Here we will describe two common modifications:

1. Changing the Mesh name

2. Changing the Mesh scale

Before you can change a mesh you will need to select it in the Scene Explorer pane on the left. The Scene Explorer has a series of tree views of currently loaded data, click the '+' symbol next to 'Nodes' to view current scene nodes.

You can ignore everything on the list with a name starting with 'default'. Depending on the number of meshes in your imported object you will see one or more named meshes. If you click on a mesh it will open the Properties tab of the Inspector panel for that mesh. 

### Changing the Mesh Name

You can change the Mesh Name in the Properties tab by simply typing in a new name in the Name Field under the 'General' section. Each mesh should have a name useful for determining what it is.

### Changing the Mesh scale

You can change the Mesh scale for each of X, Y, and Z coordinates in the Properties tab by simply typing in a numerica value greater or lesser than one for each coordinate in the Scaling Field under the 'Transforms' section. You will need to click the '+' symbol to the right of the field first. For example 0.5 in all coordinates will reduce the object in size by one half.

Generally if you need to scale one mesh of an object you should also scale any other meshes with the same values.



