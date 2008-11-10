#Copyright (c) 2008 Richard Giuly
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



#import ImageTk

#import Numeric
#blur image some
#you could have the current value comparted to the average value to see if you are on a light or dark spot
#set up just a simple gradient test image

#http://www.pygame.org/docs/tut/intro/intro.html 
from numpy import *
import numpy
import sys
#import pygame
#from Tkinter import *
#import Tkinter
import Image            #PIL
import wx

#from pygame.locals import *
#from pgu import gui

#from mlabwrap import mlab

import pickle

import copy


#if len(sys.argv) <= 1:
# from visual.graph import * # import graphing features

import os

import imod_tools

import geometry

#import cytoseg_util


global settings
settings = {}

from socket import gethostname; hostname = gethostname()
if hostname == "panther":
        import orange, orngTree, orngEnsemble
        #defaultPath = "O:\\images\\LFong\\cropped\\8bit_smaller\\"
        #defaultPath = "O:\\images\\LFong\\tif_8bit_partial\\"
        #defaultPath = "O:\\images\\LFong\\tif_8bit_partial\\"
        #defaultPath = "O:\\images\\LFong\\tif_8bit_20_images\\"
        defaultPath = "O:\\images\\LFong\\tif_8bit_10_images\\"
        #defaultPath = "O:\\images\\denk\\smallcube2\\"
        #defaultPath = "O:\\images\\denk\\smallcube_region2\\"
        #defaultPath = "O:\\images\\denk\\70x70x70_cube\\"
        #defaultPath = "O:\\images\\LFong\\one_file\\8bit\\"
        defaultOutputPath = "O:\\temp\\output\\" 
else:
        #defaultPath = "/crbsdata1/rgiuly/input/cb017_NA1000_set2/cropped204x150/"
        defaultPath = "/crbsdata1/rgiuly/input/triple_tilt/cb024/tifs_small/"
        defaultOutputPath = "/tmp/"
 
from UserDict import UserDict

# from http://code.activestate.com/recipes
class odict(UserDict):
    def __init__(self, dict = None):
        self._keys = []
        UserDict.__init__(self, dict)

    def __delitem__(self, key):
        UserDict.__delitem__(self, key)
        self._keys.remove(key)

    def __setitem__(self, key, item):
        UserDict.__setitem__(self, key, item)
        if key not in self._keys: self._keys.append(key)

    def clear(self):
        UserDict.clear(self)
        self._keys = []

    def copy(self):
        dict = UserDict.copy(self)
        dict._keys = self._keys[:]
        return dict

    def items(self):
        return zip(self._keys, self.values())

    def keys(self):
        return self._keys

    def popitem(self):
        try:
            key = self._keys[-1]
        except IndexError:
            raise KeyError('dictionary is empty')

        val = self[key]
        del self[key]

        return (key, val)

    def setdefault(self, key, failobj = None):
        UserDict.setdefault(self, key, failobj)
        if key not in self._keys: self._keys.append(key)

    def update(self, dict):
        UserDict.update(self, dict)
        for key in dict.keys():
            if key not in self._keys: self._keys.append(key)

    def values(self):
        return map(self.get, self._keys)


 

def initialize():
    global settings
    try:
        settingsFile = open('settings.pickle')
        settings = pickle.load(settingsFile)
        print 'settings'
        print settings
    except IOError, (errno, strerror):
        print "I/O error(%s): %s while reading settings file" % (errno, strerror)
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
    
    

def setToDefaultSettings():
    settings['defaultPath'] = 'c:/'
    settings['temporaryFolder'] = 'c:/temp/'

def writeSettings():
    outputFile = open('settings.pickle', 'wb')
    print 'writing settings to settings.pickle'
    print settings
    pickle.dump(settings, outputFile)
    

def array2image(a):
    #if a.typecode() == numpy.UnsignedInt8:
    #    mode = "L"
    #elif a.typecode() == numpy.Float32:
    #    mode = "F"
    #else:
    #    raise ValueError, "unsupported image mode" 
    return Image.fromstring("F", (a.shape[1], a.shape[0]), a.tostring())




#root = Tk()
#label = Label(root, text="test")
#label.pack()

def getNode(node, nameList):
    currentNode = node
    #print 'nameList'
    #print nameList
    for name in nameList:
        #print name
        currentNode = currentNode.getChild(name)
    return currentNode
    

class Blob:
    def __init__(self,center,size):
        self.center = center
        self.size = size
        
class Box:
    def __init__(self,cornerA,cornerB):
        
        # 3D point
        self.cornerA = array(cornerA)
        
        # 3D point
        self.cornerB = array(cornerB)
        
    def shape(self):
        return array(self.cornerB) - array(self.cornerA)


# represents a piece of data, like a slider
class DataNode:
    
    
    
    def __init__(self,name,type,params,valueToSave):
        self.name = name
        self.type = type
        self.params = params
        self.valueToSave = valueToSave
        self.children = []
        self.guiComponent = None
    
    def __setstate__(self, dict):
        self.__dict__ = dict
        self.guiComponent = None
    
    
    def __getstate__(self):
        result = self.__dict__.copy()
        del result['guiComponent']
        return result
        
    def get(self):
        self.valueToSave = self.guiComponent.GetValue()  #todo: you should really always use set method so this should not be necessary 
        return self.guiComponent.GetValue()
    
    def set(self, value):
        self.valueToSave = value
        self.guiComponent.SetValue(value)

    # shows children of node
    def __str__(self):
        result = '%s (' % self.name 
        for child in self.children:
            result += child.__str__() 
        result += ')'
        return result
    
    def addChild(self,node):
        self.children.append(node)

    def addChildren(self,nodeList):
        for node in nodeList:
            self.addChild(node)
    
    def getChild(self,name):
        for child in self.children:
            if child.name == name:
                return child
        print ("error: tried to access node named %s but it wasn't there" % name)
               


    def test_old(self):
        n1 = DataNode("root","root",10)
        print 'n1 type'
        print type(n1)
        n2 = DataNode("b","boolean",20)
        n3 = DataNode("c","slider",30)
        n4 = DataNode("d","slider",40)
        n5 = DataNode("e","slider",50)

        n1.addChild(n2)
        n1.addChild(n3)
        n2.addChild(n4)
        n2.addChild(n5)
        
        print 'children types'
        for x in n1.children:
            print type(x)
        f = open("temp.pickle", "w")
        pickle.dump(n1, f)
        f.close()

        f = open("temp.pickle", "r")
        loadedData = pickle.load(f)
        print "data loaded from file"
        print loadedData
        f.close()
        
        print 'testing get node'
        print getNode(loadedData, ('particleMotionTool', 'd'))
        
        return n1




            
def testcallback(arg1):
    print "call"
#
##def setTextBox(textBox, value):
# 
def setNodeValueCallback(node, value):
    print 'set %s %s' % (node, value)
    node.value = value
    
#class MyStringVar(StringVar):
#    
#    def __getstate__(self):
#        print 'get'
#        #result = {value : 25}
#        #result = {'value' : self.get()}
#
#    def __setstate__(self,dict):
#        #self.set(dict['value'])
#        print 'set'

#class MyTextBox(Entry):

class ControlsFrame(wx.Frame, wx.EvtHandler):
    
    def __init__(self, settingsTree):
        
        self.currentSubgroupIndex = -1  
        self.totals = []     
        self.childFrames = []
        
        #wx.Frame.__init__(self, None, title="Loading Images")
        
        wx.Frame.__init__(self, None, -1, 'Cytoseg - Main Window',
                          size=(800, 800))
        
        self.Move((700,100))
        self.SetSize((400,200))
        
        self.Bind(wx.EVT_CLOSE, self.onExit)
                
        #self.panel = wx.Panel(self)
        #self.panel = wx.ScrolledWindow(self, -1)
        self.panel = wx.ScrolledWindow(self, id=-1, pos=wx.DefaultPosition,
                                       size=wx.DefaultSize, style=wx.HSCROLL | wx.VSCROLL,
                                       name="scrolledWindow")
        self.panel.SetScrollbars(1, 1, 1600, 1400)
        #self.panel.FitInside()
        fgs = wx.FlexGridSizer(cols=2, hgap=10, vgap=10)
        
        imageLabel = wx.StaticText(self.panel, -1, "Image")
        fgs.Add(imageLabel)
        
        #self.Bind(wx.EVT_PAINT, self.onPaint)
        
        
        for name in filenames:
            #img1 = wx.Image(name, wx.BITMAP_TYPE_ANY)
            #w = img1.GetWidth()
            #h = img1.GetHeight()
            #img2 = img1.Scale(w/2, h/2)
            
            height = 200
            width = 100

            array = numpy.ones( (height, width, 3),numpy.int8)
            array[:,:,0] = 200
            
            image = wx.EmptyImage(width,height)
            image.SetData(array.tostring())

            bitmap = image.ConvertToBitmap()# wx.BitmapFromImage(image)
            #bitmap.SetWidth(500)
            #bitmap.SetHeight(500)

            self.sb1 = wx.StaticBitmap(self.panel, -1, wx.BitmapFromImage(image))
            self.sb1.Bind(wx.EVT_LEFT_DOWN, self.onClickedImage)
            self.sb1.Bind(wx.EVT_MOTION, self.onMouseMotionOnImage)
            self.sb1.Bind(wx.EVT_LEFT_UP, self.onButtonUp)

            fgs.Add(self.sb1)
            #fgs.Add(self.sb2)
            
           
            
            #label1 = wx.StaticText(self.panel, -1, "text1")
            #text1 = wx.TextCtrl(self.panel, -1, "text2", size=(175, -1))
            #text1.SetInsertionPoint(0)
            #label2 = wx.StaticText(self.panel, -1, "text3")
            #text2 = wx.TextCtrl(self.panel, -1, "text4", size=(175, -1))
            
            #sizer = wx.FlexGridSizer(cols=2, hgap=6, vgap=6)
            #sizer.AddMany([basicLabel, basicText, pwdLabel, pwdText])
            #fgs.AddMany([label1, text1, label2, text2])
            #panel.SetSizer(sizer)

            #self.button = wx.Button(self.panel, -1, "Hello", pos=(50, 20))
            #self.Bind(wx.EVT_BUTTON, eval('self.OnClick'), self.button)
            #self.button.SetDefault()

            #self.panel.SetSizerAndFit(self.fgs)
            #self.Fit()

        self.settingsTree = settingsTree
 
        self.generateComponents(settingsTree, 0, [], None, None, None)
        
        
        print 'timer start controls frame'
        self.startTimer()
        
        self.makeNewSubgroup()
        
        #dc = wx.ClientDC(self)
        #dc.DrawEllipse(200,200,100,100)
        
        self.panel.SetSizer(fgs)
        #self.panel.SetSizerAndFit(self.fgs)
        #self.Fit()
        
        #self.onOpenImageStack(None)
        #self.onReadClassificationFile(None)


        self.loadedVolumeBoxInFullVolumeCoords = Box((0,0,0),self.getCurrentVolume().shape)


        self.drawingSelectionBox = False
        #self._selectionBoxInLoadedVolumeCoords = Box([0,0,0], [0,0,0])
        self.selectionBoxInFullVolumeCoords = Box([0,0,0], [0,0,0])
                
        self.derivativeHasBeenComputed = False

    #def onPaint(self, event):
        #print "onPaint"
        
        #self.beepSound = wx.Sound("beep.wav")

        self.setControlEnable(('particleMotionTool','loadPartialImageStack'), False)
        
        self.currentFilename = "untitled.cytoseg"
        
    def selectionBoxInLoadedVolumeCoords(self):
        a = self.selectionBoxInFullVolumeCoords.cornerA - self.loadedVolumeBoxInFullVolumeCoords.cornerA
        b = self.selectionBoxInFullVolumeCoords.cornerB - self.loadedVolumeBoxInFullVolumeCoords.cornerA
        
        #return Box(a,b)
        
        #return self._selectionBoxInLoadedVolumeCoords
        
        return Box(a,b)
    
    # todo: remove this function and just use the variable
    def getSelectionBoxInFullVolumeCoords(self):
        #a = self._selectionBoxInLoadedVolumeCoords.cornerA + self.loadedVolumeBoxInFullVolumeCoords.cornerA
        #b = self._selectionBoxInLoadedVolumeCoords.cornerB + self.loadedVolumeBoxInFullVolumeCoords.cornerA
        
        #return Box(a,b)
        
        return self.selectionBoxInFullVolumeCoords
        

    #def temp_setFullVolumeCoordsWithLoadedVolumeCoords(

    def makeContainerForControls(self, name):
        
        #wx.Frame.__init__(self, None, -1, 'Controls',
        #                  size=(800, 800))
        
        #frame = wx.Frame()
        #frame = wx.Frame(self, None, -1, 'Controls', size=(800, 800))
        #frame = wx.Frame(None, 1, 'Controls', size=(400, 400))
        #frame = wx.Frame(self, 1, name, size=(400, 400))
        frame = wx.Frame(self, 1, name, size=(600, 800))

        panel = wx.ScrolledWindow(frame, id=-1, pos=wx.DefaultPosition,
                                       size=wx.DefaultSize, style=wx.HSCROLL | wx.VSCROLL,
                                       name="scrolledWindow")
        panel.SetScrollbars(1, 1, 1600, 1400)
        
        
        menuBar = wx.MenuBar()
        menu = wx.Menu()
        menuBar.Append(menu, "File")
        frame.SetMenuBar(menuBar)
        
        
        flexGridSizerContainer = wx.FlexGridSizer(cols=2, hgap=10, vgap=10)
        
        panel.SetSizer(flexGridSizerContainer)
        frame.Show()
        
        
        #frame.Bind(wx.EVT_CLOSE, self.onCloseChildFrame)
        
        self.childFrames.append(frame)

        return flexGridSizerContainer, panel, frame
    

    
    # in coordinates of the volume that is loaded into memory, which may by a subvolume of the full volumetric image
    #def selectedBoxCornersInLoadedVolumeCoordinates(self):
    #    box = self.cornersOf3DWindow()
    #    
    #    a = numpy.array(self.selectionBoxInLoadedVolumeCoords.cornerA)
    #    a[0] += box.cornerA[0]
    #    a[1] += box.cornerA[1]
    #    
    #    b = numpy.array(self.selectionBoxInLoadedVolumeCoords.cornerB)
    #    b[0] += box.cornerA[0]
    #    b[1] += box.cornerA[1]
    #    
    #    return Box(a, b)
    
 #   def selectedBoxCornersInFullVolumeCoordinates(self):
 #       box = self.selectedBoxCornersInLoadedVolumeCoordinates()
 #       return Box(box.cornerA + self.loadedVolumeBox.cornerA, box.cornerA + self.loadedVolumeBox.cornerB)  


    def makeSelectedVolume(self):
        box = self.selectionBoxInLoadedVolumeCoords()
        a = box.cornerA
        b = box.cornerB
        return self.getCurrentVolume()[a[0]:b[0],a[1]:b[1],a[2]:b[2]]

    #def onCloseChildFrame(self, event):
    #    print "child frame close"
    #    #self.Close(True)
        
    def onSaveVolumes(self, event):
        f = open("c:\\temp\\volumes.pickle", "wb")
        pickle.dump(volumes, f)
        f.close()
    
    def onOpenVolumes(self, event):
        global volumes
        f = open("c:\\temp\\volumes.pickle")
        volumes = pickle.load(f)
        f.close()
        
        keyList = []
        for item in volumes.items():
            keyList.append(item[0])

        # update the settings tree and the list box so it shows all variable names
        node = getNode(self.settingsTree, ('particleMotionTool','visibleVolume'))
        node.params['items'] = keyList
        listBox = node.guiComponent
        listBox.Set(keyList)
        
        listBox.SetSelection(node.valueToSave)

        

    def readIMODFile(self, event):
        #contours = imod_tools.getAllContours('O:\\images\\denk\\70x70x70_cube\\membrane.imod');
        #contours = imod_tools.getAllContours('O:\\images\\LFong\\Lisa_images_small\\test.imod');
        contours = imod_tools.getAllContours('O:\\images\\denk\\smallcube2\\membrane.imod');

        yMax = self.getCurrentVolume().shape[1]
        count = 0
        
        for contour in contours:
            particleGroup.addEmptySubgroup()
            for imodPoint in contour:
                point = array([imodPoint[0], yMax - imodPoint[1], imodPoint[2]])
                p = makeParticle(point)
                #print p.loc
                particleGroup.addToSubgroup(count, p)
            count = count + 1
         



    
    
    def addVolume(self, volume, name):
        volumes[name] = volume
        node = getNode(self.settingsTree, ('particleMotionTool','visibleVolume'))
        node.params['items'].insert(0, name)
        listBox = node.guiComponent
        listBox.InsertItems([name],0)  # todo: regenerate the whole list based on the entries in the volumes dictionary
        
    #def getGUIComponent(self, nameList):
    #    node = getNode(self.settingsTree, nameList)
    #    return node.guiComponent

    def setValue(self, nameList, value):
        node = getNode(self.settingsTree, nameList)
        node.set(value)

    def getValue(self, nameList):
        node = getNode(self.settingsTree, nameList)
        return node.get()

    
    def setControlEnable(self, nameList, booleanValue):
        node = getNode(self.settingsTree, nameList)
        node.guiComponent.Enable(booleanValue)



    def getSliderMin(self, settingsTree, nodeIdentifier):
        slider = getNode(settingsTree, nodeIdentifier).guiComponent
        return slider.GetMin()

    def getSliderMax(self, settingsTree, nodeIdentifier):
        slider = getNode(settingsTree, nodeIdentifier).guiComponent
        return slider.GetMax()   

        

    def setSliderMin(self, settingsTree, nodeIdentifier, value):
        slider = getNode(settingsTree, nodeIdentifier).guiComponent
        slider.SetRange(value, slider.GetMax())
                

    def setSliderMax(self, settingsTree, nodeIdentifier, value):
        slider = getNode(settingsTree, nodeIdentifier).guiComponent
        slider.SetRange(slider.GetMin(), value)    

    
    
    def automaticProcessButton(self, event):
        filename = 'output.cytoseg'
        print filename
        #pathToImages = old_gui.imageStackPathText.get()
        pathToImages = (getNode(self.settingsTree, ('particleMotionTool','imageStackPath'))).get() 

        #cornerA, cornerB = self.cornersOf3DWindow()
        #offset = self.selectionRectangleCornerA + cornerA
        
        box = self.selectionBoxInLoadedVolumeCoords()
        offset = box.cornerA

    
        doc = automaticProcess(self.getCurrentVolumeForProcessing(), 
                               pathToImages, # todo: is this path to images needed
                               (getNode(self.settingsTree, ('particleMotionTool','grayThreshold'))).get(),
                               (getNode(self.settingsTree, ('particleMotionTool','minimumBlobSize'))).get(),
                               (getNode(self.settingsTree, ('particleMotionTool','maximumBlobSize'))).get(),
                               (getNode(self.settingsTree, ('particleMotionTool','automaticProcess','useSubgroups'))).get(),
                               offset) 
    
        # todo: make one global object, the current document, or maybe all this stuff should be contained in a class that holds the application, then it would be a document object in the application object
        global blobs
        global particleGroup
        global edges
        blobs = doc.blobs
     
        particleGroup = doc.particleGroup
        
        
        edges = doc.edges
        
        writeDocument(doc, filename)
        
        #self.beepSound.Play()
        



    def onMarkBlobs(self, event):
        filename = 'output.cytoseg'
        print filename
        #pathToImages = old_gui.imageStackPathText.get()
        pathToImages = (getNode(self.settingsTree, ('particleMotionTool','imageStackPath'))).get() 

        #cornerA, cornerB = self.cornersOf3DWindow()
        #offset = self.selectionRectangleCornerA + cornerA
        
        box = self.selectionBoxInLoadedVolumeCoords()
        offset = box.cornerA

    
        doc = automaticProcess(self.getCurrentVolumeForProcessing(), 
                               pathToImages,  # todo: is this path to images needed
                               (getNode(self.settingsTree, ('particleMotionTool','grayThreshold'))).get(),
                               (getNode(self.settingsTree, ('particleMotionTool','minimumBlobSize'))).get(),
                               (getNode(self.settingsTree, ('particleMotionTool','maximumBlobSize'))).get(),
                               (getNode(self.settingsTree, ('particleMotionTool','automaticProcess','useSubgroups'))).get(),
                               offset) 
    
        # todo: make one global object, the current document, or maybe all this stuff should be contained in a class that holds the application, then it would be a document object in the application object
        global blobs
        global particleGroup
        global edges
        
        blobs = doc.blobs
        particleGroup.addSubgroup(doc.particleGroup.getAll())
        edges = doc.edges
        
        writeDocument(doc, filename)
        
        #self.beepSound.Play()

    def onUndoMarkBlobs(self, event):
        particleGroup.getSubgroups().pop()


        
    def findBlobsThenParticleMovement(self, event):
        global particleGroup
        global blobs
        
        v = self.getCurrentVolumeForProcessing()
        
        blobs = findBlobs(v, (getNode(self.settingsTree, ('particleMotionTool','grayThreshold'))).get())

        #cornerA, cornerB = self.cornersOf3DWindow()
        #offset = self.selectionRectangleCornerA + cornerA
        
        box = self.selectedBoxCornersInLoadedVolumeCoordinates()
        offset = box.cornerA
        
        moveBlobs(blobs, offset)
        
        particleGroup = generateParticleGroupFromBlobs(blobs)
        print particleGroup
        for i in range(0,(getNode(self.settingsTree, ('particleMotionTool','iterationsOfParticleMovement'))).get()):
            total = updateParticlePositions(self.getCurrentVolume(), self.settingsTree)
            print i
            print total
            filename = (getNode(self.settingsTree, ('particleMotionTool','tempPath'))).get() + 'temporary%d.psi' % i
            print "wrote to %s" % filename
            saveParticlesToPSI(filename, self.scaleFactorsFromGUI())
            
        self.drawParticlesInVolumeButton(None)
        
        
            
        
        
    def old_loadBlobsAndParticlesAndEdges(self, event):
        
        
        ###f = open('%s.pointList' % form['saveToTextBox'].value)
        f = open('%s.pointList' % 'output')
    
        pointList = pickle.load(f)
        f.close()
        
        # todo make these part of a global document and don't have individual global variables for blobs, particles, edges
        global blobs
        global particles
        global edges
        
        f = open('%s.blobs' % 'output')
        blobs = pickle.load(f)
        f.close()
        
        particles = []
        for point in pointList:
            particles.append(makeParticle(point))
        
        print particles
        
        ###f = open('%s.edges' % form['saveToTextBox'].value)
        f = open('%s.edges' % 'output')
    
        edges = pickle.load(f)
        f.close()

