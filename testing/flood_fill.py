import sys
sys.path.append("..")

from cytoseg_classify import *

from segmentation import *

temporaryDataFolder = "/tmp/cytoseg_data"

app = wx.PySimpleApp()
frm = ClassificationControlsFrame(makeClassifyGUITree())
frm.Show()

numpyArray = loadImageStack("data/flood_fill_test", None)

frm.addVolumeAndRefreshDataTree(numpyArray, "numpyArray")

startPoints = ((0, 0, 0), (53, 81, 6))

count = 0
for startPoint in startPoints:
    points = floodFill(numpyArray, startPoint)
    blob = Blob()
    for point in points:
        blob.addPoint(LabeledPoint(point))
    frm.addBlobAndRefreshDataTree(blob, getNode(frm.mainDoc.dataRootNode, ('Blobs',)),
                                  "blob%d" % count)
    count += 1

app.MainLoop()
