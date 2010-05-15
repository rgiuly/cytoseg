
from contour_set_detector import *

class MachineLearningTutorial(ContourSetDetector):

    def run(self, runAllSteps=True):

        self.contourClassifier.runInitialize()
        self.contourClassifier.runPersistentLoadTrainingData()
        self.contourClassifier.runPersistentLoadOriginalImage()
        self.contourClassifier.runClassifyVoxels()
        self.contourClassifier.runWriteVoxelClassificationResult()
        self.app.MainLoop()
