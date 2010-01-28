
from numpy import *
import numpy, Image
from opencv import highgui
from opencv import cv
from math import *
from matplotlib.pyplot import plot
from matplotlib.pyplot import show
from filters import *
from point_set import *
import os
from default_path import *
from volume3d_util import *
from tree import *
import wx


##################################################
#! /usr/bin/env python

print "OpenCV Python version of contours"

# import the necessary things for OpenCV
from opencv import cv
from opencv import highgui

# some default constants
_SIZE = 500
_DEFAULT_LEVEL = 3

# definition of some colors
_red = cv.cvScalar (0, 0, 255, 0);
_green = cv.cvScalar (0, 255, 0, 0);
_white = cv.cvRealScalar (255)
_black = cv.cvRealScalar (0)


def testContours():

    # create the image where we want to display results
    image = cv.cvCreateImage (cv.cvSize (_SIZE, _SIZE), 8, 1)

    # start with an empty image
    cv.cvSetZero (image)

    # draw the original picture
    for i in range (6):
        dx = (i % 2) * 250 - 30
        dy = (i / 2) * 150
        
        cv.cvEllipse (image,
                      cv.cvPoint (dx + 150, dy + 100),
                      cv.cvSize (100, 70),
                      0, 0, 360, _white, -1, 8, 0)
        cv.cvEllipse (image,
                      cv.cvPoint (dx + 115, dy + 70),
                      cv.cvSize (30, 20),
                      0, 0, 360, _black, -1, 8, 0)
        cv.cvEllipse (image,
                      cv.cvPoint (dx + 185, dy + 70),
                      cv.cvSize (30, 20),
                      0, 0, 360, _black, -1, 8, 0)
        cv.cvEllipse (image,
                      cv.cvPoint (dx + 115, dy + 70),
                      cv.cvSize (15, 15),
                      0, 0, 360, _white, -1, 8, 0)
        cv.cvEllipse (image,
                      cv.cvPoint (dx + 185, dy + 70),
                      cv.cvSize (15, 15),
                      0, 0, 360, _white, -1, 8, 0)
        cv.cvEllipse (image,
                      cv.cvPoint (dx + 115, dy + 70),
                      cv.cvSize (5, 5),
                      0, 0, 360, _black, -1, 8, 0)
        cv.cvEllipse (image,
                      cv.cvPoint (dx + 185, dy + 70),
                      cv.cvSize (5, 5),
                      0, 0, 360, _black, -1, 8, 0)
        cv.cvEllipse (image,
                      cv.cvPoint (dx + 150, dy + 100),
                      cv.cvSize (10, 5),
                      0, 0, 360, _black, -1, 8, 0)
        cv.cvEllipse (image,
                      cv.cvPoint (dx + 150, dy + 150),
                      cv.cvSize (40, 10),
                      0, 0, 360, _black, -1, 8, 0)
        cv.cvEllipse (image,
                      cv.cvPoint (dx + 27, dy + 100),
                      cv.cvSize (20, 35),
                      0, 0, 360, _white, -1, 8, 0)
        cv.cvEllipse (image,
                      cv.cvPoint (dx + 273, dy + 100),
                      cv.cvSize (20, 35),
                      0, 0, 360, _white, -1, 8, 0)

    # create window and display the original picture in it
    highgui.cvNamedWindow ("image", 1)
    highgui.cvShowImage ("image", image)

    # create the storage area
    storage = cv.cvCreateMemStorage (0)
    
    # find the contours
    nb_contours, contours = cv.cvFindContours (image,
                                               storage,
                                               cv.sizeof_CvContour,
                                               cv.CV_RETR_TREE,
                                               cv.CV_CHAIN_APPROX_SIMPLE,
                                               cv.cvPoint (0,0))

    # comment this out if you do not want approximation
    contours = cv.cvApproxPoly (contours, cv.sizeof_CvContour,
                                storage,
                                cv.CV_POLY_APPROX_DP, 3, 1)
    
    # create the window for the contours
    highgui.cvNamedWindow ("contours", 1)

    # create the trackbar, to enable the change of the displayed level
    #highgui.cvCreateTrackbar ("levels+3", "contours", 3, 7, on_trackbar)

    # call one time the callback, so we will have the 1st display done
    #on_trackbar (_DEFAULT_LEVEL)

    # create the image for putting in it the founded contours
    contours_image = cv.cvCreateImage (cv.cvSize (_SIZE, _SIZE), 8, 3)


    position = 3

    # compute the real level of display, given the current position
    levels = position - 3

    # initialisation
    _contours = contours
    
    if levels <= 0:
        # zero or negative value
        # => get to the nearest face to make it look more funny
        _contours = contours.h_next.h_next.h_next
        
    # first, clear the image where we will draw contours
    cv.cvSetZero (contours_image)
    
    # draw contours in red and green
    cv.cvDrawContours (contours_image, _contours,
                       _red, _green,
                       levels, 3, cv.CV_AA,
                       cv.cvPoint (0, 0))

    # finally, show the image
    highgui.cvShowImage ("contours", contours_image)

    # wait a key pressed to end
    highgui.cvWaitKey (0)


