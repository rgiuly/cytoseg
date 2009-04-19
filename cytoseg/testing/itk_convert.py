
# related information:
# http://paulnovo.org/WrapITKTutorial

from cytoseg_classify import *

app = wx.PySimpleApp()
frm = ClassificationControlsFrame(makeClassifyGUITree())
frm.Show()

numpyInputArray = loadImageStack("O:\\images\\HPFcere_vol\\HPF_rotated_tif\\median_then_gaussian_8bit_classified_pixels\\tif", None)

frm.addVolumeAndRefreshDataTree(numpyInputArray, "numpyInputArray")

ImageType = itk.Image[itk.UC, 3]
converter = itk.PyBuffer[ImageType]

#import scipy
#another_image_array = scipy.zeros( (10,10,10) )
itkImage = converter.GetImageFromArray(numpyInputArray)

numpyArray = converter.GetArrayFromImage(itkImage)

frm.addVolumeAndRefreshDataTree(numpyArray, "numpyArray")

app.MainLoop()

