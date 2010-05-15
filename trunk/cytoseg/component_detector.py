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


import warnings
import numpy
import logging
from cytoseg_classify import *
from contour_list_classification import *
#from mitochondria import *
from fill import *

#import sys
try:
    from enthought.mayavi.scripts import mayavi2
except ImportError:
    warnings.warn("enthought.mayavi.scripts module is not installed")
from default_path import *
#from contour_processing import *
from accuracy import *
from contour_comparison import *
from label_identifier import *

from xml.dom.minidom import Document
#from pygraph import *
try:
    from pygraph.classes.graph import *
    import pygraph.algorithms.accessibility
    from graph import *
except ImportError:
    warnings.warn("pygraph module is not installed")
import os
import colorsys
import copy as copy_module

#log = logging.getLogger('component_detector')
#logging.basicConfig(level=logging.INFO)

#enableMPI = 0
#
#if enableMPI:
#
#    # MPI code
#    from mpi4py import MPI
#    
#    comm = MPI.COMM_WORLD
#    mpiRank = comm.Get_rank()
#    mpiCommSize = comm.Get_size()
#
#else:
#
#    mpiRank = 0
    
enablePathProbabilityFilter = True # use True for mitochondria



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
    perimeterValue = gaussian(abs(131.0 - features['perimeter']), amplitude, 75)
    grayValueMatch = gaussian(abs(1 - features['averageGrayValue']), amplitude, 0.25)
    areaMatch = gaussian(abs(635 - math.sqrt(features['contourArea'])), amplitude, 300)
    return overlapValue * perimeterValue * grayValueMatch * areaMatch * areaMatch


def mitochondria_newProbability(features):

    amplitude = 1
    overlapValue = gaussian(1.0 - features['ellipseOverlap'], amplitude, 0.2)
    perimeterValue = gaussian(abs(131.0 - features['perimeter']), amplitude, 75)
    #grayValueMatch = gaussian(abs(1 - features['averageGrayValue']), amplitude, 0.25)
    grayValueMatch = features['averageGrayValue']
    area = math.sqrt(features['contourArea']) / 635.0
    #return overlapValue * perimeterValue * grayValueMatch * area * area
    return grayValueMatch * area * area * area


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

        if p < 0:
            limitedProbability = 0
        elif p > 1:
            limitedProbability = 1
        else:
            limitedProbability = p

        color = 255.0 * array(((1.0 - limitedProbability) * 10.0,
                               (limitedProbability * 10.0),
                               0))
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


def saveBlobsToJinxFile(node, filename):
    """filename: filename (without a path or an extension)"""

    doc = Document()
    #blobsNode = gui.mainDoc.dataTree.getSubtree(('Blobs',))
    main = doc.createElement("main")
    doc.appendChild(main)

    #for childNode in node.children:
    #    #print childNode.object.getXMLVoxelList(doc)
    #    #getXMLPointList should allow floating points values
    #    main.appendChild(childNode.object.getXMLObject(doc, childNode.name))
    #print doc.toprettyxml(indent="  ")

    saveBlobsToJinxFileRecursiveHelper(node, doc, main)

    file = open(os.path.join(defaultOutputPath, filename + ".xml"), "w")
    file.write(doc.toprettyxml(indent="   "))


def saveBlobsToJinxFileRecursiveHelper(node, document, documentElement):

    if node.isGroupNode:
        for childNode in node.children:
            saveBlobsToJinxFileRecursiveHelper(childNode, document, documentElement)
    else:
        documentElement.appendChild(
            node.object.getXMLObject(document, node.name))



class ComponentDetector:


    def __init__(self,
                 dataViewer,
                 dataIdentifier,
                 target,
                 originalImageFilePath,
                 contourListClassificationMethod,
                 contourListExamplesIdentifier, # file to write to
                 contourListTrainingExamplesIdentifier, # file to read from
                 voxelTrainingImageFilePath=None,
                 voxelTrainingLabelFilePath=None,
                 labelFilePaths=None,
                 voxelClassificationIteration=0):
        '''contourListExamplesIdentifier: features from detected contours go in this file
        contourListTrainingExamplesIdentifier: the classifier is generated based on these
        examples'''

        #self.app = wx.PySimpleApp()
        #self.dataViewer = ClassificationControlsFrame(makeClassifyGUITree())
        #self.dataViewer.Show()

        self.dataViewer = dataViewer

        self.dataIdentifier = dataIdentifier
        self.target = target
        self.highProbabilityContoursBaseFilename =\
            self.dataIdentifier + "_" + self.target

        #self.originalImageFilePath =\
        #    "O:/images/HPFcere_vol/HPF_rotated_tif/padding_removed/8bit"
        #self.originalImageFilePath =\
        #    "O:/images/Eric_07-10-09/normalized_tiff_files/cropped_stack/8bit"
        self.originalImageFilePath = originalImageFilePath

        self.originalVolumeName = dataIdentifier + 'OriginalVolume'
        self.voxelClassificationInputVolumeName = self.originalVolumeName
        self.blurredVolumeName = dataIdentifier + 'BlurredVolume'
        self._voxelClassificationIteration = voxelClassificationIteration

