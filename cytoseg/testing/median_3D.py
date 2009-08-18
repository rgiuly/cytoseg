import sys
sys.path.append("..")

from cytoseg_classify import *

app = wx.PySimpleApp()
frm = ClassificationControlsFrame(makeClassifyGUITree())
frm.Show()

numpyArray = loadImageStack("data/3D-blob-data", None)

frm.addVolumeAndRefreshDataTree(numpyArray, 'numpyArray')
frm.addVolumeAndRefreshDataTree(itkFilter(numpyArray, 'median', radius=1), 'median')

app.MainLoop()