#testContours()

####################################

def progressLog(message):
    if 0: print "contour_processing.py", message

class XYPlaneEllipse:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.center = array((0,0,0))
        self.angle = 0

def copyNumpyToOpenCV(numpyArray, openCVImage):
    for i in range(numpyArray.shape[1]):
        for j in range(numpyArray.shape[0]):
            openCVImage[i,j] = float(numpyArray[j,i])


#class Contour:
#    def __init__(self, points):
#        self.points = points
#        self.features = {}


class ContourDetector:


    def __init__(self, numpyImageArrayShape):
        
        #testContours()

        self.originalVolume = None
        self.probabilityFunction = None
        self.filteredVolume = None
        self.contourFilterFunction2D = None
        self.minPerimeter = 0
        self.maxPerimeter = None
        self.threshold = 0.5
        self.openCVImageSize = cv.cvSize(numpyImageArrayShape[0], numpyImageArrayShape[1])
        self.images = self.createTemporaryImages(self.openCVImageSize)

        #testContours()


    def createTemporaryImages(self, openCVSize):
        
        s = openCVSize
        #print size.__doc__
    
        images = {}
        
        progressLog("contourImage")
        images['contourImage'] = cv.cvCreateImage(s, 8, 1)
        #cvSetZero(images['contourImage'])
        
        progressLog("ellipseImage")
        images['ellipseImage'] = cv.cvCreateImage(s, 8, 1)
        #cvSetZero(images['ellipseImage'])
        
        progressLog("andImage")
        images['andImage'] = cv.cvCreateImage(s, 8, 1)
        #cvSetZero(images['andImage'])
        
        progressLog("orImage")
        images['orImage'] = cv.cvCreateImage(s, 8, 1)
        #cvSetZero(images['orImage'])
        
        progressLog("maskedImage")
        images['maskedImage'] = cv.cvCreateImage(s, 8, 1)
        #cvSetZero(images['maskedImage'])
    
    
        
        images['binaryImage'] = cv.cvCreateImage(s,8,1)
        #binaryImage = cvCreateMat(numpyArrayFilteredImage.shape[1], numpyArrayFilteredImage.shape[0], CV_8UC1)
        #cvSetZero(images['binaryImage'])
    
        progressLog("creating images")
    
        images['originalImage'] = cv.cvCreateImage(s, 8, 1)
        images['contours_image'] = cv.cvCreateImage(s, 8, 3)
        images['resultContoursImage'] = cv.cvCreateImage(s, 8, 3)
        #cvSetZero(images['contours_image'])



        images['resultDisplayImage'] = cv.cvCreateImage(s, 8, 3)
        
        return images


    def findContours(self):
        
        #testContours()

        self.contoursGroupedByImage = self.opencvDetectContours()
        contourList = nonnullObjects(self.contoursGroupedByImage)
        
        # compute the average original volume value at contour points
        for contour in contourList:
            
            #contour = contourNode.object
            total = 0
            for labeledPoint in contour.points():
                loc = labeledPoint.loc
                total += at(self.originalVolume, loc)
            average = float(total) / float(len(contour.points()))
            #print "average at the contour", average
            contour.features['averageOriginalVolumeValueAtContourPoints'] = average
        
        return self.contoursGroupedByImage


    def opencvDetectContours(self):

        #testContours()

        originalVolume = self.originalVolume
        probabilityFunction = self.probabilityFunction
        filteredVolume = self.filteredVolume
        contourFilterFunction2D = self.contourFilterFunction2D
        minPerimeter = self.minPerimeter
        maxPerimeter = self.maxPerimeter
    

        contourResultTree = GroupNode('contourResultTree')
    
        storage = cv.cvCreateMemStorage(128000)
        #storage = cv.cvCreateMemStorage(0)
    
        
        if 0:
            values = []
            domain = arange(-10.0, 10.0, 0.1)
            for x in domain:
                values.append(gaussian(x, 10, 1))
            plot(domain, values)
            show()
        
        for imageIndex in range(originalVolume.shape[2]):

            contoursInImage = GroupNode('image' + str(imageIndex))
            contourResultTree.addChild(contoursInImage)
            
            progressLog(("image index", imageIndex, "number of images:", originalVolume.shape[2])) 
            
            #i = Image.open('images/circular_regions.bmp')
            #i = Image.open("C:\\temp\\gradient_is_just_a_blur_function_data_set2_threshold.tif")
        
            #i = Image.open("O:\\images\\HPFcere_vol\\gradient_is_just_a_blur_function_data_set2\\8bit_trimmed\\thresholded\\out%04d.tif" % imageIndex)
            #originalImage = Image.open("O:\\images\\HPFcere_vol\\HPF_rotated_tif\\8bit\\training\\out%04d.tif" % (imageIndex + 3))
            
    
            originalImage = originalVolume[:,:,imageIndex]
    
            print imageIndex
    
            #print "free space", storage.free_space
    
            progressLog("creating arrays")
            
            numpy_original = array(numpy.asarray(originalImage))
    
            #size = cvSize(numpy_original.shape[0], numpy_original.shape[1])
            #images = createTemporaryImages(size)
    
    
            contourImage = self.images['contourImage']
            ellipseImage = self.images['ellipseImage']
            andImage = self.images['andImage']
            orImage = self.images['orImage']
            maskedImage = self.images['maskedImage']
            resultDisplayImage = self.images['resultDisplayImage']
            
            binaryImage = self.images['binaryImage']
            originalImage = self.images['originalImage']
            contours_image = self.images['contours_image']
            resultContoursImage = self.images['resultContoursImage']
            resultDisplayImage = self.images['resultDisplayImage']
            
            for key in self.images:
                cv.cvSetZero(self.images[key])
            
    
            progressLog("copying to image")
    
            if filteredVolume != None:
                print "contour processing using filtered volume"
                # todo: remove the asarray stuff, it's not doing anything anymore
                i = filteredVolume[:,:,imageIndex]
                progressLog("image created")
                numpyArrayFilteredImage = array(numpy.asarray(i))
                progressLog("numpy image created")
                
                #print numpyArrayFilteredImage.shape[0]
                #print numpyArrayFilteredImage.shape[1]
                for i in range(numpyArrayFilteredImage.shape[1]):
                    for j in range(numpyArrayFilteredImage.shape[0]):
                        #print i,j
                        #cvmSet(binaryImage, i, j, int(numpyArrayFilteredImage[i,j])) # this is setting the data incorrectly like it thinks the size of the entry is something other than 8 bits, maybe it thinks 32 bits
            
                        #binaryImage[i,j] = int(numpyArrayFilteredImage[j,i])
                        if numpyArrayFilteredImage[j,i] > self.threshold:
                            binaryImage[i,j] = 1
    
            elif contourFilterFunction2D != None:
                print "contour processing using original image"
                temp = cv.cvCreateImage(self.openCVImageSize, 8, 1)
                copyNumpyToOpenCV(numpy_original, temp)
                binaryImage = contourFilterFunction2D(temp)
    
            else:
                raise Exception, "filteredVolume or the contourFilterFunction2D function should be non-None"
    
            progressLog("finished copying to image")


            if 1:

                #outputFilename = os.path.join(contourOutputTemporaryFolder,
                #                              "thresholded%04d.bmp" % imageIndex)
                #outputFilename = os.path.join(contourOutputTemporaryFolder,
                #                              "temp%04d.bmp" % imageIndex)
                #highgui.cvSaveImage(outputFilename, temp)


                #import time

                #time.sleep(100)

                progressLog("find contours")

                #print "position 1"
