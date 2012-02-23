
from contour_comparison import *

contour0 = Contour()
contour0.setPoints(((0, 10, 0), (0, 0, 0), (0, 10, 0), (10, 10, 0)))

contour1 = Contour()
contour1.setPoints(((0, 10, 0), (0, 0, 0), (0, 10, 0), (10, 12, 0)))

b = biggestGap(contour0, contour1)
print "biggest gap:", b

print "bounding box:", contour0.get2DBoundingBox()

