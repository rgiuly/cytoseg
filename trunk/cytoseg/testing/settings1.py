# Map voxel values of the label volume to biological components

from label_identifier import *

def mapNumbersToComponents(detector):
    """Map voxel values of the label volume to biological components."""

    for object in (detector.componentDetector,):

        object.labelIdentifierDict['primaryObject'] =\
            LabelIdentifier(min=141, max=141)
        object.labelIdentifierDict['other'] =\
            LabelIdentifier(values=range(3,100+1)+[142]+[2]+[138])

    detector.setTarget('mitochondria_new')