#    def onLoadBlobsAndParticlesAndEdges(self, event):
#        loadBlobsAndParticlesAndEdges('output.pointList')

    def onLoadBlobsAndParticlesAndEdges(self, event):
        loadBlobsAndParticlesAndEdges('output.cytoseg')
                
    
    def display3D(self, event):
        for particle in particleGroup.getAll():
            location = particle.loc
            #box(pos=(location[0],location[1],location[2]), length=10, height=10, width=10)
            sphere(pos=location, radius=5)
        for edge in edges:
            print edge
            curve(pos=[particles[edge.node1].loc,particles[edge.node2].loc],radius=1,color=(200,0,0))
      
    
    def drawParticlesInVolumeButton(self, event):
        #global volume
        global particleGroup
     
        # NOTE: for some reason this causes segfaults to occur later in the program when the array is accessed, i think introducing this new large array causes the problem
        #red = zeros(volume.shape)
        #drawParticlesInVolume(red, particles)
        
        # todo: this shouldn't change the volume, but i have it here temporarily to display results
        drawParticlesInVolume(self.getCurrentVolume(), particleGroup.getAll(), settingsTree)
        
        #writeTiffStack(old_gui.saveImageStackPathText.get(), volume) 
        writeTiffStack((getNode(self.settingsTree, ('particleMotionTool','tempPath'))).get(), self.getCurrentVolume())
        
        
    def scaleFactorsFromGUI(self):
        #return (double(self.scaleFactor.get())/100.0,double(self.scaleFactor.get())/100.0,1.0)
        return (1,1,1)
        
    def saveParticlesToPSIButton(self, event):
        filename = "output.psi"
        saveParticlesToPSI(filename, self.scaleFactorsFromGUI())
        
    def plotBlobSizesButton(self, event):
        plotBlobSizes(blobs)
        
    def copyCurrentToTemporary(self, event):
        volumes['Temporary'] = copy.deepcopy(self.getCurrentVolume())
        
    def watershedOnTemporary(self,event):
        volumes['Temporary'] = watershed(volumes['Temporary'],26)
                            
    def startTimer(self):
        #self.t1 = wx.Timer(timerHandlerTest, id=1)
        ##self.t1.Start(200)
        #print "timerHandlerTest.Bind(wx.EVT_TIMER, timerHandlerTest.onTimerEvent, id=1)"
        #timerHandlerTest.Bind(wx.EVT_TIMER, timerHandlerTest.onTimerEvent, id=1)
        #self.t1.Start(1)
        
        self.t1 = wx.Timer(self, id=1)
        self.Bind(wx.EVT_TIMER, self.onTimerEvent, id=1)
        self.t1.Start(50)
        
        
    def onTimerEvent(self, evt):
        #print 'timer controls frame'
        threshold = None
        
        if (getNode(self.settingsTree, ('particleMotionTool','thresholdEnabled'))).get():
            threshold = (getNode(self.settingsTree, ('particleMotionTool','grayThreshold'))).get();
        
        
        #self.drawViews(volume, (1,1,1), threshold)
        if (getNode(self.settingsTree, ('particleMotionTool','moveParticlesAlongGradient'))).get():  
        
            total = updateParticlePositions(self.getCurrentVolume(), settingsTree, self.loadedVolumeBoxInFullVolumeCoords.cornerA)
            
            self.totals.append(total);
            if len(self.totals) > 100:
                self.totals.pop(0)
            
            if 0:
                sum = 0
                for i in range(0, len(self.totals)):
                    sum += self.totals[i]
                average = sum / len(self.totals)
            
                #print "average %f, current total %f" % (average, total)
        
        if (getNode(self.settingsTree, ('particleMotionTool','visualsEnabled'))).get():
            self.drawViews(self.getCurrentVolume(), threshold)
        
        global globalCount
        #print globalCount
        globalCount += 1
        

    #def OnClick(self, event):
    #            self.button.SetLabel("Clicked")

    def getCurrentVolume(self):
        #print getNode(self.settingsTree, ('particleMotionTool','visibleVolume')).guiComponent.GetSelections()
        node = getNode(self.settingsTree, ('particleMotionTool','visibleVolume'))
        listBox = node.guiComponent
        selectionList = listBox.GetSelections()
        itemNumber = selectionList[0]
        itemString = node.params['items'][itemNumber]
        #return volumes['Original']
        #print itemString
        return volumes[itemString]
    
    # todo: change name to get selected volume
    def getCurrentVolumeForProcessing(self):
        if (getNode(self.settingsTree, ('particleMotionTool','processSelectionOnly'))).get():
            return self.makeSelectedVolume()
        else:
            return self.getCurrentVolume()
    
    
    def writeExample(self, file, dictionary, classification):
        for item in dictionary.items():
            value = item[1]
            file.write("%f\t" % value)
                        
        #file.write("%s" % particleGroup.containsIntegerPoint((x,y,z)))
        file.write("%s" % classification)
        file.write("\n")
        
    
    def onMakeTabFile(self, event):
