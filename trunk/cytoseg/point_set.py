# todo: make this a superclass of Particle class
# (could call this AnnotatedPoint)
class LabeledPoint:
    def __init__(self, location):
        self.loc = location
        self.adjacentNonzeroPoints = []
        self.adjacentNonzeroValues = []
        self.adjacentNonzeroValueSet = set()



class Blob:
#    def __init__(self, center=None, size=None, points=[], color=[100,0,0]):
    def __init__(self, center=None, size=None, points=None):
        self._center = center
        self._size = size
        #self._points = points
        #self._color = color
        
        if points == None:
            self._points = []
        else:
            self._points = points    

        self._color = [0, 255, 0]
        self._probability = 0
        self.features = {}
        
        #self.averageValueFromTrainingLabelVolume = None
    
    def points(self):
        return self._points
    
    def center(self):
        return self._center
    
    def setPoints(self, points):
        self._points = points
    
    def addNumpyPoints(self, numpyPoints):
        for numpyPoint in numpyPoints:
            self.addPoint(LabeledPoint(numpyPoint))

    def color(self):
        return self._color
    
    def setColor(self, color):
        self._color = color

    def probability(self):
        return self._probability

    def setProbability(self, p):
        self._probability = p
    
    def __repr__(self):
        return "Blob_with_%d_points" % len(self.points())
    
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
    
    
    def getXMLVoxelList(self, doc):

        text = ""
        for labeledPoint in self.points():
            loc = labeledPoint.loc
            text += "%d,%d,%d " % (loc[0], loc[1], loc[2])
        
        voxelsElement = doc.createElement("voxels")
        voxelsText = doc.createTextNode(text)
        voxelsElement.appendChild(voxelsText)
        
        return voxelsElement
    

    def getAveragePointLocation(self):
        
        total = array((0, 0, 0))
        for labeledPoint in self.points():
            total += labeledPoint.loc

        return float(total) / float(numPoints())


  
