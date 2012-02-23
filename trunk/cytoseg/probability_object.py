
class ProbabilityObject():

    def __init__(self):

        self._color = [0, 255, 0]
        self._probability = None
        #self.activeDisplay = True
        self.filterActive = True


    def __repr__(self):

        return "ProbabilityObject _probability:%s" % str(self.probability()) +\
            " " +\
            "filterActive:" + str(self.filterActive) + " " +\
            "_color:" + str(self._color)

    
    def color(self):

        return self._color
    

    def setColor(self, color):

        self._color = color


    def probability(self):

        return self._probability


    def setProbability(self, p):

        self._probability = p
    