#        print ""
#        v = getCurrentVolume()
#        sh = v.shape
#        for x in range(0, sh[0]):
#            for y in range(0, sh[1]):
#                for z in range(0, sh[2]):
#                    v[x,y,z]



        file = open("c:\\temp\\output.tab", "w")
        
        volume = numpy.zeros(volumes['Original'].shape)
        #selected x, y, and z

        sh = volumes['Original'].shape
      
        
        dictionary = getFeaturesAt(self.getCurrentVolume(), [3,3,3])
        for item in dictionary.items():
                key = item[0]
                file.write("%s\t" % key)
        file.write("is_membrane\n")

        for item in dictionary.items():
                file.write("c\t")
        file.write("discrete\n")

        for item in dictionary.items():
                file.write("\t")
        file.write("class\n")

        # create a volume that has pixels turned on where the membrane is
        m = zeros(sh, numpy.uint8)
        for p in particleGroup.getAll():
            m[p.loc[0],p.loc[1],p.loc[2]] = 1
            
            # write all true examples into tab file
            d = getFeaturesAt(self.getCurrentVolume(), p.loc)
            self.writeExample(file, d, True)
            
            
        self.addVolume(m, 'membranePixel')

        
        
        for x in range(0,sh[0],2):
            print "%d out of %d" % (x, sh[0])
            for y in range(0,sh[1],2):
                for z in range(0,sh[2],2):
                    
                    d = getFeaturesAt(self.getCurrentVolume(), (x,y,z))
                    
                    #xG = volumes['xGradient'][x,y,z]
                    #yG = volumes['yGradient'][x,y,z]
                    #zG = volumes['zGradient'][x,y,z]
        
                    #st = structureTensor(xG,yG,zG)
                    #eigenValues = numpy.linalg.eigvals(st)
                    
                    self.writeExample(file, d, (volumes['membranePixel'][x,y,z] != 0))

                    
        
        file.close()







    def onLearnFeaturesOfMembranePixels(self, event):
        self.onLoadImageStack(None)
        self.derivative(None)
        self.readIMODFile(None)
        self.onMakeTabFile(None)


    #def onReadClassificationFile(self, event):
    def onClassifyPixelsOfCurrentImage(self, event):
        self.derivative(None)

        #data = orange.ExampleTable("Copy of voting2.csv")
        data = orange.ExampleTable("c:\\temp\\output.tab")
        forest = orngEnsemble.RandomForestLearner(data, trees=50, name="forest")
        
        #tree = orngTree.TreeLearner(data, sameMajorityPruning=1, mForPruning=2)#, maxDepth=40)
        
        #tree = orngTree.TreeLearner(minExamples=2, mForPrunning=2, \
        #                            sameMajorityPruning=True, name='tree')
        
       
        print "Possible classes:", data.domain.classVar.values
        #print "Probabilities for democrats:"
        if False:
            for i in range(len(data)):
                p = forest(data[i], orange.GetProbabilities)
                print "%d: %5.10f (originally %s)" % (i+1, p[1], data[i].getclass())

        #orngTree.printTxt(tree)
        
       
        
        count = 0
        v = zeros(self.getCurrentVolume().shape)
        for x in range(borderWidthForFeatures, v.shape[0]-borderWidthForFeatures):
            print x
            for y in range(borderWidthForFeatures,v.shape[1]-borderWidthForFeatures):
                for z in range(borderWidthForFeatures,v.shape[2]-borderWidthForFeatures):
                    
                    
                    #print(data[count])
                    #p = forest(data[count], orange.GetProbabilities)
                    
                    dictionary = getFeaturesAt(self.getCurrentVolume(), (x,y,z))
                    list = []
                    for item in dictionary.items():
                        value = item[1]
                        list.append(value)
                    list.append('False')
                    #p = forest(list, orange.GetProbabilities)
                    example = orange.Example(data.domain, list)
                    p = forest(example, orange.GetProbabilities)    
                    
                    #print (x,y,z)
                    #print count
                    #v[x,y,z] = numpy.log(p[1])
                    v[x,y,z] = 1 - p[1]
                    count += 1
                    #print p[1]
        
        self.addVolume(v, 'probability')
            
        
        
        

    def onExit(self, event):
        self.t1.Stop()
        for frame in self.childFrames:
            frame.Destroy()
        #self.Close(True)
        #wx.Frame.Close(self, True)
        self.Destroy()
                
    def zoomFactor(self):
        zoomPercent = (getNode(self.settingsTree, ('imageControls','zoom'))).get()
        zoom = zoomPercent / 100.0
        return zoom

    #def topLeftCornerOfWindowInVolumeCoordinates():
    def cornersOf3DWindow(self):
        volume = self.getCurrentVolume()
        
        # todo: variable name full volume should be loaded volume
        positionInFullVolume = numpy.array( 
            ((getNode(self.settingsTree, ('imageControls','xIndex'))).get(),
             (getNode(self.settingsTree, ('imageControls','yIndex'))).get(),
             (getNode(self.settingsTree, ('imageControls','zIndex'))).get()))
        

        
        #topLeft = positionInFullVolume
        #bottomRight = positionInFullVolume
        sizeX = (getNode(self.settingsTree, ('imageControls','imageWindowSizeX'))).get()
        sizeY = (getNode(self.settingsTree, ('imageControls','imageWindowSizeY'))).get()
        half = numpy.array([sizeX, sizeY, 0]) / 2
        cornerA = positionInFullVolume - half
        cornerB = positionInFullVolume + half
        
        cornerA = insideLimits(volume.shape, cornerA)
        cornerB = insideLimits(volume.shape, cornerB)
        
        return Box(cornerA, cornerB)
    
    
    def getXYImage(self, volume, displayedRegionBox):
        box = displayedRegionBox
        
        imageArray = volume[box.cornerA[0]:box.cornerB[0],
                       box.cornerA[1]:box.cornerB[1],
                       box.cornerA[2]]
        
        return imageArray.T


    def drawViews(self, volume, threshold):

        global globalCount
        
        image = self.getXYImage(volume, self.cornersOf3DWindow())
        
        colorImageShape = [image.shape[0],image.shape[1],3]
        
        if threshold != None: image = (image < threshold) * 150
        
        max = image.max()
        min = image.min()
        
        normalizedImage = (image - min) * (255.0 / (max - min)) 

        a = numpy.zeros(colorImageShape,numpy.int8)
        a[:,:,0] = normalizedImage
        a[:,:,1] = normalizedImage
        a[:,:,2] = normalizedImage
        
        imageShape = a.shape
        
        image = wx.EmptyImage(imageShape[1],imageShape[0])
        image.SetData(a.tostring())
        
        image.Rescale(self.zoomFactor() * image.GetWidth(), self.zoomFactor() * image.GetHeight(), wx.IMAGE_QUALITY_NORMAL)

        bitmap = wx.BitmapFromImage(image)

        dc = wx.BufferedDC(None, bitmap)
        self.drawParticles(dc)
        
        if (getNode(self.settingsTree, ('particleMotionTool','selectABox'))).get():
            self.drawSelectionBox(dc)

        
        self.sb1.SetBitmap(bitmap)
        
        self.sb1.Refresh()

    
        if 0:
            # xz view on the bottom of the screen
            a = Numeric.zeros((volume.shape[0],volume.shape[2],3))
            image = numpyToNumeric2D(volume[:,xyz[1],:])
            if threshold != None: image = (image < threshold) * 150
            a[:,:,0] = image #red
            a[:,:,1] = image #green
            a[:,:,2] = image #blue
            s = pygame.surfarray.make_surface(a)
            screen.blit(s,(0,volume.shape[1]+gapDistance))
        
            # yz view on the right of the screen
            a = Numeric.zeros((volume.shape[2],volume.shape[1],3))
            trans = numpyToNumeric2D(Numeric.transpose(volume[xyz[0],:,:]))
            if threshold != None: trans = (trans < threshold) * 150
            a[:,:,0] = trans #red
            a[:,:,1] = trans #green
            a[:,:,2] = trans #blue
            s = pygame.surfarray.make_surface(a)
            screen.blit(s,(volume.shape[0]+gapDistance,0))




    def generateComponents(self, node, depth, path, container, panel, frame):
        containerForChildren = container
        panelForChildren = panel
        frameForChildren = frame

        if node.type != 'group':
            label = wx.StaticText(panel, -1, str(appendToNewListAndReturnList(path, node.name)))

        if node.type == 'group':
           containerForChildren, panelForChildren, frameForChildren = self.makeContainerForControls(node.params['caption'])
           #frameForChildren.SetSize(wx.Rect(100,100))
           frameForChildren.Move(node.params['position'])
           #frameForChildren.SetSize(wx.Rect(100,100,100,100))
           frameForChildren.SetSize(node.params['size'])
           
        
        elif node.type == 'slider':

            #label = wx.StaticText(self.panel, -1, node.params['caption'])
            if 'min' in node.params:
                min = node.params['min']
            else:
                min = 0

            slider = wx.Slider(panel, -1, node.valueToSave, min, node.params['max'], pos=(10, 10), 
                               size=(250, -1),
                               style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS )
            slider.SetTickFreq(5, 1)
            container.AddMany([label, slider])
            #container.Layout()
            #container.RecalcSizes()
            #frame.SendSizeEvent()
            #self.panel.SetSizerAndFit(self.fgs)
            #self.Fit()

            node.guiComponent = slider

        #elif node.type == 'slidersFromDictionary':
            
            
            
        elif node.type == 'text':

            
            #label = wx.StaticText(self.panel, -1, node.params['caption'])
            textBox = wx.TextCtrl(panel, -1, node.valueToSave, size=(175, -1))
            #text.SetInsertionPoint(0)
            container.AddMany([label, textBox])

            #self.panel.SetSizerAndFit(self.fgs)
            #self.Fit()
            
            node.guiComponent = textBox
            
        elif node.type == 'label':

            labelComponent = wx.StaticText(panel, -1, '-')
            container.AddMany([label, labelComponent])
            node.guiComponent = labelComponent

        elif node.type == 'boolean':
            print ""
            #booleanVariable = IntVar()
            #checkBox = Checkbutton(root, text=node.params['caption'], variable=booleanVariable)
            #checkBox.pack()
            #node.guiComponent = booleanVariable
            
            #label = wx.StaticText(self.panel, -1, "check box")
            checkBox = wx.CheckBox(panel, -1, node.params['caption'], (35, 40), (150, 20))
            checkBox.SetValue(node.valueToSave)
            container.AddMany([label, checkBox])
            #self.panel.SetSizerAndFit(self.fgs)
            #self.Fit()
            
            node.guiComponent = checkBox          

        elif node.type == 'gauge':

            gauge = self.gauge = wx.Gauge(panel, -1, 50, (20, 50), (250, 25));
            container.AddMany([label, gauge])
            node.guiComponent = gauge          

            
        elif node.type == 'button':
            #label = wx.StaticText(self.panel, -1, "button")

            button = wx.Button(panel, -1, node.params['caption'])
            frame.Bind(wx.EVT_BUTTON, eval('self.' + node.valueToSave), button)
            # button.SetDefault() #what does this do? -- maybe sets as default selected button

            container.AddMany([label, button])
            #self.panel.SetSizerAndFit(self.fgs)
            #self.Fit()
            
            node.guiComponent = button


        elif node.type == 'menuItem':
            menuBar = frame.GetMenuBar()
            #menuBar.Append(node.params['caption'])
            menu = menuBar.GetMenu(0)
            item = menu.Append(-1, node.params['caption'], 'help text')
            self.Bind(wx.EVT_MENU, eval('self.' + node.valueToSave), item)

            #labelComponent = wx.StaticText(panel, -1, '-')
            #container.AddMany([label, labelComponent])


            
        elif node.type == 'listBox':

            listBox = wx.ListBox(panel, -1, (20, 20), (100, 80), node.params['items'], wx.LB_SINGLE)
            listBox.SetSelection(node.valueToSave)
            container.AddMany([label, listBox])
            node.guiComponent = listBox
            
        else:
            print "error: the component type %s is not valid" % node.type
        
        if not(container == None):
            container.Layout()
            #container.SendSizeEvent()
        #if not(frame == None):
        #    frame.SendSizeEvent()
            #frame.Layout()
        
        for child in node.children:
            self.generateComponents(child, depth+1, appendToNewListAndReturnList(path, (node.name)), containerForChildren, panelForChildren, frameForChildren)

    def onPreviewImageStack(self, event):
        path = self.getValue(('particleMotionTool','imageStackPath'))
        #self.numberOfImagesInStack(path)
        sh = imageStackShape(path)
        middleImageIndex = int(sh[2] / 2)
        #print "shape"
        #print sh
        
        # loads one image from the middle of the stack
        subvolumeBox = Box((0,0,middleImageIndex), (sh[0],sh[1],middleImageIndex+1))
        v = loadImageStack(path, subvolumeBox)

        self.setSliderMax(('imageControls','xIndex'), v.shape[0]-1)
        self.setSliderMax(('imageControls','yIndex'), v.shape[1]-1)

        self.setControlEnable(('particleMotionTool','loadPartialImageStack'), True)




    def guiLoadImageStack(self, subvolumeBox):
        print "onLoadImageStack"

        #m = cytoseg_util.winmem()
        #print "Available memory: %d megabytes" % int(m.dwAvailPhys/(1024**2))
        ##print "Available memory in megabytes:"
        ##print m.dwAvailPhys/(1024**2)
        
        # v is a volume
        v = loadImageStack((getNode(self.settingsTree, ('particleMotionTool','imageStackPath'))).get(), subvolumeBox)

        self.setSliderMax(self.settingsTree, ('imageControls','xIndex'), v.shape[0]-1)
        self.setSliderMax(self.settingsTree, ('imageControls','yIndex'), v.shape[1]-1)
        self.setSliderMax(self.settingsTree, ('imageControls','zIndex'), v.shape[2]-1)

        self.setValue(('imageControls','zIndex'), int(v.shape[2]/2))
        
        # set z coordinates of selection box
        #temp# self.selectionBoxInLoadedVolumeCoords().cornerA[2] = 0
        #temp# self.selectionBoxInLoadedVolumeCoords().cornerB[2] = v.shape[2] - 1

        self.selectionBoxInFullVolumeCoords.cornerA[2] = 0
        self.selectionBoxInFullVolumeCoords.cornerB[2] = v.shape[2] - 1

        
        #self.beepSound.Play()
        
    def onLoadImageStack(self, event):
        self.guiLoadImageStack(None)
        sh = imageStackShape(self.getValue(('particleMotionTool','imageStackPath')))
        self.loadedVolumeBoxInFullVolumeCoords = Box((0,0,0),sh)

        
    def onLoadPartialImageStack(self, event):
        
        
        selectionBox = copy.deepcopy(self.getSelectionBoxInFullVolumeCoords())
        fullStackShape = imageStackShape(self.getValue(('particleMotionTool','imageStackPath')))
        
        # assumes the user wants to open all of the z slices
        # todo: not sure if this is neccessary, the box may alread have this for the z values
        selectionBox.cornerA[2] = 0
        selectionBox.cornerB[2] = fullStackShape[2]
        
        self.guiLoadImageStack(selectionBox)
        
        self.setControlEnable(('particleMotionTool','loadPartialImageStack'), False)

        self.loadedVolumeBoxInFullVolumeCoords = copy.deepcopy(self.getSelectionBoxInFullVolumeCoords())

        #self.loadedVolumeBoxInFullVolumeCoords = selectionBox
        
        
        # todo: this is being done temporarily to prevent user from getting weird results with coordinates because i haven't tested things for multiple loads
        self.setControlEnable(('particleMotionTool','loadImageStack'), False)
        self.setControlEnable(('particleMotionTool','previewImageStack'), False)

        

    def onClickedImage(self, event):
        
        print count
                    
        #location = (event.y, event.x)
        #print dir(event)
        

        location = self.screenXYToFullVolumeXYZ((event.X, event.Y))
        #print location
        
        volume = self.getCurrentVolume()
        
        #self.old_setFeatureSliders(location)
        if self.derivativeHasBeenComputed:
            #if isInsideVolumeWithBorder(volume, location, borderWidthForFeatures):
                self.setFeatureSliders(location)
        
        # location in X-Y plane of volume
        #location = array(locationInScreenPixels) / self.zoomFactor()
        #print location

    
        
        # if clicked inside of the image
        # todo: it may be that all clicks are inside the image and this "if" statement doesn't need to be here
        # if location[0] < volume.shape[0] and location[1] < volume.shape[1]:
        if True:
            
            #(getNode(self.settingsTree, ('particleMotionTool','xIndex'))).set(location[0])
            #(getNode(self.settingsTree, ('particleMotionTool','yIndex'))).set(location[1])

            if (getNode(self.settingsTree, ('particleMotionTool','makeNewParticles'))).get():
                p = makeParticle(location)
                                 
                
                #print "self.currentSubgroupIndex"
                #print self.currentSubgroupIndex
                #print particleGroup.getSubgruops()
                particleGroup.addToSubgroup(self.currentSubgroupIndex, p)
                print particleGroup.getSubgroup(self.currentSubgroupIndex)
                    
            if (getNode(self.settingsTree, ('particleMotionTool','trackParticle'))).get():
                currentParticle = closestParticle((location[0],location[1]))
                
            ##if (form['selectParticle'].value):
            ##    # todo: don't add it to list if it's already in list
            ##    selectedParticles.append(closestParticle((location[0],location[1])))

        self.drawingSelectionBox = True
        #self.selectionBox.cornerA[0] = event.X
        #self.selectionBox.cornerA[1] = event.Y
        self.selectionBoxInFullVolumeCoords.cornerA[0] = location[0]
        self.selectionBoxInFullVolumeCoords.cornerA[1] = location[1]
        

    def onMouseMotionOnImage(self, event):
        #self.cornerA = (0,0,0)
        #self.cornerB = (event.X,event.Y,0)
        location = self.screenXYToFullVolumeXYZ((event.X, event.Y))
        if self.drawingSelectionBox:
            self.selectionBoxInFullVolumeCoords.cornerB[0] = location[0]
            self.selectionBoxInFullVolumeCoords.cornerB[1] = location[1]

    def onButtonUp(self, event):
        self.drawingSelectionBox = False


    def onMenuOpen(self, event):
        wildcard = "(*.cytoseg)|*.cytoseg|All files (*.*)|*.*"
        dialog = wx.FileDialog(self, "Open", os.getcwd(), style=wx.OPEN, wildcard=wildcard)
        if dialog.ShowModal() == wx.ID_OK:
            print dialog.GetPath()
            self.currentFilename = dialog.GetPath()
            #self.filename = dlg.GetPath()
            #self.ReadFile()
            #self.SetTitle(self.title + ' -- ' + self.filename)
            self.SetTitle(self.currentFilename)
            loadBlobsAndParticlesAndEdges(dialog.GetPath())
        dialog.Destroy()

    def onMenuSave(self, event):
        #print ""
        doc = Document()
        global particleGroup
        doc.particleGroup = particleGroup
        doc.volumeShape = self.getCurrentVolume().shape
        writeDocument(doc, self.currentFilename)

    def onMenuSaveAs(self, event):
        #print ""
        wildcard = "(*.cytoseg)|*.cytoseg|All files (*.*)|*.*"
        dialog = wx.FileDialog(self, "Save As", os.getcwd(), style=wx.OPEN, wildcard=wildcard)
        if dialog.ShowModal() == wx.ID_OK:
            print dialog.GetPath()
            #self.filename = dlg.GetPath()
            #self.ReadFile()
            #self.SetTitle(self.title + ' -- ' + self.filename)
        
            doc = Document()
            # todo: probably need doc.edges = edges
            
            #global blobs
            global particleGroup
            #doc.blobs = blobs
            doc.particleGroup = particleGroup
            doc.volumeShape = self.getCurrentVolume().shape
        
            writeDocument(doc, dialog.GetPath())
        
        dialog.Destroy()


    def onMenuInsertIntoIMODFile(self, event):
        
        wildcard = "(*.imod)|*.imod|All files (*.*)|*.*"
        dialog = wx.FileDialog(self, "Insert into IMOD File", os.getcwd(), style=wx.OPEN, wildcard=wildcard)
        if dialog.ShowModal() == wx.ID_OK:
            print dialog.GetPath()
            self.currentFilename = dialog.GetPath()
            #self.filename = dlg.GetPath()
            #self.ReadFile()
            #self.SetTitle(self.title + ' -- ' + self.filename)
            self.SetTitle(self.currentFilename)
            #loadBlobsAndParticlesAndEdges(dialog.GetPath())

            points = []
            for p in particleGroup.getAll():
                points.append(p.loc)
            
            # todo: if a space is at end of filename maybe this would use the original filename and overwrite the file. (possible bug)
            radius = (getNode(self.settingsTree, ('particleMotionTool','particleRadius'))).get()
            imod_tools.IMODFileInsertPoints(dialog.GetPath(), dialog.GetPath() + "_insert.imod", points, self.getCurrentVolume().shape, radius)
        dialog.Destroy()
        
        
        

    def onMenuExit(self, event):
        self.onExit(None)


    def drawSelectionBox(self, dc):
        box = self.getSelectionBoxInFullVolumeCoords()
        a = self.fullVolumeXYToScreenXY((box.cornerA[0], box.cornerA[1]))
        b = self.fullVolumeXYToScreenXY((box.cornerB[0], box.cornerB[1]))
        #width = box.shape()[0]
        #height = box.shape()[1]
        width = b[0] - a[0]
        height = b[1] - a[1]
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        
        dc.DrawRectangle(a[0], a[1], width, height)  


    def setFeatureSliders(self, location):
        loc = numpy.int_(location)
        dictionary = getFeaturesAt(self.getCurrentVolume(), loc)
        #if dictionary != None:
        for item in dictionary.items():
            key = item[0]
            value = item[1]
            #'featuresAtPoint',key
            
            if value < self.getSliderMin(self.viewerRootNode, (key,)):
                self.setSliderMin(self.viewerRootNode, (key,), value)

            if value > self.getSliderMax(self.viewerRootNode, (key,)):
                self.setSliderMax(self.viewerRootNode, (key,), value)
                            
            (getNode(self.viewerRootNode, (key,))).set(value)
            #(getNode(self.settingsTree, ('featuresAtPoint',key))).set(value)
            

    def old_setFeatureSliders(self, location):

        #print location
        loc = numpy.int_(location)

        #(getNode(self.settingsTree, ('featuresAtPoint','grayValue'))).set(self.getCurrentVolume()[numpy.int_(location)])
        (getNode(self.settingsTree, ('featuresAtPoint','grayValue'))).set(self.getCurrentVolume()[loc[0],loc[1],loc[2]])

        xG = volumes['xGradient'][loc[0],loc[1],loc[2]]
        yG = volumes['yGradient'][loc[0],loc[1],loc[2]]
        zG = volumes['zGradient'][loc[0],loc[1],loc[2]]
        
        (getNode(self.settingsTree, ('featuresAtPoint','xGradient'))).set(xG)
        (getNode(self.settingsTree, ('featuresAtPoint','yGradient'))).set(yG)
        (getNode(self.settingsTree, ('featuresAtPoint','zGradient'))).set(zG)

       
        eigenValues = numpy.linalg.eigvals(structureTensor(xG,yG,zG))
        print structureTensor
        print 'eigenValues'
        print eigenValues
        
        (getNode(self.settingsTree, ('featuresAtPoint','eigenValue1'))).set(eigenValues[0])
        (getNode(self.settingsTree, ('featuresAtPoint','eigenValue2'))).set(eigenValues[1])
        (getNode(self.settingsTree, ('featuresAtPoint','eigenValue3'))).set(eigenValues[2])


    def onStructureTensorView(self, event):
        
        file = open("c:\\temp\\output.tab", "w")
        
        volume = numpy.zeros(volumes['Original'].shape)
        #selected x, y, and z
        sx = (getNode(self.settingsTree, ('imageControls','xIndex'))).get()
        sy = (getNode(self.settingsTree, ('imageControls','yIndex'))).get()
        sz = (getNode(self.settingsTree, ('imageControls','zIndex'))).get()
        
        xG = volumes['xGradient'][sx,sy,sz]
        yG = volumes['yGradient'][sx,sy,sz]
        zG = volumes['zGradient'][sx,sy,sz]
        
        stAtSelectedPoint = structureTensor(xG,yG,zG)
        eigAtSelectedPoint = numpy.linalg.eigvals(stAtSelectedPoint)
        
        sh = volumes['Original'].shape
        
        file.write("eig1\teig2\teig3\tis_membrane\n")
        file.write("c\tc\tc\tdiscrete\n")
        file.write("\t\t\tclass\n")
        
        for x in range(0,sh[0]):
            print x
            for y in range(0,sh[1]):
                for z in range(0,sh[2]):
                    
                    xG = volumes['xGradient'][x,y,z]
                    yG = volumes['yGradient'][x,y,z]
                    zG = volumes['zGradient'][x,y,z]
        
                    st = structureTensor(xG,yG,zG)
                    eigenValues = numpy.linalg.eigvals(st)
                    
                    for value in eigenValues:
                        file.write("%f\t" % value)
                    file.write("%s" % particleGroup.containsIntegerPoint((x,y,z)))
                    file.write("\n")
                    
                    volume[x,y,z] = distance(eigenValues, eigAtSelectedPoint)
        
        self.addVolume(volume, 'eigenValueStructureTensorView')
        file.close()
        

    def onMakeNewSubgroup(self, event):
        self.makeNewSubgroup()

    def onFillInsideOfContours(self, event):
        count = 0
        v = self.getCurrentVolume()
        for subgroup in particleGroup.getSubgroups():
            print 'count'
            print count
            count += 1
            if len(subgroup) >= 3:
                z = subgroup[0].loc[2]
                points = []
                for particle in subgroup:
                    points.append([particle.loc[0], particle.loc[1]])
                
                for x in range(0, v.shape[0]):
                    print 'x'
                    print x
                    for y in range(0, v.shape[1]):
                        if geometry.insidePolygon(points, (x,y)):
                            v[x,y,z] = 255

    def onFillInsideOfSelectionBox(self, event):
        box = self.selectionBoxInLoadedVolumeCoords()
        a = box.cornerA
        b = box.cornerB
        v = self.getCurrentVolume()
        v[a[0]:b[0], a[1]:b[1], a[2]:b[2]] = 255


    def makeNewSubgroup(self):
        particleGroup.addEmptySubgroup()
        self.currentSubgroupIndex += 1



    def screenXYToLoadedVolumeXYZ(self, locationInScreenPixels):
        box = self.cornersOf3DWindow()
        f = self.zoomFactor() 
        x = (locationInScreenPixels[0] / f) + box.cornerA[0]
        y = (locationInScreenPixels[1] / f) + box.cornerA[1]
        z = (getNode(self.settingsTree, ('imageControls','zIndex'))).get()
        return array([x,y,z])

    #def screenXYToFullVolumeXYZ(self, locationInScreenPixels):
    #    XYZInLoadedVolume = self.screenXYToLoadedVolumeXYZ(locationInScreenPixels)
    #    box = self.loadedVolumeBoxInFullVolumeCoords
    #    print "array(XYZInLoadedVolume)", array(XYZInLoadedVolume)
    #    print "array(box.cornerA[0], box.cornerA[1])", array(box.cornerA[0], box.cornerA[1])
    #    return array(XYZInLoadedVolume) + array(box.cornerA)

    def screenXYToFullVolumeXYZ(self, locationInScreenPixels):
        windowBox = self.cornersOf3DWindow()
        b = self.loadedVolumeBoxInFullVolumeCoords
        f = self.zoomFactor() 
        x = (locationInScreenPixels[0] / f) + windowBox.cornerA[0] + b.cornerA[0]
        y = (locationInScreenPixels[1] / f) + windowBox.cornerA[1] + b.cornerA[1]
        z = (getNode(self.settingsTree, ('imageControls','zIndex'))).get()
        return array([x,y,z])
    

    def fullVolumeXYToScreenXY(self, fullVolumeXYCoords):
        ## todo: add offsets to account for subvolume inside of full volume
        #
        #box = self.loadedVolumeBoxInFullVolumeCoords
        ##print "-----------------------------"
        ##print box.cornerA[0]
        ##print box.cornerA[1]
        ##print array(box.cornerA[0], box.cornerA[1])
        ##print numpy.array(box.cornerA[0], box.cornerA[1])
        #
        #return self.loadedVolumeXYToScreenXY(fullVolumeXYCoords) - array((box.cornerA[0], box.cornerA[1]))

        windowBox = self.cornersOf3DWindow()
        b = self.loadedVolumeBoxInFullVolumeCoords
        f = self.zoomFactor()
        screenX = f * (fullVolumeXYCoords[0] - windowBox.cornerA[0] - b.cornerA[0])
        screenY = f * (fullVolumeXYCoords[1] - windowBox.cornerA[1] - b.cornerA[1])
        return (screenX, screenY)  


    def loadedVolumeXYToScreenXY(self, loadedVolumeXYCoords):
        box = self.cornersOf3DWindow()
        f = self.zoomFactor()
        screenX = f * (loadedVolumeXYCoords[0] - box.cornerA[0])
        screenY = f * (loadedVolumeXYCoords[1] - box.cornerA[1])
        return (screenX, screenY)        


    def drawParticles(self, dc):
        #print ""
                
        radius = (getNode(self.settingsTree, ('particleMotionTool','particleRadius'))).get()                
        
        for i in range(0, len(particleGroup.getSubgroups())):
            subgroup = particleGroup.getSubgroup(i)
            pen = wx.Pen("red", 1)
            c = particleGroup.getColorOfSubgroup(i)
            #pen.SetColour(c[0], c[1], c[2])
            pen.SetColour(wx.Color(c[0], c[1], c[2], 0))
            
            # zoom factor
            f = self.zoomFactor()
            
            for p in subgroup:
                 # if particle is close to current z plane, show it
                 if abs(p.loc[2] - (getNode(self.settingsTree, ('imageControls','zIndex'))).get()) <= 1:
                     dc.SetPen(pen)
                     dc.SetBrush(wx.TRANSPARENT_BRUSH)
                     x, y = self.fullVolumeXYToScreenXY((p.loc[0], p.loc[1]))
                     dc.DrawEllipse(x - f*radius, y - f*radius, 2*f*radius, 2*f*radius)
                 
            #print p.x 
            

        #for particle in particles:   
        #
        #    if 0:
        #        pygame.draw.circle(screen,(100,100,100),(particle.x[0],particle.x[1]),abs(form['zIndex'].value-particle.x[2])+2,1)
        #        if abs(form['zIndex'].value-particle.x[2]) <= 1:
        #            pygame.draw.line(screen,(100,0,0),(particle.x[0]-5,particle.x[1]),(particle.x[0]+5,particle.x[1]),1)
        #            pygame.draw.line(screen,(100,0,0),(particle.x[0],particle.x[1]-5),(particle.x[0],particle.x[1]+5),1)
        #        
        #    # really this should be a check for the same object, not the same location
        #    if currentParticle == particle:
        #        # highlight current particle in red
        #        drawCircleInAllViews(particle.x, (0,255,0), form['particleRadius'].value)
        #        #drawCircleInAllViews(particle.x, (0,255,0), 3)
        #    else:
        #        drawCircleInAllViews(particle.x, (0,0,200), form['particleRadius'].value)
        #
        ## other way to to do this would be to set the color that the particle will be drawn earlier (based on conditions) and then only draw it once. or you could check if it's in the selected list for every particle but that would be n^2 rather than just n in terms of time cost.
        #for p in selectedParticles:
        #    drawCircleInAllViews(p.x, (255,255,100), form['particleRadius'].value)


