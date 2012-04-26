# Container class to hold a probability value and a color.
# Used when an object has a certain probability of detection and a color associated with it.

class ProbabilityObject():
    """Represents a probability and color value for a detected object"""

    def __init__(self):

        self._color = [0, 255, 0]
        self._probability = None
        #self.activeDisplay = True
        self.filterActive = True


    def __repr__(self):
        """Return string representation of probability object"""

        return "ProbabilityObject _probability:%s" % str(self.probability()) +\
            " " +\
            "filterActive:" + str(self.filterActive) + " " +\
            "_color:" + str(self._color)

    
    def color(self):
        """Get color for this object"""

        return self._color
    

    def setColor(self, color):
        """Set color for this object"""

        self._color = color


    def probability(self):
        """Probability that this object is detected correctly"""

        return self._probability


    def setProbability(self, p):
        """Set probability that this object is detected correctly"""

        self._probability = p
    
