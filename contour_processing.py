
from numpy import *
import numpy, Image
from opencv import highgui
from opencv import *
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


def progressLog(message):
    if 0: print "mitochondria.py", message

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
        
        self.originalVolume = None
        self.probabilityFunction = None
        self.filteredVolume = None
        self.contourFilterFunction2D = None
        self.minPerimeter = 0
        self.maxPerimeter = None
        self.threshold = 0.5
        self.openCVImageSize = cvSize(numpyImageArrayShape[0], numpyImageArrayShape[1])
        self.images = self.createTemporaryImages(self.openCVImageSize)


    def createTemporaryImages(self, openCVSize):
        
        s = openCVSize
        #print size.__doc__
    
        images = {}
        
        progressLog("contourImage")
        images['contourImage'] = cvCreateImage(s, 8, 1)
        #cvSetZero(images['contourImage'])
        
        progressLog("ellipseImage")
        images['ellipseImage'] = cvCreateImage(s, 8, 1)
        #cvSetZero(images['ellipseImage'])
        
        progressLog("andImage")
        images['andImage'] = cvCreateImage(s, 8, 1)
        #cvSetZero(images['andImage'])
        
        progressLog("orImage")
        images['orImage'] = cvCreateImage(s, 8, 1)
        #cvSetZero(images['orImage'])
        
        progressLog("maskedImage")
        images['maskedImage'] = cvCreateImage(s, 8, 1)
        #cvSetZero(images['maskedImage'])
    
    
        
        images['binaryImage'] = cvCreateImage(s,8,1)
        #binaryImage = cvCreateMat(numpyArrayFilteredImage.shape[1], numpyArrayFilteredImage.shape[0], CV_8UC1)
        #cvSetZero(images['binaryImage'])
    
        progressLog("creating images")
    
        images['originalImage'] = cvCreateImage(s, 8, 1)
        images['contours_image'] = cvCreateImage(s, 8, 3)
        images['resultContoursImage'] = cvCreateImage(s, 8, 3)
        #cvSetZero(images['contours_image'])
    
    
    
        images['resultDisplayImage'] = cvCreateImage(s, 8, 3)
        
        return images


    def findContours(self):
        
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

        originalVolume = self.originalVolume
        probabilityFunction = self.probabilityFunction
        filteredVolume = self.filteredVolume
        contourFilterFunction2D = self.contourFilterFunction2D
        minPerimeter = self.minPerimeter
        maxPerimeter = self.maxPerimeter
    

        contourResultTree = GroupNode('contourResultTree')
    
        storage = cvCreateMemStorage(128000)
    
        
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
                cvSetZero(self.images[key])
            
    
            progressLog("copying to image")
    
            if filteredVolume != None:
                print "contour processing using filtered volume"
                # todo: remove the asarray stuff, it's not doing anything anymore
                i = filteredVolume[:,:,imageIndex]
                numpyArrayFilteredImage = array(numpy.asarray(i))
                
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
                temp = cvCreateImage(self.openCVImageSize, 8, 1)
                copyNumpyToOpenCV(numpy_original, temp)
                binaryImage = contourFilterFunction2D(temp)
    
            else:
                raise Exception, "filteredVolume or the contourFilterFunction2D function should be non-None"
    
                    
            if 1:

                #outputFilename = os.path.join(contourOutputTemporaryFolder,
                #                              "thresholded%04d.bmp" % imageIndex)
                #outputFilename = os.path.join(contourOutputTemporaryFolder,
                #                              "temp%04d.bmp" % imageIndex)
                #highgui.cvSaveImage(outputFilename, temp)

                #print "position 1"
                nb_contours, contours = cvFindContours(binaryImage,
                                                          storage,
                                                          sizeof_CvContour,
                                                          CV_RETR_LIST,
                                                          CV_CHAIN_APPROX_SIMPLE,
                                                          cvPoint(0,0))
                #print "contours", contours
                if contours == None:
                    print "no contours"
                    continue
                
                #print "position 2", contours.total
                #contours = cvApproxPoly(contours, sizeof_CvContour,
                #                           storage,
                #                           CV_POLY_APPROX_DP, 1, 1)
        
                #print "position 3"
                _red = cvScalar(0,0,255,0)
                _green = cvScalar(0,255,0,0)
                
                levels = 3
                
                _contours = contours
                
                #print _contours
                #for c in _contours.hrange():
                #    print c
                #    print cvFitEllipse2(c)
        
                #print "number of contours", contours.total # this is not the number of contours for some reason
        
                for i in range(numpy_original.shape[1]):
                    for j in range(numpy_original.shape[0]):
                        contours_image[i,j] = int(numpy_original[j,i])
                        originalImage[i,j] = int(numpy_original[j,i])
                        resultContoursImage[i,j] = int(numpy_original[j,i])
        
                progressLog("drawing contours")
                cvDrawContours(contours_image, _contours,
                                  _red, _green,
                                  levels, 1, CV_AA,
                                  cvPoint(0, 0))
        
                # process each contour
                contourIndex = 0
                for c in _contours.hrange():
    
                    count = c.total; # This is number point in contour
    
                    # Number point must be more than or equal to 6 (for cvFitEllipse_32f).        
                    if( count < 6 ):
                        continue
    
                    perimeter = cvArcLength(c)
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
                    cvSetZero(contourImage)
                    progressLog("set ellipseImage")
                    #ellipseImage = cvCreateImage(size, 8, 1)
                    cvSetZero(ellipseImage)
                    progressLog("set andImage")
                    #andImage = cvCreateImage(size, 8, 1)
                    cvSetZero(andImage)
                    progressLog("set orImage")
                    #orImage = cvCreateImage(size, 8, 1)
                    cvSetZero(orImage)
                    progressLog("set maskedImage")
                    #maskedImage = cvCreateImage(size, 8, 1)
                    cvSetZero(maskedImage)
        
                    #resultDisplayImage = cvCreateImage(size, 8, 3)
                    cvSetZero(resultDisplayImage)
    
                    progressLog("finished creating images")
            
        
                    #print cvMatchShapes(c, c, CV_CONTOURS_MATCH_I1)
                    
                    # Alloc memory for contour point set.
                    PointArray = cvCreateMat(1, count, CV_32SC2)
                    PointArray2D32f= cvCreateMat( 1, count, CV_32FC2)
                    
                    # Get contour point set.
                    cvCvtSeqToArray(c, PointArray, cvSlice(0, CV_WHOLE_SEQ_END_INDEX));
                    
                    # Convert CvPoint set to CvBox2D32f set.
                    cvConvert( PointArray, PointArray2D32f )
                    
                    box = CvBox2D()
            
                    # Fits ellipse to current contour.
                    box = cvFitEllipse2(PointArray2D32f);
    
                    progressLog("drawing contours")
                    # Draw current contour.
                    cvDrawContours(contours_image, c, CV_RGB(255,255,255), CV_RGB(255,255,255),0,1,8,cvPoint(0,0));
                    cvDrawContours(contourImage, c, CV_RGB(255,255,255), CV_RGB(255,255,255),0,CV_FILLED,8,cvPoint(0,0));
    
                    progressLog("finished drawing contours")
                    
                    # Convert ellipse data from float to integer representation.
                    center = CvPoint()
                    size = CvSize()
                    center.x = cvRound(box.center.x);
                    center.y = cvRound(box.center.y);
                    size.width = cvRound(box.size.width*0.5);
                    size.height = cvRound(box.size.height*0.5);
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
                    ellipsePointArray = cvCreateMat(1, numPolygonPoints, CV_32SC2)
                    ellipsePointArray2D32f= cvCreateMat( 1, numPolygonPoints, CV_32FC2)
                    buffer = [cvPoint(1,1), cvPoint(1,1)]
                    #print box.angle
                    #cvEllipse2Poly(center, size, int(box.angle), 0, 360, ellipsePointArray2D32f, 1)
                    #cvEllipse2Poly(center, size, int(box.angle), 0, 360, buffer, 1)
    
                    progressLog("cv ellipse")
                    
                    # Draw ellipse.
                    cvEllipse(contours_image, center, size,
                              box.angle, 0, 360,
                              CV_RGB(0,0,255), 1, CV_AA, 0);
                    cvEllipse(ellipseImage, center, size,
                              box.angle, 0, 360,
                              CV_RGB(255,255,255), -1, CV_AA, 0);
        
                    cvAnd(contourImage, ellipseImage, andImage);
                    cvOr(contourImage, ellipseImage, orImage);
        
                    andArea = cvSum(andImage)
                    orArea = cvSum(orImage)
                    contourArea = float(cvSum(contourImage)[0])
                    #print contourArea
        
                    cvCopy(originalImage, maskedImage, contourImage)
                    
                    #print orArea
        
        
                    progressLog("fraction of overlap calculation")
        
                    fractionOfOverlap = float(andArea[0]) / float(orArea[0])
        
                    #amplitude = 1
                    #perimeterValue = gaussian(abs(74.0 - perimeter), amplitude, 10)
    
                    averageGrayValue = (float(cvSum(maskedImage)[0]) / float(cvSum(contourImage)[0]))
    
    
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
                    color = CV_RGB(255, 255, 0)
                    if 0:
                        rgbList = colorFromProbability(contourObject.probability)
                        color = CV_RGB(rgbList[0], rgbList[1], rgbList[2])
                    cvDrawContours(resultDisplayImage, c, color, CV_RGB(255,255,255),0,CV_FILLED,8,cvPoint(0,0));
        
                    thickness = 1
                    cvDrawContours(resultContoursImage, c, color, CV_RGB(255,255,255),0,thickness,8,cvPoint(0,0));
        
                    #cvDrawContours(contours_image, ellipsePointArray, CV_RGB(255,255,255), CV_RGB(128,255,128),0,1,8,cvPoint(0,0))
    
                    progressLog("finished drawing contours with color based on mitochondria like properties")
    
                    #cvReleaseImage(contourImage)
                    #cvReleaseImage(ellipseImage)
                    #cvReleaseImage(andImage)
                    #cvReleaseImage(orImage)
                    #cvReleaseImage(maskedImage)
                    
                    if 0:
                    
                        outputFilename = os.path.join(contourOutputTemporaryFolder, "out%04d_%04d.bmp" % (imageIndex, contourIndex))
                        highgui.cvSaveImage(outputFilename, contourImage)
            
                        outputFilename = os.path.join(contourOutputTemporaryFolder, "out%04d_%04d_and.bmp" % (imageIndex, contourIndex))
                        highgui.cvSaveImage(outputFilename, andImage)
            
                        outputFilename = os.path.join(contourOutputTemporaryFolder, "out%04d_%04d_or.bmp" % (imageIndex, contourIndex))
                        highgui.cvSaveImage(outputFilename, orImage)
            
                        outputFilename = os.path.join(contourOutputTemporaryFolder, "out%04d_%04d_masked.bmp" % (imageIndex, contourIndex))
                        highgui.cvSaveImage(outputFilename, maskedImage)
            
                        outputFilename = os.path.join(contourOutputTemporaryFolder, "out%04d_%04d_display.bmp" % (imageIndex, contourIndex))
                        highgui.cvSaveImage(outputFilename, resultDisplayImage)
        
        
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

        size = cvGetSize(openCVImage)

        progressLog("filteredImage")
        filteredImage = cvCreateImage(size, 8, 1)
        cvSetZero(filteredImage)

        progressLog("filteredImage2")
        filteredImage2 = cvCreateImage(size, 8, 1)
        cvSetZero(filteredImage2)
    
        progressLog("filteredImage3")
        filteredImage3 = cvCreateImage(size, 8, 1)
        cvSetZero(filteredImage3)


        cvSmooth(originalImage, filteredImage, CV_GAUSSIAN, 7, 7, 40)

        cvSub(originalImage, filteredImage, filteredImage2)
        #cvExp(filteredImage2, filteredImage3)
        #cvCmp(originalImage, filteredImage, filteredImage2, CV_CMP_GT)

        #cvCmpS(filteredImage2, 5, filteredImage3, CV_CMP_GT)
        cvCmpS(filteredImage2, 0, filteredImage3, CV_CMP_GT)

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

