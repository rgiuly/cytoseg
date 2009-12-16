from data_viewer import *
from geometry import *
from neural_network import *

#from scipy import ndimage
#import geometry

#import SciPy
import statistics
import os
import threading
try:
    import orange, orngTree, orngEnsemble
    print "orange loaded"
except ImportError:
    print "orange data mining tool not loaded" 

from filters import *
from volume3d_util import *

cubeSizeNames = ('3X3', '5X5', '7x7')
cubeOffsets = (1, 2, 3)
#salientLabelValue = 100

count = 0

class Bubble:
    def __init__(self, location, radius, thickness):
        self.loc = location
        self.radius = radius
        self.thickness = thickness



class BubblePhantom:
    
    def __init__(self, signalBubbles, noiseBubbles, volumeShape):
        self.volumeShape = volumeShape
        self.signalBubbles = signalBubbles
        self.noiseBubbles = noiseBubbles
        
        self.salientLabelValue = 100
        
    def createSignalVolume(self):
        bubbles = self.signalBubbles
        return self.createVolumeWithBubbles(bubbles)

    def createVolume(self):
        bubbles = self.signalBubbles + self.noiseBubbles
        return self.createVolumeWithBubbles(bubbles)


    def createVolumeWithBubbles(self, bubbles):
        
        
        v = numpy.zeros(self.volumeShape, numpy.uint8)
        
        for x in range(self.volumeShape[0]):
            for y in range(self.volumeShape[1]):
                for z in range(self.volumeShape[2]):
                    #print ""
                    for bubble in bubbles:
                        distanceFromSphereSurface = abs(bubble.radius - distance(bubble.loc, array([x,y,z])))
                        v[x,y,z] += gaussian(distanceFromSphereSurface, 50, bubble.thickness)
    
        return v



    def createSignalLabelVolume(self):
        #return 100.0 * (self.createSignalVolume() > 20)
        return self.salientLabelValue * (self.createSignalVolume() > 20)


def makeClassifyGUITree():
    rootNode = makeDefaultGUITree()
    #print "rootNode"
    #print rootNode
    node = getNode(rootNode, ('particleMotionTool',))
    #print node
    #node.insertChildrenAt((
    node.addChildren((
                    DataNode("facesProbabilityThreshold","slider",{'caption' : 'facesProbabilityThreshold', 'max' : 300},0),
                    DataNode("useFacesProbabilityThreshold","boolean",{'caption' : 'useFacesProbabilityThreshold'},False),
                    DataNode("displayPixelFeature","boolean",{'caption' : 'displayPixelFeature'},False),
                    #DataNode("learnFeaturesOfMembraneVoxels","button",{'caption' : 'step 1. learnFeaturesOfMembraneVoxels'},'old_onLearnFeaturesOfMembraneVoxels'),
                    #DataNode("classifyVoxelsOfCurrentImage","button",{'caption' : 'step 2. classifyVoxelsOfCurrentImage'},'old_onClassifyVoxelsOfCurrentImage'),
                    DataNode("learnFeaturesOfMembraneVoxels","button",{'caption' : 'step 1. learnFeaturesOfMembraneVoxels'},'onLearnFeaturesOfMembraneVoxels'),
                    #DataNode("classifyVoxelsOfCurrentImage","button",{'caption' : 'step 2. classifyVoxelsOfCurrentImage'},'old_onClassifyVoxelsOfCurrentImage'),
                    DataNode("classifyVoxelsOfImageStack","button",{'caption' : 'step 2. classifyVoxelsOfImageStack'},'onClassifyVoxelsOfImageStack'),

                    #DataNode("learnFeaturesOfMembraneFaces","button",{'caption' : 'learnFeaturesOfMembraneFaces'},'onLearnFeaturesOfMembraneFaces'),
                    DataNode("findAndClassifyFaces","button",{'caption' : 'findAndClassifyFaces'},'onFindAndClassifyFaces'),

                    DataNode("calculateDerivatives","button",{'caption' : 'calculateDerivatives'},'onCalculateDerivatives'),
                    DataNode("calculateSecondDerivatives","button",{'caption' : 'calculateSecondDerivatives'},'onCalculateSecondDerivatives'),
                    DataNode("convolutionTest","button",{'caption' : 'convolutionTest'},'onConvolutionTest'),
                    DataNode("makeVoxelClassificationDataFile","button",{'caption' : 'makeVoxelClassificationDataFile'},'old_onMakeVoxelClassificationDataFile'),
                    DataNode("makePointFeatureViewer","button",{'caption' : 'makePointFeatureViewer'},'onMakePointFeatureViewer'),
                    DataNode("makeFaceFeatureViewer","button",{'caption' : 'makeFaceFeatureViewer'},'onMakeFaceFeatureViewer'),
                    DataNode("makeBubblePhantom","button",{'caption' : 'Make Bubble Phantom'},'onMakeBubblePhantom')))
    
    return rootNode


class ClassificationSequenceThread(threading.Thread):

#todo: make a class like this that you can pass an arbitary function to and have it run the function in the thread
    
    def __init__(self, frame):
        threading.Thread.__init__(self)
        self.frame = frame
    
    def run(self):
        self.frame.runClassificationSequence()
        



