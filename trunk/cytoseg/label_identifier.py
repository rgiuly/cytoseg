# LabelIdentifier class for defining how a value or set of values in a label
# volume maps to a type of object.

import numpy

class LabelIdentifier:
    """
    Represents a label for a particular biological object.
    Specifies the voxel label value or values that are associated with this object.
    """

    def __init__(self, min=None, max=None, values=None):

        self.min = min
        self.max = max

        if values != None:
            self.values = {}
            for value in values:
                self.values[value] = True
        else:
            self.values = None
        #self.values = values


    def isMember(self, value):
        """Value is a value in a label raster. If the value matches this label identifier,
        then return True. Otherwise return false."""

        returnValue = False

        if self.min != None and self.max != None:
            if self.min <= value <= self.max:
                returnValue = True

        if self.values != None:
            if value in self.values:
                returnValue = True

        return returnValue


    def count(self, volume):
        """Count how many times this label occurs in the volume."""

        countResult = 0

        for x in range(volume.shape[0]):
            for y in range(volume.shape[1]):
                for z in range(volume.shape[2]):
                    if self.isMember(volume[x,y,z]):
                        countResult += 1

        return countResult


    def getBooleanVolume(self, inputLabel):
        """Make a single label volume for only this label's object type."""

        returnVolume = numpy.zeros(inputLabel.shape, dtype=bool)

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
        """
        Each key of the dictionary is the name of an object type.
        Each value of the dictionary is a LabelIdentifier.
        Convenience method to get the object type (dictionary key) name based on the label value.
        """

        className = None

        for target in self:
            #print "target", target
            #print "value", value
            #print "self[target].isMember(value)", self[target].isMember(value)
            if self[target].isMember(value):
                className = target

        return className

