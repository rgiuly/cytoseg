# Map voxel values of the label volume to biological components

from label_identifier import *

def mapNumbersToComponents(detector):
    """Map voxel values of the label volume to biological components."""

    for object in (detector.componentDetector,):

        object.labelIdentifierDict['primaryObject'] =\
            LabelIdentifier('primaryObject', min=141, max=141)
        object.labelIdentifierDict['other'] =\
            LabelIdentifier('other', values=range(3,100+1)+[142]+[2]+[138]+[0])

    detector.setTarget('mitochondria_new')