#        self.voxelTrainingClassificationResultPath =\
#            ('Volumes', dataIdentifier + 'VoxelTrainingClassificationResult'
#             + '_' + str(self._voxelClassificationIteration))
#
#        self.voxelClassificationResultPath =\
#            ('Volumes', dataIdentifier + 'VoxelClassificationResult'
#             + '_' + str(self._voxelClassificationIteration))
#
#
#        if self._voxelClassificationIteration > 0:
#
#            self.previousVoxelTrainingClassificationResultPath =\
#                ('Volumes', dataIdentifier + 'VoxelTrainingClassificationResult'
#                 + '_' + str(self._voxelClassificationIteration - 1))
#
#            self.previousVoxelClassificationResultPath =\
#                ('Volumes', dataIdentifier + 'VoxelClassificationResult'
#                 + '_' + str(self._voxelClassificationIteration - 1))
#
#        else:
#
#            self.previousVoxelTrainingClassificationResultPath = None
#            self.previousVoxelClassificationResultPath = None


        # this is for old accuracy check
        self.fullManualSegNodePath =\
            ('Volumes', dataIdentifier + 'FullManualSeg')

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

        self.contourListClassificationMethod = contourListClassificationMethod

        self.contoursNodeName = dataIdentifier + '_' + self.target + 'Contours'
        self.contoursNodePath = (self.contoursNodeName,)
        self.contourPathsNodePath = (dataIdentifier + '_' + self.target + 'ContourPaths',)
        if contourListExamplesIdentifier != None:
            self.contourListExamplesIdentifier = contourListExamplesIdentifier +\
                                                '_' + self.target
        self.contourListTrainingExamplesIdentifier =\
            contourListTrainingExamplesIdentifier +\
            '_' + self.target
        self.labelFilePaths = labelFilePaths

        self.fullManualSegFilePath = None

        self.numberOfTrainingLayersToProcess = None

        self.numberOfLayersToProcess = None
        self.trainingRegion = None
        self.regionToClassify = None
        self.numberOfThresholds = 1
        self.firstThreshold = 0.5
        self.thresholdStep = 0.1

        #self.minVoxelLabelValue = 1
        #self.maxVoxelLabelValue = None

        self.displayParametersDict = {}
        self.displayParametersDict['mitochondria'] = ContourAndBlobDisplayParameters()
        self.displayParametersDict['mitochondria'].numberOfContoursToDisplay = None #20
        self.displayParametersDict['mitochondria'].contourProbabilityThreshold = 0.08
        self.displayParametersDict['mitochondria_new'] = ContourAndBlobDisplayParameters()
        self.displayParametersDict['mitochondria_new'].numberOfContoursToDisplay = None #20
        self.displayParametersDict['mitochondria_new'].contourProbabilityThreshold = 0.06
        self.displayParametersDict['blankInnerCell'] = ContourAndBlobDisplayParameters()
        self.displayParametersDict['blankInnerCell'].numberOfContoursToDisplay = 20
        self.displayParametersDict['blankInnerCell'].contourProbabilityThreshold = 0 #0.1
        self.displayParametersDict['vesicles'] = ContourAndBlobDisplayParameters()
        self.displayParametersDict['vesicles'].numberOfContoursToDisplay = 5 #500 #5 #20
        self.displayParametersDict['vesicles'].contourSegmentTubeRadius = 0.1
        self.displayParametersDict['vesicles'].contourCenterMarkerSize = 0.5
        self.displayParametersDict['vesicles'].contourProbabilityThreshold = 0.15
        
        self.probabilityFunctionDict = {}
        self.probabilityFunctionDict['mitochondria'] = mitochondriaProbability
        self.probabilityFunctionDict['mitochondria_new'] =\
            mitochondria_newProbability
        self.probabilityFunctionDict['vesicles'] = vesicleProbability
        self.probabilityFunctionDict['blankInnerCell'] = blankInnerCellProbability
        self.probabilityFunctionDict['membranes'] = blankInnerCellProbability
        self.probabilityFunctionDict['membranes_test'] = blankInnerCellProbability
        self.pathLength = {}
        self.pathLength['mitochondria'] = 3
        self.pathLength['vesicles'] = 1
        self.pathLength['blankInnerCell'] = 1
        self.enable3DPlot = False
        #numberOfLayersToProcess = 7

        #targetKeys = ['mitochondria', 'blankInnerCell', 'vesicles', 'membranes'] 
        #self.minVoxelLabelValue = {}
        #self.maxVoxelLabelValue = {}

        self.labelIdentifierDict = {}

        ## setting defaults so that 1 or greater represents the label
        #for key in targetKeys:
        #    self.minVoxelLabelValue[key] = 1
        #    self.maxVoxelLabelValue[key] = None

        #for key in targetKeys:

        #    self.labelIdentifierDict[key] = LabelIdentifier(min=1)