class ClassificationControlsFrame(ControlsFrame):


    def __init__(self, settingsTree):
        ControlsFrame.__init__(self, settingsTree)
        print "ClassificationControlsFrame init"
        
        self.mouseClickCallbackDict['updatePointFeaturesAtMouseLocation'] = self.updatePointFeaturesAtMouseLocation
        self.mouseClickCallbackDict['printBlobNameAtMouseLocation'] = self.printBlobNameAtMouseLocation
        self.refreshGUI()
        
        #sourceType = 'phantom'
        sourceType = 'imageFile'
        
        # this chooses whether to use original image or probability of salient pixel image for watershed
        useOriginalForWatershed = True

        self.viewerRootNode = None


        thread = ClassificationSequenceThread(self)
        thread.start()


        if 0:
            # display volumes
            self.getPersistentVolume_old('test_Original')
            self.getPersistentVolume_old('voxelClassificationOnTestVolume_ProbabilityVolume')
            self.getPersistentVolume_old('forFaceTraining_ProbabilityVolume')
                        
            for i in range(3):
                self.getPersistentVolume_old('%s_0Gradient_blur%d' % ('test', i))
                self.getPersistentVolume_old('%s_1Gradient_blur%d' % ('test', i))
                self.getPersistentVolume_old('%s_2Gradient_blur%d' % ('test', i))


    def runClassificationSequence(self):

        voxelTrainingImageFilePath = "O:\\images\\HPFcere_vol\\HPF_rotated_tif\\three_compartment\\"
        voxelTrainingLabelFilePath = "O:\\images\\HPFcere_vol\\HPF_rotated_tif\\three_compartment\\membrane_label_for_three_compartments\\"

        #self.trainingImageFilePath = "O:\\images\\HPFcere_vol\\HPF_rotated_tif\\8bit\\training\\filtered_tif\\"
        self.trainingImageFilePath = "O:\\images\\HPFcere_vol\\HPF_rotated_tif\\median_then_gaussian_8bit\\"
        self.trainingLabelFilePath = "O:\\images\\HPFcere_vol\\face_training_labels_feb_2009\\"
        self.trainingMembranePhantom = self.membranePhantom1
        
        self.testImageFilePath = "O:\\images\\HPFcere_vol\\HPF_rotated_tif\\seg3D\\tifs\\cropped\\" 
        self.testMembranePhantom = self.membranePhantom2

        self.derivativesForPointViewerIdentifier = "test"

        currentStep = 0
        
        
        if 0:
            print "running step", currentStep
            if currentStep == 0:
                # uses training data
                self.learnFeaturesOfMembraneVoxels(voxelTrainingImageFilePath, voxelTrainingLabelFilePath, "c:\\temp\\output.tab")
                
                # uses test data, generates voxel probabilities
                self.classifyVoxels('intermediate1', 'forFaceTraining', "c:\\temp\\output.tab", self.trainingImageFilePath)

            elif currentStep == 1:
                self.classifyVoxels('intermediate2', 'voxelClassificationOnTestVolume', self.testImageFilePath)


            elif currentStep == 2:
                # uses training data
                self.learnFeaturesOfMembraneFaces(sourceType, useOriginalForWatershed, self.trainingImageFilePath, self.trainingLabelFilePath, 'faceTraining', 'forFaceTraining_ProbabilityVolume', (1, 1, 0, 0))
                
                # uses test data, uses pixel probabilities for test data
                self.findAndClassifyFaces('faceTraining', sourceType, useOriginalForWatershed, 'voxelClassificationOnTestVolume_ProbabilityVolume', (1, 0, 0))
                
            elif currentStep == 3:
                self.learnFeaturesOfMembraneFaces(sourceType, useOriginalForWatershed, self.trainingImageFilePath, self.trainingLabelFilePath, 'faceTraining', 'forFaceTraining_ProbabilityVolume', (0, 0, 1, 1))
                self.findAndClassifyFaces('faceTraining', sourceType, useOriginalForWatershed, 'voxelClassificationOnTestVolume_ProbabilityVolume', (0, 1, 1))




    def calculateDerivatives(self, volume, groupName):
        
        #from mlabwrap import mlab

        #self.getCurrentVolume()
        #s = [5,5,5]
        volumeShape = [9,9,9]
        
        # todo: not really using cubeOffsets list anymore so you could remove it from the code
        for i in range(len(cubeOffsets)):
            #offset = cubeOffsets[i] * 2
            offset = 1
            for coordinate in range(0,3):
                sigma = .5 + i
                #g = [[None,None],[None,None],[None,None]]
                offsetVector = [0,0,0]
                #offsetVector[coordinate] = offset
                offsetVector[coordinate] = offset + (i*2)
                #print 'offset', offset
                print "amount of blur ", sigma

                DoOG = differenceOfOffsetGaussians(volumeShape, offsetVector, sigma)

                convolvedVolume = ndimage.convolve(array(volume, dtype=float), DoOG)
                
                #self.addPersistentVolumeAndRefreshDataTree(mlab.convn(volume, DoOG, 'same'), '%s_%dGradient_blur%d' % (groupName, coordinate, i))
                self.addPersistentVolumeAndRefreshDataTree(convolvedVolume, '%s_%dGradient_blur%d' % (groupName, coordinate, i))
                #print '%dGradient%f' % (coordinate, sigma)
        
        #volumes['Original'] = mlab.abs(g2 - g1)


    # calculates elements of Hessian matrix
    def calculateSecondDerivatives(self, volume, groupName):

        from mlabwrap import mlab
        volumeShape = [9,9,9]
        sigma = 0.5

        for coordinateA in range(3):
            for coordinateB in range(3):
                
                offsetVectorA = [0,0,0]
                offsetVectorA[coordinateA] = 1
                
                offsetVectorB = [0,0,0]
                offsetVectorB[coordinateB] = 1
                
                DoOG_A = differenceOfOffsetGaussians(volumeShape, offsetVectorA, sigma)
                DoOG_B = differenceOfOffsetGaussians(volumeShape, offsetVectorB, sigma)
                secondDerivativeKernel = mlab.convn(DoOG_A, DoOG_B, 'same')
                self.addPersistentVolumeAndRefreshDataTree(mlab.convn(volume, secondDerivativeKernel, 'same'), '%s_%d,%d' % (groupName, coordinateA, coordinateB))

        
    
    def onCalculateDerivatives(self, event):
        if self.getCurrentVolume() == None:
            raise Exception, "no current volume is selected"
        else:
            self.calculateDerivatives(self.getCurrentVolume(), 'default')


    def onCalculateSecondDerivatives(self, event):
        self.calculateSecondDerivatives(self.getCurrentVolume(), 'default')


    def onConvolutionTest(self, event):
        kernel = zeros((5,5,5))
        kernel[2,2,2] = 1
        result = ndimage.convolve(array(self.getCurrentVolume(), dtype=float), kernel)
        self.addVolumeAndRefreshDataTree(result, 'ConvolutionTest')


    def onMakePointFeatureViewer(self, event):
        if self.getCurrentVolume() == None:
            print "error: no volume selected"
        else:
            dictionary = getPointFeaturesAt(self.getCurrentVolume(), self.derivativesForPointViewerIdentifier, self, [3,3,3])
            for item in dictionary.items():
                print item[0]
            self.viewerRootNode = self.makeFeatureViewer(dictionary, 'featureSelection', "Feature Selection")


    def onMakeFaceFeatureViewer(self, event):
        #print ""
        dictionary = getFaceFeatures(self.getCurrentBlob(), self.mainDoc.volumeDict['Original'], self.superVoxelDict)
        self.blobFeatureViewerRootNode = self.makeFeatureViewer(dictionary, 'faceFeatureSelection', "Face Feature Selection")


    def onMakeBubblePhantom(self, event):
        
        # shape of volume
        sh = (30,35,40)
        #sh = (15,15,15)
        factor = 30
        #centers = [array([10,10,10])]
        
                
        membraneBubbles = [Bubble(factor * array([.5, .5, .5]), 6, .4),
                           Bubble(factor * array([0, .4, .5]), 8, .2),
                           Bubble(factor * array([.6, .8, 1]), 7, .6),
                           Bubble(factor * array([0, .5, .5]), 7, .2),
                           Bubble(factor * array([.3, 1, .8]), 7, .4),
                           Bubble(factor * array([.5, .5, .5]), 12, .6)]
                   
        noiseBubbles = [Bubble(factor * array([.2, 1.0, .5]), 14, 4),
                        Bubble(factor * array([1.0, .2, .5]), 14, 4),
                        Bubble(factor * array([1.0, 1.0, .2]), 14, 4)]
                   
        #radius = 5

        b = BubblePhantom(membraneBubbles, noiseBubbles, sh) 
        
        v = b.createSignalVolume()
        
        #self.addVolume(255-v, 'Original')
        self.addPersistentVolumeAndRefreshDataTree(v, 'Original')
        
        #membraneLabelVolume = makeBubblePhantom(membraneBubbles, sh) > 20
        #self.addVolume(membraneLabelVolume, 'MembraneLabelVolume')
        
        

    def makeFeatureViewer(self, dictionary, nodeName, caption):
        #self.viewerRootNode = DataNode("root","group","params","value")
        
        viewerNode = DataNode(nodeName,"group",{'caption' : caption, 'position' : (700,300), 'size' : (500,700)},None)
        
        #for key in getFeaturesAt(self.getCurrentVolume(), [3,3,3]):
        #dictionary = getFeaturesAt(self.getCurrentVolume(), [3,3,3])

        listOfFeatures = []
        
        for item in dictionary.items():
            key = item[0]
            node = DataNode(key,"slider",{'caption' : key, 'min' : -300, 'max' : 300},0)
            viewerNode.addChild(node)
            listOfFeatures.append(key)
            

        featureSelection = DataNode(nodeName,"listBox",{'caption' : caption, 'items' : listOfFeatures},0)
        viewerNode.addChild(featureSelection)

        self.generateComponents(viewerNode, 0, [], None, None, None)

        return viewerNode


    def getXYImage(self, volume, displayedRegionBox):

        if not(self.getValue(('particleMotionTool','displayPixelFeature'))):
            
            imageArray = ControlsFrame.getXYImage(self, volume, displayedRegionBox)
            
        else:
            
            if self.viewerRootNode != None:
            
                selectedFeature = (getNode(self.viewerRootNode, ('featureSelection',))).guiComponent.GetStringSelection()
                #print selectedFeature
               
                imageArray = zeros((displayedRegionBox.shape()[0], displayedRegionBox.shape()[1]))
                box = displayedRegionBox
                for x in range(box.cornerA[0] + borderWidthForFeatures+1, box.cornerB[0] - borderWidthForFeatures-1):
                    for y in range(box.cornerA[1] + borderWidthForFeatures+1, box.cornerB[1] - borderWidthForFeatures-1):
                        location = (x, y, box.cornerA[2])
                        
                        # if z value is out of range just return a image that has zeros in it
                        if not(isInsideVolumeWithBorder(volume, location, borderWidthForFeatures)):
                            return imageArray
                        
                        dictionary = getPointFeaturesAt(self.getCurrentVolume(), self.derivativesForPointViewerIdentifier, self, location)
                        #print dictionary
                        #print imageArray.shape
                        #print 'volume shape', volume.shape
                        #print 'box.cornerA[2]', box.cornerA[2]
                        imageArray[location[0], location[1]] = dictionary[selectedFeature]
                        #imageArray[location[0], location[1]] = 1
                
            else:
                imageArray = zeros((10,10))
                
        #return log(imageArray)
        
        return(imageArray)

        

    def old_onMakeVoxelClassificationDataFile(self, event):

        file = open("c:\\temp\\output.tab", "w")

        currentVolume = self.getCurrentVolume()
        sh = currentVolume.shape

        volume = numpy.zeros(sh)
        #selected x, y, and z
        
        dictionary = getPointFeaturesAt(currentVolume, self, [3,3,3])
        featureList = []
        for item in dictionary.items():
            key = item[0]
            featureList.append(key)
        
        writeOrangeNativeDataFormatHeader(file, featureList)
        
        # create a volume that has pixels turned on where the membrane is
        m = zeros(sh, numpy.uint8)
        for p in particleGroup.getAll():
            
            # todo: isInsideVolumeWithBorder should take shape as argument rather than volume
            if isInsideVolumeWithBorder(volume, p.loc, borderWidthForFeatures):
                m[p.loc[0],p.loc[1],p.loc[2]] = 1
                
                # write all true examples into tab file
                d = getPointFeaturesAt(currentVolume, self, p.loc)
                self.writeExample(file, d, True)
            
            
        self.addPersistentVolumeAndRefreshDataTree(m, 'MembraneVoxel')
        membraneVoxelVolume = self.getVolume('MembraneVoxel')
        
        border = borderWidthForFeatures
        for x in range(border,sh[0]-border,2):
            print "%d out of %d" % (x, sh[0])
            for y in range(border,sh[1]-border,2):
                for z in range(border,sh[2]-border,2):
                    
                    d = getPointFeaturesAt(currentVolume, self, (x,y,z))
                    
                    #xG = volumes['xGradient'][x,y,z]
                    #yG = volumes['yGradient'][x,y,z]
                    #zG = volumes['zGradient'][x,y,z]
        
                    #st = structureTensor(xG,yG,zG)
                    #eigenValues = numpy.linalg.eigvals(st)
                    
                    self.writeExample(file, d, (membraneVoxelVolume[x,y,z] != 0))

                    
        
        file.close()



