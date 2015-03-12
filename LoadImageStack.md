# Example Code #

This example initializes the GUI and then reads an image stack.



To run this sample:

python load\_stack.py
from the folder: cytoseg/testing/

To view the volume, in the dataTreeForVolumeSelection tree, select numpyArray (in the Volumes folder)


---

file: cytoseg/testing/load\_stack.py

```
import sys
sys.path.append("..")

from cytoseg_classify import *

app = wx.PySimpleApp()
frm = ClassificationControlsFrame(makeClassifyGUITree())
frm.Show()

numpyArray = loadImageStack("data/3D-blob-data", None)

frm.addVolumeAndRefreshDataTree(numpyArray, "numpyArray")

app.MainLoop()

```