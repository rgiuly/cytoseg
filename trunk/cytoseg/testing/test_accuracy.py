
from numpy import *
from accuracy import *

actual   = array([1,  1,  0,  0,  0,  0])
computed = array([1,  0,  1,  0,  1,  0])
#                 tp  fn  fp  tn  fp  tn

#                         count
# fp: false positives     2
# tp: true positives      1
# fn: false negatives     1
# tn: true negatives      2

accuracy = Accuracy(actual, computed)
accuracy.printAccuracy()
