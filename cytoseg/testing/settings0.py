# Map voxel values of the label volume to biological components

from label_identifier import *

def mapNumbersToComponents(detector):
    """Map voxel values of the label volume to biological components."""

    detector.componentDetector.labelIdentifierDict['membranes'] =\
        LabelIdentifier(min=2, max=2)
    detector.componentDetector.labelIdentifierDict['mitochondria'] =\
        LabelIdentifier(min=141, max=141)
    detector.componentDetector.labelIdentifierDict['blankInnerCell'] =\
        LabelIdentifier(values=range(3,100+1)+[142])
    detector.componentDetector.labelIdentifierDict['vesicles'] =\
        LabelIdentifier(min=138, max=138)

    #todo: remove requirement for this to be here
    detector.setTarget('mitochondria_new')
