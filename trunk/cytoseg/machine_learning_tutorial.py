
from contour_set_detector import *

class MachineLearningTutorial(ContourSetDetector):

    def run(self, runAllSteps=True):

        self.contourClassifier.target = 'mitochondria_new'
        print "target:", self.contourClassifier.target
        #self.contourClassifier.runInitialize()
        #self.contourClassifier.runPersistentLoadTrainingData()
        #self.contourClassifier.runPersistentLoadOriginalImage()
        #self.contourClassifier.runClassifyVoxels()
        #self.contourClassifier.runWriteVoxelClassificationResult()
        #self.app.MainLoop()

        self.contourClassifier.runInitialize()
        self.contourClassifier.runLoadTrainingData()
        self.contourClassifier.runLoadInputImage()
        self.contourClassifier.runClassifyVoxels()
        self.contourClassifier.runWriteVoxelClassificationResult()
