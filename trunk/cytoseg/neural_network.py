
from numpy import *
from scipy import ndimage
from data_viewer import borderWidthForFeatures

class NeuralNetwork():


    def __init__(self, inputVolume):

        self.inputVolume = inputVolume
        self.outputVolume = zeros(inputVolume.shape, dtype=float32)
        self.weights = ones((11, 11, 1), dtype=float32)


    def update(self):

        sh = self.weights.shape

        #self.outputVolume[:] = self.inputVolume[:]

        ndimage.convolve(self.inputVolume,
                         self.weights / float(sh[0] * sh[1] * sh[2]),
                         output=self.outputVolume)
        self.outputVolume[:] = tanh(self.outputVolume)[:]

#        v = self.inputVolume
#
#        for x in range(borderWidthForFeatures, v.shape[0]-borderWidthForFeatures):
#            #print x, "out of", v.shape[0]-borderWidthForFeatures-1
#            for y in range(borderWidthForFeatures,v.shape[1]-borderWidthForFeatures):
#                for z in range(borderWidthForFeatures,v.shape[2]-borderWidthForFeatures):
#                    
#                    self.outputVolume[x,y,z] = float(v[x,y,z]) + float(v[x+1,y,z]) + float(v[x,y+1,z]) + float(v[x,y,z+1])


    def getOutput(self):

        return self.outputVolume



class NeuralNetworkLearner:

    def __init__(self, inputVolume, outputVolume):

        self.network = NeuralNetwork(inputVolume)
        self.trainingOutputVolume = outputVolume
        self.updateCount = 0


    def error(self):

        total = 0
        self.network.update()
        v = self.trainingOutputVolume

        for x in range(borderWidthForFeatures[0], v.shape[0]-borderWidthForFeatures[0]):
            #print x, "out of", v.shape[0]-borderWidthForFeatures-1
            for y in range(borderWidthForFeatures[1], v.shape[1]-borderWidthForFeatures[1]):
                for z in range(borderWidthForFeatures[2],
                               v.shape[2]-borderWidthForFeatures[2]):

                    total += abs(self.network.outputVolume[x,y,z] -
                                 self.trainingOutputVolume[x,y,z])

        return total


    def update(self):

        #step = 0.5
        step = 5.0# * pow(0.9, self.updateCount)

        error = self.error()
        print "NeuralNetwork error: %f" % error

        weights = self.network.weights
        sh = weights.shape

        for x in range(sh[0]):
            for y in range(sh[1]):
                for z in range(sh[2]):

                    weight = weights[x, y, z]

                    weights[x, y, z] = weight + step
                    errorForIncrease = self.error()
                    #print "errorForIncrease", errorForIncrease

                    if errorForIncrease < error:
                        #self.network.offsets[key] = weight + step
                        pass
                    else:
                        weights[x, y, z] = weight - step
                        errorForDecrease = self.error()
                        #print "errorForDecrease", errorForDecrease
                        if errorForDecrease < error:
                            #weights[x, y, z] = weight - step
                            pass
                        else:
                            weights[x, y, z] = weight

        self.updateCount += 1

