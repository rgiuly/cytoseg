
from containers import *
from cytoseg_classify import *
from probability_object import *


class ContourListProperties(ProbabilityObject):


    def __init__(self):

        self.featureDict = None
        self.className = None
        self.intersectionOfLabelSets = None
        self.isConnected = None


    def __repr__(self):

        return "ContourListProperties\n" +\
                str(self.className) + "\n" +\
                "intersectionOfLabelSets: " + str(self.intersectionOfLabelSets) + "\n" +\
                "isConnected: " + str(self.isConnected) + "\n" +\
                str(self.featureDict)



def isConnected(contourListNode):

    intersectionOfLabelSets = contourListNode.children[0].object.labelSet
    for contourNode in contourListNode.children:
        intersectionOfLabelSets.intersection_update(contourNode.object.labelSet)

    if intersectionOfLabelSets:
        return True # set is not empty
    else:
        return False # set is empty


def getContourListFeatures(contourListNode):

    featureDict = odict()
    lastContourFeatures = None
    count = 0

    for contourNode in contourListNode.children:

        contour = contourNode.object
        for featureName in contour.features:
            key = 'contour%d_%s' % (count, featureName)
            #print key
            featureDict[key] = contour.features[featureName]
            if lastContourFeatures != None:
                differenceKey = 'difference_' + key
                featureDict[differenceKey] = lastContourFeatures[featureName] -\
                        contour.features[featureName]
        count += 1
        lastContourFeatures = contour.features

    return featureDict


def getContourListProperties(contourListNode):

    contourListProperties = ContourListProperties()
    contourListProperties.featureDict = getContourListFeatures(contourListNode)
    #contourListProperties.className
    #contourListProperties.intersectionOfLabelSets
    contourListProperties.isConnected = isConnected(contourListNode)

    return contourListProperties


def recordFeaturesOfContourLists(dataViewer,
                                 inputTrainingContourListsNodePath,
                                 outputExamplesFilename):


    file = open(outputExamplesFilename, "w")

    print "recordFeaturesOfContourLists file name: " + outputExamplesFilename

    contourListsNode =\
        dataViewer.mainDoc.dataTree.getSubtree(inputTrainingContourListsNodePath)
    
    # get point features at the arbitrary point [3,3,3] to get a list of feature names
    dictionary = getContourListFeatures(contourListsNode.children[0])
    featureList = []
    for item in dictionary.items():
        key = item[0]
        featureList.append(key)
    
    writeOrangeNativeDataFormatHeader(file, featureList)

    for contourListNode in contourListsNode.children:
                
                contourListProperties = contourListNode.object
                dataViewer.writeExample(file,
                                        contourListProperties.featureDict,
                                        contourListProperties.isConnected)

                
    
    file.close()


def classifyContourLists(dataViewer,
                         inputTrainingExamplesFilename,
                         contourListsNodePath):
    
    #identifier = 'test'

    data = orange.ExampleTable(inputTrainingExamplesFilename)
    
    minimumExamples = len(data) / 5
    
    tree = orngTree.TreeLearner(storeNodeClassifier = 0,
                                storeContingencies=0,
                                storeDistributions=1,
                                minExamples=minimumExamples, ).instance()
    gini = orange.MeasureAttribute_gini()
    tree.split.discreteSplitConstructor.measure = \
     tree.split.continuousSplitConstructor.measure = gini
    tree.maxDepth = 5
    tree.split = orngEnsemble.SplitConstructor_AttributeSubset(tree.split, 3)

    forest = orngEnsemble.RandomForestLearner(data, trees=50,
                                              name="forest", learner=tree)
    
   
    print "number of examples:", len(data)
    print "minimumExamples:", minimumExamples
    
    count = 0

    print "data.domain.attributes", data.domain.attributes, len(data.domain.attributes) 
    print "data.domain.variables", data.domain.variables, len(data.domain.variables)

    print "Possible classes:", data.domain.classVar.values

    contourListsNode =\
        dataViewer.mainDoc.dataTree.getSubtree(contourListsNodePath)

    for contourListNode in contourListsNode.children:
        
        #dictionary = getFeaturesAt(self.getCurrentVolume(), self.mainDoc.volumeDict, (x,y,z))
        #dictionary = getFaceFeatures('training', faceBlob, volume, superVoxelDict, self.mainDoc.volumeDict)
        dictionary = getContourListFeatures(contourListNode)
        list = []
        #print "dictionary.items()", len(dictionary.items()), dictionary.items()
        for item in dictionary.items():
            value = item[1]
            list.append(value)
        list.append('False') # todo: what would happen if you used True here

        example = orange.Example(data.domain, list)
        p = forest(example, orange.GetProbabilities)    
        
        # todo: this should be checked once immediately after the training data file is read rather than checked here
        if len(p) == 1:
            raise Exception, "There is only one class in the data. There should be two classes like true and false."
        
        contourListNode.object.setProbability(p[1])

        colorScaleFactor = 5.0

        for contourNode in contourListNode.children:
            contourNode.object.setColor([200 - ((colorScaleFactor * p[1]) * 200),
                                         (colorScaleFactor * p[1]) * 200, 0]) 
            #contourNode.object.setProbability(p[1])
