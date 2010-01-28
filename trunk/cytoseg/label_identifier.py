
class LabelIdentifier:

    def __init__(self, min, max=None):

        self.min = min
        self.max = max


    def isMember(self, value):

        if self.max == None:
            if value >= self.min:
                return True
        else:
            if self.min <= value <= self.max:
                return True
            else:
                return False

