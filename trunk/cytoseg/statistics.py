# Utility functions for calculating statistics

import numpy

def moment(values, c, exponent):
    """Returns moment about the value c"""

    total = 0.0
    for value in values:
        total += ((value-c)**exponent)
    return total / len(values)


def moments(values):
    """Returns mean, standard deviation, third moment, fourth moment"""

    meanValue = numpy.mean(values)
    return (meanValue,
            numpy.sqrt(moment(values, meanValue, 2)),
            moment(values, meanValue, 3),
            moment(values, meanValue, 4))


def sortAndReturnQuantiles(values):
    """Returns minimum, 0.25-quantile, median, 0.75-quantile, maximum"""
    
    values.sort()
    N = len(values)
    return (values[0], values[N/4], values[N/2], values[(3*N)/4], values[N-1])