#                image = cv.cvCreateImage (cv.cvSize (300, 300), 8, 1)
#            # start with an empty image
#            cv.cvSetZero (image)
#        
#            _red = cv.cvScalar (0, 0, 255, 0);
#            _green = cv.cvScalar (0, 255, 0, 0);
#            _white = cv.cvRealScalar (255)
#            _black = cv.cvRealScalar (0)
#
#            # draw the original picture
#            for i in range (6):
#                dx = (i % 2) * 250 - 30
#                dy = (i / 2) * 150
#                
#                cv.cvEllipse (image,
#                              cv.cvPoint (dx + 150, dy + 100),
#                              cv.cvSize (100, 70),
#                              0, 0, 360, _white, -1, 8, 0)
#                cv.cvEllipse (image,
#                              cv.cvPoint (dx + 115, dy + 70),
#                              cv.cvSize (30, 20),
#                              0, 0, 360, _black, -1, 8, 0)
#                cv.cvEllipse (image,
#                              cv.cvPoint (dx + 185, dy + 70),
#                              cv.cvSize (30, 20),
#                              0, 0, 360, _black, -1, 8, 0)
#                cv.cvEllipse (image,
#                              cv.cvPoint (dx + 115, dy + 70),
#                              cv.cvSize (15, 15),
#                              0, 0, 360, _white, -1, 8, 0)
#                cv.cvEllipse (image,
#                              cv.cvPoint (dx + 185, dy + 70),
#                              cv.cvSize (15, 15),
#                              0, 0, 360, _white, -1, 8, 0)
#                cv.cvEllipse (image,
#                              cv.cvPoint (dx + 115, dy + 70),
#                              cv.cvSize (5, 5),
#                              0, 0, 360, _black, -1, 8, 0)
#                cv.cvEllipse (image,
#                              cv.cvPoint (dx + 185, dy + 70),
#                              cv.cvSize (5, 5),
#                              0, 0, 360, _black, -1, 8, 0)
#                cv.cvEllipse (image,
#                              cv.cvPoint (dx + 150, dy + 100),
#                              cv.cvSize (10, 5),
#                              0, 0, 360, _black, -1, 8, 0)
#                cv.cvEllipse (image,
#                              cv.cvPoint (dx + 150, dy + 150),
#                              cv.cvSize (40, 10),
#                              0, 0, 360, _black, -1, 8, 0)
#                cv.cvEllipse (image,
#                              cv.cvPoint (dx + 27, dy + 100),
#                              cv.cvSize (20, 35),
#                              0, 0, 360, _white, -1, 8, 0)
#                cv.cvEllipse (image,
#                              cv.cvPoint (dx + 273, dy + 100),
#                              cv.cvSize (20, 35),
#                              0, 0, 360, _white, -1, 8, 0)
#
#                progressLog("show image")
#
#                highgui.cvShowImage("image", image)
#                #highgui.cvShowImage("image", temp)
#                highgui.cvWaitKey(0)


                nb_contours, contours = cv.cvFindContours(binaryImage,
                                                          storage,
                                                          cv.sizeof_CvContour,
                                                          cv.CV_RETR_LIST,
                                                          cv.CV_CHAIN_APPROX_SIMPLE,
                                                          cv.cvPoint(0,0))
