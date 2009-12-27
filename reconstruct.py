#3D Measuring Tool
#Copyright (C) 2008 Richard J Giuly
#
#This library is free software; you can redistribute it and/or
#modify it under the terms of the GNU Lesser General Public
#License as published by the Free Software Foundation; either
#version 2.1 of the License, or (at your option) any later version.
#
#This library is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#Lesser General Public License for more details.


pathToReconstructFiles = "./reconstruct_data/"

import xml.dom.minidom
import string
from visual import *
import numpy
import os
import random
import copy
#doc = xml.dom.minidom.Document()


class Group:
    #members = []
    #color = (1,1,1)
    def __init__(self, m, c=(1,1,1)):
        self.members = m
        self.color = c
        self.label = label(pos=(0,0,0),text="hello")
        self.label.visible = False

    def setColor(self, c):
        for m in self.members:
            m.setColor(c)

    def addMember(self, m):
        self.members.append(m)
        self.label.pos = self.members[0].centerPoint()
        self.label.visible = True
        
    def mostDistantPoints(self):
        allPoints = []
        
        # this could be more general, like contours are nodes and nodes have children and groups are nodes and groups have children
        #for contour in members
         #   allPoints = allPoints + contour.points
        
        
        # todo: handle error of not enough points
        
        # initialize
        point1 = allPoints[0]
        point2 = allPoints[1]
        minDist = numpy.linalg.norm(allPoints[0] - allPoints[1])

        # todo: this counts everthing twice, not totally efficient
        #for i in range(0, len(allPoints)):
        #    for j in range(0, len(allPoints))
        #        dist = numpy.linalg.norm(allPoints[i] - allPoints[j])
        #        if dist < minDist:
        #            point1 = allPoints[i]
        #            point2 = allPoints[j]
                    
                


class Contour:
    #points = []
    #graphicsObjects = []
    #color = (1,1,1)
    def __init__(self, p, c=(1,1,1)):
        self.points = p
        self.color = c
        self.graphicsObjects = []
        self.marker = sphere(pos=(0,0,0), color=(1,0,0), radius=.15)
        self.marker.visible = False

        
    def hasGraphicsObject(self, object):
        value = False
        for g in self.graphicsObjects:
            if g == object:
                value = True
        return value
    
    def centerPoint(self):
        total = numpy.array([0,0,0])
        for p in self.points:
            total += p

        #return total / len(self.points)
        return self.points[0]
    
    def update(self):
        self.marker.pos = self.centerPoint()
        
    def setColor(self, c):
        for g in self.graphicsObjects:
            g.color = c
        
    #todo: def set point list, then you don't need update



class Path:

    def __init__(self, idParameter):
        #rdict = Registry.GetKey('MyScript', True)
        self.points = []
        self.label = None #label(pos=[0,0,0], text='new')
        self.curveObject = None
        self.id = idParameter  
        self.graphicsObjects = []
        #nameString = 'item%d' % rdict['count']
        #rdict['count'] += 1
        
        #tex = Text3d.New(nameString)
        #tex.setText('%d' % idParameter)
        #self.id = idParameter
        #label = tex

        #print tex
        #cur = Scene.getCurrent()

        #ob = Object.New('Text')
        #ob.link(tex)
        #cur.link(ob)        
        #ob.makeDisplayList()
        
        #self.textObject = ob
        
        #Blender.Window.RedrawAll()
        #label.setText('x') # once redraw all is called this comand won't do anything
                
#    def updateTextLocation(self):
#        self.textObject.LocX = self.points[0][0]
#        self.textObject.LocY = self.points[0][1]
#        self.textObject.LocZ = self.points[0][2]
                
    def draw(self):
        
             
             if len(self.points) > 0:
                 labelPosition = self.points[0]
             else:
                 labelPosition = (0,0,0)
             
             
#        for i in range(1, len(self.points)):
#            makeEdge(self.points[i-1],self.points[i])
             self.curveObject = curve(pos=self.points, radius=0.005)
             allObjects.append(self.curveObject)
             #self.graphicsObjects.append(self.curveObject)
             #self.label = label(pos=self.points[0], text='%f' % self.length()) 
             self.label = label(pos=labelPosition, text='%d' % self.id) 
             allObjects.append(self.label)
             #self.graphicsObjects.append(self.label)

    # todo: use this when deleting this object
    def deleteGraphicsObjects(self):
        #for o in self.graphicsObjects:
        #    o.visible = 0
        #self.graphicsObjects = []
        self.curveObject.visible = 0
        self.curveObject = None
        self.label.visible = 0
        self.label = None

    def __getstate__(self):
        odict = copy.deepcopy(self.__dict__)
        del odict['label']
        del odict['curveObject']
        
        return odict
        