def insideLimits(shape, point):
    # todo: add a check to make sure the point has the type that it should have
    newPoint = copy.deepcopy(point)
    for coordinateIndex in range(0, len(point)):
        if newPoint[coordinateIndex] >= shape[coordinateIndex]:
            newPoint[coordinateIndex] = shape[coordinateIndex]
        elif newPoint[coordinateIndex] < 0:
            newPoint [coordinateIndex] = 0
    return newPoint
        

def appendToNewListAndReturnList(list, element):
    newList = copy.deepcopy(list)
    newList.append(element)
    return newList



def makeParticle(location):
    global particleIDCount
    
    if len(location) != 3:
        raise Exception, "Make particle requires a vector with 3 elements"

    
    p = Particle()
    p.loc = numpy.array(location)
    p.color = (200.0*random.random(), 200.0*random.random(), 200.0*random.random())

    particleIDCount = particleIDCount + 1
    p.id = particleIDCount
    #p.graphicsObjectHandle = canvas.create_oval(0,0,10,10)

    return p


def makeDefaultGUITree():
    rootNode = DataNode("root","group",{'caption' : 'root', 'position' : (100,100), 'size' : (100,100)},"value")
    #print 'n1 type'
    #print type(n1)
    

    imageControlsNode = DataNode("imageControls","group",{'caption' : 'imageControls', 'position' : (700,500), 'size' : (500,400)},None)
    imageControlsNode.addChildren((
                    DataNode("xIndex","slider",{'caption' : 'X', 'max' : 300},0),
                    DataNode("yIndex","slider",{'caption' : 'Y', 'max' : 300},0),
                    DataNode("zIndex","slider",{'caption' : 'Z', 'max' : 300},0),

                    DataNode("zoom","slider",{'caption' : 'Zoom', 'max' : 800},200),
                    DataNode("imageWindowSizeX","slider",{'caption' : 'Window Width', 'max' : 10000},300),
                    DataNode("imageWindowSizeY","slider",{'caption' : 'Window Height', 'max' : 10000},300)))
                    

    particleMotionToolNode = DataNode("particleMotionTool","group",{'caption' : 'particleMotionTool', 'position' : (100,100), 'size' : (600,800)},None)
    particleMotionToolNode.addChildren((
                    DataNode("makeNewSubgroup","button",{'caption' : 'Make New Subgroup'},'onMakeNewSubgroup'),
                    DataNode("menuOpen","menuItem",{'caption' : 'Open'},'onMenuOpen'),
                    DataNode("menuSave","menuItem",{'caption' : 'Save'},'onMenuSave'),
                    DataNode("menuSaveAs","menuItem",{'caption' : 'Save As'},'onMenuSaveAs'),
                    DataNode("menuInsertIntoIMODFile","menuItem",{'caption' : 'Insert into IMOD File'},'onMenuInsertIntoIMODFile'),
                    DataNode("menuExit","menuItem",{'caption' : 'Exit'},'onMenuExit'),

                    DataNode("visibleVolume","listBox",{'caption' : 'visibleVolume', 'items' : ['Original', 'Temporary']},0),

                    DataNode("selectABox","boolean",{'caption' : 'Select a Box'},True),
                    DataNode("processSelectionOnly","boolean",{'caption' : 'processSelectionOnly'},True),

                    DataNode("previewImageStack","button",{'caption' : 'Preview Image Stack'},'onPreviewImageStack'),
                    DataNode("loadImageStack","button",{'caption' : 'Load Image Stack'},'onLoadImageStack'),
                    DataNode("loadPartialImageStack","button",{'caption' : 'Load Partial Image Stack'},'onLoadPartialImageStack'),

                    DataNode("saveVolumes","button",{'caption' : 'saveVolumes'},'onSaveVolumes'),
                    DataNode("openVolumes","button",{'caption' : 'openVolumes'},'onOpenVolumes'),
                    
                    DataNode("learnFeaturesOfMembranePixels","button",{'caption' : 'learnFeaturesOfMembranePixels'},'onLearnFeaturesOfMembranePixels'),
                    DataNode("classifyPixelsOfCurrentImage","button",{'caption' : 'classifyPixelsOfCurrentImage'},'onClassifyPixelsOfCurrentImage'),

                    DataNode("makeTabFile","button",{'caption' : 'makeTabFile'},'onMakeTabFile'),
                    DataNode("findBlobsThenParticleMovement","button",{'caption' : 'findBlobsThenParticleMovement'},'findBlobsThenParticleMovement'),
                    DataNode("readIMODFile","button",{'caption' : 'readIMODFile'},'readIMODFile'),
                    DataNode("saveParticlesToPSI","button",{'caption' : 'Save particles to output.psi'},'saveParticlesToPSIButton'),
                    DataNode("visualsEnabled","boolean",{'caption' : 'Visuals Enabled'},True),

                    DataNode("copyCurrentToTemporary","button",{'caption' : 'copyCurrentToTemporary'},'copyCurrentToTemporary'),
                    DataNode("watershedOnTemporary","button",{'caption' : 'watershedOnTemporary'},'watershedOnTemporary'),

                    DataNode("imageStackPath","text",{'caption' : 'Image Stack Path'},defaultPath),
                    DataNode("tempPath","text",{'caption' : 'Temporary Files Path'},defaultOutputPath),
                    DataNode("thresholdEnabled","boolean",{'caption' : 'Threshold Enabled'},False),
                    DataNode("grayThreshold","slider",{'caption' : 'Gray Threshold', 'max' : 300},25),
                    DataNode("makeNewParticles","boolean",{'caption' : 'Make New Particles'},False),
                    DataNode("trackParticle","boolean",{'caption' : 'Track Particle'},False),
                    DataNode("selectParticle","boolean",{'caption' : 'Select Particle'},False),
                    DataNode("moveParticlesAlongGradient","boolean",{'caption' : 'Move Particles along Gradient'},False),
                    DataNode("grayGradientForce","slider",{'caption' : 'Force from Gray Gradient', 'max' : 300},90),
                    DataNode("particleRadius","slider",{'caption' : 'Particle Radius', 'max' : 300},9),
                    DataNode("minimumBlobSize","slider",{'caption' : 'Min Blob Size', 'max' : 300},80),
                    DataNode("maximumBlobSize","slider",{'caption' : 'Max Blob Size', 'max' : 300},10),
                    DataNode("iterationsOfParticleMovement","slider",{'caption' : 'iterationsOfParticleMovement', 'max' : 300},300),
                    DataNode("randomStepSize","slider",{'caption' : 'Random Step Size', 'max' : 300},10),
                    DataNode("repulsiveForce","slider",{'caption' : 'Repulsive Force', 'max' : 300},10),

    
                    #DataNode("openImageStack","button",{'caption' : 'Open Image Stack'},'onOpenImageStack'),
                    DataNode("automaticProcess","button",{'caption' : 'Automatic Process'},'automaticProcessButton'),
                    DataNode("markBlobs","button",{'caption' : 'Mark Blobs'},'onMarkBlobs'),
                    DataNode("undoMarkBlobs","button",{'caption' : 'Undo Mark Blobs'},'onUndoMarkBlobs'),

                    #DataNode("findBlobsThenParticleMovement","button",{'caption' : 'findBlobsThenParticleMovement'},'findBlobsThenParticleMovement'),
                    DataNode("loadParticlesAndEdges","button",{'caption' : 'Load Particles and Edges'},'onLoadBlobsAndParticlesAndEdges'),
                    DataNode("display3D","button",{'caption' : 'Display 3D'},'display3D'),
                    DataNode("drawParticlesInVolume","button",{'caption' : 'Draw Particles in Volume'},'drawParticlesInVolumeButton'),
                    #DataNode("saveParticlesToPSI","button",{'caption' : 'Save particles to output.psi'},'saveParticlesToPSIButton'),
                    DataNode("plotBlobSizes","button",{'caption' : 'Plot blob sizes'},'plotBlobSizesButton'),
                    #DataNode("derivative","button",{'caption' : 'Derivative'},'derivative'),
                    DataNode("structureTensorView","button",{'caption' : 'structureTensorView'},'onStructureTensorView'),
                    DataNode("fillInsideOfContours","button",{'caption' : 'fillInsideOfContours'},'onFillInsideOfContours'),
                    DataNode("fillInsideOfSelectionBox","button",{'caption' : 'fillInsideOfSelectionBox'},'onFillInsideOfSelectionBox'),
                    DataNode("exit","button",{'caption' : 'Exit'},'onExit')))

