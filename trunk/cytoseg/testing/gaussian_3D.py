import sys
sys.path.append("..")

from cytoseg_classify import *

app = wx.PySimpleApp()
frm = ClassificationControlsFrame(makeClassifyGUITree())
frm.Show()

numpyArray = loadImageStack("data/3D-blob-data", None)

frm.addVolumeAndRefreshDataTree(numpyArray, 'numpyArray')
frm.addVolumeAndRefreshDataTree(itkFilter(numpyArray,
                                           'SmoothingRecursiveGaussian',
                                           sigma=1),
                                          'SmoothingRecursiveGaussian')

app.MainLoop()
