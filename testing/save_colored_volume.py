import sys
sys.path.append("..")

from cytoseg_classify import *

temporaryDataFolder = "/tmp/cytoseg_data"

app = wx.PySimpleApp()
frm = ClassificationControlsFrame(makeClassifyGUITree())
frm.Show()

red = loadImageStack("data/color_test/red", None)
green = loadImageStack("data/color_test/green", None)
blue = loadImageStack("data/color_test/blue", None)

frm.addVolumeAndRefreshDataTree(red, "red")
frm.addVolumeAndRefreshDataTree(green, "green")
frm.addVolumeAndRefreshDataTree(blue, "blue")

writeTiffStackRGB(defaultOutputPath, red, green, blue)

app.MainLoop()
