# Map voxel values of the label volume to biological components

from label_identifier import *

def mapNumbersToComponents(detector):
    """Map voxel values of the label volume to biological components."""

    for object in (detector.componentDetector,):

        object.labelIdentifierDict['mitochondria'] =\
            LabelIdentifier('mitochondria', min=1, max=255)
        object.labelIdentifierDict['other'] =\
            LabelIdentifier('other', min=0, max=0)

    detector.setTarget('mitochondria_new')
