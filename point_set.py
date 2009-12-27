
#from tree import Node

# todo: make this a superclass of Particle class
# (could call this AnnotatedPoint)

from numpy import *
from probability_object import *

#class PointSet(Node):
class PointSet(ProbabilityObject):
#    def __init__(self, center=None, size=None, points=[], color=[100,0,0]):
    def __init__(self, center=None, size=None, points=None):
        
        #Node.__init__(self)
        ProbabilityObject.__init__(self)
        
        self._center = center
        self._size = size
        #self._points = points
        #self._color = color
        
        if points == None:
            self._points = []
        else:
            self._points = points    

        self.features = {}
        self.labelSet = set()
        self.labelCountDict = None
        self.XMLTag = 'pointSet'
        self.pointListXMLTag = 'points'
        self.pointXMLFormatString = '%g %g %g, '
        
        #self.averageValueFromTrainingLabelVolume = None
    
    def points(self):
        return self._points
    
    def locations(self):
        resultList = []
        for object in self._points:
            if isinstance(object, list):
                resultList.append(object)
            elif isinstance(object, tuple):
                resultList.append(object)
            elif isinstance(object, LabeledPoint):
                resultList.append(object.loc)
            else:
                raise Exception, "Objects in the point list of the Blob should be list, tuple, or LabeledPoint class, not of type %s." % type(object)
        return resultList
    
    def center(self):
        return self._center
    
    def setPoints(self, points):
        self._points = points
    
    def addNumpyPoints(self, numpyPoints):
        for numpyPoint in numpyPoints:
            self.addPoint(LabeledPoint(numpyPoint))

    def __repr__(self):
        #return "Blob_with_%d_points" % len(self.points())
        return "PointSet " +\
                "labelCountDict: " + str(self.labelCountDict) + " " +\
                "labelSet: " + str(self.labelSet) + " " +\
                "probability(): " + str(self.probability())
    
    def setCenter(self, centerPoint):
        self._center = centerPoint

    def size(self):
        return self._size
    
    def setSize(self, size):
        self._size = size
    
    def addToSize(self, value):
        self._size += value
    
    #def addToSize(self, value):
    #    self._size += value
    
    
    # this is sort of like size() but size can be set to anything so there is no guarantee they will be the same.
    def numPoints(self):
        return len(self.points())

    def addPoint(self, labeledPoint):
        self._points.append(labeledPoint)
    
    def addNonzeroVoxels(self, volume):
        
        for i in range(volume.shape[0]):
            for j in range(volume.shape[1]):
                for k in range(volume.shape[2]):
                    if volume[i, j, k] != 0:
                        self.addPoint(LabeledPoint((i, j, k)))
    
    
#    def getLocationsXML(self, doc):
#
#        text = ""
#        for loc in self.locations():
#            text += self.pointXMLFormatString % (loc[0], loc[1], loc[2])
#        
#        voxelsElement = doc.createElement(self.pointListXMLTag)
#        voxelsText = doc.createTextNode(text)
#        voxelsElement.appendChild(voxelsText)
#        
#        return voxelsElement


    def getLocationsString(self):

        text = ""
        for loc in self.locations():
            text += self.pointXMLFormatString % (loc[0], loc[1], loc[2])
        
        return text
    

    def getAveragePointLocation(self):
        
        total = array((0, 0, 0))
        for labeledPoint in self.points():
            total += labeledPoint.loc

        return total / float(self.numPoints())
    

    def getXMLObject(self, doc, nodeName):

        #print dir(self)
        objectElement = doc.createElement(self.XMLTag)
        objectElement.setAttribute('name', nodeName)
        objectElement.setAttribute('class', 'Vesicle')
        objectElement.setAttribute('points', self.getLocationsString())

        return objectElement


class LabeledPoint:
    def __init__(self, location):
        self.loc = location
        self.adjacentNonzeroPoints = []
        self.adjacentNonzeroValues = []
        self.adjacentNonzeroValueSet = set()



class Blob(PointSet):

    def __init__(self, center=None, size=None, points=None):
        PointSet.__init__(self, center, size, points)
        self.XMLTag = 'blob'
        self.pointListXMLTag = 'voxels'
        self.pointXMLFormatString = '%d, %d, %d '



class Contour(PointSet):

    def __init__(self, center=None, size=None, points=None):
        PointSet.__init__(self, center, size, points)
        self.XMLTag = 'Contour'



class ProbabilityFilter():

    def __init__(self, minimumRequiredProbability):
        self.minimumRequiredProbability = minimumRequiredProbability

    def isValid(self, node):
        return node.object.probability() >= self.minimumRequiredProbability



