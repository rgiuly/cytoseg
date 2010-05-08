
from label_identifier import *

def mapNumbersToComponents(detector):

    detector.contourClassifier.labelIdentifierDict['mitochondria'] =\
        LabelIdentifier(min=141, max=141)
    detector.contourClassifier.labelIdentifierDict['other'] =\
        LabelIdentifier(values=range(3,100+1)+[142]+[2]+[138])

    detector.setTarget('mitochondria_new')