#    def learnFeaturesOfMembraneVoxels(self, voxelTrainingImageFilePath, voxelTrainingLabelFilePath, voxelExamplesFilename):
#
#
#        file = open(voxelExamplesFilename, "w")
#
#        originalVolume = loadImageStack(voxelTrainingImageFilePath, None)
#        sh = originalVolume.shape
#
#        self.calculateDerivatives(originalVolume, 'training')
#
#        volume = numpy.zeros(sh)
#        #selected x, y, and z
#        
#        # get point features at the arbitrary point [3,3,3] to get a list of feature names
#        dictionary = getPointFeaturesAt(originalVolume, 'training', self, [3,3,3])
#        featureList = []
#        for item in dictionary.items():
#            key = item[0]
#            featureList.append(key)
#        
#        writeOrangeNativeDataFormatHeader(file, featureList)
#
#        # create a volume that has pixels turned on where the membrane is
#        membraneVoxelVolume = loadImageStack(voxelTrainingLabelFilePath, None)            
#        
#        self.addPersistentVolumeAndRefreshDataTree(membraneVoxelVolume, 'MembraneVoxel')
#        
#        border = borderWidthForFeatures
#        for x in range(border,sh[0]-border,2):
#            print "%d out of %d" % (x, sh[0])
#            for y in range(border,sh[1]-border,2):
#                for z in range(border,sh[2]-border,2):
#                    
#                    d = getPointFeaturesAt(originalVolume, 'training', self, (x,y,z))
#                    
#                    #xG = volumes['xGradient'][x,y,z]
#                    #yG = volumes['yGradient'][x,y,z]
#                    #zG = volumes['zGradient'][x,y,z]
#        
#                    #st = structureTensor(xG,yG,zG)
#                    #eigenValues = numpy.linalg.eigvals(st)
#                    
#                    self.writeExample(file, d, (membraneVoxelVolume[x,y,z] != 0))
#
#                    
#        
#        file.close()

    def learnFeaturesOfMembraneVoxels(self,
                                      voxelTrainingImageNodePath,
                                      voxelTrainingLabelNodePath,
                                      voxelExamplesFilename):


        file = open(voxelExamplesFilename, "w")

        originalVolume = self.getPersistentObject(voxelTrainingImageNodePath)
        sh = originalVolume.shape

        self.calculateDerivatives(originalVolume, 'training')

        volume = numpy.zeros(sh)
        #selected x, y, and z
        
        # get point features at the arbitrary point [3,3,3] to get a list of feature names
        dictionary = getPointFeaturesAt(originalVolume, 'training', self, [3,3,3])
        featureList = []
        for item in dictionary.items():
            key = item[0]
            featureList.append(key)
        
        writeOrangeNativeDataFormatHeader(file, featureList)

        # create a volume that has pixels turned on where the membrane is
        membraneVoxelVolume = self.getPersistentObject(voxelTrainingLabelNodePath)
        
        #self.addPersistentVolumeAndRefreshDataTree(membraneVoxelVolume, 'MembraneVoxel')
        
        border = borderWidthForFeatures
        for x in range(border,sh[0]-border,2):
            print "%d out of %d" % (x, sh[0])
            for y in range(border,sh[1]-border,2):
                for z in range(border,sh[2]-border,2):
                    
                    d = getPointFeaturesAt(originalVolume, 'training', self, (x,y,z))
                    
                    #xG = volumes['xGradient'][x,y,z]
                    #yG = volumes['yGradient'][x,y,z]
                    #zG = volumes['zGradient'][x,y,z]
        
                    #st = structureTensor(xG,yG,zG)
                    #eigenValues = numpy.linalg.eigvals(st)
                    
                    self.writeExample(file, d, (membraneVoxelVolume[x,y,z] != 0))

                    
        
        file.close()



    #def old_onLearnFeaturesOfMembraneVoxels(self, event):
    #    self.onLoadImageStack(None)
    #    self.onCalculateDerivatives(None)
    #    self.readIMODFile(None)
    #    self.onMakeVoxelClassificationDataFile(None)

    #def learnFeaturesOfMembraneVoxels(self):
    #    pass
    #    # comment: loadImageStack(originalVolumeName, filename)
    #    
    #    
    #    # comment: calculateDerivatives(prefix)
    #    # calculateDerivatives(volume, groupName)
    #    
    #    
    #    # comment: loadImageStack(membraneLabelVolumeName, filename)
    #    # membraneLabelVolume = loadImageStack(trainingLabelFilePath, None)
    #    
    #    # comment: makeVoxelClassificationDataFile(originalVolumeName, membraneLabelVolumeName)

    def onLearnFeaturesOfMembraneVoxels(self, event):

        dialog = wx.DirDialog(self, "Training Image Stack", os.getcwd(), style=wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            voxelTrainingImageFilePath = dialog.GetPath()
            print "Training Image Stack", dialog.GetPath()
        dialog.Destroy()

        dialog = wx.DirDialog(self, "Training Label Stack", os.getcwd(), style=wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            voxelTrainingLabelFilePath = dialog.GetPath()
            print "Training Label Stack", dialog.GetPath()
        dialog.Destroy()

        wildcard = "(*.tab)|*.tab|All files (*.*)|*.*"
        dialog = wx.FileDialog(self, "Write Examples to File", os.getcwd(), style=wx.OPEN, wildcard=wildcard)
        if dialog.ShowModal() == wx.ID_OK:
            print dialog.GetPath()
            voxelExamplesFilename = dialog.GetPath()
        dialog.Destroy()

        
        self.learnFeaturesOfMembraneVoxels(voxelTrainingImageFilePath,
                                           voxelTrainingLabelFilePath,
                                           voxelExamplesFilename)



    factor = 15.0
    #factor = 30.0
    
    membranePhantomVolumeShape = (round(1*factor), round(1.16*factor), round(1.33*factor))

    membraneBubbles1 = [Bubble(factor * array([.5, .5, .5]), 6, .4),
                   Bubble(factor * array([0, .4, .5]), 8, .2),
                   Bubble(factor * array([.6, .8, 1]), 7, .6),
                   Bubble(factor * array([0, .5, .5]), 7, .2),
                   Bubble(factor * array([.3, 1, .8]), 7, .4),
                   Bubble(factor * array([.5, .5, .5]), 12, .6)]
                   
    noiseBubbles1 = [Bubble(factor * array([.2, 1.0, .5]), 14, 4),
                Bubble(factor * array([1.0, .2, .5]), 14, 4),
                Bubble(factor * array([1.0, 1.0, .2]), 14, 4)]

    membraneBubbles2 = [Bubble(factor * array([.5, .5, .5]), 6, .4),
                   Bubble(factor * array([.4, 0, .5]), 8, .2),
                   Bubble(factor * array([.6, 1, .8]), 7, .6),
                   Bubble(factor * array([.5, 0, .5]), 7, .2),
                   Bubble(factor * array([.3, .8, 1]), 7, .4),
                   Bubble(factor * array([.5, .5, .5]), 12, .6)]


    #membraneBubbles2 = [Bubble(factor * array([.5, .5, .5]), 6, .8),
    #               Bubble(factor * array([.4, 0, .5]), 8, .2),
    #               Bubble(factor * array([.6, 1, .8]), 7, .6),
    #               Bubble(factor * array([.5, 0, .5]), 7, .2),
    #               Bubble(factor * array([.3, .8, 1]), 7, .4),
    #               Bubble(factor * array([.5, .5, .5]), 12, 1.2)]
                   
    noiseBubbles2 = [Bubble(factor * array([.2, .5, 1.0]), 14, 4),
                Bubble(factor * array([.2, 1.0, .5]), 14, 4),
                Bubble(factor * array([1.0, .2, 1.0]), 14, 4)]


    membranePhantom1 = BubblePhantom(membraneBubbles1, noiseBubbles1, membranePhantomVolumeShape)
    membranePhantom2 = BubblePhantom(membraneBubbles2, noiseBubbles2, membranePhantomVolumeShape)



    #def calculateBordersBetweenWatershedRegions(self, originalVolume, watershedVolumeName, inbetweenPointsBlobName):
       




    # generates watershed transform and blob of pixels between watershed regions, saves watershed transform and blob
    def calculateBorderBlobs(self, originalVolume, originalVolumeName, watershedVolumeName, inbetweenPointsBlobName):

        #self.addVolume(255-v, 'Original')
        self.addPersistentVolumeAndRefreshDataTree(originalVolume, originalVolumeName)
        
        #resizedVolume = makeEnlargedVolume(originalVolume, 2)
        
        #watershedVolume = watershed(resizedVolume, 26)
        watershedVolume = watershed(originalVolume, 26)
        self.addPersistentVolumeAndRefreshDataTree(watershedVolume, watershedVolumeName)

        blobForBorderVoxels = makeBlobFromVoxelsLabeledZero(watershedVolume, 1)

        #self.addBlobAndRefreshDataTree(blobForBorderVoxels, self.getBlobsNode(), inbetweenPointsBlobName)

        computeAdjacentValueSets(watershedVolume, blobForBorderVoxels)
        self.addPersistentBlobAndRefreshDataTree(blobForBorderVoxels, inbetweenPointsBlobName)
        
        if 0:
            listSizes = []
            for labeledPoint in blob.points():
                if len(labeledPoint.adjacentNonzeroValueSet) != 2:
                    listSizes.append(len(labeledPoint.adjacentNonzeroValueSet))
            print "list of sizes other than 2"
            print listSizes
        
        

    def splitBlobIntoFacesAndComputeSuperVoxelFeatures(self, facesNodeName, nonfacesNodeName, inbetweenPointsBlobName, membraneLabelVolumeName, watershedVolumeName):

        #self.onOpenDocument(None)
        #print "finished opening document"
    
        facesNode = DataNode(facesNodeName, 'type of node', None, None)
        self.getBlobsNode().addChild(facesNode)

        nonfacesNode = DataNode(nonfacesNodeName, 'type of node', None, None)
        self.getBlobsNode().addChild(nonfacesNode)

        
        #blobDict = splitBlobBasedOnAdjacentValueSet(self.mainDoc.blobDict['inbetweenPoints'])
        logStart("splitBlobBasedOnAdjacentValueSet")
        blobDict = splitBlobBasedOnAdjacentValueSet(self.getPersistentBlob(inbetweenPointsBlobName))
        logFinished("splitBlobBasedOnAdjacentValueSet")

        logStart("add blobs to tree")
       
        for key in blobDict:
            #self.mainDoc.blobDict['face_%s' % str(key)] = blobDict[key]
            #self.mainDoc.blobDict['%s' % str(key)] = blobDict[key]
            
            # faces have exactly two adjacent supervoxels. (other blobs are considered nonfaces)
            if len(key) == 2:
                self.addBlob(blobDict[key], facesNode, str(key))
            else:
                self.addBlob(blobDict[key], nonfacesNode, str(key))

    
        self.refreshGUI()

        logFinished("add blobs to tree")


        superVoxelDict = computeSuperVoxelFeatures(self.getPersistentVolume_old(watershedVolumeName))

        return (blobDict, superVoxelDict)

    def learnFeaturesOfMembraneFaces(self, sourceType, useOriginalForWatershed, trainingImageFilePath, trainingLabelFilePath, generatedDataIdentifier, volumeForWatershedName, doPart):

        if sourceType == 'phantom':
            membranePhantom = self.trainingMembranePhantom
            salientLabelValue = membranePhantom.salientLabelValue
        elif sourceType == 'imageFile':
            salientLabelValue = 1
        else:
            raise Exception, "invalid type %s" % sourceType                



        logStart("learnFeaturesOfMembraneFaces")

        if len(doPart) != 4:
            raise Exception, "doPart should be a list of 4 boolean values"

        prefix = generatedDataIdentifier + "_"
        membraneLabelVolumeName = prefix+'MembraneLabelVolume'
        originalVolumeName = prefix+'Original'

        if doPart[0]:

            if sourceType == 'phantom':
                originalVolume = self.makeEnlargedPhantom(membranePhantom)
            elif sourceType == 'imageFile':
                # load training image data from disk
                originalVolume = loadImageStack(trainingImageFilePath, None)
            else:
                raise Exception, "invalid type %s" % sourceType                

            if useOriginalForWatershed:
                volumeForWatershed = originalVolume
            else:
                volumeForWatershed = self.getPersistentVolume_old(volumeForWatershedName)


            # generates watershed transform and blob of pixels between watershed regions, saves watershed transform and blob
            self.calculateBorderBlobs(volumeForWatershed, originalVolumeName, prefix+'Watershed', prefix+'inbetweenPoints')  

            self.calculateDerivatives(self.getPersistentVolume_old(originalVolumeName), generatedDataIdentifier)


        if doPart[1]:

            if sourceType == 'phantom':
                #todo: enlarge the volume before thresholding rather than after
                membraneLabelVolume = membranePhantom.createSignalLabelVolume()
                membraneLabelVolume = makeEnlargedVolume(membraneLabelVolume, 2)
            elif sourceType == 'imageFile':
                # load membrane label volume from disk
                membraneLabelVolume = loadImageStack(trainingLabelFilePath, None)
            else:
                raise Exception, "invalid type %s" % sourceType

            self.addPersistentVolumeAndRefreshDataTree(membraneLabelVolume, membraneLabelVolumeName)

        if doPart[2]:

            # splits the blob of pixels that are inbetween watershed regions to produce faces
            blobDict, superVoxelDict = self.splitBlobIntoFacesAndComputeSuperVoxelFeatures(prefix+'faces', prefix+'nonfaces', prefix+'inbetweenPoints', prefix+'MembraneLabelVolume', prefix+'Watershed')
        
            #self.onMakePointFeatureViewer(None)
            #self.onMakeFaceFeatureViewer(None)

            # set blob colors
            for key in blobDict:
                value = calculateAverageValue(blobDict[key], self.getPersistentVolume_old(membraneLabelVolumeName))
                blobDict[key].setColor(faceBlobColorBasedOnAverageValue(value, salientLabelValue))
        
        
        if doPart[3]:
            # make face classification data file
            logStart("writeFaceClassificationTrainingData")
            self.writeFaceClassificationTrainingData(generatedDataIdentifier, "c:\\temp\\%sfaceClassificationTrainingData.tab" % prefix, superVoxelDict, prefix+'faces', prefix+'Original', volumeForWatershedName, membraneLabelVolumeName, salientLabelValue)
            logFinished("writeFaceClassificationTrainingData")

        logFinished("learnFeaturesOfMembraneFaces")        


    def onFindAndClassifyFaces(self, event):
        pass

    def makeEnlargedPhantom(self, membranePhantom):
            v = membranePhantom.createVolume()
            v = makeEnlargedVolume(v, 2)
            return v
    
    def findAndClassifyFaces(self, inputFileIdentifier, sourceType, useOriginalForWatershed, volumeForWatershedName, doPart):
        
        logStart("findAndClassifyFaces")
        
        
        if len(doPart) != 3:
            raise Exception, "doPart should be a list of 3 boolean values"

        generatedDataIdentifier = 'test'
        prefix = generatedDataIdentifier + "_"
        originalVolumeName = prefix+'Original'


        if doPart[0]:
        
            if sourceType == 'phantom':
                membranePhantom = self.testMembranePhantom
                originalVolume = self.makeEnlargedPhantom(membranePhantom)
            elif sourceType == 'imageFile':
                #self.onLoadImageStack(None)
                # todo: the volume should come from the data tree rather than this dictionary and the dictionary for volumes should nolonger exist
                #originalVolume = self.getPersistentVolume_old('LoadedVolume')
                originalVolume = loadImageStack(self.testImageFilePath, None)            
                self.addPersistentVolumeAndRefreshDataTree(originalVolume, originalVolumeName)


            else:
                raise Exception, "invalid type %s" % sourceType

            # generates watershed transform and blob of pixels between watershed regions, saves watershed transform and blob
            # todo: originalVolumeName should be something like forWatershedVolumeName
            if useOriginalForWatershed:
                volumeForWatershed = originalVolume
            else:
                volumeForWatershed = self.getPersistentVolume_old(volumeForWatershedName)
            
            self.calculateBorderBlobs(volumeForWatershed, originalVolumeName, prefix+'Watershed', prefix+'inbetweenPoints')  

            self.calculateDerivatives(self.getPersistentVolume_old(originalVolumeName), generatedDataIdentifier)


        if doPart[1]:

            # splits the blob of pixels that are inbetween watershed regions to produce faces
            blobDict, superVoxelDict = self.splitBlobIntoFacesAndComputeSuperVoxelFeatures(prefix+'faces', prefix+'nonfaces', prefix+'inbetweenPoints', prefix+'MembraneLabelVolume', prefix+'Watershed')
        
            #self.onMakePointFeatureViewer(None)
            #self.onMakeFaceFeatureViewer(None)
        
        if doPart[2]:
            # read face classification data file
            # todo: filter blobDict so it only has faces with exactly two adjacencies - or use faces in the data tree that you have already filtered in this way
            faceDict = {}
            for key in blobDict:
                if len(key) == 2:
                    faceDict[key] = blobDict[key]
            # todo: remove the volumeDict and use the data tree instead
            self.classifyFaces(inputFileIdentifier, faceDict, self.getPersistentVolume_old(originalVolumeName), self.getPersistentVolume_old(volumeForWatershedName), superVoxelDict)

        logFinished("findAndClassifyFaces")        


    # todo: could make this global function rather than member function
    def classifyFaces(self, inputFileIdentifier, faceBlobDict, volume, probabilityVolume, superVoxelDict):

        #tree = orngTree.TreeLearner(storeNodeClassifier = 0, storeContingencies=0, storeDistributions=1, minExamples=5, ).instance()
        tree = orngTree.TreeLearner(storeNodeClassifier = 0, storeContingencies=0, storeDistributions=1, minExamples=150, ).instance()
        gini = orange.MeasureAttribute_gini()
        tree.split.discreteSplitConstructor.measure = tree.split.continuousSplitConstructor.measure = gini
        tree.maxDepth = 5
        tree.split = orngEnsemble.SplitConstructor_AttributeSubset(tree.split, 3)

        data = orange.ExampleTable("c:\\temp\\%s_faceClassificationTrainingData.tab" % inputFileIdentifier)
        #forest = orngEnsemble.RandomForestLearner(data, trees=50, name="forest", learner=tree)

        print "data.domain.attributes", data.domain.attributes, len(data.domain.attributes) 
        print "data.domain.variables", data.domain.variables, len(data.domain.variables)

        #forest = orngEnsemble.RandomForestLearner(data, trees=50, name="forest")
        forest = orngEnsemble.RandomForestLearner(data, trees=300, name="forest")
        
        print "Possible classes:", data.domain.classVar.values

        #print probabilities
        if False:
            for i in range(len(data)):
                p = forest(data[i], orange.GetProbabilities)
                print "%d: %5.10f (originally %s)" % (i+1, p[1], data[i].getclass())

        
        for key in faceBlobDict:
            
            faceBlob = faceBlobDict[key]
            
            #dictionary = getFeaturesAt(self.getCurrentVolume(), self.mainDoc.volumeDict, (x,y,z))
            #dictionary = getFaceFeatures('training', faceBlob, volume, superVoxelDict, self.mainDoc.volumeDict)
            dictionary = getFaceFeatures('test', faceBlob, volume, probabilityVolume, superVoxelDict, self)
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
            
            faceBlob.setColor([200 - (p[1] * 200), p[1] * 200, 0]) 
            faceBlob.setProbability(p[1])


    def writeFaceClassificationTrainingData(self, identifier, filename, superVoxelDict, facesNodeName, originalVolumeName, probabilityVolumeName, membraneLabelVolumeName, salientLabelValue):

        file = open(filename, "w")
        
        sh = self.getPersistentVolume_old(originalVolumeName).shape

        volume = numpy.zeros(sh)
        #selected x, y, and z
        
        dummyDictionary = makeFaceFeaturesDictionary()
        featureList = []
        for item in dummyDictionary.items():
            key = item[0]
            featureList.append(key)
        
        writeOrangeNativeDataFormatHeader(file, featureList)
        
        facesNode = getNode(self.getBlobsNode(), (facesNodeName,))
        for faceNode in facesNode.children:
            faceBlob = faceNode.object
            d = getFaceFeatures(identifier, faceBlob, self.getPersistentVolume_old(originalVolumeName), self.getPersistentVolume_old(probabilityVolumeName), superVoxelDict, self)
            
            # assume it is a salient face if average value is greater than a certain number
            averageValue = calculateAverageValue(faceBlob, self.getPersistentVolume_old(membraneLabelVolumeName))
            self.writeExample(file, d, faceBlobSalientBasedOnAverageValue(averageValue, salientLabelValue))
            #print "faceBlobSalientBasedOnAverageValue(averageValue)"
            #print faceBlobSalientBasedOnAverageValue(averageValue)
        
        file.close()



    #def onReadClassificationFile(self, event):
#    def old_onClassifyVoxelsOfCurrentImage(self, event):
#        self.onCalculateDerivatives(None)
#
#        tree = orngTree.TreeLearner(storeNodeClassifier = 0, storeContingencies=0, storeDistributions=1, minExamples=5000, ).instance()
#        gini = orange.MeasureAttribute_gini()
#        tree.split.discreteSplitConstructor.measure = tree.split.continuousSplitConstructor.measure = gini
#        tree.maxDepth = 5
#        tree.split = orngEnsemble.SplitConstructor_AttributeSubset(tree.split, 3)
#
#
#
#        #data = orange.ExampleTable("Copy of voting2.csv")
#        data = orange.ExampleTable("c:\\temp\\output.tab")
#        forest = orngEnsemble.RandomForestLearner(data, trees=50, name="forest", learner=tree)
#        
#        #tree = orngTree.TreeLearner(data, sameMajorityPruning=1, mForPruning=2)#, maxDepth=40)
#        
#        #tree = orngTree.TreeLearner(minExamples=2, mForPrunning=2, \
#        #                            sameMajorityPruning=True, name='tree')
#        
#       
#        print "Possible classes:", data.domain.classVar.values
#        #print "Probabilities for democrats:"
#        if True:
#            for i in range(len(data)):
#                p = forest(data[i], orange.GetProbabilities)
#                print "%d: %5.10f (originally %s)" % (i+1, p[1], data[i].getclass())
#
#        #orngTree.printTxt(tree)
#        
#       
#        
#        count = 0
#        v = zeros(self.getCurrentVolume().shape)
#        for x in range(borderWidthForFeatures, v.shape[0]-borderWidthForFeatures):
#            print x, "out of", v.shape[0]-borderWidthForFeatures-1
#            for y in range(borderWidthForFeatures,v.shape[1]-borderWidthForFeatures):
#                for z in range(borderWidthForFeatures,v.shape[2]-borderWidthForFeatures):
#                    
#                    
#                    #print(data[count])
#                    #p = forest(data[count], orange.GetProbabilities)
#                    
#                    dictionary = getPointFeaturesAt(self.getCurrentVolume(), self, (x,y,z))
#                    list = []
#                    for item in dictionary.items():
#                        value = item[1]
#                        list.append(value)
#                    list.append('False') # todo: what would happen if you used True here
#                    #p = forest(list, orange.GetProbabilities)
#                    example = orange.Example(data.domain, list)
#                    p = forest(example, orange.GetProbabilities)    
#                    
#                    #print (x,y,z)
#                    #print count
#                    #v[x,y,z] = numpy.log(p[1])
#                    v[x,y,z] = numpy.log(1 - p[1])
#                    count += 1
#                    #print p[1]
#        
#        self.addPersistentVolumeAndRefreshDataTree(v, 'probability')

    def onClassifyVoxelsOfImageStack(self, event):

        dialog = wx.DirDialog(self, "Choose Image Stack for Pixel Classification", os.getcwd(), style=wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            inputImageStackPath = dialog.GetPath()
        dialog.Destroy()

        wildcard = "(*.tab)|*.tab|All files (*.*)|*.*"
        dialog = wx.FileDialog(self, "Choose Examples File", os.getcwd(), style=wx.OPEN, wildcard=wildcard)
        if dialog.ShowModal() == wx.ID_OK:
            print dialog.GetPath()
            voxelExamplesFilename = dialog.GetPath()
        dialog.Destroy()


        self.classifyVoxels('intermediate2', 'voxelClassificationOnTestVolume', voxelExamplesFilename, inputImageStackPath)

#    def classifyVoxels(self,
#                       intermediateDataIdentifier,
#                       outputDataIdentifier,
#                       voxelExamplesFilename,
#                       inputImageStackPath):
#        
#        #identifier = 'test'
#
#        data = orange.ExampleTable(voxelExamplesFilename)
#        
#        minimumExamples = len(data) / 5
#        
#        inputVolume = loadImageStack(inputImageStackPath, None)
#        
#        self.calculateDerivatives(inputVolume, intermediateDataIdentifier)
#
#        tree = orngTree.TreeLearner(storeNodeClassifier = 0, storeContingencies=0, storeDistributions=1, minExamples=minimumExamples, ).instance()
#        gini = orange.MeasureAttribute_gini()
#        tree.split.discreteSplitConstructor.measure = tree.split.continuousSplitConstructor.measure = gini
#        tree.maxDepth = 5
#        tree.split = orngEnsemble.SplitConstructor_AttributeSubset(tree.split, 3)
#
#        forest = orngEnsemble.RandomForestLearner(data, trees=50, name="forest", learner=tree)
#        
#       
#        print "Possible classes:", data.domain.classVar.values
#        if False:
#            for i in range(len(data)):
#                p = forest(data[i], orange.GetProbabilities)
#                print "%d: %5.10f (originally %s)" % (i+1, p[1], data[i].getclass())
#
#        print "number of examples:", len(data)
#        print "minimumExamples:", minimumExamples
#        
#        count = 0
#
#        v = zeros(inputVolume.shape)
#        self.addPersistentVolumeAndRefreshDataTree(v, outputDataIdentifier + '_ProbabilityVolume')
#
#        logV = zeros(inputVolume.shape)
#        self.addPersistentVolumeAndRefreshDataTree(logV, outputDataIdentifier + '_LogProbabilityVolume')
#
#        for x in range(borderWidthForFeatures, v.shape[0]-borderWidthForFeatures):
#            print x, "out of", v.shape[0]-borderWidthForFeatures-1
#            for y in range(borderWidthForFeatures,v.shape[1]-borderWidthForFeatures):
#                for z in range(borderWidthForFeatures,v.shape[2]-borderWidthForFeatures):
#                    
#                    
#                    dictionary = getPointFeaturesAt(inputVolume, intermediateDataIdentifier, self, (x,y,z))
#                    list = []
#                    for item in dictionary.items():
#                        value = item[1]
#                        list.append(value)
#                    list.append('False') # todo: what would happen if you used True here
#                    example = orange.Example(data.domain, list)
#                    p = forest(example, orange.GetProbabilities)    
#                    
#                    v[x,y,z] = p[1]
#                    logV[x,y,z] = numpy.log(p[1])
#                    count += 1
        

    def classifyVoxels(self,
                       intermediateDataIdentifier,
                       outputDataIdentifier,
                       voxelExamplesFilename,
                       inputImageNodePath):
        
        #identifier = 'test'

        data = orange.ExampleTable(voxelExamplesFilename)
        
        minimumExamples = len(data) / 5
        
        inputVolume = self.getPersistentObject(inputImageNodePath)
        
        self.calculateDerivatives(inputVolume, intermediateDataIdentifier)

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
        
       
        print "Possible classes:", data.domain.classVar.values
        if False:
            for i in range(len(data)):
                p = forest(data[i], orange.GetProbabilities)
                print "%d: %5.10f (originally %s)" % (i+1, p[1], data[i].getclass())

        print "number of examples:", len(data)
        print "minimumExamples:", minimumExamples
        
        count = 0

        v = zeros(inputVolume.shape)
        logV = zeros(inputVolume.shape)
        #self.addPersistentVolumeAndRefreshDataTree(v,
        #                                outputDataIdentifier + '_ProbabilityVolume')

        for x in range(borderWidthForFeatures, v.shape[0]-borderWidthForFeatures):
            print x, "out of", v.shape[0]-borderWidthForFeatures-1
            for y in range(borderWidthForFeatures,v.shape[1]-borderWidthForFeatures):
                for z in range(borderWidthForFeatures,v.shape[2]-borderWidthForFeatures):
                    
                    
                    dictionary = getPointFeaturesAt(inputVolume,
                                        intermediateDataIdentifier, self, (x,y,z))
                    list = []
                    for item in dictionary.items():
                        value = item[1]
                        list.append(value)
                    list.append('False') # todo: what would happen if you used True here
                    example = orange.Example(data.domain, list)
                    p = forest(example, orange.GetProbabilities)    
                    
                    v[x,y,z] = p[1]
                    logV[x,y,z] = numpy.log(p[1])
                    count += 1

        self.addPersistentVolumeAndRefreshDataTree(v, outputDataIdentifier)

        self.addPersistentVolumeAndRefreshDataTree(logV,
                                        outputDataIdentifier + '_LogProbabilityVolume')


    def classifyVoxelsNN(self,
                         intermediateDataIdentifier,
                         outputDataIdentifier,
                         voxelExamplesFilename,
                         inputImageNodePath):

        inputVolume = self.getPersistentObject(inputImageNodePath)
        
        network = NeuralNetwork(inputVolume)
        #network.input = inputVolume
        network.update()

        #v = zeros(inputVolume.shape)


        self.addPersistentVolumeAndRefreshDataTree(network.getOutput(),
                                                   outputDataIdentifier)


    def setPointFeatureSliders(self, location):
        # todo: rename self.viewerRootNode to self.pointFeatureViewerRootNode
        viewerNode = self.viewerRootNode
        loc = numpy.int_(location)
        dictionary = getPointFeaturesAt(self.getCurrentVolume(), self, loc)
        self.setFeatureSliders(viewerNode, dictionary)
        
    def setBlobFeatureSliders(self, blob):
    #def setBlobFeatureSliders(self, location):
        #print ""
        #loc = numpy.int_(location)
        #dictionary = getFeaturesAt(self.getCurrentVolume(), self.mainDoc.volumeDict, loc)
        #(getNode(self.viewerRootNode, (key,))).set(value)
        #self.setFeatureSliders_(viewerNode, dictionary)
        viewerNode = self.blobFeatureViewerRootNode
        dictionary = getFaceFeatures(blob, self.mainDoc.volumeDict['Original'], self.superVoxelDict)
        self.setFeatureSliders(viewerNode, dictionary)


    # todo: function is not written yet
    def calculateDistributionFeatures(faceBlob, volume):
        print ""
        
        

    def setFeatureSliders(self, viewerNode, dictionary):
        #loc = numpy.int_(location)
        #dictionary = getFeaturesAt(self.getCurrentVolume(), self.mainDoc.volumeDict, loc)
        #if dictionary != None:
        for item in dictionary.items():
            key = item[0]
            value = item[1]
            #'featuresAtPoint',key
            
            if value < self.getSliderMin(viewerNode, (key,)):
                self.setSliderMin(viewerNode, (key,), value)

            if value > self.getSliderMax(viewerNode, (key,)):
                self.setSliderMax(viewerNode, (key,), value)
                            
            #(getNode(self.viewerRootNode, (key,))).set(value)
            #(getNode(self.settingsTree, ('featuresAtPoint',key))).set(value)
            #viewerNode.set(value)
            (getNode(viewerNode, (key,))).set(value)


    def printBlobNameAtMouseLocation(self, event):
        # display information about the blob at this point
        if (getNode(self.settingsTree, ('particleMotionTool','drawBlobs'))).get():
            loadedVolumeLocation = self.screenXYToLoadedVolumeXYZ((event.X, event.Y))
            #blob = self.mainDoc.blobDict['InbetweenPoints']
            #blob = getNode(self.getBlobsNode(), ('InbetweenPoints',)).object
            #print "value %s" % str(at(self.getCurrentVolume(), loadedVolumeLocation))
            
            watershedLabel = at(self.mainDoc.volumeDict['Watershed1'], loadedVolumeLocation)
            print "watershed label %s" % str(watershedLabel)

            print "size %d" % self.superVoxelDict[watershedLabel].size()

            facesNode = getNode(self.getBlobsNode(), ('faces',))
            for childNode in facesNode.children:
                blob = childNode.object
                for labeledPoint in blob.points():
                    if (loadedVolumeLocation.round() == labeledPoint.loc).all():
                        #if len(labeledPoint.adjacentNonzeroValueSet) > 0:
                        #    print labeledPoint.adjacentNonzeroValueSet
                        #    #listBox = getNode(self.settingsTree, ('particleMotionTool','blobList')).guiComponent
                        #    
                        #    # sets the current blob to the one that was clicked
                        #    #listBox.SetStringSelection(str(frozenset(labeledPoint.adjacentNonzeroValueSet)))
                        #    #self.setBlobFeatureSliders(blob)
                        #    
                        #    #facesDict = getNode(self.getBlobsNode(), ('faces',)).children
                        #    
                        #    
                        #    self.setBlobFeatureSliders(self.getCurrentBlob())
                        treeControl = getNode(self.settingsTree, ('particleMotionTool','dataTree')).guiComponent
                        itemId = childNode.guiComponent
                        treeControl.SelectItem(itemId)
                        self.setBlobFeatureSliders(blob)




class FaceBlob(Blob):
    def __init__(self):
        Blob.__init__(self)
        self.adjacentSuperVoxelIDs = None
        #self.averageValueFromTrainingLabelVolume = None


        


#class ExtendedTreeCtrl(wx.TreeCtrl):
#    getItemIdWithData(data):
#        root = self.GetRootItem()
        
    

# todo: rename to getPointFeaturesAt
# todo: gui parameter should just be the node that has the volumes you need as its children
def getPointFeaturesAt(volume, derivativeVolumesIdentifier, gui, point):
    # f is dictionary of features
    

    if not(isInsideVolumeWithBorder(volume, point, borderWidthForFeatures)):
        raise Exception, 'The point %s is not inside the volume enough. In needs to be away from the border by %d pixels.' % (point, borderWidthForFeatures)
    
    f = odict()



    
    #sizeIdentifiers = ('3x3x3', '5x5x5', '7x7x7')
    sizeIdentifiers = ('(3)', '(5)', '(7)')
    v = [None, None, None] 
    
    #for i in range(3):
    for i in range(1):
        size = i+1
        v = volume[point[0]-size:point[0]+size,point[1]-size:point[1]+size,point[2]-size:point[2]+size]
    
    
        #if isInsideVolumeWithBorder(volume, point, border):
        #    # 3 by 3 by 3 chunk of volume
        #    v3 = volume[point[0]-1:point[0]+1,point[1]-1:point[1]+1,point[2]-1:point[2]+1]
        #else:
        #    v3 = zeros([3,3,3])
        
        #(CUBE_3X3, CUBE_5X5, CUBE_7X7) = (0, 1, 2)     
        
        #i = 0
        #todo: note that getVolume may be a slow operation
        xG = at(gui.getVolume('%s_0Gradient_blur%d' % (derivativeVolumesIdentifier, i)), point)
        yG = at(gui.getVolume('%s_1Gradient_blur%d' % (derivativeVolumesIdentifier, i)), point)
        zG = at(gui.getVolume('%s_2Gradient_blur%d' % (derivativeVolumesIdentifier, i)), point)

        if i == 0:
            f['grayValue'] = at(volume, point)
            #'differenceOfGaussian'
            f['gradientMagnitude'] = sqrt(pow(xG,2) + pow(yG,2) + pow(zG,2))
            
            
        stAtSelectedPoint = structureTensor(xG,yG,zG)
        
        sortedEigAtSelectedPoint = numpy.linalg.eigvals(stAtSelectedPoint)
        sortedEigAtSelectedPoint.sort()

        prefix = sizeIdentifiers[i] + '_'
        
        f[prefix + 'eig0'] = sortedEigAtSelectedPoint[0]
        f[prefix + 'eig1'] = sortedEigAtSelectedPoint[1]
        f[prefix + 'eig2'] = sortedEigAtSelectedPoint[2]
    
        values = v.flatten(1)
        #print "i", i, "values", values
    
        moments = statistics.moments(values)
        f[prefix + 'mean'] = moments[0]
        f[prefix + 'standardDeviation'] = moments[1]
        f[prefix + 'thirdMoment'] = moments[2]
        f[prefix + 'fourthMoment'] = moments[3]
        
        quantiles = statistics.sortAndReturnQuantiles(values)
        f[prefix + 'minimum'] = quantiles[0]
        f[prefix + '0.25-quantile'] = quantiles[1]
        f[prefix + 'median'] = quantiles[2]
        f[prefix + '0.75-quantile'] = quantiles[3]
        f[prefix + 'maximum'] = quantiles[4]
    
    
    
    
    
        
        # Distribution of the gradient magnitude
        #'gmStandardDeviation'
        #'gmThirdMoment'
        #'gmFourthMoment'
        #'gmMinimum'
        #'gm0.25-quantile'
        #'gmMedian'
        #'gm0.75-quantile'
        #'gmtMaximum'
    
    return f


    
#def makeFaceFeaturesDictionary():
#    return OrderedDictionaryFixedKeyList({'logNumberOfVoxels':None,
#                                          'logDifference':None,
#
#                                          'grayValue_mean':None,
#                                          'grayValue_standardDeviation':None,
#                                          'grayValue_thirdMoment':None,
#                                          'grayValue_fourthMoment':None,
#                                          'grayValue_minimum':None,
#                                          'grayValue_0.25-quantile':None,
#                                          'grayValue_median':None,
#                                          'grayValue_0.75-quantile':None,
#                                          'grayValue_maximum':None,
#
#                                          'gradientMagnitude_mean':None,
#                                          'gradientMagnitude_standardDeviation':None,
#                                          'gradientMagnitude_thirdMoment':None,
#                                          'gradientMagnitude_fourthMoment':None,
#                                          'gradientMagnitude_minimum':None,
#                                          'gradientMagnitude_0.25-quantile':None,
#                                          'gradientMagnitude_median':None,
#                                          'gradientMagnitude_0.75-quantile':None,
#                                          'gradientMagnitude_maximum':None,
#
#                                          'voxelProbability_mean':None,
#                                          'voxelProbability_standardDeviation':None,
#                                          'voxelProbability_thirdMoment':None,
#                                          'voxelProbability_fourthMoment':None,
#                                          'voxelProbability_minimum':None,
#                                          'voxelProbability_0.25-quantile':None,
#                                          'voxelProbability_median':None,
#                                          'voxelProbability_0.75-quantile':None,
#                                          'voxelProbability_maximum':None})

def makeFaceFeaturesDictionary():
    list = ['logNumberOfVoxels',
                                          'logDifference',

#                                          'grayValue_mean',
#                                          'grayValue_standardDeviation',
#                                          'grayValue_thirdMoment',
#                                          'grayValue_fourthMoment',
#                                          'grayValue_minimum',
#                                          'grayValue_0.25-quantile',
#                                          'grayValue_median',
#                                          'grayValue_0.75-quantile',
#                                          'grayValue_maximum',
#
#                                          'gradientMagnitude_mean',
#                                          'gradientMagnitude_standardDeviation',
#                                          'gradientMagnitude_thirdMoment',
#                                          'gradientMagnitude_fourthMoment',
#                                          'gradientMagnitude_minimum',
#                                          'gradientMagnitude_0.25-quantile',
#                                          'gradientMagnitude_median',
#                                          'gradientMagnitude_0.75-quantile',
#                                          'gradientMagnitude_maximum',

                                          'voxelProbability_mean',
                                          'voxelProbability_standardDeviation',
                                          'voxelProbability_thirdMoment',
                                          'voxelProbability_fourthMoment',
                                          'voxelProbability_minimum',
                                          'voxelProbability_0.25-quantile',
                                          'voxelProbability_median',
                                          'voxelProbability_0.75-quantile',
                                          'voxelProbability_maximum']
    return OrderedDictionaryFixedKeyList(list)

                                           
                                           
#//////////////////////////////////////////////////////////////////
# todo: use the data tree as parameter rather than whole gui
def getFaceFeatures(gradientIdentifier, faceBlob, originalVolume, probabilityVolume, superVoxelDict, gui):
    # f is dictionary of features
    
    f = makeFaceFeaturesDictionary()
    
    #self.mainDoc.blobDict['inbetweenPoints'][faceIdentifier]
    
    f['logNumberOfVoxels'] = log(faceBlob.numPoints())
    #f['grayValue'] = at(volume, point)
    
    if len(faceBlob.adjacentSuperVoxelIDs) != 2:
        raise Exception, "The face blob with id %s does not have exactly two adjacent super voxels." % faceBlob.adjacentSuperVoxelIDs
    
    
    sv = [None, None]
    i = 0
    for superVoxelID in faceBlob.adjacentSuperVoxelIDs:
        sv[i] = superVoxelDict[superVoxelID]
        i += 1
    
    f['logDifference'] = log(1 + abs(sv[0].size() - sv[1].size()))

    xGradientVolume = gui.getPersistentVolume_old(gradientIdentifier + "_" + '0Gradient_blur%d' % 1)
    yGradientVolume = gui.getPersistentVolume_old(gradientIdentifier + "_" + '1Gradient_blur%d' % 1)
    zGradientVolume = gui.getPersistentVolume_old(gradientIdentifier + "_" + '2Gradient_blur%d' % 1)

    grayValues = []
    gradientMagnitudes = []
    voxelProbabilities = []
    for point in faceBlob.points():

        grayValues.append(at(originalVolume, point.loc))

        xG = at(xGradientVolume, point.loc)
        yG = at(yGradientVolume, point.loc)
        zG = at(zGradientVolume, point.loc)
        gradientMagnitudes.append(sqrt(pow(xG,2) + pow(yG,2) + pow(zG,2)))

        voxelProbabilities.append(at(probabilityVolume, point.loc))

    valueTypeDict = {}
    #valueTypeDict['grayValue'] = grayValues
    #valueTypeDict['gradientMagnitude'] = gradientMagnitudes 
    valueTypeDict['voxelProbability'] = voxelProbabilities

    for key in valueTypeDict:
        
        prefix = key + "_"
        
        values = valueTypeDict[key]

        moments = statistics.moments(values)
        f[prefix + 'mean'] = moments[0]
        f[prefix + 'standardDeviation'] = moments[1]
        f[prefix + 'thirdMoment'] = moments[2]
        f[prefix + 'fourthMoment'] = moments[3]
    
        quantiles = statistics.sortAndReturnQuantiles(values)
        f[prefix + 'minimum'] = quantiles[0]
        f[prefix + '0.25-quantile'] = quantiles[1]
        f[prefix + 'median'] = quantiles[2]
        f[prefix + '0.75-quantile'] = quantiles[3]
        f[prefix + 'maximum'] = quantiles[4]

   
    return f


def makeBlobFromVoxelsLabeledZero(volume, widthOfBorderToIgnore):
    w = widthOfBorderToIgnore
    blob = Blob()
    for x in range(w, volume.shape[0]-w):
        for y in range(w, volume.shape[1]-w):
            for z in range(w, volume.shape[2]-w):
                if volume[x,y,z] == 0:
                    blob.points().append(LabeledPoint((x,y,z)))
    return blob

def computeSuperVoxelFeatures(watershedVolume):
    print "computing super voxel features"
    superVoxelDict = {}
    for x in range(watershedVolume.shape[0]):
        for y in range(watershedVolume.shape[1]):
            for z in range(watershedVolume.shape[2]):
                superVoxelIndex = watershedVolume[x,y,z]
                if superVoxelIndex in superVoxelDict:
                    superVoxelDict[superVoxelIndex].addToSize(1)
                else:
                    superVoxelDict[superVoxelIndex] = Blob()
                    superVoxelDict[superVoxelIndex].setSize(0)
                    
    return superVoxelDict




# todo: move this to cytoseg_classify.py    
# return a dictionary of blobs, each has an index that is based on the set of adjacent regions (if the point is adjacent to region 2 and 3 for example, it's dictionary entry key will be a set with elements 2 and 3)
def splitBlobBasedOnAdjacentValueSet(blob):
    dictionary = {}
    
    for labeledPoint in blob.points():
        
        # valueSet is used as a key
        
        valueSet = frozenset(labeledPoint.adjacentNonzeroValueSet)
        
        # create new face if needed
        if not(valueSet in dictionary):
            faceBlob = FaceBlob()
            faceBlob.adjacentSuperVoxelIDs = valueSet
            dictionary[valueSet] = faceBlob #[] #Blob()
        
        
        # todo: it's sort of redundant to stor the set specifying adjacencies in every labeled point considering all of them (in the blob) have the same adjacent blobs 
        dictionary[valueSet].points().append(labeledPoint)
        
        #dictionary[valueSet].append(labeledPoint)

        #print '----------------------------------'
        #print dictionary[valueSet].points()[0:10]
        #print valueSet
        
        #items = dictionary.items()
        #for item in items:
        #    print item
            #print item[0]
            #print item[1][0:10]
            #print len(item[1])
        #    print dictionary[item[0]].points()[0:10]
    
    return dictionary


   
# computes the adjacent values that are not zero, for each point in the blob.
# stores the result in the labeled points of the blob
def computeAdjacentValueSets(volume, blob):
    for labeledPoint in blob.points():
        computeAdjacentValueSet(volume, labeledPoint)

def computeAdjacentValueSet(volume, labeledPoint):
    for offset in adjacentOffsets:
        p = labeledPoint.loc + offset
        #labeledPoint.adjacentNonZeroPoints = []
        #print p

        if at(volume, p) != 0:
            #print '--------------------'
            #print p
            #labeledPoint.adjacentNonzeroPoints.append(p)
            #labeledPoint.adjacentNonzeroValues.append(at(volume,p))
            labeledPoint.adjacentNonzeroValueSet.add(at(volume,p))

def calculateAverageValue(faceBlob, binaryLabelVolume):
    total = 0.0
    
    for labeledPoint in faceBlob.points():
        total += float(at(binaryLabelVolume, labeledPoint.loc))
        
    return float(total) / float(len(faceBlob.points()))


def faceBlobColorBasedOnAverageValue(value, salientLabelValue):

    if faceBlobSalientBasedOnAverageValue(value, salientLabelValue):
        return [0, 200, 0] # bright green
    else:
        return [100, 0, 100] # dark purple 


def faceBlobSalientBasedOnAverageValue(value, salientLabelValue):

    # the face is considered salient if 50% of pixels or more are marked salient
    if value > (0.5 * salientLabelValue):
        return True # bright green
    
    # if the face is not salient:
    else:
        return False # dark purple 
        

def writeOrangeNativeDataFormatHeader(file, featureList):
    
        for featureName in featureList:
            file.write("%s\t" % featureName)
        file.write("is_membrane\n")

        for featureName in featureList:
            file.write("c\t")
        file.write("discrete\n")

        for featureName in featureList:
            file.write("\t")
        file.write("class\n")


def startClassificationControlsFrame():
    
    app = wx.PySimpleApp()
    #frm = ClassificationControlsFrame(makeDefaultGUITree())
    frm = ClassificationControlsFrame(makeClassifyGUITree())
    frm.Show()
    
    
    
    #print 'settings test'
    #print settings
    #count = 0
    #old_gui = old_GUI(settingsTree)
    
    
        
    #root.update() # fix geometry
    
    ##try:
    ##while 0:
    
    
            
    ##except TclError:
    ##    #print 'test output'
    ##    
     ##   settings['defaultPath'] = old_gui.imageStackPathText.get()
    ##    settings['temporaryFolder'] = old_gui.saveImageStackPathText.get() 
    ##        
    ##    writeSettings();
    ##    pass # to avoid errors when the window is closed
    
    
    
    app.MainLoop()
   


#---------------------------------------------------------------

#count = 0