#                nb_contours, contours = cv.cvFindContours(image,
#                                                          storage,
#                                                          cv.sizeof_CvContour,
#                                                          cv.CV_RETR_LIST,
#                                                          cv.CV_CHAIN_APPROX_SIMPLE,
#                                                          cv.cvPoint(0,0))
#                storage = cv.cvCreateMemStorage(0)
#                nb_contours, contours = cv.cvFindContours (image,
#                                                           storage,
#                                                           cv.sizeof_CvContour,
#                                                           cv.CV_RETR_TREE,
#                                                           cv.CV_CHAIN_APPROX_SIMPLE,
#                                                           cv.cvPoint (0,0))

                #contours = None

                progressLog("finished find contours")


                #print "contours", contours
                if contours == None:
                    print "no contours"
                    continue
                
                #print "position 2", contours.total
                #contours = cvApproxPoly(contours, sizeof_CvContour,
                #                           storage,
                #                           CV_POLY_APPROX_DP, 1, 1)
        
                #print "position 3"
                _red = cv.cvScalar(0,0,255,0)
                _green = cv.cvScalar(0,255,0,0)
                
                levels = 3
                
                _contours = contours
                
                #print _contours
                #for c in _contours.hrange():
                #    print c
                #    print cvFitEllipse2(c)
        
                #print "number of contours", contours.total # this is not the number of contours for some reason
        
                progressLog("copy")

                for i in range(numpy_original.shape[1]):
                    for j in range(numpy_original.shape[0]):
                        contours_image[i,j] = int(numpy_original[j,i])
                        originalImage[i,j] = int(numpy_original[j,i])
                        resultContoursImage[i,j] = int(numpy_original[j,i])
        
                progressLog("drawing contours")
                cv.cvDrawContours(contours_image, _contours,
                                  _red, _green,
                                  levels, 1, cv.CV_AA,
                                  cv.cvPoint(0, 0))
        
                # process each contour
                contourIndex = 0
                for c in _contours.hrange():
    
                    count = c.total; # This is number point in contour
    
                    # Number point must be more than or equal to 6 (for cvFitEllipse_32f).        
                    if( count < 6 ):
                        continue
    
                    perimeter = cv.cvArcLength(c)
                    #print perimeter
    
                    if perimeter < minPerimeter:
                        continue
    
                    if maxPerimeter != None:
                        if perimeter > maxPerimeter:
                            continue
    
                    progressLog(("processing contour", contourIndex, "number of contours", _contours.total))
                    
                    pointList = []
                    for point in c:
                        pointList.append(LabeledPoint(array((point.x, point.y, imageIndex))))
                    #for point in c:
                    #    print point
                    #print pointList
    
                    progressLog("making point set")
    
                    contourObject = Contour(points=pointList)
                    #contourObject = Blob(points=pointList)
                    contourNode = Node()
                    contourNode.object = contourObject
                    contoursInImage.addChild(contourNode)
                    
                    #print c
                    if c.v_next != None: print "c.v_next", c.v_next
                    if c.v_prev != None: print "c.v_prev", c.v_prev
    
                    progressLog("setting flags")
                    
                    #print c.flags
                    c.flags = 1117327884 #value for outer (not inner) contour
                    #print "c.h_next", c.h_next
                    #print "c.h_prev", c.h_prev
    
                    progressLog("creating images")
                    
                    #size = cvSize(numpyArrayFilteredImage.shape[0], numpyArrayFilteredImage.shape[1])
                    progressLog("set contourImage")
                    #contourImage = cvCreateImage(size, 8, 1)
                    cv.cvSetZero(contourImage)
                    progressLog("set ellipseImage")
                    #ellipseImage = cvCreateImage(size, 8, 1)
                    cv.cvSetZero(ellipseImage)
                    progressLog("set andImage")
                    #andImage = cvCreateImage(size, 8, 1)
                    cv.cvSetZero(andImage)
                    progressLog("set orImage")
                    #orImage = cvCreateImage(size, 8, 1)
                    cv.cvSetZero(orImage)
                    progressLog("set maskedImage")
                    #maskedImage = cvCreateImage(size, 8, 1)
                    cv.cvSetZero(maskedImage)
        
                    #resultDisplayImage = cvCreateImage(size, 8, 3)
                    cv.cvSetZero(resultDisplayImage)
    
                    progressLog("finished creating images")
            
        
                    #print cvMatchShapes(c, c, CV_CONTOURS_MATCH_I1)
                    
                    # Alloc memory for contour point set.
                    PointArray = cv.cvCreateMat(1, count, cv.CV_32SC2)
                    PointArray2D32f = cv.cvCreateMat(1, count, cv.CV_32FC2)
                    
                    # Get contour point set.
                    cv.cvCvtSeqToArray(c, PointArray, cv.cvSlice(0, cv.CV_WHOLE_SEQ_END_INDEX));
                    
                    # Convert CvPoint set to CvBox2D32f set.
                    cv.cvConvert( PointArray, PointArray2D32f )
                    
                    # this seems unnecessary
                    box = cv.CvBox2D()
            
                    # Fits ellipse to current contour.
                    box = cv.cvFitEllipse2(PointArray2D32f);
    
                    progressLog("drawing contours")
                    # Draw current contour.
                    cv.cvDrawContours(contours_image, c, cv.CV_RGB(255,255,255), cv.CV_RGB(255,255,255),0,1,8,cv.cvPoint(0,0));
                    cv.cvDrawContours(contourImage, c, cv.CV_RGB(255,255,255), cv.CV_RGB(255,255,255),0,cv.CV_FILLED,8,cv.cvPoint(0,0));
    
                    boundingBox = contourObject.get2DBoundingBox()
                    width = boundingBox[1][0] - boundingBox[0][0] + 1
                    height = boundingBox[1][1] - boundingBox[0][1] + 1
                    contourObject.binaryImage = zeros((width, height), dtype=int8)
                    for x in range(boundingBox[0][0], boundingBox[1][0]+1):
                        for y in range(boundingBox[0][1], boundingBox[1][1]+1):
                            if contourImage[y,x] != 0:
                                value = 1
                            else:
                                value = 0
                            contourObject.binaryImage[x-boundingBox[0][0],
                                                      y-boundingBox[0][1]] = value

                    progressLog("finished drawing contours")
                    
                    # Convert ellipse data from float to integer representation.
                    center = cv.CvPoint()
                    size = cv.CvSize()
                    center.x = cv.cvRound(box.center.x);
                    center.y = cv.cvRound(box.center.y);
                    size.width = cv.cvRound(box.size.width*0.5);
                    size.height = cv.cvRound(box.size.height*0.5);
                    box.angle = -box.angle;
    
                    ellipse = XYPlaneEllipse()
                    ellipse.width = size.width
                    ellipse.height = size.height
                    ellipse.center = array((center.x, center.y, imageIndex))
                    ellipse.angle = box.angle
                    contourObject.bestFitEllipse = ellipse
    
                    #ellipseWidth = min(size.width, size.height)
                    #ellipseHeight = max(size.width, size.height)
                    #ellipseAspectRatio = ellipseHeight / ellipseWidth  
        
                    #cvEllipse2Poly
                    # Alloc memory for contour point set.
                    numPolygonPoints = 30
                    ellipsePointArray = cv.cvCreateMat(1, numPolygonPoints, cv.CV_32SC2)
                    ellipsePointArray2D32f= cv.cvCreateMat( 1, numPolygonPoints, cv.CV_32FC2)
                    buffer = [cv.cvPoint(1,1), cv.cvPoint(1,1)]
                    #print box.angle
                    #cvEllipse2Poly(center, size, int(box.angle), 0, 360, ellipsePointArray2D32f, 1)
                    #cvEllipse2Poly(center, size, int(box.angle), 0, 360, buffer, 1)
    
                    progressLog("cv ellipse")
                    
                    # Draw ellipse.
                    cv.cvEllipse(contours_image, center, size,
                              box.angle, 0, 360,
                              cv.CV_RGB(0,0,255), 1, cv.CV_AA, 0);
                    cv.cvEllipse(ellipseImage, center, size,
                              box.angle, 0, 360,
                              cv.CV_RGB(255,255,255), -1, cv.CV_AA, 0);
        
                    cv.cvAnd(contourImage, ellipseImage, andImage);
                    cv.cvOr(contourImage, ellipseImage, orImage);
        
                    andArea = cv.cvSum(andImage)
                    orArea = cv.cvSum(orImage)
                    contourArea = float(cv.cvSum(contourImage)[0])
                    #print contourArea
        
                    cv.cvCopy(originalImage, maskedImage, contourImage)
                    
                    #print orArea
        
        
                    progressLog("fraction of overlap calculation")
        
                    fractionOfOverlap = float(andArea[0]) / float(orArea[0])
        
                    #amplitude = 1
                    #perimeterValue = gaussian(abs(74.0 - perimeter), amplitude, 10)
    
                    averageGrayValue = (float(cv.cvSum(maskedImage)[0]) / float(cv.cvSum(contourImage)[0]))
    
    
                    contourObject.features['ellipseOverlap'] = fractionOfOverlap
                    contourObject.features['perimeter'] = perimeter
                    contourObject.features['averageGrayValue'] = averageGrayValue
                    contourObject.features['contourArea'] = contourArea
                    #print contourObject.features['averageGrayValue']
                    #contourObject.features['mitochondria-like'] = overlapValue * perimeterValue * contourObject.features['grayValueMatch'] * areaMatch
                    if 0:
                        contourObject.setProbability(probabilityFunction(contourObject.features))
                    #contourObject.features['mitochondria-like'] = areaMatch
                    
                    #print imageIndex, contourIndex, ". perimeter:", perimeter, "  overlap:", fractionOfOverlap
    
                    progressLog("draw contour with color based on mitochondria like properties")
        
                    #color = CV_RGB(int(255.0*overlapValue),int(255.0*perimeterValue),50)
                    #color = CV_RGB(50,int(255.0*(overlapValue**1)*(perimeterValue**1)),50)
                    #color = CV_RGB(255 - (contourObject.probability() * 6),int(255.0*contourObject.probability()) * 6.0,50)
                    color = cv.CV_RGB(255, 255, 0)
                    if 0:
                        rgbList = colorFromProbability(contourObject.probability)
                        color = cv.CV_RGB(rgbList[0], rgbList[1], rgbList[2])
                    cv.cvDrawContours(resultDisplayImage, c, color, cv.CV_RGB(255,255,255),0,cv.CV_FILLED,8,cv.cvPoint(0,0));
        
                    thickness = 1
                    cv.cvDrawContours(resultContoursImage, c, color, cv.CV_RGB(255,255,255),0,thickness,8,cv.cvPoint(0,0));
        
                    #cvDrawContours(contours_image, ellipsePointArray, CV_RGB(255,255,255), CV_RGB(128,255,128),0,1,8,cvPoint(0,0))
    
                    progressLog("finished drawing contours with color based on mitochondria like properties")
    
                    #cvReleaseImage(contourImage)
                    #cvReleaseImage(ellipseImage)
                    #cvReleaseImage(andImage)
                    #cvReleaseImage(orImage)
                    #cvReleaseImage(maskedImage)
                    
                    if 0:
                    
                        outputFilename = os.path.join(contourOutputTemporaryFolder, "out%04d_%04d.bmp" % (imageIndex, contourIndex))
                        highgui.cv.cvSaveImage(outputFilename, contourImage)
            
                        outputFilename = os.path.join(contourOutputTemporaryFolder, "out%04d_%04d_and.bmp" % (imageIndex, contourIndex))
                        highgui.cv.cvSaveImage(outputFilename, andImage)
            
                        outputFilename = os.path.join(contourOutputTemporaryFolder, "out%04d_%04d_or.bmp" % (imageIndex, contourIndex))
                        highgui.cv.cvSaveImage(outputFilename, orImage)
            
                        outputFilename = os.path.join(contourOutputTemporaryFolder, "out%04d_%04d_masked.bmp" % (imageIndex, contourIndex))
                        highgui.cv.cvSaveImage(outputFilename, maskedImage)
            
                        outputFilename = os.path.join(contourOutputTemporaryFolder, "out%04d_%04d_display.bmp" % (imageIndex, contourIndex))
                        highgui.cv.cvSaveImage(outputFilename, resultDisplayImage)
        
        
                    contourIndex = contourIndex + 1
                    
                # Show image. HighGUI use.
                #highgui.cvShowImage( "Result", contours_image );
        
            
            if 0:
                highgui.cvNamedWindow("original", 1)
                highgui.cvShowImage("original", binaryImage)
                
                highgui.cvNamedWindow("contours", 1)
                highgui.cvShowImage("contours", contours_image)
    
            progressLog("writing output files")
    
    
            outputFilename = os.path.join(contourOutputTemporaryFolder, "out%04d.bmp" % imageIndex)
            highgui.cvSaveImage(outputFilename, contours_image)
        
            outputFilename = os.path.join(contourOutputTemporaryFolder, "result%04d.bmp" % imageIndex)
            highgui.cvSaveImage(outputFilename, resultContoursImage)

            #contourResultTree.addChild(contoursInImage)
        
            #print outputFilename
        print "output written to file stack"
        
        #highgui.cvWaitKey(0)
    
        return contourResultTree
        
    #findMitochondria()


