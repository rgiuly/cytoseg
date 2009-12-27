import numpy

# moment about the value c
def moment(values, c, exponent):
    total = 0.0
    for value in values:
        total += ((value-c)**exponent)
    return total / len(values)

# returns mean, standard deviation, third moment, fourth moment
def moments(values):
    meanValue = numpy.mean(values)
    return (meanValue,
            numpy.sqrt(moment(values, meanValue, 2)),
            moment(values, meanValue, 3),
            moment(values, meanValue, 4))


# returns minimum, 0.25-quantile, median, 0.75-quantile, maximum
def sortAndReturnQuantiles(values):
    
    values.sort()
    N = len(values)
    return (values[0], values[N/4], values[N/2], values[(3*N)/4], values[N-1])
