
from label_identifier import *

def mapNumbersToComponents(detector):

    #detector.contourClassifier.minVoxelLabelValue['mitochondria'] = 3
    #detector.contourClassifier.minVoxelLabelValue['membranes'] = 2
    #detector.contourClassifier.maxVoxelLabelValue['membranes'] = 2
    #detector.contourClassifier.labelIdentifierDict['membranes'] =\
    #    LabelIdentifier(min=100, max=300)
    detector.contourClassifier.labelIdentifierDict['membranes'] =\
        LabelIdentifier(min=2, max=2)
    #detector.contourClassifier.labelIdentifierDict['mitochondria'] =\
    #    LabelIdentifier(min=3, max=250)
    detector.contourClassifier.labelIdentifierDict['mitochondria'] =\
        LabelIdentifier(min=141, max=141)
    #detector.contourClassifier.labelIdentifierDict['blankInnerCell'] =\
    #    LabelIdentifier(min=150, max=150)
    #detector.contourClassifier.labelIdentifierDict['blankInnerCell'] =\
    #    LabelIdentifier(min=0, max=0)
    detector.contourClassifier.labelIdentifierDict['blankInnerCell'] =\
        LabelIdentifier(values=range(3,100+1)+[142])
    ##detector.contourClassifier.labelIdentifierDict['blankInnerCell'] =\
    ##    LabelIdentifier(values=(0,))
    #detector.contourClassifier.labelIdentifierDict['vesicles'] =\
    #    LabelIdentifier(min=255, max=255)
    detector.contourClassifier.labelIdentifierDict['vesicles'] =\
        LabelIdentifier(min=138, max=138)

    # this setting affects contour detection (not voxel processing)
    #detector.setTarget('membranes')
    detector.setTarget('mitochondria_new')
