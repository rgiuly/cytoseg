# data location configuration file

import sys
sys.path.append("..")

from command_reader import CommandReader
from machine_learning_tutorial import MachineLearningTutorial
from label_identifier import *

commandReader = CommandReader()

detector = MachineLearningTutorial(commandReader.param, guiVisible=False)
detector.dataIdentifier = "sbfsem_080309"
#detector.dataViewer.mainDoc.dataTree.rootFolderPath = "G:/cytoseg_data/sbfsem"
detector.dataViewer.mainDoc.dataTree.rootFolderPath =\
    commandReader.param['cytosegDataFolder']

detector.contourClassifier.numberOfLayersToProcess = 14
detector.contourClassifier.numberOfTrainingLayersToProcess = 7

detector.contourClassifier.labelIdentifierDict['blankInnerCell'] =\
        LabelIdentifier(min=0, max=0)
detector.contourClassifier.labelIdentifierDict['membranes'] =\
        LabelIdentifier(min=1, max=255)

detector.setTarget('membranes')
detector.run(runAllSteps=0)
