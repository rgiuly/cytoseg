
from cytoseg_classify import *
from default_path import *
from contour_processing import *

def probabilityFunction(features):
    amplitude = 1
    overlapValue = gaussian(1.0 - features['ellipseOverlap'], amplitude, 0.2)
    perimeterValue = gaussian(abs(11.0 - features['perimeter']), amplitude, 2.0)
    grayValueMatch = gaussian(abs(0.8 - features['averageGrayValue']), amplitude, 0.25)
    areaMatch = gaussian(abs(60 - math.sqrt(features['contourArea'])), amplitude, 10)
    #print features
    return overlapValue * perimeterValue * grayValueMatch * areaMatch

app = wx.PySimpleApp()
frm = ClassificationControlsFrame(makeClassifyGUITree())
frm.Show()

blurredVolume = loadImageStack("data/3d-blob-data", None)
blurredVolume = blurredVolume[:,:,10:15]

#originalVolume = originalVolume[:,:,3:]
#filteredVolume = filteredVolume[:,:,3:]

frm.addPersistentVolumeAndRefreshDataTree(blurredVolume, 'InputVolume')

detector = ContourDetector()
detector.originalVolume = frm.getPersistentVolume_old('InputVolume')
detector.filteredVolume = frm.getPersistentVolume_old('InputVolume')
detector.probabilityFunction = probabilityFunction

contours = detector.findContours()

# add a node for all detected contours
contoursNode = DataNode('contours', 'contours node type', {}, None)
contoursNode.addObjectList(contours)
#contoursNode.enableRecursiveRendering = False
frm.addPersistentSubtreeAndRefreshDataTree((), contoursNode)

app.MainLoop()

