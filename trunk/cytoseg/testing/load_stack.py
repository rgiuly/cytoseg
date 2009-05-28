import sys
sys.path.append("..")

from cytoseg_classify import *

temporaryDataFolder = "/tmp/cytoseg_data"

app = wx.PySimpleApp()
frm = ClassificationControlsFrame(makeClassifyGUITree())
frm.Show()

numpyArray = loadImageStack("data/3D-blob-data", None)

frm.addVolumeAndRefreshDataTree(numpyArray, "numpyArray")

app.MainLoop()
