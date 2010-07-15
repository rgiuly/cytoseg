
from label_identifier import *

def mapNumbersToComponents(detector):

    #for object in (detector.contourClassifier, detector.contourTrainer):
    for object in (detector.contourClassifier,):

        object.labelIdentifierDict['mitochondria'] =\
            LabelIdentifier(min=141, max=141)
        object.labelIdentifierDict['other'] =\
            LabelIdentifier(values=range(3,100+1)+[142]+[2]+[138])

    #todo: this shouldn't be here
    detector.setTarget('mitochondria_new')