def greaterThanSurroundingPixelsFilter(openCVImage):

        originalImage = openCVImage

        size = cv.cvGetSize(openCVImage)

        progressLog("filteredImage")
        filteredImage = cv.cvCreateImage(size, 8, 1)
        cv.cvSetZero(filteredImage)

        progressLog("filteredImage2")
        filteredImage2 = cv.cvCreateImage(size, 8, 1)
        cv.cvSetZero(filteredImage2)
    
        progressLog("filteredImage3")
        filteredImage3 = cv.cvCreateImage(size, 8, 1)
        cv.cvSetZero(filteredImage3)


        cv.cvSmooth(originalImage, filteredImage, cv.CV_GAUSSIAN, 7, 7, 40)

        cv.cvSub(originalImage, filteredImage, filteredImage2)
        #cvExp(filteredImage2, filteredImage3)
        #cvCmp(originalImage, filteredImage, filteredImage2, CV_CMP_GT)

        #cvCmpS(filteredImage2, 5, filteredImage3, CV_CMP_GT)
        cv.cvCmpS(filteredImage2, 0, filteredImage3, cv.CV_CMP_GT)

        return filteredImage3



def highProbabilityContours(contourList, threshold):

    highProbabilityContourList = []

    #for contour in contours[0:2000:10]:
    for contour in contourList:
        #mitochondriaLikeness = contour.features['mitochondria-like']
        mitochondriaLikeness = contour.probability()
        #print mitochondriaLikeness
        if mitochondriaLikeness > threshold:
            highProbabilityContourList.append(contour)
    
    return highProbabilityContourList


def colorFromProbability(probability):
    rgbList = (255 - (probability() * 6),
               int(255.0*probability()) * 6.0,
               50)
    return rgbList

