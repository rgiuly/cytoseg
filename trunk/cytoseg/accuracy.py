
from numpy import *
import math


class Accuracy:

    def __init__(self, actualLabelVolume, computedLabelVolume):

        self.actualLabelVolume = actualLabelVolume
        self.computedLabelVolume = computedLabelVolume


    # computed true, but actual value is false
    def falsePositives(self):

        #print "self.computedLabelVolume shape:%s" % str(self.computedLabelVolume.shape)
        #print "self.actualLabelVolume shape:%s" % str(self.actualLabelVolume.shape)

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


    def accuracy(self):

        return (float(self.truePositives()) + float(self.trueNegatives())) /\
               (float(self.actualPositives()) + float(self.actualNegatives()))


    def VOC(self):

        return float(self.truePositives()) /\
               (float(self.truePositives()) + float(self.falsePositives()) + float(self.falseNegatives()))


    def printAccuracy(self):

        print "false positives:", self.falsePositives()
        print "true positives:", self.truePositives()
        print "false negatives:", self.falseNegatives()
        print "true negatives:", self.trueNegatives()
        print "size(self.actualLabelVolume):", size(self.actualLabelVolume)
        #print self.actualLabelVolume
        print "error:",\
            float(self.falsePositives() + self.falseNegatives()) /\
            float(size(self.actualLabelVolume))
        #print "true positives / actual positives:",\
        #    float(self.truePositives()) /\
        #    float(self.actualPositives())
        #print "false positives / actual positives:",\
        #    float(self.falsePositives()) /\
        #    float(self.actualPositives())
        tpr = self.truePositiveRate()
        fpr = self.falsePositiveRate()
        print "true positive rate:", float(tpr)
        print "false positive rate:", float(fpr)
        print "accuracy:", self.accuracy()
        print "VOC:", self.VOC()
        print "distance from ideal point:", math.sqrt(math.pow(fpr,2) + math.pow(tpr-1.0, 2))
        print "my error measure:", 5*fpr + (1-tpr)
        print "my error measure 2:", 5*math.pow(fpr,2) + math.pow((1-tpr),2)
        print "my error measure 3:", 10*fpr + (1-tpr)
        print "my error measure 4:", math.sqrt(math.pow(10*fpr,2) + math.pow((1-tpr),2))
        print "my error measure 5:", math.sqrt(math.pow(5*fpr,2) + math.pow((1-tpr),2))
        print "my error measure 6:", math.sqrt(math.pow(7*fpr,2) + math.pow((1-tpr),2)), "use this"