#    featuresAtPointNode = DataNode("featuresAtPoint","group",{'caption' : 'Features at Point', 'position' : (700,300), 'size' : (500,500)},None)
#    featuresAtPointNode.addChildren(((DataNode("mouseAtPixel","label",{'caption' : 'Position', 'min' : -300, 'max' : 300},0)),
#                    (DataNode("grayValue","slider",{'caption' : 'Gray Value', 'min' : -300, 'max' : 300},0)),
#                    (DataNode("xGradient","slider",{'caption' : 'xGradient', 'min' : -300, 'max' : 300},0)),
#                    (DataNode("yGradient","slider",{'caption' : 'yGradient', 'min' : -300, 'max' : 300},0)),
#                    (DataNode("zGradient","slider",{'caption' : 'zGradient', 'min' : -300, 'max' : 300},0)),
#                    (DataNode("eigenValue1","slider",{'caption' : 'eigenValue1', 'min' : -100, 'max' : 100},0)),
#                    (DataNode("eigenValue2","slider",{'caption' : 'eigenValue2', 'min' : -100, 'max' : 100},0)),
#                    (DataNode("eigenValue3","slider",{'caption' : 'eigenValue3', 'min' : -100, 'max' : 100},0))))

    rootNode.addChild(imageControlsNode)
    rootNode.addChild(particleMotionToolNode)
    #rootNode.addChild(featuresAtPointNode)
    
    getNode(rootNode, ('particleMotionTool', 'automaticProcess')).addChild(
                    DataNode("useSubgroups","boolean",{'caption' : 'Use Subgroups'},False))

    
    
    print 'children types'
    for x in rootNode.children:
        print type(x)
    f = open("temp.pickle", "w")
    pickle.dump(rootNode, f)
    f.close()

    f = open("temp.pickle", "r")
    loadedData = pickle.load(f)
    print "data loaded from file"
    print loadedData
    f.close()
    
    print 'testing get node'
    print getNode(loadedData, ('particleMotionTool', 'd'))
    
    return rootNode
              
  


class old_GUI:
    
    
                
    def generateComponents1(self, node, depth):
        if node.type == 'slider':
            label = Label(root,  text=node.params['caption'])
            label.pack()
            #slider = Scale(root, from_=0, to=100, orient=HORIZONTAL, length=100, command=lambda arg1: setNodeValueCallback(node, slider.get()))
            slider = Scale(root, from_=0, to=100, orient=HORIZONTAL, length=100)
            slider.set(node.valueToSave)
            slider.pack()
            node.guiComponent = slider
            
        elif node.type == 'text':
            label = Label(root,  text=node.params['caption'])
            label.pack()
            textBox = Entry(root)
            textBoxString = StringVar()    #todo add callback to this tkinter variable
            textBoxString.set(node.valueToSave)
            textBox.config(textvariable=textBoxString)
            textBox.pack()
            #textBoxString.trace("w", testcallback)
            #textBoxString.set("123456789")
            #f = open("temp.pickle", "w")
            #pickle.dump(textBoxString, f)
            #f.close()
            #f = open('temp.pickle')
            #x = pickle.load(f)
            #print 'testing the pickle of a string variable tkinter'
            #print type(x)
            ##print x.get()
            #textBoxString
            node.guiComponent = textBox

        elif node.type == 'boolean':
            booleanVariable = IntVar()
            checkBox = Checkbutton(root, text=node.params['caption'], variable=booleanVariable)
            checkBox.pack()
            node.guiComponent = booleanVariable

            

            
        else:
            print "(old) error: the component type %s is not valid" % node.type
            
            
        for child in node.children:
            self.generateComponents(child, depth+1)
    

      
        
        
        
        
        
    def buttonPressedOnImage(self, even):
        print '%s %s' % (event.x, event.y)
    
    
    def updateParticleGraphics(self):
        global particles
        # radius of circle
        R = (getNode(old_gui.settingsTree, ('particleMotionTool','particleRadius'))).get()
        for p in particles:
            self.canvas.coords(p.graphicsObjectHandle, self.canvas.canvasx(p.loc[1]-R), self.canvas.canvasy(p.loc[0]-R), self.canvas.canvasx(p.loc[1]+R), self.canvas.canvasy(p.loc[0]+R))
            #self.canvas.itemconfig(p.graphicsObjectHandle, color="red")
            
            if abs(p.loc[2] - (getNode(old_gui.settingsTree, ('imageControls','zIndex'))).get()) < 3: 
                self.canvas.itemconfig(p.graphicsObjectHandle, outline="red")
            else:
                self.canvas.itemconfig(p.graphicsObjectHandle, outline="")
    
    
        
    #def startTimer(self):
    #    self.handler = TimerHandler()
    #    self.t1 = wx.Timer(self.handler, id=1000)
    #    self.t1.Start(200)
    #    self.handler.Bind(wx.EVT_TIMER, self.handler.OnTimerEvent, id=1000)
        
    
    def __init__(self, settingsTree):
        
        self.settingsTree = settingsTree
        
        ##self.generateComponents(settingsTree, 0)
        
        self.visualsEnabled = IntVar()
        #self.thresholdEnabled = IntVar()
        
        #label = Label(root,  text="Gray Threshold")
        #label.pack()
        #self.grayThreshold = Scale(root, from_=0, to=300, orient=HORIZONTAL, length=300)
        #self.grayThreshold.set(90)
        #self.grayThreshold.pack()


        label = Label(root,  text="Minimum Blob Size")
        label.pack()
        self.minBlobSize = Scale(root, from_=0, to=300, orient=HORIZONTAL, length=300)
        self.minBlobSize.set(100)
        self.minBlobSize.pack()


        label = Label(root,  text="Scale factor for X and Y coordinates when writing to text file (percent)")
        label.pack()
        self.scaleFactor = Scale(root, from_=0, to=300, orient=HORIZONTAL, length=300)
        self.scaleFactor.set(100)
        self.scaleFactor.pack()



        #self.xIndex = Scale(root, from_=0, to=500, orient=HORIZONTAL)
        #self.xIndex.pack()

        #self.yIndex = Scale(root, from_=0, to=500, orient=HORIZONTAL)
        #self.yIndex.pack()

        #self.zIndex = Scale(root, from_=0, to=500, orient=HORIZONTAL)
        #self.zIndex.pack()


        c = Checkbutton(root, text="visualsEnabled", variable=self.visualsEnabled)
       
        c.pack()


        #thresholdCheck = Checkbutton(root, text="thresholdEnabled", variable=self.thresholdEnabled)
       
        #thresholdCheck.pack()

        #self.imageStackPathTextBox = Entry(root)
        #self.imageStackPathText = StringVar()
        #self.imageStackPathText.set(settings['defaultPath'])
        #self.imageStackPathTextBox.config(textvariable=self.imageStackPathText)
        #self.imageStackPathTextBox.pack()
        

        #self.saveImageStackPathTextBox = Entry(root)
        #self.saveImageStackPathText = StringVar()
        ##self.saveImageStackPathText.set("i:/temp/")
        #self.saveImageStackPathText.set(settings['temporaryFolder'])
        #self.saveImageStackPathTextBox.config(textvariable=self.saveImageStackPathText)
        #self.saveImageStackPathTextBox.pack()


        
        ##self.openStackButton = Button(root, text="Open Image Stack", command=openImageStackButton)
        ##self.openStackButton.pack()





        #self.label = Label()
        #self.label.pack()
        
        self.canvasScrollRegionSize = 800
        
        frame = Frame(root, bd=2, relief=SUNKEN)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        #frame.grid_columnconfigure(1, weight=1)

        
        self.viewScrollbarX = Scrollbar(frame, orient=HORIZONTAL)
        self.viewScrollbarX.grid(row=1, column=0, sticky=E+W)
        
        self.viewScrollbarY = Scrollbar(frame)
        self.viewScrollbarY.grid(row=0, column=1, sticky=N+S)
        
        self.canvas = Canvas(frame, bd=0, scrollregion=(0, 0, 100, 100),
                xscrollcommand=self.viewScrollbarX.set,
                yscrollcommand=self.viewScrollbarY.set)
        
        
                
        self.canvas.grid(row=0, column=0, sticky=N+S+E+W)
        #self.canvas.config(anchor=SE)
        ##self.canvas.bind("<Button-1>",self.buttonDownOnCanvas)
        
        self.viewScrollbarX.config(command=self.canvas.xview)
        self.viewScrollbarY.config(command=self.canvas.yview)
        
        #frame.grid(row=0, column=1)
        
        #frame.pack(side=TOP)
        #frame.pack(side=RIGHT,padx=10,pady=10)
        #frame.pack()
        frame.place(x=10,y=10,width=400,height=300)
        
        
        
        if 0:
            frame = Frame(root, bd=2, relief=SUNKEN)
    
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)
            
            self.canvas = Canvas(frame)
            self.canvas.pack()
            
            self.imageScrollX = Scrollbar(frame)
            self.imageScrollX.pack()
            self.imageScrollY = Scrollbar(frame)
            self.imageScrollY.pack()
            
            self.canvas.config(xscrollcommand=self.imageScrollX.set)        
            self.canvas.config(yscrollcommand=self.imageScrollY.set)        
            
            self.canvas.config(bd=0, scrollregion=(0, 0, 100, 100))
            
            self.imageScrollX.config(command=self.canvas.xview)
            self.imageScrollY.config(command=self.canvas.yview)
            
            frame.pack()
            
        #print "*********** start timer**************"
        #self.startTimer()

            
            
            
            
                

