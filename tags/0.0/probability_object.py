
class ProbabilityObject():

    def __init__(self):

        self._color = [0, 255, 0]
        self._probability = 0
        #self.activeDisplay = True
        self.filterActive = True


    def __repr__(self):

        return "ProbabilityObject probability: %s" % str(self.probability())

    
    def color(self):

        return self._color
    

    def setColor(self, color):

        self._color = color


    def probability(self):

        return self._probability


    def setProbability(self, p):

        self._probability = p
    
