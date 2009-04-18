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

        self._color = [100,0,0]
        self._probability = 0
        self.features = {}
        
        #self.averageValueFromTrainingLabelVolume = None
    
    def points(self):
        return self._points
    
    def center(self):
        return self._center
    
    def setPoints(self, points):
        self._points = points 
    
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

  