class Edge:
    # could could use something like the immutable list (n1, n2) to represent the two nodes and then they could be accessed by index
    node1 = None ########################################## is this a member variable???????? or a class variable?????????????????
    node2 = None

class Document:
    # could have file name for image data here also
    #blobs = None 
    #edges = None
    #particleGroup = None
    def dummyFunction():
        print ""
    
def volumeOfSphere(radius):
    return (4/3)*3.14*radius*radius*radius

def generateParticleGroupFromBlobs(blobs):
    pg = ParticleGroup()
    
    for b in blobs:
        subgroup = []
        #if b.size > 20000:
        #    continue
        numParticles = round(1.1 * b.size / volumeOfSphere(getNode(settingsTree, ('particleMotionTool','particleRadius')).get()))
        print "numParticles"
        print numParticles
        for i in range(0,numParticles):
            p = makeParticle(b.center)
            subgroup.append(p)
            #subgroup.append(p.makeCopyWithUniqueID())
        pg.addSubgroup(subgroup)
        
    return pg

def moveBlobs(blobs, offset):
    for b in blobs:
        b.center = numpy.array(b.center) + numpy.array(offset)

def automaticProcess(volume, pathToImages, grayThreshold, minSize, maxSize, useSubgroups, offset):
    # todo: make openImageStack return a volume rather than setting a global variable
    #openImageStack(pathToImages)
    blobs = findBlobs(volume, grayThreshold)
    
    moveBlobs(blobs, offset)
    
    doc = Document()
    doc.blobs = blobs
    doc.particleGroup = ParticleGroup()
    #doc.particleGroup.addSubgroup(subgroup)
    
#    if useSubgroups:
#        for p in particles:
#            doc.particleGroup.addSubgroup(
#    else:
#        for p in particles:
#            doc.particleGroup.addToSubgroup(0, p)

    if useSubgroups:
        doc.particleGroup = generateParticleGroupFromBlobs(blobsSmallerThan(blobs, pow(maxSize,3)))
        #doc.particleGroup = generateParticleGroupFromBlobs(blobs)
        
        #print ""
        #for p in particles:
        #    subgroup = []
        #    for i in range(0,5):
        #        #subgroup.append(copy.deepcopy(p))  # todo: it would be better to use a new particle function here incase the particles have unique id's in them
        #        subgroup.append(p.makeCopyWithUniqueID())
        #    doc.particleGroup.addSubgroup(subgroup)
    else:
        centers = centersOfBlobsLargerThan(blobsSmallerThan(blobs, pow(maxSize,3)), minSize)
        particles = makeParticlesAtPoints(centers)
        doc.particleGroup.addSubgroup(particles)
        

    # todo: this should take the volume as an argument
    #doc.edges = findEdges(doc.particles)
    
    return doc

def writeDocument(doc, filename):
    f = open(filename, "w")
    pickle.dump(doc, f)
    f.close()


def old_writeDocument(doc, baseFilename):
    pointList = []
    for i in range(0,len(doc.particles)):
        x = float(doc.particles[i].loc[0])
        y = float(doc.particles[i].loc[1])
        z = float(doc.particles[i].loc[2])
        
        pointList.append((x,y,z))

    print "writing files %s.pointList and %s.edges" % (baseFilename, baseFilename)

    f = open("%s.blobs" %baseFilename, "w")
    pickle.dump(doc.blobs, f)
    f.close()

    # todo: don't save this, just save the blobs and you will know what the points are by finding the blobs that are large enough
    f = open("%s.pointList" %baseFilename, "w")
    pickle.dump(pointList, f)
    f.close()
        
    f = open("%s.edges" %baseFilename, "w")
    pickle.dump(doc.edges, f)
    f.close()


def loadBlobsAndParticlesAndEdges(filename):
    
    
    ###f = open('%s.pointList' % form['saveToTextBox'].value)
    #f = open('%s.pointList' % 'output')
    
    # todo make these part of a global document and don't have individual global variables for blobs, particles, edges
    global blobs
    global particleGroup
    global edges
    
    f = open(filename)
    doc = pickle.load(f)
    f.close()
    
    # todo: there should be one global variable, the document, with members blobs, particleGroup, edges
    blobs = doc.blobs
    particleGroup = doc.particleGroup
    edges = doc.edges
    

def displayHelp(arg1):
    print 'Keyboard Contols:'
    print 'LEFT to move -x direction'
    print 'RIGHT to move +x direction'
    print 'UP to move +y direction'
    print 'DOWN to move -y direction'
    print '+ to move +z direction'
    print '- to move -z direction'
    print ''
    print 'Author: Richard Giuly, 2008'


    
#if 0: ###    
#    class StarControl(old_gui.Table):
#        
#        lineIntegralLabel = None
#        
#        #volume = zeros((3,3,3))
#        def __init__(self,volume):
#            old_gui.Table.__init__(self)
#            fg = (255,255,255)
#            
#            #self.tr()
#            #self.td(old_gui.Label("Image: ",color=fg),align=1)
#            #e = old_gui.HSlider(1,0,numImages-1,size=20,width=100,height=16,name='imageIndex')
#            #self.td(e)
#    
#            self.tr()
#            self.td(old_gui.Label("xIndex: ",color=fg),align=1)
#            e = old_gui.HSlider(1,0,2,size=20,width=100,height=16,name='xIndex')
#            self.td(e)
#    
#            #self.tr()
#            self.td(old_gui.Label("yIndex: ",color=fg),align=1)
#            e = old_gui.HSlider(1,0,2,size=20,width=100,height=16,name='yIndex')
#            self.td(e)
#    
#            #self.tr()
#            self.td(old_gui.Label("zIndex: ",color=fg),align=1)
#            e = old_gui.HSlider(1,0,2,size=20,width=100,height=16,name='zIndex')
#            self.td(e)
#    
#            initializePositionSliders(form,volume)
#    
#            self.tr()
#            self.td(old_gui.Label("Gray Gradient Force: ",color=fg),align=1)
#            e = old_gui.HSlider(300,0,800,size=20,width=100,height=16,name='grayGradientForce')
#            self.td(e)
#    
#            self.tr()
#            self.td(old_gui.Label("Particle Radius: ",color=fg),align=1)
#            e = old_gui.HSlider(3,2,20,size=20,width=100,height=16,name='particleRadius')
#            self.td(e)
#    
#      
#            
#            #self.tr()
#            #self.td(old_gui.Label("Size: ",color=fg),align=1)
#            #e = old_gui.HSlider(2,1,5,size=20,width=100,height=16,name='size')
#            #self.td(e)
#            
#            self.tr()
#            self.td(old_gui.Label("Enable Visuals: ",color=fg),align=1)
#            self.td(old_gui.Switch(value=False,name='visualsEnabled'),align=-1)
#    
#            self.tr()
#            self.td(old_gui.Label("Make New Particles: ",color=fg),align=1)
#            self.td(old_gui.Switch(value=False,name='makeNewParticles'),align=-1)
#    
#            self.tr()
#            self.td(old_gui.Label("Track Particle: ",color=fg),align=1)
#            self.td(old_gui.Switch(value=False,name='trackParticle'),align=-1)
#    
#            self.tr()
#            self.td(old_gui.Label("Select Particles: ",color=fg),align=1)
#            self.td(old_gui.Switch(value=False,name='selectParticle'),align=-1)
#    
#    
#            self.tr()
#            self.td(old_gui.Label("Threshold Enabled: ",color=fg),align=1)
#            self.td(old_gui.Switch(value=False,name='thresholdEnabled'),align=-1)
#            self.td(old_gui.Label(": ",color=fg),align=1)
#            e = old_gui.HSlider(90,0,300,size=20,width=100,height=16,name='grayThreshold')
#    
#            self.td(e)
#    
#    
#            self.tr()
#            self.td(old_gui.Label("Move Particles along Gradient: ",color=fg),align=1)
#            self.td(old_gui.Switch(value=False,name='moveParticlesAlongGradient'),align=-1)
#    
#    
#            
#            self.td(old_gui.Label("Radio"))
#            g = old_gui.Group()
#    
#            #self.tr()
#            #self.td(old_gui.Radio(g,value='selectOne'))
#            #self.td(old_gui.Label("Select One",color=fg),align=1)
#    
#            #self.tr()
#            #self.td(old_gui.Radio(g,value='selectGroup'))
#            #self.td(old_gui.Label("Select Group",color=fg),align=1)
#    
#            
#            
#            saveToTextBox = old_gui.Input("output",width=400,name='saveToTextBox')
#            self.tr()
#            button = old_gui.Button("Automatic process, save to: ")
#            self.td(button)
#            button.connect(old_gui.CLICK, automaticProcessButton, None)
#            self.td(saveToTextBox)
#    
#    
#            
#            pathInput = old_gui.Input(settings['defaultPath'],width=400,name='imageStackPathTextBox')
#            self.tr()
#            button = old_gui.Button("Open tif or bmp Stack in:")
#            self.td(button)
#            button.connect(old_gui.CLICK, loadImageStackButton, None)
#            self.td(pathInput)
#    
#    
#            self.tr()
#            self.td(old_gui.Label("Line integral: ",color=fg),align=1)
#            #self.lineIntegralLabel = old_gui.Label("--",color=fg) 
#            self.lineIntegralLabel = old_gui.Input("--",size=20) 
#            self.td(self.lineIntegralLabel,align=1)
#    
#    
#            self.tr()
#            button = old_gui.Button("Save Image Stack To: ")
#            button.connect(old_gui.CLICK, writeTiffStackButton, None)
#            self.td(button)
#            self.inputSaveStackPath = old_gui.Input("c:/temp/",size=20,name='saveImageStackPathTextBox') 
#            self.td(self.inputSaveStackPath,align=1)
    
    


#def initializePositionSliders(form, volume):
#
#    form['xIndex'].value = int(volume.shape[0] / 2)
#    form['xIndex'].min = 0
#    form['xIndex'].max = volume.shape[0]-1
#
#    form['yIndex'].value = int(volume.shape[1] / 2)
#    form['yIndex'].min = 0
#    form['yIndex'].max = volume.shape[1]-1
#
#    form['zIndex'].value = int(volume.shape[2] / 2)
#    form['zIndex'].min = 0
 #   form['zIndex'].max = volume.shape[2]-1


#def numberOfImagesInStack(path):
#    fileList = os.listdir(path)
#    fileList = stringsWithImageFileExtensions(fileList)
#    return len(fileList)

def imageStackShape(path):
    fileList = os.listdir(path)
    fileList = stringsWithImageFileExtensions(fileList)
    if len(fileList) == 0:
        raise Exception, "There is no image stack in the folder %s" % path
    
    filename = path + fileList[0]    
     
    # from the PIL documentation:
    # "This is a lazy operation; the actual image data is not read from the file until you try to process the data"
    # this will allow us to read the file size without reading the full contents of the file
    image = Image.open(filename)    

    #return (image.size[1], image.size[0], len(fileList))
    return (image.size[0], image.size[1], len(fileList))
    

# todo: make subvolumeBox an optional parameter
def loadImageStack(path, subvolumeBox):
    
    global volumes
    
    
    #volume = volumes['Original']
    
    fileList = os.listdir(path)
    fileList = stringsWithImageFileExtensions(fileList)
    fileList.sort()
    print fileList
        
    numImages = len(fileList)

    firstImage = True
    #import pygame
    
    
    if subvolumeBox == None:
        NOT_SET = -1
        box = Box((NOT_SET,NOT_SET,0),(NOT_SET,NOT_SET,numImages))
    else:
        box = subvolumeBox
    
    # for each z coordinate    
    for i in range(box.cornerA[2], box.cornerB[2]):

        #if hostname == "panther":
        #        filename = "I:/ncmir_data/caulobacter/bmp/c%03d.bmp" % i
        #else:
        #        filename = "/ncmir_data/caulobacter/bmp/c%03d.bmp" % i
        
        filename = path + fileList[i]    
            
        #surface1 = pygame.image.load(filename)
        #array3dFromSurface = pygame.surfarray.array3d(surface1)
        #array2d = array3dFromSurface[:,:,RED]

        im1 = Image.open(filename)
        im1 = im1.transpose(Image.ROTATE_270)
        #im1 = im1.transpose(Image.ROTATE_180)
        im1 = im1.transpose(Image.FLIP_LEFT_RIGHT)

        array2d = numpy.fromstring(im1.tostring(), uint8)
        #a = a.T
        #array2d = a
        print "loading image index %d, number of images %d" % (i, numImages)
        print 'array2d shape'
        print array2d.shape
        print im1.size[0] * im1.size[1]
        
        if im1.size[0] * im1.size[1] != array2d.shape[0]:
            print 'error: problem loading the image %s. possible problem: it has to be 8bit to work' % filename
        else:
                   
            array2d.shape = im1.size[1], im1.size[0]
            #print "old shape %d %d" % (im1.size[1], im1.size[0])
            
            if (subvolumeBox == None):
                box.cornerA[0] = 0
                box.cornerB[0] = im1.size[1]
            
                box.cornerA[1] = 0
                box.cornerB[1] = im1.size[0]
    
            # get X and Y dimensions from the first image and initialize the 3D volume
            if firstImage:
                #volume = numpy.zeros((imRed.shape[0],imRed.shape[1],numImages))
                ##volume = numpy.zeros((array2d.shape[0],array2d.shape[1],numImages),Float32)

                #print "shape %s" % str(box.shape())
                #print "array2d %s" % str(array2d.shape)
                
                volume = numpy.zeros(box.shape(), numpy.uint8)

                firstImage = False
    
            #volume[:,:,i] = numpy.asarray(imRed)
            
    
            #volume[:,:,i] = array2d.T
            print "i shape cornerA cornerB" 
            print (i, array2d.shape, box.cornerA, box.cornerB)
            
            volume[:,:,i-box.cornerA[2]] = array2d[box.cornerA[0]:box.cornerB[0], box.cornerA[1]:box.cornerB[1]] 
            ##todo: make the lines below work
            ##old_gui.xIndex.config(from_=0,to=volume.shape[0]-1)
            ##old_gui.yIndex.config(from_=0,to=volume.shape[1]-1)
            ##old_gui.zIndex.config(from_=0,to=volume.shape[2]-1)
            
    
            #for index1 in range(0,array3dFromSurface.shape[0]):
            #    for index2 in range(0,array3dFromSurface.shape[1]):
            #        #volume[index1,index2,i] = array3dFromSurface[index1,index2,0]
            #        volume[index1,index2,i] = index2 
                    
            ###global form
            ###initializePositionSliders(form,volume)
    
        #volume[:,:,:] = 100
        #for i in range(0,volume.shape[0]):
        #    for j in range(0,volume.shape[1]):
        #        for k in range(0,volume.shape[2]):
        #            volume[i,j,k] = (i + j + k) * 10
        
        
    volumes['Original'] = volume
    #volume[0:5,0:10,0:20] = 100
    return volume
    
    

