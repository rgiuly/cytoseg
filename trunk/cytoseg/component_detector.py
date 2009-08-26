#Copyright (c) 2008 by individual cytoseg contributors
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.


import numpy
from cytoseg_classify import *
#from mitochondria import *
from fill import *
#import sys
from enthought.mayavi.scripts import mayavi2
from default_path import *
from contour_processing import *
from xml.dom.minidom import Document
#from pygraph import *
from graph import *
import os
import colorsys



def mitochondriaProbability_old(features):

    amplitude = 1
    overlapValue = gaussian(1.0 - features['ellipseOverlap'], amplitude, 0.2)
    perimeterValue = gaussian(abs(250.0 - features['perimeter']), amplitude, 150)
    grayValueMatch = gaussian(abs(1 - features['averageGrayValue']), amplitude, 0.25)
    areaMatch = gaussian(abs(700 - math.sqrt(features['contourArea'])), amplitude, 500)
    return overlapValue * perimeterValue * grayValueMatch * areaMatch


def mitochondriaProbability(features):

    amplitude = 1
    overlapValue = gaussian(1.0 - features['ellipseOverlap'], amplitude, 0.2)
    perimeterValue = gaussian(abs(81.0 - features['perimeter']), amplitude, 75)
    grayValueMatch = gaussian(abs(1 - features['averageGrayValue']), amplitude, 0.25)
    areaMatch = gaussian(abs(435 - math.sqrt(features['contourArea'])), amplitude, 300)
    return overlapValue * perimeterValue * grayValueMatch * areaMatch


def blankInnerCellProbability(features):

    amplitude = 1
    overlapValue = gaussian(1.0 - features['ellipseOverlap'], amplitude, 0.2)
    perimeterValue = gaussian(abs(250.0 - features['perimeter']), amplitude, 150)
    grayValueMatch = gaussian(features['averageGrayValue'], amplitude, 0.25)
    areaMatch = gaussian(abs(700 - math.sqrt(features['contourArea'])), amplitude, 500)
    return overlapValue * perimeterValue * grayValueMatch * areaMatch


def vesicleProbability(features):

    amplitude = 1
    overlapValue = gaussian(1.0 - features['ellipseOverlap'], amplitude, 0.2)
    perimeterValue = gaussian(abs(15 - features['perimeter']), amplitude, 5)
    grayValueMatch = gaussian(abs(0.5 - features['averageGrayValue']), amplitude, 0.5)
    areaMatch = gaussian(abs(70 - math.sqrt(features['contourArea'])), amplitude, 20)
    grayValueAtContourPointsMatch = gaussian(abs(160 - features['averageOriginalVolumeValueAtContourPoints']), amplitude, 160)
    return overlapValue * perimeterValue * grayValueMatch * areaMatch * grayValueAtContourPointsMatch


def updateContourProbabilities(contoursGroupedByImage, probabilityFunction):

    contourList = nonnullObjects(contoursGroupedByImage)
    print "updateContourProbabilities"

    for contour in contourList:

        p = probabilityFunction(contour.features)
        contour.setProbability(p)
        print p
        color = 255.0 * array((1.0 - (p * 10.0), (p * 10.0), 0))
        contour.setColor(color)


#def findContoursInVolume(gui, contourProbabilityFunction, originalVolumeName, filteredVolumeName, highProbabilityContoursNodeName):
#    """
#    originalVolumeName: input
#    filteredVolumeName: input
#    highProbabilityContoursNodeName: output
#    """
#    
#    originalVolume = gui.getPersistentVolume_old(originalVolumeName)
#    filteredVolume = gui.getPersistentVolume_old(filteredVolumeName)
#    
#    #lastZ = 5
#    lastZ = originalVolume.shape[2]
#    #contours = findMitochondria(originalVolume[:,:,0:lastZ], filteredVolume[:,:,0:lastZ])
#    contours = findContours(originalVolume[:,:,0:lastZ], contourProbabilityFunction, filteredVolume[:,:,0:lastZ])
#
#    contoursNode = DataNode(highProbabilityContoursNodeName, 'contours node type', {}, None)
#    contoursNode.addObjectList(contours)
#    
#    gui.addPersistentSubtreeAndRefreshDataTree((), contoursNode)



