
import os
import socket
from time import localtime, strftime
import pickle
import default_path
import matplotlib.pyplot as pyplot

from containers import *





def plotROC(plotDataItem, formatString=''):

    truePositiveRates = plotDataItem['truePositiveRates']
    falsePositiveRates = plotDataItem['falsePositiveRates']

    curve = pyplot.plot(falsePositiveRates, truePositiveRates, formatString)

    return curve


def plotSinglePoint(plotDataItem, color='r', marker='o', size=10):

    xCoord = plotDataItem['singlePointX']
    yCoord = plotDataItem['singlePointY']
    print "xCoord", xCoord
    print "yCoord", yCoord
    return pyplot.scatter((xCoord,),
                          (yCoord,),
                          s=size,
                          c=color,
                          marker=marker)


def plotFromFile(filename):

    pyplot.hold(True)

    fullFilename = os.path.join(default_path.cytosegDataFolder, filename)
    file = open(fullFilename, 'rb')

    plotData = pickle.load(file)

    file.close()

    graphicsObjectDict = odict()

    if 0:
        for volumeName in plotData:
    
            print volumeName
    
            #print "falsePositiveRates", falsePositiveRates
            #print "truePositiveRates", truePositiveRates
    
            graphicsObjectDict[volumeName] = plotROC(plotData[volumeName])
            plotSinglePoint(plotData[volumeName])


    if 1:
        graphicsObjectDict['Original Image'] = plotROC(plotData['originalVolume'], formatString='g--')
        if 'radonVolume' in plotData:
            graphicsObjectDict['Radon-Like Features'] = plotROC(plotData['radonVolume'], formatString='r-.')
        graphicsObjectDict['Voxel Classifier Output'] = plotROC(plotData['voxelClassificationVolume'], formatString='b')
        graphicsObjectDict['Salient Contours'] = plotSinglePoint(plotData['contourOutputVolume'], size=20)
        graphicsObjectDict['Level Set Output'] = plotSinglePoint(plotData['blobOutputVolume'], color='y', marker='^', size=40)

    print plotData

    graphicsObjects = []
    labels = []

    for item in graphicsObjectDict.items():
        volumeName = item[0]
        graphicsObjects.append(graphicsObjectDict[volumeName])
        labels.append(volumeName)

    if 1:
        pyplot.figlegend(graphicsObjects, labels, 'upper right')

    pyplot.xlabel('False Positive Rate')
    pyplot.ylabel('True Positive Rate')
    pyplot.grid(True)

    #pyplot.axis([0.05, 0.3, 0.7, 1])
    #pyplot.axis([0, 0.3, 0.7, 1])
    pyplot.axis([0, 0.3, 0.6, 1])
    #pyplot.axis([0, 1, 0, 1])

    pyplot.show()



def setDataFolder(folder):

    if socket.gethostname() == 'cytoseg.crbs.ucsd.edu':
        baseFolder = "/home/rgiuly/"
    else:
        baseFolder = "O:/"

    #cytosegDataFolder = os.path.join(baseFolder, "cytoseg_data")
    #cytosegDataFolder = os.path.join(baseFolder, "cytoseg_data_dentate_gyrus")
    #cytosegDataFolder = os.path.join(baseFolder, "cytoseg_data_retina")
    cytosegDataFolder = os.path.join(baseFolder, folder)
    default_path.defaultTemporaryFolder = cytosegDataFolder
    default_path.cytosegDataFolder = cytosegDataFolder
    default_path.contourOutputTemporaryFolder = cytosegDataFolder
    default_path.defaultOutputPath = cytosegDataFolder



#plotFromFile("plotData_2010-12-05_18.30.19.pickle")
#plotFromFile("plotData_2010-12-30_10.13.49.pickle")
#plotFromFile("plotData_2011-01-26_10.50.52.pickle")
#plotFromFile("plotData_2011-01-28_11.57.23.pickle") #paper
#plotFromFile("plotData_2011-11-20_23.28.32.pickle")
#plotFromFile("plotData_2011-11-21_13.10.43.pickle") # cerebellum
#plotFromFile("plotData_2011-11-27_15.07.53.pickle") # dentate gyrus
#plotFromFile("plotData_2011-12-04_15.58.39.pickle") # retina
#plotFromFile("plotData_2011-12-05_01.45.07.pickle")
#plotFromFile("plotData_2011-12-05_18.05.40.pickle")
#plotFromFile("plotData_2011-12-05_22.06.24.pickle")

#setDataFolder("cytoseg_data_CA3")
#plotFromFile("plotData_2011-12-11_01.38.19.pickle")
#plotFromFile("plotData_2011-12-14_00.09.43.pickle")
#plotFromFile("plotData_2011-12-14_00.25.35.pickle")
#plotFromFile("plotData_2011-12-24_22.55.22.pickle")

setDataFolder("cytoseg_data")
plotFromFile("plotData_2011-12-27_18.20.54.pickle")

