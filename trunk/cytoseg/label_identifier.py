
import numpy

class LabelIdentifier:

    def __init__(self, min, max=None):

        self.min = min
        self.max = max


    def isMember(self, value):

        if self.max == None:
            if value >= self.min:
                return True
        else:
            if self.min <= value <= self.max:
                return True
            else:
                return False


    def count(self, volume):

        countResult = 0

        for x in range(volume.shape[0]):
            for y in range(volume.shape[1]):
                for z in range(volume.shape[2]):
                    if self.isMember(volume[x,y,z]):
                        countResult += 1

        return countResult


    # select a single label volume from the set of labels in inputLabel
    def getBooleanVolume(self, inputLabel):

        if self.max == None:
            return inputLabel >= self.min
        else:
            return numpy.logical_and(self.min <= inputLabel, inputLabel <= self.max)