#def display3DContours():
#
#    view_numpy()


    
    #view_numpy()

    #enthought_mlab.plot3d(*zip(contour.points))
#    for point in contour.points:
#        #print point
#        #print point[0]
#        #print point[1]
#        #print point[2]
#        ball = enthought_mlab.points3d([point[0]], [point[1]], [point[2]], scale_factor=16, scale_mode='none', resolution=20, color=(1,0,0), name='ball')
    

#    source = ArraySource(transpose_input_array=False)
#    source.scalar_data = originalVolume
#    enthought.mayavi.add_source(source)
#    ipw = ImagePlaneWidget()
#    enthought.mayavi.add_module(ipw)
#    ipw.module_manager.scalar_lut_manager.show_scalar_bar = True
#
#    ipw_y = ImagePlaneWidget()
#    enthought.mayavi.add_module(ipw_y)
#    ipw_y.ipw.plane_orientation = 'y_axes'


#@mayavi2.standalone
def display3DContours(dataViewer, inputVolumeName, highProbabilityContoursNodeName, displayParameters):
    """Example showing how to view a 3D numpy array in mayavi2.
    """
    
    numberOfContoursToDisplay = displayParameters.numberOfContoursToDisplay

    from enthought.mayavi.sources.array_source import ArraySource
    from enthought.mayavi.modules.outline import Outline
    from enthought.mayavi.modules.image_plane_widget import ImagePlaneWidget
    from enthought.mayavi.modules.iso_surface import IsoSurface
    
    # 'mayavi' is always defined on the interpreter.
    #mayavi.new_scene()
    from enthought.mayavi.api import Engine
    e = Engine()
    e.start()
    s = e.new_scene()

    # Make the data and add it to the pipeline.
    # todo: load this from the data tree of cytoseg
    #originalVolume = loadImageStack(driveName + "/images/HPFcere_vol/HPF_rotated_tif/median_then_gaussian_8bit", None)
    originalVolume = dataViewer.getPersistentVolume_old(inputVolumeName)
    #originalVolume = loadImageStack("O:/images/3D-blob-data/small_crop", None)
    #originalVolume = originalVolume[:,:,3:]

    data1 = array(originalVolume, dtype=float)
    data = numpy.transpose(data1).copy()
    data.shape = data.shape[::-1]

    src = ArraySource(transpose_input_array=False)
    src.scalar_data = data
    e.add_source(src)
    # Visualize the data.
    #o = Outline()
    #mayavi.add_module(o)
    ipw = ImagePlaneWidget()
    e.add_module(ipw)
    ipw.module_manager.scalar_lut_manager.show_scalar_bar = True

    ipw_y = ImagePlaneWidget()
    e.add_module(ipw_y)
    ipw_y.ipw.plane_orientation = 'y_axes'

    ipw_z = ImagePlaneWidget()
    e.add_module(ipw_z)
    ipw_z.ipw.plane_orientation = 'z_axes'

