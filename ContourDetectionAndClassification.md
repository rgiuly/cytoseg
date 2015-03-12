To run this example

  * change directory to cytoseg/testing/
  * run the command python find\_contours.py

In this example, probabilityFunction defines the probability that the contour belongs to a given class based on a set of features:

```
def probabilityFunction(features):
    amplitude = 1
    overlapValue = gaussian(1.0 - features['ellipseOverlap'], amplitude, 0.2)
    perimeterValue = gaussian(abs(11.0 - features['perimeter']), amplitude, 2.0)
    grayValueMatch = gaussian(abs(0.8 - features['averageGrayValue']), amplitude, 0.25)
    areaMatch = gaussian(abs(60 - math.sqrt(features['contourArea'])), amplitude, 10)
    return overlapValue * perimeterValue * grayValueMatch * areaMatch
```


A window will pop up when this file runs.

Processing takes some time and the console output will report progress.

Note:
To use the full gui, you'll need to resize the window labeled `ParticleMotionTool`, this will make scroll bars appear. (This is a work around for a bug - the scroll bars don't appear at startup.)

To view output after processing completes:
  * make sure the contours item is selected in the `dataTree`
  * make sure the `InputVolume` item is selected in the `dataTreeForVolumeSelection`
  * adjust zIndex in the `imageControls` window



![http://cytoseg.googlecode.com/svn/trunk/cytoseg/docs/contour_classification.png](http://cytoseg.googlecode.com/svn/trunk/cytoseg/docs/contour_classification.png)