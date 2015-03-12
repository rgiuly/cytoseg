# Blob detection Tutorial #
  1. If necessary, download and install [IMOD](http://bio3d.colorado.edu/imod/).
  1. Start cytoseg. (Inside the cytoseg folder, type python main.py at a command prompt in Windows or Linux)
  1. Set the imageStackPath text box to the tif stack you want to open. For example:  c:\your\_folder\
  1. Press "Load Image Stack"
  1. Select "startDefiningBoxAtMouseLocation"
  1. Use the mouse to draw a box (from top left corner to bottom right) that defines the region where you want blob detection to occur.
  1. Press "Mark Blobs"

In this tutorial the blob positions are inserted into an existing [IMOD](http://bio3d.colorado.edu/imod/) model file. IMOD is a freely available program that we will use to visualize out 3D data.

To insert into an existing IMOD file:
  1. Using IMOD, create and save a model file.
  1. File -> Insert into an existing IMOD model file.
  1. Pick the existing IMOD file. A new file will be created with the detected points inserted.
  1. Use IMOD to open the newly created file.

![http://cytoseg.googlecode.com/svn/wiki/cytoseg_screenshot.png](http://cytoseg.googlecode.com/svn/wiki/cytoseg_screenshot.png)

A new file will be created that has spheres inserted at blob centers



<br>
Result shown in IMOD:<br>
<br>
<img src='http://cytoseg.googlecode.com/svn/wiki/imod_blob_screenshot.png' />



<br>
Result shown in IMOD 3D model view:<br>
<br>
<img src='http://cytoseg.googlecode.com/svn/wiki/imod_blob_3D_view_screenshot.png' />