#    def voxelTrainingClassificationResultPaths():
#
#        paths = []
#        for i in range(self._voxelClassificationIteration + 1):
#            paths.append(('Volumes', dataIdentifier + 'VoxelTrainingClassificationResult'
#                          + '_' + str(self._voxelClassificationIteration)))
#
#
#    def voxelClassificationResultPaths():
#
#        paths = []
#        for i in range(self._voxelClassificationIteration + 1):
#            paths.append(('Volumes', dataIdentifier + 'VoxelClassificationResult'
#                          + '_' + str(self._voxelClassificationIteration)))


    def voxelTrainingClassificationResultPath(self, iteration):

        return ('Volumes', self.dataIdentifier + 'VoxelTrainingClassificationResult'
                + '_' + str(iteration))


    def voxelClassificationResultPath(self, iteration):

        return ('Volumes', self.dataIdentifier + 'VoxelClassificationResult'
                + '_' + str(iteration))


    def currentVoxelTrainingClassificationResultPath(self):

        return self.voxelTrainingClassificationResultPath(
                                    self._voxelClassificationIteration)


    def currentVoxelClassificationResultPath(self):

        return self.voxelClassificationResultPath(self._voxelClassificationIteration)


    def previousVoxelTrainingClassificationResultPath(self):

        return self.voxelTrainingClassificationResultPath(
                                    self._voxelClassificationIteration - 1)


    def previousVoxelClassificationResultPath(self):

        return self.voxelClassificationResultPath(self._voxelClassificationIteration - 1)


    def writeContoursToImageStack(self, pathToContoursNode):

        print "writing contours to image stack", defaultOutputPath

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


    # todo: numberOfLayersToProcess parameter seems redundant
    def preclassificationFilter(self, dataViewer, numberOfLayersToProcess=None):

        # todo: use runLoadOriginalImage to do this
        originalImageNodePath = ('Volumes', 'originalImage')

        originalImage = loadImageStack(self.originalImageFilePath, None)

        originalImage = originalImage[:, :, 0:self.numberOfLayersToProcess]

        # this might be redundant
        dataViewer.addVolumeAndRefreshDataTree(originalImage, originalImageNodePath[1])

        print "starting itk filtering"
        medianFilteredImage = itkFilter(originalImage, 'Median', radius=1)
        blurredImage = itkFilter(medianFilteredImage, 'SmoothingRecursiveGaussian', sigma=1)
        print "itk filtering complete"

        dataViewer.addPersistentVolumeAndRefreshDataTree(originalImage,
                                                         self.originalVolumeName)

        dataViewer.addPersistentVolumeAndRefreshDataTree(blurredImage,
                                                         self.blurredVolumeName)


    def classifyVoxels_old(self, dataViewer, numberOfLayersToProcess=None,
                           minLabelValue=1, maxLabelValue=None):

        inputVolumeDict = odict()
        originalImageNodePath = ('Volumes', 'originalImage')
        inputVolumeDict['originalVolume'] =\
            self.dataViewer.getPersistentObject(originalImageNodePath)
        if self._voxelClassificationIteration > 0:
            inputVolumeDict['previousResult'] =\
                self.dataViewer.getPersistentObject(
                    self.previousVoxelClassificationResultPath)

        # inputVolumeName = self.blurredVolumeName for sfn2009 results
        
        #inputImageFilePath =\
        #    driveName + "/images/HPFcere_vol/HPF_rotated_tif/median_then_gaussian_8bit"
        exampleListFileName = os.path.join(cytosegDataFolder, "exampleList.tab")
        
        voxelTrainingImageNodePath = ('Volumes', 'voxelTrainingImage')
        voxelTrainingLabelNodePath = ('Volumes', 'voxelTrainingLabel')
        inputImageNodePath = ('Volumes', 'inputImage')
    
        # load training images
        dataViewer.addVolumeAndRefreshDataTree(
            loadImageStack(self.voxelTrainingImageFilePath,
                           None,
                           maxNumberOfImages=self.numberOfTrainingLayersToProcess),
            voxelTrainingImageNodePath[1])
    
        inputTrainingVolumeDict = odict()
        inputTrainingVolumeDict['originalVolume'] =\
            self.dataViewer.getPersistentObject(voxelTrainingImageNodePath)
        if self._voxelClassificationIteration > 0:
            inputTrainingVolumeDict['previousResult'] =\
                self.dataViewer.getPersistentObject(
                    self.previousVoxelTrainingClassificationResultPath)

        # load training labels
        rawLabelVolume = loadImageStack(self.voxelTrainingLabelFilePath,
                            None,
                            maxNumberOfImages=self.numberOfTrainingLayersToProcess)

        # open input image data to be classified
        #inputImage = self.dataViewer.getPersistentVolume_old(self.blurredVolumeName)
        inputImage = self.dataViewer.getPersistentVolume_old(
                                                    self.voxelClassificationInputVolumeName)
        # crop input image data if specified
        if numberOfLayersToProcess != None:
            inputImage = inputImage[:, :, 0:numberOfLayersToProcess]

        if maxLabelValue == None:
            labelVolume = rawLabelVolume >= minLabelValue
        else:
            labelVolume =\
                logical_and(minLabelValue <= rawLabelVolume,
                            rawLabelVolume <= maxLabelValue)

        dataViewer.addVolumeAndRefreshDataTree(labelVolume, voxelTrainingLabelNodePath[1])
        
        #inputImage = loadImageStack(inputImageFilePath, None)
        
        dataViewer.addVolumeAndRefreshDataTree(inputImage, inputImageNodePath[1])
    
        if self.voxelClassificationMethod == 'randomForest':

            # uses training data
            print "learning features of training data"
            dataViewer.learnFeaturesOfMembraneVoxels(inputTrainingVolumeDict,
                                                     voxelTrainingImageNodePath,
                                                     voxelTrainingLabelNodePath,
                                                     exampleListFileName)
        
            # uses training data, generates voxel probabilities
            print "classifying training set voxels"
            dataViewer.classifyVoxels('intermediateTrainingDataLabel1',
                               self.currentVoxelTrainingClassificationResultPath(),
                               exampleListFileName,
                               inputTrainingVolumeDict,
                               voxelTrainingImageNodePath)

            # uses test data, generates voxel probabilities
            print "classifying voxels"
            dataViewer.classifyVoxels('intermediateTestDataLabel1',
                               self.currentVoxelClassificationResultPath(),
                               exampleListFileName,
                               inputVolumeDict,
                               inputImageNodePath)

        elif self.voxelClassificationMethod == 'neuralNetwork':

            #dataViewer.learnFeaturesOfMembraneVoxels(voxelTrainingImageNodePath,
            #                                  voxelTrainingLabelNodePath,
            #                                  exampleListFileName)

            dataViewer.classifyVoxelsNN('intermediateDataLabel1',
                               self.currentVoxelClassificationResultPath()[1],
                               exampleListFileName,
                               inputImageNodePath)


    #def classifyVoxels(self, dataViewer, labelIdentifier, numberOfLayersToProcess=None):
    def classifyVoxels(self, dataViewer, numberOfLayersToProcess=None):

        inputVolumeDict = odict()
        originalImageNodePath = ('Volumes', 'originalImage')
        inputVolumeDict['originalVolume'] =\
            self.dataViewer.getPersistentObject(originalImageNodePath)
        if self._voxelClassificationIteration > 0:
            resultsNode = self.dataViewer.mainDoc.dataTree.getSubtree(
                            self.previousVoxelClassificationResultPath())
            #resultsNode = getNode(self.dataViewer.mainDoc.dataRootNode,
            #                self.previousVoxelClassificationResultPath)
            for childNode in resultsNode.children:
                inputVolumeDict['previousResult_' + childNode.name] = childNode.object
                    #self.dataViewer.getPersistentObject(
                    #    self.previousVoxelClassificationResultPath)

        # inputVolumeName = self.blurredVolumeName for sfn2009 results
        
        #inputImageFilePath =\
        #    driveName + "/images/HPFcere_vol/HPF_rotated_tif/median_then_gaussian_8bit"
        #exampleListFileName = os.path.join(cytosegDataFolder, "exampleList%d.tab" % mpiRank)
        exampleListFileName = os.path.join(cytosegDataFolder, "exampleList.tab")
        
        voxelTrainingImageNodePath = ('Volumes', 'voxelTrainingImage')
        voxelTrainingLabelNodePath = ('Volumes', 'voxelTrainingLabel')
        inputImageNodePath = ('Volumes', 'inputImage')
    
        ## load training images
        #dataViewer.addVolumeAndRefreshDataTree(
        #    loadImageStack(self.voxelTrainingImageFilePath,
        #                   self.trainingRegion,
        #                   maxNumberOfImages=self.numberOfTrainingLayersToProcess),
        #    voxelTrainingImageNodePath[1])
    
        inputTrainingVolumeDict = odict()
        inputTrainingVolumeDict['originalVolume'] =\
            self.dataViewer.getPersistentObject(voxelTrainingImageNodePath)
        if self._voxelClassificationIteration > 0:
            #inputTrainingVolumeDict['previousResult'] =\
            #    self.dataViewer.getPersistentObject(
            #        self.previousVoxelTrainingClassificationResultPath)

            resultsNode = self.dataViewer.mainDoc.dataTree.getSubtree(
                            self.previousVoxelTrainingClassificationResultPath())

            for childNode in resultsNode.children:
                inputTrainingVolumeDict['previousResult_' + childNode.name] =\
                    childNode.object

        ## load training labels
        #labelVolume = loadImageStack(self.voxelTrainingLabelFilePath,
        #                    self.trainingRegion,
        #                    maxNumberOfImages=self.numberOfTrainingLayersToProcess)

        # open input image data to be classified
        #inputImage = self.dataViewer.getPersistentVolume_old(self.blurredVolumeName)
        inputImage = self.dataViewer.getPersistentVolume_old(
                                                    self.voxelClassificationInputVolumeName)
        # crop input image data if specified
        if numberOfLayersToProcess != None:
            inputImage = inputImage[:, :, 0:numberOfLayersToProcess]

        #if maxLabelValue == None:
        #    labelVolume = rawLabelVolume >= minLabelValue
        #else:
        #    labelVolume =\
        #        logical_and(minLabelValue <= rawLabelVolume,
        #                    rawLabelVolume <= maxLabelValue)

        #dataViewer.addVolumeAndRefreshDataTree(labelVolume, voxelTrainingLabelNodePath[1])
        
        #inputImage = loadImageStack(inputImageFilePath, None)
        
        dataViewer.addVolumeAndRefreshDataTree(inputImage, inputImageNodePath[1])
    
        if self.voxelClassificationMethod == 'randomForest':

            # uses training data
            print "recording features of training data"
            dataViewer.recordLocalFeatures(inputTrainingVolumeDict,
                                           self.labelIdentifierDict,
                                           voxelTrainingImageNodePath,
                                           voxelTrainingLabelNodePath,
                                           exampleListFileName)
        
            # uses training data, generates voxel probabilities
            print "classifying training set voxels"
            dataViewer.classifyVoxels('intermediateTrainingDataLabel1',
                               self.currentVoxelTrainingClassificationResultPath(),
                               exampleListFileName,
                               inputTrainingVolumeDict,
                               voxelTrainingImageNodePath)

            # uses test data, generates voxel probabilities
            print "classifying voxels"
            print "volume shapes"
            for item in inputVolumeDict.items():
                key = item[0]
                print key, inputVolumeDict[key].shape
            dataViewer.classifyVoxels('intermediateTestDataLabel1',
                               self.currentVoxelClassificationResultPath(),
                               exampleListFileName,
                               inputVolumeDict,
                               inputImageNodePath)

        elif self.voxelClassificationMethod == 'neuralNetwork':

            #dataViewer.learnFeaturesOfMembraneVoxels(voxelTrainingImageNodePath,
            #                                  voxelTrainingLabelNodePath,
            #                                  exampleListFileName)

            dataViewer.classifyVoxelsNN('intermediateDataLabel1',
                               self.currentVoxelClassificationResultPath()[1],
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

            originalVolumeShape = originalVolume.shape

            detector = ContourDetector((originalVolumeShape[0], originalVolumeShape[1]))
            detector.threshold = threshold
            detector.probabilityFunction = self.probabilityFunctionDict[self.target]

    
            if (self.target == 'mitochondria') or (self.target == 'blankInnerCell'):
                #blurredVolume = loadImageStack(driveName + "/images/HPFcere_vol/HPF_rotated_tif/median_then_gaussian_8bit", None)
                #filteredVolume = loadImageStack(driveName + "/images/HPFcere_vol/HPF_rotated_tif/median_then_gaussian_8bit_classified_pixels/tif", None)
                
                #originalVolume = originalVolume[:,:,3:]
                #filteredVolume = filteredVolume[:,:,3:]
                
                #self.dataViewer.addPersistentVolumeAndRefreshDataTree(blurredVolume, self.blurredVolumeName)
                #self.dataViewer.addPersistentVolumeAndRefreshDataTree(filteredVolume, self.voxelClassificationResultPath[1])

                if numberOfLayersToProcess != None:
                    detector.originalVolume = self.dataViewer.getPersistentVolume_old(self.blurredVolumeName)\
                    [:, :, 0:numberOfLayersToProcess]
                    detector.filteredVolume = self.dataViewer.getPersistentVolume_old(self.currentVoxelClassificationResultPath()[1])\
                    [:, :, 0:numberOfLayersToProcess]
                else:
                    detector.originalVolume = self.dataViewer.getPersistentVolume_old(self.blurredVolumeName)
                    detector.filteredVolume = self.dataViewer.getPersistentVolume_old(self.currentVoxelClassificationResultPath()[1])
    
                #detector.originalVolume = frm.getPersistentVolume_old(blurredVolumeName)
                if self.target == 'mitochondria':
                    #detector.probabilityFunction = mitochondriaProbability
                    detector.filteredVolume = filterVolume2D(detector.filteredVolume,
                                                            'GrayscaleErode', kernelSize=4)
                elif self.target == 'blankInnerCell':
                    #detector.probabilityFunction = blankInnerCellProbability
                    detector.filteredVolume = filterVolume2D(detector.filteredVolume,
                                                             'GrayscaleDilate',
                                                             kernelSize=4)
                else:
                    raise Exception, "Invalid target"
                #detector.filteredVolume = frm.getPersistentVolume_old(filteredVolumeName)
    
            elif self.target == 'vesicles':
            
                #detector = ContourDetector()
                fullVolume = self.dataViewer.getPersistentVolume_old(self.originalVolumeName)
    
                if numberOfLayersToProcess != None:
                    detector.originalVolume = fullVolume[:, :, 0:numberOfLayersToProcess]
                else:
                    detector.originalVolume = fullVolume
    
                #detector.probabilityFunction = vesicleProbability
                detector.contourFilterFunction2D = greaterThanSurroundingPixelsFilter
                detector.minPerimeter = 1
                detector.maxPerimeter = 50

            elif self.target == 'membranes':

                if numberOfLayersToProcess != None:
                    detector.originalVolume = self.dataViewer.getPersistentVolume_old(self.originalVolumeName)\
                    [:, :, 0:numberOfLayersToProcess]
                    detector.filteredVolume = self.dataViewer.getPersistentVolume_old(self.currentVoxelClassificationResultPath()[1])\
                    [:, :, 0:numberOfLayersToProcess]
                else:
                    detector.originalVolume = self.dataViewer.getPersistentVolume_old(self.originalVolumeName)
                    detector.filteredVolume = self.dataViewer.getPersistentVolume_old(self.currentVoxelClassificationResultPath()[1])

            elif self.target == 'membranes_test':
            
                if numberOfLayersToProcess != None:
                    detector.originalVolume = self.dataViewer.getPersistentVolume_old(self.originalVolumeName)\
                    [:, :, 0:numberOfLayersToProcess]
                    detector.filteredVolume = self.dataViewer.getPersistentVolume_old(self.originalVolumeName)\
                    [:, :, 0:numberOfLayersToProcess]
                else:
                    detector.originalVolume = self.dataViewer.getPersistentVolume_old(self.originalVolumeName)
                    detector.filteredVolume = self.dataViewer.getPersistentVolume_old(self.originalVolumeName)

            elif self.target == 'mitochondria_new':
            
                detector.retrievalMode = cv.CV_RETR_EXTERNAL

                if numberOfLayersToProcess != None:
                    detector.originalVolume = self.dataViewer.getPersistentVolume_old(self.originalVolumeName)\
                    [:, :, 0:numberOfLayersToProcess]
                    detector.filteredVolume = self.dataViewer.getPersistentVolume_old(self.originalVolumeName)\
                    [:, :, 0:numberOfLayersToProcess]
                else:
                    detector.originalVolume = self.dataViewer.getPersistentVolume_old(self.originalVolumeName)
                    detector.filteredVolume = self.dataViewer.getPersistentVolume_old(self.originalVolumeName)

            else:

                raise Exception, "findContours: invalid target: %s" % self.target


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
            #self.writeContoursToImageStack(self.contoursNodePath)
            
            self.dataViewer.refreshTreeControls()


#    def groupContoursByConnectedComponents(self, contoursGroupedByImage):
#        
#        #contourList = flattenTreeToNodes(contoursGroupedByImage)
#        contourList = nonnullObjectNodes(contoursGroupedByImage)
#
#        graph = Graph()
#        
#        for contour in contourList:
#            graph.add_node_object(contour)
#            #print contour.object.getAveragePointLocation()
#            print contour.name
#            contour.object.setColor((200, 100, 0))
#        
#        for imageIndex in range(len(contoursGroupedByImage.children) - 1):
#            for contourNode1 in contoursGroupedByImage.children[imageIndex].children:
#                contour1 = contourNode1.object
#                center1 = contour1.getAveragePointLocation()
#                for contourNode2 in contoursGroupedByImage.children[imageIndex + 1].children:
#                    contour2 = contourNode2.object
#                    center2 = contour2.getAveragePointLocation()
#                    if linalg.norm(center1 - center2) < 10.0:
#                        graph.add_edge(contourNode1.name, contourNode2.name)
#                    #print linalg.norm(center1 - center2)
#
#        return pygraph.algorithms.accessibility.connected_components(graph), graph


    def groupContoursByConnectedComponents(self, contoursNode):
        
        contourList = nonnullObjectNodes(contoursNode)

        g = Graph()
        
        for contour in contourList:
            g.add_node_object(contour)
            #print contour.object.getAveragePointLocation()
            print contour.name
            contour.object.setColor((200, 100, 0))
        
        # regroup contours according to image only, not threshold and image
        numLayers = contoursNode.children[0].numberOfChildren()
        contoursGroupedByImage = GroupNode('contoursGroupedByImage')

        for layerIndex in range(numLayers):
            contoursGroupedByImage.addChild(Node('layer_%d' % layerIndex))

        for imageLayersNode in contoursNode.children:
            for layerIndex in range(len(imageLayersNode.children) - 1):
                layerNode = imageLayersNode.children[layerIndex]
                contoursGroupedByImage.children[layerIndex].addChildren(layerNode.children)

        self.dataViewer.addPersistentSubtreeAndRefreshDataTree((), contoursGroupedByImage)

        contourPairNode = GroupNode('contourPairNode')
        contourPairNode.children = [None, None]
        for imageIndex in range(len(contoursGroupedByImage.children) - 1):
            for contourNode1 in contoursGroupedByImage.children[imageIndex].children:
                contour1 = contourNode1.object
                center1 = contour1.getAveragePointLocation()
                for contourNode2 in contoursGroupedByImage.children[imageIndex + 1].children:
                    contour2 = contourNode2.object
                    contourPairNode.children[0] = contourNode1
                    contourPairNode.children[1] = contourNode2
                    featureDict = getContourListFeatures(contourPairNode,
                                        includeIndividualContourFeatures=False)
                    print featureDict
                    center2 = contour2.getAveragePointLocation()
                    #if linalg.norm(center1 - center2) < 10.0:
                    if linalg.norm(center1 - center2) < 50.0:
                        if overlap(contour1, contour2) > 0.4:
                            g.add_edge((contourNode1.name, contourNode2.name))
                        #print "overlap", overlap(contour1, contour2)
                    #print len(g.edges())
                    #print linalg.norm(center1 - center2)

        return pygraph.algorithms.accessibility.connected_components(g), g


    def computeContourRegions(self):

        for labelName in self.labelFilePaths.keys():
            self.dataViewer.addPersistentVolumeAndRefreshDataTree(
                                    loadImageStack(self.labelFilePaths[labelName], None),
                                    labelName)

        contoursRootNode = self.dataViewer.mainDoc.dataTree.getSubtree(
                                                                self.contoursNodePath)
        self.dataViewer.refreshTreeControls()

        # flatten tree of contours into a list
        contourList = nonnullObjects(contoursRootNode)

        # visit each contour and look at the label that goes with each point
        for contour in contourList:
            count = {}
            for labelName in self.labelFilePaths.keys():
                count[labelName] = 0
                labelVolume = self.dataViewer.getVolume(labelName)
                for location in contour.locations():
                    if at(labelVolume, location) != 0:
                        count[labelName] += 1

                # if more than half of the points have a certain label,
                # assign that label to the contour
                if count[labelName] > (contour.numPoints() / 2):
                    contour.labelSet.add(labelName)
                    #print contour.labelSet
            contour.labelCountDict = count

        self.dataViewer.mainDoc.dataTree.writeSubtree(self.contoursNodePath)


    def makeContourLists(self, probabilityThreshold, pathLength):

        #startIndex = 3
        #pathLength = 3

        self.dataViewer.getPersistentVolume_old(self.originalVolumeName)
        self.dataViewer.mainDoc.dataTree.getSubtree(self.contoursNodePath)
        self.dataViewer.refreshTreeControls()

        #allContoursAtPlane = getNode(self.dataViewer.mainDoc.dataRootNode,
        #                             self.contoursNodePath + ('thresholdIndex_0',))
        contoursNode = getNode(self.dataViewer.mainDoc.dataRootNode,
                                     self.contoursNodePath)

        newContourStack = GroupNode('ContourStack')

        firstThresholdNode = contoursNode.children[0]
        numPlanes = len(firstThresholdNode.children)
        for i in range(numPlanes):
            newContourStack.addChild(GroupNode('plane_%d' % i))

        for thresholdSetNode in contoursNode.children:
            for contourPlaneNodeIndex in range(numPlanes):
                #print len(thresholdSetNode.children)
                #print numPlanes
                contourPlaneNode = thresholdSetNode.children[contourPlaneNodeIndex]
                for contourNode in contourPlaneNode.children:
                    newContourStack.children[contourPlaneNodeIndex].addChild(contourNode)

        self.dataViewer.addPersistentSubtreeAndRefreshDataTree((), newContourStack)

        allPathsNode = GroupNode(self.contourPathsNodePath[0])

        for startIndex in range(numPlanes - pathLength):

            pathList = GroupNode()
            #pathList.addChild(GroupNode())
    
            # initialize the paths with the contours at the startIndex plane
            planeNode = newContourStack.children[startIndex]
            for contourNode in planeNode.children:
                pathNode = GroupNode()
                pathNode.addChild(contourNode)
                pathList.addChild(pathNode)

            for planeIndex in range(startIndex + 1, startIndex + pathLength):
    
                print "planeIndex:", planeIndex, "pathLength:", pathLength
    
                planeNode = newContourStack.children[planeIndex]
    
                newPathList = GroupNode()
    
                for contourNode in planeNode.children:
    
                    # contour that may be appended to path if it is close enough
                    newContour = contourNode.object
                    newCenter = newContour.getAveragePointLocation()
    
                    for pathNode in pathList.children:
    
                        # last contour in path that may be appended to
                        endOfPathContourNode = pathNode.children[-1]
                        contour1 = endOfPathContourNode.object
                        center1 = contour1.getAveragePointLocation()
    
                        if linalg.norm(center1 - newCenter) < 40:
    
                            newPathNode = copy_module.deepcopy(pathNode)
                            newPathNode.addObject(newContour)
                            newPathList.addChild(newPathNode)
    
                pathList = newPathList
                #pathList.name = 'planeIndex_%d' % planeIndex

            # calculate features
            for contourListNode in pathList.children:
                contourListNode.object = getContourListProperties(contourListNode)

            # calculate probabilities based on features
            classifyContourListsBayes(mitochondriaProbability, pathList)

            filteredPathList = GroupNode()

            # filter out low probability paths
            for contourListNode in pathList.children:
                #print contourListNode.object.probability()
                if contourListNode.object.probability() >\
                   pow(probabilityThreshold, pathLength) / 200.0\
                   or not(enablePathProbabilityFilter):
                    filteredPathList.addChild(contourListNode)

            allPathsNode.addChildren(filteredPathList.children)
            
        self.dataViewer.addPersistentSubtreeAndRefreshDataTree((), allPathsNode)


    def calculateContourListFeatures(self):

        contourListsNode = self.dataViewer.mainDoc.dataTree.getSubtree(self.contourPathsNodePath)

        for contourListNode in contourListsNode.children:
            contourListNode.object = getContourListProperties(contourListNode)

        self.dataViewer.mainDoc.dataTree.writeSubtree(self.contourPathsNodePath)
    
    
    def calculateVoxelClassificationAccuracy(self):

        if self.fullManualSegFilePath == None:
            raise Exception,\
                "fullManualSegFilePath is None, no actual segmentation specified"

        resultVolume =\
            self.dataViewer.getPersistentObject(self.currentVoxelClassificationResultPath())
        fullManualSegVolume = loadImageStack(self.fullManualSegFilePath,
                                             None,
                                             maxNumberOfImages=self.numberOfLayersToProcess)
        self.dataViewer.addVolumeAndRefreshDataTree_new(fullManualSegVolume,
                                                        self.fullManualSegNodePath)

        #print resultVolume[10, 10, 10]

        for i in range(0, 20, 1):

            threshold = i / 20.0
            print "threshold:", threshold

            accuracy = Accuracy(fullManualSegVolume, (resultVolume > threshold))
            accuracy.printAccuracy()


    def calculateFinalAccuracy(self):

        if self.fullManualSegFilePath == None:
            raise Exception,\
                "fullManualSegFilePath is None, no actual segmentation specified"

        resultVolume = loadImageStack("O:/images/HPFcere_vol/HPF_rotated_tif/output/blobOutput",
                                      None,
                                      maxNumberOfImages=self.numberOfLayersToProcess)
        self.dataViewer.addVolumeAndRefreshDataTree_new(resultVolume,
                                                        self.fullManualSegNodePath)

        fullManualSegVolume = loadImageStack(self.fullManualSegFilePath,
                                             None,
                                             maxNumberOfImages=self.numberOfLayersToProcess)
        self.dataViewer.addVolumeAndRefreshDataTree_new(fullManualSegVolume,
                                                        self.fullManualSegNodePath)

        #print resultVolume[10, 10, 10]

        accuracy = Accuracy(fullManualSegVolume, resultVolume)
        accuracy.printAccuracy()


    def calculateVoxelClassificationAccuracy_new(self):

        import matplotlib.pyplot as pyplot

        #if self.fullManualSegFilePath == None:
        #    raise Exception,\
        #        "fullManualSegFilePath is None, no actual segmentation specified"

        #resultVolume = loadImageStack("O:/images/HPFcere_vol/HPF_rotated_tif/output/blobOutput",
        #                              None,
        #                              maxNumberOfImages=self.numberOfLayersToProcess)
        #resultVolume = getPersistentObject(self.voxelClassificationResultPath)
        #self.dataViewer.addVolumeAndRefreshDataTree_new(resultVolume,
        #                                                self.fullManualSegNodePath)

        # load and display full manual segmentation
        #fullManualSegVolume = loadImageStack(self.voxelTrainingLabelFilePath,
        #                                     None,
        #                                     maxNumberOfImages=self.numberOfLayersToProcess)
        fullManualSegVolume = loadImageStack(self.fullManualSegFilePath,
                                             None,
                                             maxNumberOfImages=self.numberOfLayersToProcess)
        self.dataViewer.addVolumeAndRefreshDataTree_new(fullManualSegVolume,
                                                        self.fullManualSegNodePath)


        #pyplot.hold(False)

        # for each type of subcellular component
        #for childNode in resultsNode.children:
        for target in self.labelIdentifierDict:

            pyplot.hold(True)

            for iteration in range(self._voxelClassificationIteration + 1):

                resultsNode = self.dataViewer.mainDoc.dataTree.getSubtree(
                                            self.voxelClassificationResultPath(iteration))


                #target = childNode.name

                #resultVolume = childNode.object

                try:

                    resultVolume = resultsNode.getChild(target).object

                    #self.dataViewer.addVolumeAndRefreshDataTree_new(resultVolume,
                    #                                                self.fullManualSegNodePath)

                    #fullManualSegVolume = loadImageStack(self.fullManualSegFilePath,
                    #                                     None,
                    #                                     maxNumberOfImages=self.numberOfLayersToProcess)

                    #print resultVolume[10, 10, 10]

                    targetLabel = self.labelIdentifierDict[target].getBooleanVolume(
                                                                fullManualSegVolume)

                    self.dataViewer.addVolumeAndRefreshDataTree_new(targetLabel,
                                                                ('Volumes',
                                                                 target + 'Label'))

                    truePositiveRates = []
                    falsePositiveRates = []

                    for i in range(0, 20, 1):

                        threshold = i / 20.0
                        print "target:", target
                        print "threshold:", threshold

                        b = borderWidthForFeatures

                        accuracy = Accuracy(targetLabel[b[0]:-b[0], b[1]:-b[1], b[2]:-b[2]],
                                            (resultVolume[b[0]:-b[0], b[1]:-b[1], b[2]:-b[2]]
                                             > threshold))
                        accuracy.printAccuracy()

                        truePositiveRates.append(accuracy.truePositiveRate())
                        falsePositiveRates.append(accuracy.falsePositiveRate())


                    pyplot.plot(falsePositiveRates, truePositiveRates)
                    pyplot.axis([0, 0.3, 0.7, 1])
                    pyplot.title(target)
                    pyplot.xlabel('False Positive Rate')
                    pyplot.ylabel('True Positive Rate')
                    pyplot.grid(True)

                except NodeDoesNotExist:

                    warnings.warn("Subcellular component node %s does not exist." %
                                  target)

            pyplot.show()


    def calculateFinalAccuracyWithManualCorrection(self):

        if self.fullManualSegFilePath == None:
            raise Exception,\
                "fullManualSegFilePath is None, no actual segmentation specified"

        resultVolume = loadImageStack("O:\images\HPFcere_vol\HPF_rotated_tif\output\cleaned with seg3d",
                                      None,
                                      maxNumberOfImages=self.numberOfLayersToProcess)
        self.dataViewer.addVolumeAndRefreshDataTree_new(resultVolume,
                                                        self.fullManualSegNodePath)

        fullManualSegVolume = loadImageStack(self.fullManualSegFilePath,
                                             None,
                                             maxNumberOfImages=self.numberOfLayersToProcess)
        self.dataViewer.addVolumeAndRefreshDataTree_new(fullManualSegVolume,
                                                        self.fullManualSegNodePath)

        #print resultVolume[10, 10, 10]

        accuracy = Accuracy(fullManualSegVolume, resultVolume)
        accuracy.printAccuracy()


    def runInitialize(self):

        #defaultStepNumber = 4
        #self.target = 'mitochondria'
        #self.target = 'blankInnerCell'
        #self.target = 'vesicles'
        #numberOfContoursToDisplay = None
#        self.displayParametersDict = {}
#        self.displayParametersDict['mitochondria'] = ContourAndBlobDisplayParameters()
#        self.displayParametersDict['mitochondria'].numberOfContoursToDisplay = None #20
#        self.displayParametersDict['mitochondria'].contourProbabilityThreshold = 0.08
#        self.displayParametersDict['blankInnerCell'] = ContourAndBlobDisplayParameters()
#        self.displayParametersDict['blankInnerCell'].numberOfContoursToDisplay = 20
#        self.displayParametersDict['blankInnerCell'].contourProbabilityThreshold = 0 #0.1
#        self.displayParametersDict['vesicles'] = ContourAndBlobDisplayParameters()
#        self.displayParametersDict['vesicles'].numberOfContoursToDisplay = 5 #500 #5 #20
#        self.displayParametersDict['vesicles'].contourSegmentTubeRadius = 0.1
#        self.displayParametersDict['vesicles'].contourCenterMarkerSize = 0.5
#        self.displayParametersDict['vesicles'].contourProbabilityThreshold = 0.15
#        
#        self.probabilityFunctionDict = {}
#        self.probabilityFunctionDict['mitochondria'] = mitochondriaProbability
#        self.probabilityFunctionDict['vesicles'] = vesicleProbability
#        self.probabilityFunctionDict['blankInnerCell'] = blankInnerCellProbability
#        self.pathLength = {}
#        self.pathLength['mitochondria'] = 3
#        self.pathLength['vesicles'] = 1
#        self.pathLength['blankInnerCell'] = 1
#        self.enable3DPlot = False
#        #numberOfLayersToProcess = 7
#
#        self.minVoxelLabelValue['mitochondria'] = 1
#        self.maxVoxelLabelValue['mitochondria'] = None
#        self.minVoxelLabelValue['blankInnerCell'] = 1
#        self.maxVoxelLabelValue['blankInnerCell'] = None
#        self.minVoxelLabelValue['vesicles'] = 1
#        self.maxVoxelLabelValue['vesicles'] = None

        #if len(sys.argv) < 2:
        #    print "step not specified, using default step", defaultStepNumber
        #    stepNumber = defaultStepNumber
        #else:
        #    stepNumber = int(sys.argv[1])    
        
        #print "running step number", stepNumber
        
        #self.app = wx.PySimpleApp()
        #self.dataViewer = ClassificationControlsFrame(makeClassifyGUITree())
        #self.dataViewer.Show()
        
        #contoursNodeName = target + 'Contours'
        #self.groupedContoursNodeName = self.target + 'ContoursGroupedByImage'
        self.highProbabilityContoursNodeName = self.target + 'HighProbabilityContours'
    
        if self.target == 'mitochondria':
            self.fastMarchInputVolumeName = self.currentVoxelClassificationResultPath()[1]
        elif self.target == 'vesicles':
            self.fastMarchInputVolumeName = self.originalVolumeName
        else: print "find_3d_blobs target error"


    def runPersistentLoadOriginalImage(self):

        originalImageNodePath = ('Volumes', 'originalImage')

        originalImage = loadImageStack(self.originalImageFilePath, self.regionToClassify)

        originalImage = originalImage[:, :, 0:self.numberOfLayersToProcess]

        self.dataViewer.addVolumeAndRefreshDataTree(originalImage, originalImageNodePath[1])

        self.dataViewer.addPersistentVolumeAndRefreshDataTree(originalImage,
                                                         self.originalVolumeName)


    def runPersistentLoadTrainingData(self):

        voxelTrainingImageNodePath = ('Volumes', 'voxelTrainingImage')
        voxelTrainingLabelNodePath = ('Volumes', 'voxelTrainingLabel')

        # load training images
        self.dataViewer.addVolumeAndRefreshDataTree_new(
            loadImageStack(self.voxelTrainingImageFilePath,
                           self.trainingRegion,
                           maxNumberOfImages=self.numberOfTrainingLayersToProcess),
                           voxelTrainingImageNodePath)

        # load training labels
        labelVolume = loadImageStack(self.voxelTrainingLabelFilePath,
                            self.trainingRegion,
                            maxNumberOfImages=self.numberOfTrainingLayersToProcess)

        self.dataViewer.addVolumeAndRefreshDataTree_new(labelVolume,
                                                voxelTrainingLabelNodePath)


    def runPreclassificationFilter(self):

            self.preclassificationFilter(self.dataViewer,
                                numberOfLayersToProcess=self.numberOfLayersToProcess)


    def runClassifyVoxels(self):

        self.classifyVoxels(self.dataViewer,
                            #self.labelIdentifierDict[self.target],
                            numberOfLayersToProcess=self.numberOfLayersToProcess)


    def runWriteVoxelClassificationResult(self):

            #log.info("runWriteVoxelClassificationResult")
            print "runWriteVoxelClassificationResult"

            # write classification result to a stack of tiffs
    
            #volume = self.dataViewer.getPersistentObject(
            #    list(self.voxelClassificationResultPath).append('0'))
            resultsNode = self.dataViewer.mainDoc.dataTree.getSubtree(
                            self.currentVoxelClassificationResultPath())
            self.dataViewer.refreshTreeControls()

            for childNode in resultsNode.children:
                volume = childNode.object
                path = os.path.join(self.blobImageStackOutputFolder, childNode.name)
                if not(os.path.exists(path)):
                    os.mkdir(path)
                b = borderWidthForFeatures
                if self.regionToClassify == None:
                    writeTiffStack(path, volume * 255.0)
                else:
                    writeTiffStack(path,
                                volume[b[0]:-b[0], b[1]:-b[1], b[2]:-b[2]] * 255.0,
                                startIndex=self.regionToClassify.cornerA[2]+b[2])

                inputVolume = self.dataViewer.getPersistentVolume_old(
                    self.voxelClassificationInputVolumeName)
                compositeImagePath = os.path.join(path, "composite")
                if not(os.path.exists(compositeImagePath)):
                    os.mkdir(compositeImagePath)
                if self.regionToClassify == None:
                    writeTiffStackRGB(compositeImagePath,
                                   volume * 255.0,
                                   volume * 255.0,
                                   inputVolume)
                else:
                    writeTiffStackRGB(compositeImagePath,
                            volume[b[0]:-b[0], b[1]:-b[1], b[2]:-b[2]] * 255.0,
                            volume[b[0]:-b[0], b[1]:-b[1], b[2]:-b[2]] * 255.0,
                            inputVolume[b[0]:-b[0], b[1]:-b[1], b[2]:-b[2]])



    def runFindContours(self):

            #testContours()

            self.dataViewer.mainDoc.dataRootNode.addChild(GroupNode(self.contoursNodeName))

            for thresholdIndex in range(self.numberOfThresholds):

                self.findContours("thresholdIndex_%d" % thresholdIndex,
                    self.firstThreshold + (self.thresholdStep * thresholdIndex),
                    self.numberOfLayersToProcess)

            self.dataViewer.mainDoc.dataTree.writeSubtree(self.contoursNodePath)
            #self.dataViewer.mainDoc.dataTree.writeSubtree(('Contours', 'thresholdIndex_3'))


    def runMakeContourLists(self):

            self.makeContourLists(
                self.displayParametersDict[self.target].contourProbabilityThreshold,
                self.pathLength[self.target])


#    def runMainLoop(self):
#
#        print "running main gui loop"
#
#        self.app.MainLoop()


    def runWriteContoursToImageStack(self):

        self.writeContoursToImageStack(self.contoursNodePath)


    def loadOriginalVolume(self):

        self.dataViewer.getPersistentVolume_old(self.originalVolumeName)


    def loadVoxelClassificationResult(self):

        self.dataViewer.getPersistentVolume_old(
                                self.currentVoxelClassificationResultPath()[1])


    def loadItemsForViewing(self):

        # load items for viewing and diagnostics
        self.dataViewer.getPersistentVolume_old(self.originalVolumeName)
        self.dataViewer.getPersistentVolume_old(
                                self.currentVoxelClassificationResultPath()[1])
        contoursGroupedByImage = self.dataViewer.mainDoc.dataTree.getSubtree(
                                  (self.contoursNodeName,))
        updateContourProbabilities(contoursGroupedByImage,
                                   self.probabilityFunctionDict[self.target])
        #self.dataViewer.mainDoc.dataTree.getSubtree(self.contoursNodePath)

        # load contour paths for processing
        self.dataViewer.mainDoc.dataTree.getSubtree(self.contourPathsNodePath)

        if self.contourListClassificationMethod == 'randomForest':
            classifyContourLists(self.dataViewer,
                    inputTrainingExamplesIdentifier=\
                        self.contourListTrainingExamplesIdentifier,
                    contourListsNodePath=self.contourPathsNodePath)
        elif self.contourListClassificationMethod == 'bayes':
            classifyContourListsNodePathBayes(self.dataViewer,
                    self.probabilityFunctionDict[self.target],
                    contourListsNodePath=self.contourPathsNodePath)
        else:
            raise Exception, "invalid classification method"

        self.dataViewer.refreshTreeControls()


    def saveContourPathsToJinxFile(self):

        # save contour paths to Jinx file

        saveBlobsToJinxFile(self.dataViewer.mainDoc.dataTree.getSubtree(
                                                        self.contourPathsNodePath),
                            self.target + "_contours")


    def run3DShellActiveContourToDetect3DBlobs(self):

        # perform 3D shell active contour to detect 3D blobs

        fillAndDisplayResults(self.dataViewer, self.fastMarchInputVolumeName,
                                   self.contourPathsNodePath[0],
                                   self.displayParametersDict[self.target],
                                   self.enable3DPlot,
                                   fillMethod='shellActiveContour')


    def run3DShellActiveContourToDetect3DBlobsHighProbabilityOnly(self):

            # perform 3D shell active contour to detect 3D blobs
    
            if self.enable3DPlot:
                display3DContours(self.dataViewer, self.originalVolumeName, self.highProbabilityContoursNodeName,
                                    self.displayParametersDict[self.target])
    
            fillAndDisplayResults(self.dataViewer, self.fastMarchInputVolumeName,
                                       self.highProbabilityContoursNodeName,
                                       self.displayParametersDict[self.target],
                                       self.enable3DPlot,
                                       fillMethod='shellActiveContour')


    def runContourProbabilityFilter(self):

            # - calculate probabilities
            # - filter (threshold) contours by probability
            # - add a node for the high probability contours

            allContoursNode =\
                self.dataViewer.mainDoc.dataTree.getSubtree((self.contoursNodeName,))
            #allContours = allContoursNode.makeChildrenObjectList()
            #highProbabilityContoursNode = DataNode(highProbabilityContoursNodeName, 'contours node type', {}, None)
            #highProbabilityContoursNode.addObjectList(highProbabilityContours(allContours, displayParametersDict[target].contourProbabilityThreshold))
            #highProbabilityContoursNode.enableRecursiveRendering = False

            updateContourProbabilities(allContoursNode,
                                       self.probabilityFunctionDict[self.target])

            #todo: this should filter the tree not just copy it
            threshold = self.displayParametersDict[self.target].contourProbabilityThreshold
            highProbabilityContoursNode = copyTree(allContoursNode,
                                                   ProbabilityFilter(threshold))
            #highProbabilityContoursNode = copyTree(allContoursNode)
            highProbabilityContoursNode.name = self.highProbabilityContoursNodeName
 
            self.dataViewer.addPersistentSubtreeAndRefreshDataTree((), highProbabilityContoursNode)
            self.dataViewer.getPersistentVolume_old(self.originalVolumeName)
            self.dataViewer.refreshTreeControls()

            print self.highProbabilityContoursNodeName
            saveBlobsToJinxFile(self.dataViewer.mainDoc.dataTree.getSubtree(
                                                (self.highProbabilityContoursNodeName,)),
                                                self.highProbabilityContoursBaseFilename)

            # write contours to an image stack for viewing
            self.writeContoursToImageStack((self.highProbabilityContoursNodeName,))


    def runWrite3DBlobsVolume(self):

            # write 3D blobs to a stack of tiffs
    
            allBlobs = self.dataViewer.getPersistentVolume_old(self.fastMarchInputVolumeName + 'AllFastMarchBlobs')
            self.dataViewer.refreshTreeControls()
            writeTiffStack(self.blobImageStackOutputFolder, (allBlobs > 0) * 255.0)


    def runGroupContoursByConnectedComponents(self):
            
            contoursGroupedByImage = self.dataViewer.mainDoc.dataTree.getSubtree(
                                      (self.contoursNodeName,))
            updateContourProbabilities(contoursGroupedByImage,
                                       self.probabilityFunctionDict[self.target])
            connectedComponents, graph =\
                self.groupContoursByConnectedComponents(contoursGroupedByImage)
            
            #count = 0
            s = 1.0
            v = 1.0
            
            print connectedComponents
            
            for nodeNameKey in connectedComponents:
                #nodeName = connectedComponents[key]
                attributes = graph.node_attributes(nodeNameKey)
                contourNode = attributes[0]
                #h = 0.05 * count
                h = 0.05 * connectedComponents[nodeNameKey]
                print contourNode.object.color()
                print "h", h, "s", s, "v", v
                h = remainder(h, 1.0)
                contourNode.object.setColor(255.0 * array(colorsys.hsv_to_rgb(h, s, v)))
                #contourNode.object.setColor((200, 200, 200))
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


    def runStep(self, stepNumber):
        

        print "running step number", stepNumber
        self.runInitialize()
        

        if stepNumber == 0:

            self.runPreclassificationFilter()


        elif stepNumber == 1:

            self.runClassifyVoxels()


        elif stepNumber == 2:

            self.dataViewer.getPersistentVolume_old(
                                    self.currentVoxelClassificationResultPath()[1])


        # find contours
        elif stepNumber == 3:

            self.runFindContours()


        elif stepNumber == 4:

            self.dataViewer.getPersistentVolume_old(self.originalVolumeName)
            self.computeContourRegions()


        elif stepNumber == 5:

            self.writeContoursToImageStack(self.contoursNodePath)


        elif stepNumber == 6:

            self.dataViewer.getPersistentVolume_old(self.originalVolumeName)

            saveBlobsToJinxFile(
                self.dataViewer.mainDoc.dataTree.getSubtree(self.contoursNodePath))

            self.dataViewer.refreshTreeControls()


        elif stepNumber == 7:
            
            self.runMakeContourLists()


        elif stepNumber == 8:

            saveBlobsToJinxFile(
                self.dataViewer.mainDoc.dataTree.getSubtree(self.contourPathsNodePath))


#        elif stepNumber == 8:
#
#            self.calculateContourListFeatures()


        elif stepNumber == 9:

            self.calculateContourListFeatures()
            recordFeaturesOfContourLists(self.dataViewer,
                            inputTrainingContourListsNodePath=self.contourPathsNodePath,
                            outputExamplesIdentifier=self.contourListExamplesIdentifier)
            self.dataViewer.getPersistentVolume_old(self.originalVolumeName)

            if self.labelFilePaths != None:
                for labelName in self.labelFilePaths.keys():
                    self.dataViewer.getPersistentVolume_old(labelName)

            self.dataViewer.refreshTreeControls()


        elif stepNumber == 10:
            
            self.loadItemsForViewing()


        elif stepNumber == 11:

            self.saveContourPathsToJinxFile()


        elif stepNumber == 12:
    
            self.run3DShellActiveContourToDetect3DBlobs()


        elif stepNumber == 106:

            self.runContourProbabilityFilter()
    
        
        elif stepNumber == 107:

            self.runGroupContoursByConnectedComponents()


        elif stepNumber == 108:
    
            # use GUI to display high probability contours
    
            if self.enable3DPlot: display3DContours(self.dataViewer, self.originalVolumeName, self.highProbabilityContoursNodeName,
                                                self.displayParametersDict[self.target])
            self.dataViewer.mainDoc.dataTree.getSubtree((self.highProbabilityContoursNodeName,))
            self.dataViewer.refreshTreeControls()
    
    
        elif stepNumber == 109:
    
            self.run3DShellActiveContourToDetect3DBlobsHighProbabilityOnly()
    

        elif stepNumber == 110:
    
            # write 3D blobs to an XML file and into a stack of tiffs for viewing
    
            self.dataViewer.mainDoc.dataTree.readSubtree(('Blobs',))
            saveBlobsToJinxFile(self.dataViewer.mainDoc.dataTree.getSubtree(('Blobs',)))
            original = self.dataViewer.getPersistentVolume_old(self.originalVolumeName)
            allBlobs = self.dataViewer.getPersistentVolume_old(self.fastMarchInputVolumeName + 'AllFastMarchBlobs')
            self.dataViewer.refreshTreeControls()
            writeTiffStackRGB(defaultOutputPath,
                              #redVolume=rescale(allBlobs, 0, 255.0),
                              redVolume = (allBlobs > 0) * 255.0,
                              greenVolume=original,
                              blueVolume=None)
            writeTiffStack(os.path.join(defaultOutputPath, "blobVolume"),
                           (allBlobs > 0) * 255.0)
    
    
        print "finished step"
        self.runMainLoop()


    def runVoxelTestSteps(self):

        self.runStep(0)
        self.runStep(1)


    def runContourTestSteps(self):

        ##self.runStep(3)
        self.runStep(7)
        self.runStep(9)
        #self.runStep(10)
        self.runStep(106)