#    def __setstate__(self,dict):
#        dict['label'] = None
#        dict['curveObject'] = None
#        self.__dict__ = dict     
        
        
    #    print ""    

        
    def length(self):
            pointList = self.points
            #if thisislength(self.points) == 1:
            #    return 0
            
            if len(self.points) == 1:
                return 0
            
            total = 0
            for i in range(1,len(pointList)):
                vector = numpy.array(pointList[i-1]) - numpy.array(pointList[i])
                dist = numpy.linalg.norm(vector)
                total += dist
            
            return total    

    def redraw(self):
            self.deleteGraphicsObjects()
            self.draw()
     

    def removeLastPoint(self):
            if len(self.points) > 1:
                self.points.pop(-1)
                self.redraw()
            else:
                print 'backspaced pressed but there is no edge to delete'


def remove_whitespace_nodes(node, unlink=False):
    """Removes all of the whitespace-only text decendants of a DOM node.
    
    When creating a DOM from an XML source, XML parsers are required to
    consider several conditions when deciding whether to include
    whitespace-only text nodes. This function ignores all of those
    conditions and removes all whitespace-only text decendants of the
    specified node. If the unlink flag is specified, the removed text
    nodes are unlinked so that their storage can be reclaimed. If the
    specified node is a whitespace-only text node then it is left
    unmodified."""
    
    remove_list = []
    for child in node.childNodes:
        if child.nodeType == xml.dom.Node.TEXT_NODE and \
           not child.data.strip():
            remove_list.append(child)
        elif child.hasChildNodes():
            remove_whitespace_nodes(child, unlink)
    for node in remove_list:
        node.parentNode.removeChild(node)
        if unlink:
            node.unlink()




def readReconstructFile(filename, zLevel):
    
    scene.autocenter = 1
    scene.autoscale = 1

    
    contourList = []
    doc = xml.dom.minidom.parse(filename)
    #doc = remove_whitespace_nodes(doc1)
    
    remove_whitespace_nodes(doc)
    
    transformIndex = 1
    contourIndex = 0
    #print doc.childNodes[1].childNodes[transformIndex].childNodes[contourIndex].attributes['points'].value
    #print doc.childNodes[1].childNodes[1].childNodes[3].attributes['points'].value
    
    
  
    for transformNode in doc.childNodes[1].childNodes:
        for node in transformNode.childNodes:
            if node.nodeName == 'Contour':
                contourNode = node
                #print contourNode
                str = contourNode.attributes['points'].value
                
                # replace commas with spaces
                str = str.replace(',',' ')
                
                lst = string.split(str)
                #print lst
                #print float(lst[0])
                numberList = map(float, lst)
        
                pointList = []
                while len(numberList) >= 2:
                    # read three numbers from the list and make them a point
                    point = numpy.array((numberList.pop(0), numberList.pop(0), zLevel))
                    pointList.append(point)
                
                if len(numberList) > 0:
                    # todo: this  should be a warning, like if there some way python reports a warning it should use that
                    print  'number of points in contour was not divisible by 2, they come in x y pairs of 2, so this is probably an error'

                    
                #print pointList
                
                
                
                contourList.append(Contour(pointList))
            
    contourList.pop(0) # the first contour is not really a contour so remove it
    #print doc.childNodes[1].childNodes[1].attributes['points'].name
    #print doc.childNodes[1].childNodes[1].attributes['points'].value
    
    
    #print doc.childNodes[1].childNodes[1].nodeType

    
    scene.autocenter = 0
    scene.autoscale = 0

    return contourList


                

filenameList = os.listdir(pathToReconstructFiles)
#filenameList = [filenameList[0]]
#filenameList.pop(0)
#filenameList.pop(0)
#filenameList.sort()
zLevel = 0
colors = []
for i in range(0,1000):
    colors.append((random.random()+.2, random.random()+.2, 0)) 

allContours = []
for filename in filenameList:
    contourList = readReconstructFile(pathToReconstructFiles + filename, zLevel)
    print filename
    
    for contourIndex in range(0, len(contourList)):
        contour = contourList[contourIndex]
        #print contour
        
        #c = curve( pos=contour.points, color=(.5,.5,.5), radius=.01 )
        #contour.graphicsObjects.append(c)
        
        for point in contour.points:
            # i use this because in vpython spheres can be picked but contours (curves) cannot... if curves could be picked i would not need to render the points
            s = sphere(pos=point, color=colors[contourIndex], radius=.01)
            contour.graphicsObjects.append(s)
            
    zLevel = zLevel + 0.2    
    
    allContours = allContours + contourList
        
#currentList = []
currentGroup = Group([])
groups = []

#lastPoint = None
#curves = []
paths = []
#currentCurveIndex = None
currentPathIndex = None
#labels = []
allObjects = []
currentPathID = 0

def length(pointList):
    if len(pointList) == 1:
        return 0
    
    total = 0
    for i in range(1,len(pointList)):
        vector = numpy.array(pointList[i-1]) - numpy.array(pointList[i])
        dist = numpy.linalg.norm(vector)
        total += dist
    
    return total

