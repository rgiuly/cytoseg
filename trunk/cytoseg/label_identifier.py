
import numpy

class LabelIdentifier:

    def __init__(self, min=None, max=None, values=None):

        self.min = min
        self.max = max
        self.values = values


    def isMember(self, value):

        returnValue = False

        #if self.max == None:
        #    if value >= self.min:
        #        return True
        #else:
        if self.min != None and self.max != None:
            if self.min <= value <= self.max:
                returnValue = True

        if self.values != None:
            if value in self.values:
                returnValue = True

        return returnValue


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

        returnVolume = numpy.zeros(inputLabel.shape, dtype=bool)

        #if self.max == None:
        #    return inputLabel >= self.min
        #else:
        #    return numpy.logical_and(self.min <= inputLabel, inputLabel <= self.max)
        if self.min != None and self.max != None:
            returnVolume = numpy.logical_and(self.min <= inputLabel, inputLabel <= self.max)

        if self.values != None:
            for value in self.values:
                returnVolume |= (inputLabel == value)
            #if value in self.values:
            #    returnValue = True

        return returnVolume


class LabelIdentifierDict(dict):

    def getClassName(self, value):

        className = None

        for target in self:
            #print "target", target
            #print "value", value
            #print "self[target].isMember(value)", self[target].isMember(value)
            if self[target].isMember(value):
                className = target

        return className