def makeParticlesAtBlobCentersButton(arg1):
    print 'makeParticlesAtBlobCenters'
    #print arg1 
    global particles
    particles = makeParticlesAtPoints(blobCenters)


def makeParticlesAtPoints(points):
    particleList = []
    for location in points:
        p = makeParticle(location)
        particleList.append(p)
    return particleList
        
def calculateAndSaveBlobCenters(arg1):
    global blobCenters
    file = open("blobCenters.pickle", "w")
    b = findBlobs(volume, form['grayThreshold'].value, sizeThreshold)
    print b
    writePointList(b,file)
    file.close()
    blobCenters = b #store in global variable
    

def loadBlobCenters(arg1):
    global blobCenters
    print 'loadBlobCenters'
    file = open("blobCenters.pickle", "rb")
    #print file
    blobCenters = readPointList(file)
    print blobCenters
    file.close()


def distance(vector1,vector2):
    return numpy.linalg.norm(vector2-vector1)

#def reverseIndicies(v):
#    print 'reverse indicies'
#    v1 = numpy.zeros((v.shape[2],v.shape[1],v.shape[0]))
#    for i in range(0,v.shape[0]):
#        print "%d out of %d" % (i,v.shape[0])
#        for j in range(0,v.shape[1]):
#            for k in range(0,v.shape[2]):
#                v1[k,j,i] = v[i,j,k]
#    return v1;

def findBlobs(volume, grayThreshold):
    
    # this should not be here, it's a temporary setting
    #grayThreshold = 1.8
    
    from mlabwrap import mlab

    
    #the volume1 variable is used mainly just so i can resize the volume with the following line if needed (other reason is that i wanted the flatten from numpy which worked with the resized array whereas the .flatten of Numeric did not work):
    #volume1 = numpy.array(volume[0:250,000:250,0:10])
    
    #volume1 = numpy.array(volume)
    
    #rev = reverseIndicies(volume1)
    
    #TRUE = 1
    FALSE = 0
    showResults = FALSE
    
    #centroids, areas = mlab.findBlobs(volume.flat,grayThreshold,volume.shape[0],volume.shape[1],volume.shape[2],nout=2)
    centroidsMatrix, areas = mlab.findBlobs(volume.flatten(),volume.shape[2],volume.shape[1],volume.shape[0],grayThreshold,showResults,nout=2)
    # all centers expected to be too high by one pixel because matlab starts array index at 1 and python starts at 0

    #centroids = [];
    #for i in range(0,centroidsMatrix.shape[0])
    #    centroids.append(centroidsMatrix(i,:));
    #print 'areas'
    #print areas[0]
    
    
    blobs = [];
    #for i in range(0,centroidsMatrix.shape[0]):
    #    center = numpy.array([centroidsMatrix[i,1],centroidsMatrix[i,0],centroidsMatrix[i,2]])
    #    blobVolume = areas[0,i]
    #    blobs.append(Blob(center,blobVolume))
    
    centroids = matlabToPythonPointList(centroidsMatrix)
    
    for i in range(0,centroidsMatrix.shape[0]):
        center = centroids[i]
        blobVolume = areas[0,i]
        blobs.append(Blob(center,blobVolume))


    return blobs


def watershed(volume, connectivity):
    
    from mlabwrap import mlab
    watershedVolumeFlattenedArray = mlab.watershedWrapper(volume.flatten(),volume.shape[2],volume.shape[1],volume.shape[0],connectivity)
    watershedVolumeFlattenedArray.shape = volume.shape
    return watershedVolumeFlattenedArray


def matlabToPythonPointList(matlabPointList):
    newPoints = []
    for point in matlabPointList:
        newPoints.append(numpy.array((point[2]-1, point[0]-1, point[1]-1)))
    return newPoints


def centersOfBlobsLargerThan(blobs, sizeThreshold):
    centers = []
    for b in blobs:
        if b.size > sizeThreshold:
            centers.append(b.center)
    return centers

def blobsSmallerThan(blobs, sizeThreshold):
    newList = []
    for b in blobs:
        if b.size < sizeThreshold:
            newList.append(b)
    return newList

#print distance(array([0,0,3]),array([0,0,-1]))

particleIDCount = 0

class ParticleGroup:
    def __init__(self):
        self.subgroups = []
        #self.colorOfSubgroups = [[0, 255, 0]]
        self.colorOfSubgroups = []
        
    def addToSubgroup(self, subgroupIndex, particle):
        self.subgroups[subgroupIndex].append(particle)
    
    def getSubgroup(self, subgroupIndex):
        return self.subgroups[subgroupIndex]
    
    def addEmptySubgroup(self):
        self.subgroups.append([])
        self.colorOfSubgroups.append([255*random.random(), 255*random.random(), 255])

    def addSubgroup(self, subgroup):
        self.subgroups.append(subgroup)
        self.colorOfSubgroups.append([255*random.random(), 255*random.random(), 255])
        
    def getSubgroups(self):
        return self.subgroups
    
    def getColorOfSubgroup(self, subgroupIndex):
        #print subgroupIndex
        #print self.colorOfSubgroups
        return self.colorOfSubgroups[subgroupIndex]
    
    def getAll(self):
        all = []
        for subgroup in self.subgroups:
            all = all + subgroup
        return all
        
    # casts point coordinates to integers and checks to see if they match
    def containsIntegerPoint(self, pointWithIntegerCoordinates):
        all = self.getAll()
        for p in all:
            if numpy.alltrue(numpy.int_(p.loc) == pointWithIntegerCoordinates):
                return True
        return False
    
        

#class ParticleSubgroup should extend the list class
        

class Particle:
    
        # todo: i think these are class variable that are not used, so they can be removed
        x = array([0.,0.,0.])
        v = array([0.,0.,0.])
        color = (0.,0.,0.)
        
        # used to return color of background to what it should be
        backgroundColor = (0.,0.,0.)
        id = -1
                
        #graphicsObjectHandle = None
        
        def makeCopyWithUniqueID(self):
            global particleIDCount
            p = copy.deepcopy(self)
            particleIDCount = particleIDCount + 1
            p.id = particleIDCount
            return p

        
        
def saveParticlesToPSI(filename, scaleFactors):
    
    particles = particleGroup.getAll()
    
    file = open(filename,'w')
    headerText = '# PSI Format 1.0\n#\n# column[0] = "x"\n# column[1] = "y"\n# column[2] = "z"\n%d 0 0\n1.00 0.00 0.00\n0.00 1.00 0.00\n0.00 0.00 1.00\n\n' % len(particles)
    
    file.write(headerText)
    
    useIntegers = False
    centers = []
    separator = " "
    for p in particles:
        centers.append(p.loc)
    writePointListText(centers, file, scaleFactors, useIntegers, separator)
    
    file.close()



def writePointList(points, file):
    # save as list of lists because pickling the list of numpy or Numeric arrays doesn't seem to work
    pointList = []
    for p in points:
        coordinateList = []
        for i in range(0,len(p)):
            coordinateList.append(float(p[i]))
        pointList.append(coordinateList)
    pickle.dump(pointList, file)



def readPointList(file):
    points = []
    
    pointList = pickle.load(file)
    
   
    for coordinateList in pointList:
        point = numpy.array(coordinateList)

        
        points.append(point)

    return points


def writePointListText(points, file, scaleFactors=(1,1,1), useIntegers=False, separator=","):
    # save to comma separated value file
    for p in points:
        for i in range(0,len(p)):
            
            value = p[i] * scaleFactors[i]
            
            if useIntegers:
                num = int(value)
            else:
                num = value
            
            # leaves the comma out if it's the last element on the line
            if i != (len(p)-1):
                text = ("%f" + separator) % num
            else:
                text = "%f" % num
                
            file.write(text)
        file.write("\n")



def saveParticleCentersCSV(param1):
    print 'saveBlobCenters'
    file = open('particles.csv', 'w')
    centers = []
    for p in particles:
        centers.append(p.loc)
    useIntegers = True
    writePointListText(centers, file, scaleFactorsFromGUI(), useIntegers)
    file.close()


def selectNothing(arg1):
    global selectedParticles
    # todo: if there is a "make list empty" method, use that
    selectedParticles = []

def deleteSelectedParticles(arg1):
    global selectedParticles
    for p in selectedParticles:
        particles.remove(p)
    selectedParticles = []
    
def lineIntegral(volume, point1, point2):
    #print point1
    #print point2
    diff = point2 - point1
    # take steps of length 1
    dist = numpy.linalg.norm(diff)
    
    if dist == 0:
        return 0
    
    step = diff / dist
    
    #number of iterations. taking steps of size 1.
    N = int(round(dist))
    
    total = 0
    for i in range(0,N):
        position = point1 + (float(i) * step)
        total += volume[int(position[0]),int(position[1]),int(position[2])]
        
    return total
    
edges = []
    
def findEdges(particles):
    edges = []
    for i in range(0,len(particles)-1):
        print "%d out of %d" % (i,len(particles)-1)
        for j in range(i+1,len(particles)):
            #print "i %d" % i
            #print "j %d" % j
            dist = distance(particles[i].loc,particles[j].loc)
            
            # Only compute the line integral if the distance is reasonable small. This check for small distance is done because the line integral is computationally expensive.
            if dist < 40:
#                if lineIntegral(volume,particles[i].x,particles[j].x) < 1900:
                if lineIntegral(volume,particles[i].loc,particles[j].loc) < 19:
                    edge = Edge()
                    edge.node1 = i
                    edge.node2 = j
                    edges.append(edge)
                    print edge
    return edges

def findEdgesButton(arg1):
    global edges
    edges = findEdges(particles)
                            

      

#def stringsWith(listOfStrings, str):
#    result = []
#    for s in listOfStrings:
#        if s.find(str) != -1:
#            result.append(s)
#    return result


def stringsWithImageFileExtensions(listOfStrings):
    #todo: string comparison should ignore case
    result = []
    for s in listOfStrings:
        if (s.find('.tif') != -1) or (s.find('.bmp') != -1):
            result.append(s)
    return result


def fillCube(volume, center, edgeWidth):
    
    
    half = edgeWidth/2
    #half = 0
    # boundaries of cube
    
    a = numpy.array([0,0,0])
    b = numpy.array([0,0,0])

    c =    [int(center[0]),int(center[1]),int(center[2])] 

    
    for i in range(0,3):
        a[i] = c[i] - half
        b[i] = c[i] + half
        
        if a[i] < 0 or a[i] >= (volume.shape[i]):
            print 'error1'
            return
            print 'error'
        if b[i] < 0 or b[i] >= (volume.shape[i]):
            print 'error1'
            return
            print 'error'
        
    
    # todo: it would be nice to use an increment so that when they are overlapping the number is higher and you notice the overlp, like a += rather than an =
    volume[a[0]:b[0],a[1]:b[1],a[2]:b[2]] = 200
    #print c
    #print volume.shape
    #volume[1,1,1] = 200
    #volume[c[0],c[1],:] = 200
    #print "starting access"
    #print c
    #print volume.shape
    #volume[c[0],c[1],c[2]] = 200
    #print "ending access"
    

def isInsideVolume(volume, point):
    s = volume.shape
    if point[0] < s[0] and point[1] < s[1] and point[2] < s[2] and point[0] >= 0 and point[1] >= 0 and point[2] >= 0:
        return True
    else:
        return False

def structureTensor(xG, yG, zG):
    # xG = x gradient
    # yG = y gradient
    # zG = z gradient
    return array([[pow(xG,2), xG*yG, xG*zG],
                  [xG*yG, pow(yG,2), yG*zG],
                  [xG*zG, yG*zG, pow(zG,2)]])

    

def fillSphere(volume, center, radius):
    for x in range(-radius+center[0], radius+center[0]):
        for y in range(-radius+center[1], radius+center[1]):
            for z in range(-radius+center[2], radius+center[2]):
                if isInsideVolume(volume, [x,y,z]):
                    if sqrt(pow((x-center[0]),2) + pow((y-center[1]),2) + pow((z-center[2]),2)) < radius:
                        volume[x,y,z] = 255
                    
            
    

def drawParticlesInVolume(volume, particles, settingsTree):
    count = 0
    for p in particles:
        count = count + 1
        #print count
        #print "out of"
        #print len(particles)
        #print p
        #print p.x
        #print volume.shape
        
        #fillCube(volume, p.x, 5)
        fillSphere(volume, p.loc, getNode(settingsTree, ('particleMotionTool','particleRadius')).get())









def plotBlobSizes(blobs):

    import pylab

    blobIndices = arange(0,len(blobs),1)
    blobSizes = zeros(len(blobs))
    for i in range(0,len(blobs)):
        blobSizes[i] = blobs[i].size
        
    pylab.plot(blobIndices, blobSizes, linewidth=1.0)
    pylab.grid(True)
    pylab.show()
    
                        
def writeTiffStackButton(arg1):
    writeTiffStack(form['saveImageStackPathTextBox'].value, volume, volume, volume)                        
                         
# todo: path and filename combining should be done with a function for certain operating system i think
def writeTiffStack_version1(path, redVolume, greenVolume, blueVolume):
    maxValue = 255
    
    #path = 'c:/temp/'
    for i in range(0,redVolume.shape[2]):
        # all the volumes of each color should have the same dimensions (shape)
        colorImageArray = numpy.zeros((redVolume.shape[0], redVolume.shape[1], 3), numpy.uint8)
        
        colorImageArray[:,:,0] = redVolume[:,:,i]
        colorImageArray[:,:,1] = greenVolume[:,:,i]
        colorImageArray[:,:,2] = blueVolume[:,:,i]
        #colorImageArray[:,:,3] = maxValue
        
        #image = Image.fromarray(colorImageArray, 'RGB')
        
        image = Image.fromstring("F", (a.shape[1],a.shape[0]), a.tostring())
        
        
        fullName = path + ('output%0.3d' % i) + '.tiff'
        print fullName
        image.save(fullName)

