This page is under construction


Uses connected components on thresholded images to locate blobs. Then uses a gradient decent (with particle repulsion) approach to locate the darkest point on each blob.

When objects are too close the connected components analysis alone will often consider them one blob (picture of this). The particle simulation step enables detection of distinct objects even if they are one connected component (picture of this).


---

# Detecting Larger Blobs in Sample Dataset #
  * open image stack
  * set particle radius 10 pixels
  * set threshold 121
  * findBlobsThenParticleMovement
    * (300 iterations of particle movement will happen)

  * psi files will appear in tmp directory at each iteration




---

# Detecting Smaller Blobs in Sample Dataset #
  * set min blob size 6
  * set max blob size 5  (which means 53)
  * set threshold 121

  * uncheck "use subgroups"
  * (no groups of particles or particle movement used)

  * click automatic process

  * save particles to output.psi



---


![http://cytoseg.googlecode.com/svn/wiki/3Dview_after_particle_movement2.png](http://cytoseg.googlecode.com/svn/wiki/3Dview_after_particle_movement2.png)

(Output visualized using [3D Slicer](http://www.slicer.org/), a free visualization tool.)



# See Also #
http://blogs.mathworks.com/steve/2007/08/31/intensity-weighted-centroids/