#    if 1:
        
    # Enthought library imports
    
    #import enthought
    from enthought.mayavi import mlab as enthought_mlab
    
    
    
    
    
    
    
    from enthought.mayavi.scripts import mayavi2
    
    from enthought.mayavi import mlab as enthought_mlab

    import enthought.mayavi
    
    #mayavi.new_scene()
    #ball = enthought_mlab.points3d(1, 1, 1, scale_factor=16, scale_mode='none', resolution=20, color=(1,0,0), name='ball')

    
    node = dataViewer.mainDoc.dataTree.getSubtree((highProbabilityContoursNodeName,))
    #frm.refreshTreeControls()
    #contours = node.makeChildrenObjectList()

    #highProbabilityContourList = highProbabilityContours(contours)
    contourList = node.makeChildrenObjectList()
    #for contour in contours[0:2000:10]:

    #if numberOfContoursToDisplay != None:
    #    highProbabilityContourList = highProbabilityContourList[0:numberOfContoursToDisplay]

    for contour in contourList[:numberOfContoursToDisplay]:
        print "process contour"
        x = []
        y = []
        z = []
        for point in contour.points():
            x.append(point.loc[0])
            y.append(point.loc[1])
            z.append(point.loc[2])

        mitochondriaLikeness = contour.probability()
        #enthought_mlab.plot3d(x, y, z, tube_radius=1, color=(.1, mitochondriaLikeness*2.0, 0))
        enthought_mlab.plot3d(x, y, z, tube_radius=displayParameters.contourSegmentTubeRadius, color=(.1, mitochondriaLikeness, 0))
        #draw a sphere at contour.bestFitEllipse.center
        center = contour.bestFitEllipse.center
        # points3d requires lists of length 2 or more with distinct numbers in them for the first 4 arguments, that's why zeros are used, this may be a bug in the points3d function that i'm working around with the zeros
        enthought_mlab.points3d((0, center[0]), (0, center[1]), (0, center[2]), (0, 1), colormap="copper", scale_factor=displayParameters.contourCenterMarkerSize)
        
    print "finished sending contours to mayavi"

    #enthought_mlab.contour3d(data, contours=3)
    #enthought_mlab.contour3d(originalVolume, contours=3)


class ContourAndBlobDisplayParameters:

    def __init__(self):
        self.numberOfContoursToDisplay = None
        self.contourSegmentTubeRadius = 1
        self.contourCenterMarkerSize = 5
        self.enable3DPlot = True
        self.contourProbabilityThreshold = 0


def saveBlobsToJinxFile(node):

        doc = Document()
        #blobsNode = gui.mainDoc.dataTree.getSubtree(('Blobs',))
        main = doc.createElement("main")
        doc.appendChild(main)

        #for childNode in node.children:
        #    #print childNode.valueToSave.getXMLVoxelList(doc)
        #    #getXMLPointList should allow floating points values
        #    main.appendChild(childNode.valueToSave.getXMLObject(doc, childNode.name))
        #print doc.toprettyxml(indent="  ")

        saveBlobsToJinxFileRecursiveHelper(node, doc, main)

        file = open(os.path.join(defaultOutputPath, "blobs.xml"), "w")
        file.write(doc.toprettyxml(indent="   "))


def saveBlobsToJinxFileRecursiveHelper(node, document, documentElement):

        if node.isGroupNode:
            for childNode in node.children:
                saveBlobsToJinxFileRecursiveHelper(childNode, document, documentElement)
        else:
            documentElement.appendChild(
                node.valueToSave.getXMLObject(document, node.name))



