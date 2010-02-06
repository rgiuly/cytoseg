
from numpy import *


class Accuracy:

    def __init__(self, actualLabelVolume, computedLabelVolume):

        self.actualLabelVolume = actualLabelVolume
        self.computedLabelVolume = computedLabelVolume


    # computed true, but actual value is false
    def falsePositives(self):

        return sum(1 * logical_and(self.computedLabelVolume,
                                   logical_not(self.actualLabelVolume)))


    # computed true, and that agrees with the actual value
    def truePositives(self):

        return sum(1 * logical_and(self.computedLabelVolume,
                                   self.actualLabelVolume))


    # computed false, but actual value is true
    def falseNegatives(self):

        return sum(1 * logical_and(logical_not(self.computedLabelVolume),
                                   self.actualLabelVolume))


    # computed false, and that agrees with the actual value
    def trueNegatives(self):

        return sum(1 * logical_and(logical_not(self.computedLabelVolume),
                                   logical_not(self.actualLabelVolume)))


    def actualPositives(self):

        # todo: there may be a simpler way to convert to a boolean
        return sum(1 * logical_not(logical_not(self.actualLabelVolume)))


    def actualNegatives(self):

        return sum(1 * logical_not(self.actualLabelVolume))


    def truePositiveRate(self):

        return float(self.truePositives()) /\
               float(self.actualPositives())


    def falsePositiveRate(self):

        return float(self.falsePositives()) /\
               float(self.actualNegatives())


    def printAccuracy(self):

        print "false positives:", self.falsePositives()
        print "true positives:", self.truePositives()
        print "false negatives:", self.falseNegatives()
        print "true negatives:", self.trueNegatives()
        print "error:",\
            float(self.falsePositives() + self.falseNegatives()) /\
            float(size(self.actualLabelVolume))
        #print "true positives / actual positives:",\
        #    float(self.truePositives()) /\
        #    float(self.actualPositives())
        #print "false positives / actual positives:",\
        #    float(self.falsePositives()) /\
        #    float(self.actualPositives())
        print "true positive rate:", self.truePositiveRate()
        print "false positive rate:", self.falsePositiveRate()

