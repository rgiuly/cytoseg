
from numpy import *
from scipy import ndimage
from data_viewer import borderWidthForFeatures

class StencilNeuralNetwork():


    offsets = {(0,0):1,
               (1,1):1, (3,3):1, (5,5):1,
               (-1,1):1, (-3,3):1, (-5,5):1,
               (-1,-1):1, (-3,-3):1, (-5,-5):1,
               (1,-1):1, (3,-3):1, (5,-5):1,
               (1,0):1, (3,0):1, (5,0):1,
               (-1,0):1, (-3,0):1, (-5,0):1,
               (0,1):1, (0,3):1, (0,5):1,
               (0,-1):1, (0,-3):1, (0,-5):1}


    def __init__(self, inputVolume):

        self.inputVolume = inputVolume
        self.outputVolume = zeros(inputVolume.shape, dtype=float32)


    def update(self):

        weights = zeros((11, 11, 1), dtype=float32)

        for key in self.offsets:

            weights[key[0] + 5, key[1] + 5] = self.offsets[key]

        #self.outputVolume[:] = self.inputVolume[:]

        ndimage.convolve(self.inputVolume, weights / float(len(self.offsets)),
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



class StencilNeuralNetworkLearner:

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
            for y in range(borderWidthForFeatures[1],v.shape[1]-borderWidthForFeatures[1]):
                for z in range(borderWidthForFeatures[2],
                               v.shape[2]-borderWidthForFeatures[2]):

                    total += abs(self.network.outputVolume[x,y,z] -
                                 self.trainingOutputVolume[x,y,z])

        return total


    def update(self):

        #step = 0.5
        step = 5.0 * pow(0.9, self.updateCount)

        error = self.error()
        print "NeuralNetwork error: %f" % error

        for key in self.network.offsets:
            weight = self.network.offsets[key]

            self.network.offsets[key] = weight + step
            errorForIncrease = self.error()

            if errorForIncrease < error:
                #self.network.offsets[key] = weight + step
                pass
            else:
                self.network.offsets[key] = weight - step
                errorForDecrease = self.error()
                if errorForDecrease < error:
                    #self.network.offsets[key] = weight - step
                    pass
                else:
                    self.network.offsets[key] = weight

        self.updateCount += 1