class CellComponentDetector:


    def __init__(self,
                 originalImageFilePath,
                 voxelTrainingImageFilePath,
                 voxelTrainingLabelFilePath):
        #self.originalImageFilePath =\
        #    "O:/images/HPFcere_vol/HPF_rotated_tif/padding_removed/8bit"
        #self.originalImageFilePath =\
        #    "O:/images/Eric_07-10-09/normalized_tiff_files/cropped_stack/8bit"
        self.originalImageFilePath = originalImageFilePath

        #self.voxelTrainingImageFilePath =\
        #    "O:\\images\\HPFcere_vol\\HPF_rotated_tif\\three_compartment\\"
        #self.voxelTrainingLabelFilePath =\
        #    "O:\\images\\HPFcere_vol\\HPF_rotated_tif\\three_compartment\\membrane_label_for_three_compartments\\"
        #self.voxelTrainingImageFilePath =\
        #    "O:/images/Eric_07-10-09/normalized_tiff_files/training/images"
        #self.voxelTrainingLabelFilePath =\
        #    "O:/images/Eric_07-10-09/normalized_tiff_files/training/label"
        self.voxelTrainingImageFilePath = voxelTrainingImageFilePath
        self.voxelTrainingLabelFilePath = voxelTrainingLabelFilePath

        self.contoursNodeName = 'Contours'
        self.contoursNodePath = (self.contoursNodeName,)


    def writeContoursToImageStack(self, pathToContoursNode):

        #contoursNode = frm.mainDoc.dataTree.getSubtree((highProbabilityContoursNodeName,))
        #contoursNode = frm.mainDoc.dataTree.getSubtree((contoursNodeName,))
        contoursNode = self.dataViewer.mainDoc.dataTree.getSubtree(pathToContoursNode)
        originalVolume = self.dataViewer.getPersistentVolume_old(self.originalVolumeName)
        contourRenderingVolume = zeros(originalVolume.shape)
        contourProbabilityVolume = zeros(originalVolume.shape)
        tempVolume = array(originalVolume)
        self.dataViewer.renderPointSetsInVolumeRecursive(contourRenderingVolume, contoursNode)
        self.dataViewer.renderPointSetsInVolumeRecursive(contourProbabilityVolume, contoursNode,
                                                  valueMode='probability')
        self.dataViewer.renderPointSetsInVolumeRecursive(tempVolume, contoursNode)
        self.dataViewer.addVolume(contourRenderingVolume, 'ContourVolume')
        self.dataViewer.refreshTreeControls()
        writeTiffStackRGB(defaultOutputPath,
                          redVolume=contourRenderingVolume,
                          greenVolume=contourProbabilityVolume*6.0,
                          blueVolume=tempVolume)


    def preclassificationFilter(self, dataViewer, numberOfLayersToProcess=None):

        originalImageNodePath = ('Volumes', 'originalImage')

        originalImage = loadImageStack(self.originalImageFilePath, None)

        dataViewer.addVolumeAndRefreshDataTree(originalImage, originalImageNodePath[1])

        medianFilteredImage = itkFilter(originalImage, 'Median', radius=1)
        blurredImage = itkFilter(medianFilteredImage, 'SmoothingRecursiveGaussian', sigma=1)

        dataViewer.addPersistentVolumeAndRefreshDataTree(originalImage,
                                                         self.originalVolumeName)

        dataViewer.addPersistentVolumeAndRefreshDataTree(blurredImage,
                                                         self.blurredVolumeName)


    def classifyVoxels(self, dataViewer, numberOfLayersToProcess=None):
        
        #inputImageFilePath =\
        #    driveName + "/images/HPFcere_vol/HPF_rotated_tif/median_then_gaussian_8bit"
        exampleListFileName = os.path.join(cytosegDataFolder, "exampleList.tab")
        
        inputImage = self.dataViewer.getPersistentVolume_old(self.blurredVolumeName)

        voxelTrainingImageNodePath = ('Volumes', 'voxelTrainingImage')
        voxelTrainingLabelNodePath = ('Volumes', 'voxelTrainingLabel')
        inputImageNodePath = ('Volumes', 'inputImage')
    
        dataViewer.addVolumeAndRefreshDataTree(loadImageStack(self.voxelTrainingImageFilePath, None),
                                        voxelTrainingImageNodePath[1])
    
        dataViewer.addVolumeAndRefreshDataTree(loadImageStack(self.voxelTrainingLabelFilePath, None),
                                        voxelTrainingLabelNodePath[1])
        
        #inputImage = loadImageStack(inputImageFilePath, None)
        
        if numberOfLayersToProcess != None:
            inputImage = inputImage[:, :, 0:numberOfLayersToProcess]

        dataViewer.addVolumeAndRefreshDataTree(inputImage, inputImageNodePath[1])
    
        # uses training data
        print "learning features of training data"
        dataViewer.learnFeaturesOfMembraneVoxels(voxelTrainingImageNodePath,
                                          voxelTrainingLabelNodePath,
                                          exampleListFileName)
        
        # uses test data, generates voxel probabilities
        print "classifying voxels"
        dataViewer.classifyVoxels('intermediateDataLabel1',
                           self.filteredVolumeName,
                           exampleListFileName,
                           inputImageNodePath)


    def findContours(self, groupNodeName, threshold, numberOfLayersToProcess):

            #originalVolume = loadImageStack(driveName + "/images/HPFcere_vol/HPF_rotated_tif/median_then_gaussian_8bit", None)
            #originalVolume = loadImageStack(driveName + "/images/HPFcere_vol/HPF_rotated_tif/8bit", None)
            #originalVolume = loadImageStack(driveName + "/images/HPFcere_vol/HPF_rotated_tif/padding_removed/8bit", None)
            originalVolume =\
                self.dataViewer.getPersistentVolume_old(self.originalVolumeName)

            #originalVolume = originalVolume[:,:,3:]
            
            #self.dataViewer.addPersistentVolumeAndRefreshDataTree(originalVolume,
            #                                                      self.originalVolumeName)

            detector = ContourDetector()
            detector.threshold = threshold
            detector.probabilityFunction = self.probabilityFunctionDict[self.target]

    
            if (self.target == 'mitochondria') or (self.target == 'blankInnerCell'):
                #blurredVolume = loadImageStack(driveName + "/images/HPFcere_vol/HPF_rotated_tif/median_then_gaussian_8bit", None)
                #filteredVolume = loadImageStack(driveName + "/images/HPFcere_vol/HPF_rotated_tif/median_then_gaussian_8bit_classified_pixels/tif", None)
                
                #originalVolume = originalVolume[:,:,3:]
                #filteredVolume = filteredVolume[:,:,3:]
                
                #self.dataViewer.addPersistentVolumeAndRefreshDataTree(blurredVolume, self.blurredVolumeName)
                #self.dataViewer.addPersistentVolumeAndRefreshDataTree(filteredVolume, self.filteredVolumeName)

                if numberOfLayersToProcess != None:
                    detector.originalVolume = self.dataViewer.getPersistentVolume_old(self.blurredVolumeName)\
                    [:, :, 0:numberOfLayersToProcess]
                    detector.filteredVolume = self.dataViewer.getPersistentVolume_old(self.filteredVolumeName)\
                    [:, :, 0:numberOfLayersToProcess]
                else:
                    detector.originalVolume = self.dataViewer.getPersistentVolume_old(self.blurredVolumeName)
                    detector.filteredVolume = self.dataViewer.getPersistentVolume_old(self.filteredVolumeName)
    
                #detector.originalVolume = frm.getPersistentVolume_old(blurredVolumeName)
                if self.target == 'mitochondria':
                    #detector.probabilityFunction = mitochondriaProbability
                    detector.filteredVolume = filterVolume2D(detector.filteredVolume,
                                                            'erode', kernelSize=4)
                elif self.target == 'blankInnerCell':
                    #detector.probabilityFunction = blankInnerCellProbability
                    detector.filteredVolume = filterVolume2D(detector.filteredVolume,
                                                             'GrayscaleDilate',
                                                             kernelSize=4)
                else:
                    raise Exception, "Invalid target"
                #detector.filteredVolume = frm.getPersistentVolume_old(filteredVolumeName)
    
            elif self.target == 'vesicles':
            
                detector = ContourDetector()
                fullVolume = self.dataViewer.getPersistentVolume_old(self.originalVolumeName)
    
                if numberOfLayersToProcess != None:
                    detector.originalVolume = fullVolume[:, :, 0:numberOfLayersToProcess]
                else:
                    detector.originalVolume = fullVolume
    
                #detector.probabilityFunction = vesicleProbability
                detector.contourFilterFunction2D = greaterThanSurroundingPixelsFilter
                detector.minPerimeter = 1
                detector.maxPerimeter = 50
    
            else:
                print "find_3D_blobs target error"
    
    
            contoursGroupedByImage = detector.findContours()
            #contoursGroupedByImage.name = self.groupedContoursNodeName
            contoursGroupedByImage.name = groupNodeName
            #contours = flattenTree(contoursGroupedByImage)
            
            # add a node for all detected contours
            #contoursNode = DataNode(contoursNodeName, 'contours node type', {}, None)
            #contoursNode.addObjectList(contours)
            #contoursNode.enableRecursiveRendering = False
            #self.gui.addPersistentSubtreeAndRefreshDataTree((), contoursNode)
            #self.dataViewer.addSubtreeAndRefreshDataTree(self.contoursNodePath,
            #                                             contoursGroupedByImage)
            contoursNode = getNode(self.dataViewer.mainDoc.dataRootNode,
                                   self.contoursNodePath)
            contoursNode.addChild(contoursGroupedByImage)
            #saveBlobsToJinxFile(contoursNode)

            # write contours to an image stack for viewing
            #self.writeContoursToImageStack((contoursNodeName,))
            #self.writeContoursToImageStack((self.groupedContoursNodeName,))
            self.writeContoursToImageStack(self.contoursNodePath)


    def groupContours(self, contoursGroupedByImage):
        
        #contourList = flattenTreeToNodes(contoursGroupedByImage)
        contourList = nonnullObjectNodes(contoursGroupedByImage)

        graph = Graph()
        
        for contour in contourList:
            graph.add_node_object(contour)
            #print contour.valueToSave.getAveragePointLocation()
            print contour.name
            contour.valueToSave.setColor((200, 100, 0))
        
        for imageIndex in range(len(contoursGroupedByImage.children) - 1):
            for contourNode1 in contoursGroupedByImage.children[imageIndex].children:
                contour1 = contourNode1.valueToSave
                center1 = contour1.getAveragePointLocation()
                for contourNode2 in contoursGroupedByImage.children[imageIndex + 1].children:
                    contour2 = contourNode2.valueToSave
                    center2 = contour2.getAveragePointLocation()
                    if linalg.norm(center1 - center2) < 10.0:
                        graph.add_edge(contourNode1.name, contourNode2.name)
                    #print linalg.norm(center1 - center2)

        return pygraph.algorithms.accessibility.connected_components(graph), graph


    def runStep(self, stepNumber):
        
        #defaultStepNumber = 4
        #self.target = 'mitochondria'
        self.target = 'blankInnerCell'
        #self.target = 'vesicles'
        #numberOfContoursToDisplay = None
        displayParametersDict = {}
        displayParametersDict['mitochondria'] = ContourAndBlobDisplayParameters()
        displayParametersDict['mitochondria'].numberOfContoursToDisplay = 20
        displayParametersDict['mitochondria'].contourProbabilityThreshold = 0
        displayParametersDict['blankInnerCell'] = ContourAndBlobDisplayParameters()
        displayParametersDict['blankInnerCell'].numberOfContoursToDisplay = 20
        displayParametersDict['blankInnerCell'].contourProbabilityThreshold = 0.1
        displayParametersDict['vesicles'] = ContourAndBlobDisplayParameters()
        displayParametersDict['vesicles'].numberOfContoursToDisplay = 5 #500 #5 #20
        displayParametersDict['vesicles'].contourSegmentTubeRadius = 0.1
        displayParametersDict['vesicles'].contourCenterMarkerSize = 0.5
        displayParametersDict['vesicles'].contourProbabilityThreshold = 0.27
        
        self.probabilityFunctionDict = {}
        self.probabilityFunctionDict['mitochondria'] = mitochondriaProbability
        self.probabilityFunctionDict['vesicles'] = vesicleProbability
        self.probabilityFunctionDict['blankInnerCell'] = blankInnerCellProbability
        enable3DPlot = False
        #numberOfLayersToProcess = 7
        numberOfLayersToProcess = None
        
        
        #if len(sys.argv) < 2:
        #    print "step not specified, using default step", defaultStepNumber
        #    stepNumber = defaultStepNumber
        #else:
        #    stepNumber = int(sys.argv[1])    
        
        print "running step number", stepNumber
        
        app = wx.PySimpleApp()
        self.dataViewer = ClassificationControlsFrame(makeClassifyGUITree())
        self.dataViewer.Show()
        
        
        self.originalVolumeName = 'OriginalVolume'
        self.blurredVolumeName = 'BlurredVolume'
        self.filteredVolumeName = 'MembraneClassifierFilterVolume'
        #contoursNodeName = target + 'Contours'
        #self.groupedContoursNodeName = self.target + 'ContoursGroupedByImage'
        highProbabilityContoursNodeName = self.target + 'HighProbabilityContours'
    
        if self.target == 'mitochondria': fastMarchInputVolumeName = self.filteredVolumeName
        elif self.target == 'vesicles': fastMarchInputVolumeName = self.originalVolumeName
        else: print "find_3d_blobs target error"
        

        if stepNumber == 0:

            self.preclassificationFilter(self.dataViewer,
                                         numberOfLayersToProcess=numberOfLayersToProcess)


        if stepNumber == 1:

            self.classifyVoxels(self.dataViewer,
                                numberOfLayersToProcess=numberOfLayersToProcess)


        elif stepNumber == 2:

            self.dataViewer.getPersistentVolume_old(self.filteredVolumeName)


        #print "starting find"
        elif stepNumber == 3:
            
            self.dataViewer.mainDoc.dataRootNode.addChild(GroupNode(self.contoursNodeName))

            for thresholdIndex in range(0, 4):

                self.findContours("thresholdIndex_%d" % thresholdIndex,
                                  0.2 * thresholdIndex,
                                  numberOfLayersToProcess)

            self.dataViewer.mainDoc.dataTree.writeSubtree(self.contoursNodePath)
            #self.dataViewer.mainDoc.dataTree.writeSubtree(('Contours', 'thresholdIndex_3'))


        elif stepNumber == 4:
                saveBlobsToJinxFile(
                    self.dataViewer.mainDoc.dataTree.getSubtree(self.contoursNodePath))


        elif stepNumber == 5:

            # - calculate probabilities
            # - threshold by probability
            # - add a node for the high probability contours

            allContoursNode =\
                self.dataViewer.mainDoc.dataTree.getSubtree((self.groupedContoursNodeName,))
            #allContours = allContoursNode.makeChildrenObjectList()
            #highProbabilityContoursNode = DataNode(highProbabilityContoursNodeName, 'contours node type', {}, None)
            #highProbabilityContoursNode.addObjectList(highProbabilityContours(allContours, displayParametersDict[target].contourProbabilityThreshold))
            #highProbabilityContoursNode.enableRecursiveRendering = False

            updateContourProbabilities(allContoursNode,
                                       self.probabilityFunctionDict[self.target])

            #todo: this should filter the tree not just copy it
            threshold = displayParametersDict[self.target].contourProbabilityThreshold
            highProbabilityContoursNode = copyTree(allContoursNode,
                                                   ProbabilityFilter(threshold))
            #highProbabilityContoursNode = copyTree(allContoursNode)
            highProbabilityContoursNode.name = highProbabilityContoursNodeName
 
            self.dataViewer.addPersistentSubtreeAndRefreshDataTree((), highProbabilityContoursNode)
            self.dataViewer.getPersistentVolume_old(self.originalVolumeName)
            self.dataViewer.refreshTreeControls()

            # write contours to an image stack for viewing
            self.writeContoursToImageStack((highProbabilityContoursNodeName,))
    
        
        elif stepNumber == 6:
            
            contoursGroupedByImage = self.dataViewer.mainDoc.dataTree.getSubtree(
                                      (self.groupedContoursNodeName,)) 
            updateContourProbabilities(contoursGroupedByImage,
                                       self.probabilityFunctionDict[self.target])
            connectedComponents, graph = self.groupContours(contoursGroupedByImage)
            
            #count = 0
            s = 0.5
            v = 0.5
            
            print connectedComponents
            
            for nodeNameKey in connectedComponents:
                #nodeName = connectedComponents[key]
                attributes = graph.node_attributes(nodeNameKey)
                contourNode = attributes[0]
                #h = 0.05 * count
                h = 0.05 * connectedComponents[nodeNameKey]
                print contourNode.valueToSave.color()
                print "h", h, "s", s, "v", v
                h = remainder(h, 1.0)
                contourNode.valueToSave.setColor(255.0 * array(colorsys.hsv_to_rgb(h, s, v)))
                #contourNode.valueToSave.setColor((200, 200, 200))
                #count += 1

            originalVolume = self.dataViewer.getPersistentVolume_old(self.originalVolumeName)
            contourRenderingVolume = zeros((originalVolume.shape[0],
                                            originalVolume.shape[1],
                                            originalVolume.shape[2],
                                            3))

            self.dataViewer.renderPointSetsInVolumeRecursive(contourRenderingVolume,
                                                      contoursGroupedByImage,
                                                      valueMode='RGB')

