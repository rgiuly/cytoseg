
from label_identifier import *

def mapNumbersToComponents(detector):

    #for object in (detector.componentDetector, detector.contourTrainer):
    for object in (detector.componentDetector,):

        object.labelIdentifierDict['mitochondria'] =\
            LabelIdentifier(min=1, max=255)
        object.labelIdentifierDict['other'] =\
            LabelIdentifier(min=0, max=0)

    #todo: this shouldn't be here
    detector.setTarget('mitochondria_new')
