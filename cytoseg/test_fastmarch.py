from cytoseg_classify import *
from fastmarch import *

app = wx.PySimpleApp()
frm = ClassificationControlsFrame(makeClassifyGUITree())
frm.Show()

numpyInputArray = loadImageStack("O:\\images\\HPFcere_vol\\HPF_rotated_tif\\median_then_gaussian_8bit_classified_pixels\\tif", None)

frm.addVolumeAndRefreshDataTree(numpyInputArray, "numpyInputArray")

seedLocationVolume = zeros(numpyInputArray.shape)

position = [40, 80, 10]

fillSphere(seedLocationVolume, position, 5)

outputImage = fastMarch(numpyInputArray, position)

frm.addVolumeAndRefreshDataTree(outputImage, "Output")
frm.addVolumeAndRefreshDataTree(seedLocationVolume, "Seed")

app.MainLoop()