#            writeTiffStackRGB(os.path.join(defaultOutputPath, "rgb"),
#                              contourRenderingVolume[:, :, :, 0],
#                              contourRenderingVolume[:, :, :, 1],
#                              contourRenderingVolume[:, :, :, 2])

            originalVolumeDark = originalVolume * 0.5

            writeTiffStackRGB(os.path.join(defaultOutputPath, "rgb"),
                              contourRenderingVolume[:, :, :, 0] + originalVolumeDark,
                              contourRenderingVolume[:, :, :, 1] + originalVolumeDark,
                              contourRenderingVolume[:, :, :, 2] + originalVolumeDark)


        elif stepNumber == 7:
    
            # use GUI to display high probability contours
    
            if enable3DPlot: display3DContours(self.dataViewer, self.originalVolumeName, highProbabilityContoursNodeName,
                                                displayParametersDict[self.target])
            self.dataViewer.mainDoc.dataTree.getSubtree((highProbabilityContoursNodeName,))
            self.dataViewer.refreshTreeControls()
    
    
        elif stepNumber == 8:
    
            # perform 3D shell active contour to detect 3D blobs
    
            if enable3DPlot:
                display3DContours(self.dataViewer, self.originalVolumeName, highProbabilityContoursNodeName,
                                    displayParametersDict[self.target])
    
            fillAndDisplayResults(self.dataViewer, fastMarchInputVolumeName,
                                       highProbabilityContoursNodeName,
                                       displayParametersDict[self.target],
                                       enable3DPlot,
                                       fillMethod='shellActiveContour')
    
        elif stepNumber == 9:
    
            # write 3D blobs to an XML file and into a stack of tiffs for viewing
    
            self.dataViewer.mainDoc.dataTree.readSubtree(('Blobs',))
            saveBlobsToJinxFile(self.dataViewer.mainDoc.dataTree.getSubtree(('Blobs',)))
            original = self.dataViewer.getPersistentVolume_old(self.originalVolumeName)
            allBlobs = self.dataViewer.getPersistentVolume_old(fastMarchInputVolumeName + 'AllFastMarchBlobs')
            self.dataViewer.refreshTreeControls()
            writeTiffStackRGB(defaultOutputPath,
                              #redVolume=rescale(allBlobs, 0, 255.0),
                              redVolume = (allBlobs > 0) * 255.0,
                              greenVolume=original,
                              blueVolume=None)
    
    
        print "finished step"
        app.MainLoop()