def writeTiffStack(path, volume):
    maxValue = 255
    
    a = numpy.zeros((volume.shape[0], volume.shape[1]), int8)
    
    #path = 'c:/temp/'
    for i in range(0,volume.shape[2]):

        #a[:,:] = 
        a[:,:] = volume[:,:,i]
        
        image = Image.fromstring("L", (a.shape[1],a.shape[0]), a.tostring())
        
        
        fullName = path + ('output%0.3d' % i) + '.bmp'
        print fullName
        image.save(fullName)
        
        
class TimerHandler(wx.EvtHandler):

    #def OnTimerEvent(self, evt):
    #     print 'timer'
    #     updateParticlePositions()
    
    def onTimerEvent(self, evt):
        #print 'timer'
        updateParticlePositions()
        a = 1


         
def updateParticlePositions(volume, settingsTree, offsetOfLoadedVolumeInFullVolume):
    
    global count
    
    index=0
    count = count + 1
    #print form['speed'].value
    #totalMovement = 0
    totalForceSum = 0
    

    #if inside the event handling for loop this tends to miss the last motion you make on the slider
    if 0:
        newResults = form.results()
    #if lastResults['imageIndex'] != newResults['imageIndex']:
    #    #print 'imageIndex'
    #    #print form['imageIndex'].value
    #
    #    imageIndex = form['imageIndex'].value
    
    
    if 0:
    #if count % 100 == 0: 
        #if old_old_gui.thresholdEnabled.get():
        if (getNode(old_old_gui.settingsTree, ('particleMotionTool','thresholdEnabled'))).get():
            #threshold = old_old_gui.grayThreshold.get()
            threshold = (getNode(old_gui.settingsTree, ('particleMotionTool','grayThreshold'))).get()
        else:
            threshold = None
        
        #print 'hello'

        drawViews(volume, ((getNode(old_gui.settingsTree, ('imageControls','xIndex'))).get(),
                      (getNode(old_gui.settingsTree, ('imageControls','yIndex'))).get(),
                      (getNode(old_gui.settingsTree, ('imageControls','zIndex'))).get()), threshold)
        
        old_gui.updateParticleGraphics()
        
        if 0:        
            
            # draw centers of dark spots in image
            #for blobCenter in blobCenters:
            #    drawCircleInAllViews(blobCenter, (200,200,0), 3)
    
            # update label that shows line integral between particles
            if len(selectedParticles) >= 2: 
                table.lineIntegralLabel.value = "(%f)" % lineIntegral(volume, selectedParticles[0].loc, selectedParticles[1].loc)
            
            # draw connections between close ribosomes
            drawEdges(edges)
            #print edges


    if 0:    
        lastResults = newResults

    if 0:
        for event in pygame.event.get():
            
    
    
            
            if event.type == pygame.QUIT: sys.exit()
      
            if event.type == pygame.KEYDOWN:
                #print 'keydown'
                #print event.key
                if currentParticle != None:
                    if event.key == pygame.K_RIGHT:
                        currentParticle.loc[0] += 1
                    if event.key == pygame.K_LEFT:
                        currentParticle.loc[0] += -1
                    if event.key == pygame.K_UP:
                        currentParticle.loc[1] += -1
                    if event.key == pygame.K_DOWN:
                        currentParticle.loc[1] += 1
                    if event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                        currentParticle.loc[2] += 1
                    if event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                        currentParticle.loc[2] += -1
                
            #print form['grayGradientForce'].value    
            app.event(event)
        if 0:    
            if (form['trackParticle'].value):
                if currentParticle != None:
                    form['xIndex'].value = currentParticle.loc[0];
                    form['yIndex'].value = currentParticle.loc[1];
                    form['zIndex'].value = currentParticle.loc[2];



    # calculation location of every particle
    #if (getNode(settingsTree, ('particleMotionTool','moveParticlesAlongGradient'))).get():  
    if 1:
        #for particle in selectedParticles:
        
        #for particles in particleGroup.getSubgroups():
        lastGroup = [particleGroup.getSubgroups()[-1]]
        for particles in lastGroup:
            for particle in particles:   
    
                xr = array([int(floor(particle.loc[0])), int(floor(particle.loc[1])), int(floor(particle.loc[2]))]) - offsetOfLoadedVolumeInFullVolume 
                
                d = (getNode(settingsTree, ('particleMotionTool','particleRadius'))).get() # offset for calculating gradient
                
                # check if particle is still located inside of volume
                outOfRange = False
                for k in range(0,3):
                    if xr[k] <= (d+1):
                        xr[k]=d
                        outOfRange = True
                    if xr[k] >= volume.shape[k]-(d+1):
                        xr[k]=volume.shape[k]-(d+1)
                        outOfRange = True
    
                #if outOfRange:
                #    particles.remove(particle)
                #if outOfRange:
                #    continue
    
        
                # todo: could you use xr[2] rather than zIndex here?
                #c = volume[xr[0], xr[1], form['zIndex'].value]
                #screen.set_at((xr[0], xr[1]), (c,c,c))
                
            

                dx[0] = double(volume[xr[0]+d, xr[1], xr[2]]) - double(volume[xr[0]-d, xr[1], xr[2]])
                dx[1] = double(volume[xr[0], xr[1]+d, xr[2]]) - double(volume[xr[0], xr[1]-d, xr[2]])
                dx[2] = double(volume[xr[0], xr[1], xr[2]+d]) - double(volume[xr[0], xr[1], xr[2]-d])
            
                #todo: this calulates things twice from a to b and b to a and doesn't need to, the distance measuring thing for particles does it twice when it doesn't need to
                # calculate force exerted by other particles on the current particle
                forceFromOthers = array([0,0,0]);
                for j in range(0,len(particles)):
                    #print "id %d %d" % (particle.id, particles[j].id)
                    if particle.id != particles[j].id: 
                        dist = distance(particle.loc, particles[j].loc)
                        #magnitude = 1000000.0/pow(dist,2)
                        
                        #magnitude = 100.0/pow(dist,2)
                        #print dist
                        R = (getNode(settingsTree, ('particleMotionTool','particleRadius'))).get()
                        reverseFactor = 1
                        if dist < 2 * R: # push away from nearby particle
                            magnitude = 1
                        elif dist > 2.4 * R and dist < 4 * R:   # (<4 or <5 seemed to work) pull closer to particle that somewhat close
                            #magnitude = 0
                            magnitude = 0.1 #what if you leave this line out... you did once before
                            reverseFactor = -1
                        else:
                            magnitude = 0
                        
                        # todo: if dist is zero this is an error
                        if dist > 0.000001:
                            direction = reverseFactor*((particle.loc - particles[j].loc)/dist)
                        else:
                            # todo: it would be better to make this random
                            direction = array([1,0,0])
                        
                        #print [direction, magnitude]
                        forceFromOthers = forceFromOthers + direction*magnitude    
            
                dt = .1
                grayFactor = (double((getNode(settingsTree, ('particleMotionTool','grayGradientForce'))).get())/100.0)
                F = -grayFactor*dx #+ forceFromOthers # todo: take fourceFromOthers out of this
                #F = forceFromOthers
                #print forceFromOthers
                
                m = 100.
                
                particle.v = (particle.v * .95) + (F/m)*dt
                
        
                randomStepSize = double((getNode(settingsTree, ('particleMotionTool','randomStepSize'))).get())/20.0
                offset =  randomStepSize * (array([random.random(),random.random(),random.random()]) - [0.5,0.5,0.5])
                
                #angle = 2.0 * 3.14 * random.random()
                #offset = [.4*sin(angle),.4*cos(angle),0] #todo: why is this zero in the z direction
                
                
                #total = total + offset
                count = count+1;
                
                #normOfForceFromOthers = numpy.linalg.norm(forceFromOthers)
                #if normOfForceFromOthers < .00000001:
                #    displacementFromOthers = numpy.array([0.,0.,0.])
                #else:
                #    displacementFromOthers = forceFromOthers/normOfForceFromOthers
                
                displacementFromOthers = forceFromOthers * double((getNode(settingsTree, ('particleMotionTool','repulsiveForce'))).get())/100.0
                #print "displacementFromOthers"
                #print displacementFromOthers
                #print forceFromOthers

                #print displacementFromOthers
                change = dt*particle.v + (0.5 * (F/m) * (dt*dt))  + offset + displacementFromOthers
                particle.loc = particle.loc + change
                
                #totalMovement += numpy.linalg.norm(change)
                totalForceSum += numpy.linalg.norm(dt*particle.v + (0.5 * (F/m) * (dt*dt)) + displacementFromOthers)
        
                #particle.backgroundColor = screen.get_at((particle.x[0], particle.x[1]))
                #screen.set_at((particle.x[0], particle.x[1]), particle.color)
                
    #return totalMovement
    return totalForceSum
        
    
         

###pygame.init()

A = zeros((3,3,3))
A[2] = [[1,3,4],[2,4,2],[3,4,5]]
print A

size = width, height = 1000, 760
speed = [1, 1]
black = 0, 0, 0

###screen = pygame.display.set_mode(size)






#ball = pygame.image.load("ball.bmp")


RED = 0
GREEN = 1
BLUE = 2

from socket import gethostname; hostname = gethostname()

#########################################################################
#########################################################################




#if len(sys.argv) > 1:
#    defaultPath = '/home/rgiuly/cs/for_rgiuly/calbmp/'
#    openImageStack(defaultPath)
#    loadParticlesAndEdges(None)
#    red = zeros(volume.shape)
#    drawParticlesInVolume(red, particles)
#    writeTiffStack('/crbsdata1/rgiuly/tmp/', red, volume, volume)
  



# test volume
#volume = Numeric.ones((20,20,20))  * 200
#volume[3,4,5] =1
#volume[13,14,15] = 1


#screen = pygame.display.set_mode((640,480),SWSURFACE)
###form = old_gui.Form()
###app = old_gui.App()


##volume = numpy.ones((40,140,30), Float32) * 100

#volumes = {}
volumes = odict()

borderWidthForFeatures = 1
    


volumes['Original'] = numpy.ones((20,70,15)) * 100
# make the array a gradient
for i in range(0,volumes['Original'].shape[0]):
    for j in range(0,volumes['Original'].shape[1]):
        for k in range(0,volumes['Original'].shape[2]):
            volumes['Original'][i,j,k] = (i + j + k) * 10


volumes['Temporary'] = numpy.ones((40,140,30)) * 100
# make the array a gradient
for i in range(0,volumes['Temporary'].shape[0]):
    for j in range(0,volumes['Temporary'].shape[1]):
        for k in range(0,volumes['Temporary'].shape[2]):
            volumes['Temporary'][i,j,k] = (i + j + k) * 1


###table = StarControl(volume)



###container = old_gui.Container(align=-1,valign=-1)
###container.add(table,0,400)

if 0: ###
    menus = old_gui.Menus([
    ("Menu/Make Particles at Blob Centers", makeParticlesAtBlobCentersButton, None),
    ("Menu/Calculate and Save Blob Centers", calculateAndSaveBlobCenters, None),
    ("Menu/Load Blob Centers", loadBlobCenters, None),
    ("Menu/Save Centers to particles.csv", saveParticleCentersCSV, None),
    ("Menu/Select Nothing", selectNothing, None),
    ("Menu/Delete Selected Particles", deleteSelectedParticles, None),
    ("Menu/Find Edges",  findEdgesButton, None),
    ("Menu/Display 3D", display3D, None),
    ("Menu/Help",  displayHelp, None),
    ("Menu/Load Particles and Edges", loadParticlesAndEdges, None),
    ("Menu/Draw Particles in Volume", drawParticlesInVolumeButton, None)
    ])
    





#particles = []

particleGroup = ParticleGroup()


F = array([0.0,0.0,0.0])
dx = array([0.0,0.0,0.0])
    

total = array([0.0,0.0,0.0])
#count = 0

#imageIndex = 0
###lastResults = form.results()

gapDistance = 5

def numpyToNumeric2D(numpyArray):
    a = Numeric.zeros((numpyArray.shape[0], numpyArray.shape[1]))
    for i in range(0,numpyArray.shape[0]):
        for j in range(0,numpyArray.shape[1]):
            a[i,j] = numpyArray[i,j]
    return a

im = None
photoImage = None
label = None
globalCount = 0


def drawCircleInAllViews(location, color, radius):
    # xy view
    pygame.draw.circle(screen,color,(location[0],location[1]),radius,1)
    
    # xz view
    pygame.draw.circle(screen,color,(location[0],location[2]+volume.shape[1]+gapDistance),radius,1)
    
    # yz view
    pygame.draw.circle(screen,color,(location[2]+volume.shape[0]+gapDistance, location[1]),radius,1)
    
def closestParticle(location):
    # location is an x y location
    minValue = distance(array([location[0],location[1]]), array([particles[0].loc[0], particles[0].loc[1]]))
    closest = particles[0]
    for i in range(0,len(particles)):
        dist = distance(array([location[0],location[1]]), array([particles[i].loc[0], particles[i].loc[1]]))
        if dist < minValue:
            closest = particles[i]
            minValue = dist
            
    return closest

def drawEdges(edges):
    for edge in edges:
        x1 = particles[edge.node1].loc[0]
        y1 = particles[edge.node1].loc[1]

        x2 = particles[edge.node2].loc[0]
        y2 = particles[edge.node2].loc[1]

        pygame.draw.line(screen,(200,0,200),(x1,y1),(x2,y2),1)


# 3D gaussian
global defaultType
defaultType = numpy.float32
def gaussian(shape, position, amplitude, sigma):
    # sigma is fatness
    volume = zeros(shape, defaultType)
    for x in range(0, shape[0]):
        for y in range(0, shape[1]):
            for z in range(0, shape[2]):
                dist = distance(position, array([x,y,z]))
                #volume[x,y,z] = dist * 20
                volume[x,y,z] = amplitude * exp(-pow(dist, 2) / (2*pow(sigma,2)))
    return volume
            

def at(volume, point):
    return volume[point[0],point[1],point[2]]

def isInsideVolumeWithBorder(volume, point, border):
    s = volume.shape
    if point[0] < s[0] - border and point[1] < s[1] - border and point[2] < s[2] - border and point[0] >= border and point[1] >= border and point[2] >= border:
        return True
    else:
        return False

    
    
     
    
####################################################

print sys.argv    
    
    
    



    

#blobCenters = findBlobs(volume,grayThreshold,sizeThreshold)
#blobCenters = findBlobs(volume,grayThreshold,0)
blobCenters = []

#print 'value_from_volume'
#print volume[5,5,5]

# main loop
#currentParticle = particles[0]
currentParticle = None
count = 0
#selectedParticles = copy.copy(particleGroup.getSubgroup(0)) 

#setToDefaultSettings()
#writeSettings()
initialize() 
dn = DataNode("test_name", "test_type", "test_params", "test_value")
#settingsTree = dn.makeGUITree()

filenames = ['O:\images\LFong\cropped\8bit_smaller\8bit_smaller0000.tif' ]

timerHandlerTest = TimerHandler()




# "CytoSeg, Copyright Richard J Giuly 2008"