while 1:
    
    if scene.kb.keys: # is there an event waiting to be processed?
        s = scene.kb.getkey() # obtain keyboard information
        
        # switch to different curve
        if s==' ':
            currentCurveIndex
        
        # new curve
        if s=='n':
            #curves.append([])
            p = Path(currentPathID)
            
            paths.append(p)
            currentPathID += 1
            
            p.draw()
            
            #p.label = label(text='*')
            #allObjects.append(p.label)

            currentPathIndex = len(paths)-1
            
            lastPoint = None

        if s=='s':
            #print 'writing path.pickle'
            #f = open('path.pickle', 'w')
            #pickle.dump(curves, f)
            #f.close()
            
            print 'writing paths.pickle'
            f = open('paths.pickle', 'w')
            #test = Path(2)
            #test.points = [[1,2,3]]
            #paths = [test]
            pickle.dump(paths, f)
            f.close()

            
            
            
            
        
        if s=='o':
        
            #remove all curves that you drew
            for o in allObjects:
                o.visible = 0
            allObjects = []
                
            #print 'opening path.pickle'
            #f = open('path.pickle', 'r')
            #curves = pickle.load(f)
            #f.close()
            #
            #labels = []
            #
            #for c in curves:
            #    curveObject = curve(pos=c, radius=0.005)
            #    allObjects.append(curveObject)
            #    lab = label(pos=c[-1], text='%f' % length(c)) 
            #    labels.append(lab)
            #    allObjects.append(lab)
            #   
            #currentCurveIndex = None
            
            print 'opening paths.pickle'
            f = open('paths.pickle', 'r')
            paths = pickle.load(f)
            f.close()
            
            for p in paths:
                print p
                print p.points
                p.draw()

            #currentCurveIndex = None
            currentPathIndex = None
            
            # this assumes the last path has the highest id, so that the next one created will have a higher id and not use any of the numbers already used
            currentPathID = paths[-1].id + 1

        if s=='p':
            print "------------------------------"
            print "path number, path length"
            for p in paths:
                print "%d, %f" % (p.id, p.length())
        
        movementStep = 0.1 / scene.scale.z
        if s=='right':
            scene.center = scene.center + numpy.array([-movementStep,0,0])
        
        if s=='left':
            scene.center = scene.center + numpy.array([movementStep,0,0])

        if s=='up':
            scene.center = scene.center + numpy.array([0,-movementStep,0])
            
        if s=='down':
            scene.center = scene.center + numpy.array([0,movementStep,0])
            

        if s=='page up':
            #scene.center = scene.center + numpy.array([0,0,movementStep])
            scene.scale = scene.scale * 1.1
            
        if s=='page down':
            #scene.center = scene.center + numpy.array([0,0,-movementStep])
            scene.scale = scene.scale / 1.1


        if s=='backspace':
            if currentPathIndex != None:
            
                # remove last point from the list
                paths[currentPathIndex].removeLastPoint()
            
            
        print s
    
    if scene.mouse.clicked:
        # if shift is held down, center the view on the object clicked
        if scene.mouse.shift:
            m = scene.mouse.getclick()
            pick = scene.mouse.pick
            if pick != None:
                scene.center = pick.pos
        # if shift is not held down, add a segment to the current path
        else:
            m = scene.mouse.getclick()
            #loc = m.pos
            #print loc
            #sphere(pos=loc, radius=0.1, color=(1,0,0))
            pick = scene.mouse.pick
            if (pick!=None):
    #            if currentCurveIndex != None:
                if currentPathIndex != None:
                    #pick.color = (1,1,1)
                    currentPoint = (pick.pos.x, pick.pos.y, pick.pos.z)
                    #curves[currentCurveIndex].append(currentPoint)
                    paths[currentPathIndex].points.append(currentPoint)
                    paths[currentPathIndex].redraw()
                    
                    #if lastPoint == None:
                        #labels[currentCurveIndex].text = '%f' % length(curves[currentCurveIndex])
                    #else:
                    #if lastPoint != None:
                    #    paths[currentPathIndex].redraw()
                        #c = curve(pos=[lastPoint, currentPoint], radius=0.005)
                        #allObjects.append(c)
    
                    #labels[currentCurveIndex].text = '%f' % length(curves[currentCurveIndex])
                    #labels[currentCurveIndex].pos = array(currentPoint) + array([.05,.05,.05])
                        
                    # todo: handle doing this with updateLabel method in Path class    
                    #paths[currentPathIndex].label.text = '%d' % paths[currentPathIndex].id
                    #paths[currentPathIndex].label.pos = array(currentPoint) + array([.05,.05,.05])
    
                    
                    #lastPoint = currentPoint
                    #print curves[currentCurveIndex]
                    print paths[currentPathIndex].points
                    
                else:
                    print 'not adding point because no current curve'
                
                



