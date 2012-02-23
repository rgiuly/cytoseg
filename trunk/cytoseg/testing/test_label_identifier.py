
from label_identifier import *
from numpy import *

labelIdentifer = LabelIdentifier(min=2, max=3)

a = zeros((10, 10, 10))
a[0,0,0] = 1
a[0,1,0] = 2
a[1,0,1] = 3
a[1,1,1] = 4

print labelIdentifer.count(a)

