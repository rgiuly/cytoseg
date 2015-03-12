# Introduction #

Cytoseg is a tool for automatic segmentation of 3D biological datasets, with emphasis on 3D electron microscopy. It works best for 3D blob shaped objects like mitochondria, lysosomes, etc.

Many machine learning based tools use only pixel classification to segment objects. This can lead to noisy results that require a large amount of manual correction (and often are not smooth in 3D). The fundamental problem is that local texture does not always enough determine if pixel is really a part of a particular object or not.

To address this challenge, Cytoseg uses 3 steps of automatic processing. The first is pixel classification. The second step detects contours at multiple thresholds and uses another classification step to decide which contours most likely belong to the object of interest. By analysing contour geometry, Cytoseg can make decisions based on more that just local texture. Effectively, the reduces the about of incorrect objects detected after threshold of the pixel classification. Results after step 2 still typically lack some 3D smoothness. The 3rd step helps to increase the smoothness and typically increases accuracy also. This allows Cytoseg to produce segmentations that are accurate and smooth.

Cytoseg is a command line based tool. To install it, you'll need to follow the installation instructions. It's best to first try the example in the [User's Guide](Usage.md) and then modify it slightly for your task.

Cytoseg is written in Python and uses the completely open source pythonxy platform (which includes scipy and ITK image processing tools). Cytoseg uses machine learning functionality from the [Orange](http://orange.biolab.si/) data mining suite. Cytoseg is currently in beta stage.


<h2> Automatic Result Examples </h2>
| **Mitochondria Segmentation in Cerebellum** <br>  <img src='http://cytoseg.googlecode.com/svn/trunk/cytoseg/docs/mito_example_animated.gif' /> <table><thead><th> <b>Automatic Mitochondria Segmentation in Dentate Gyrus</b> <br> <a href='http://www.youtube.com/watch?feature=player_embedded&v=3uo5Q9Gl-Gg' target='_blank'><img src='http://img.youtube.com/vi/3uo5Q9Gl-Gg/0.jpg' width='425' height=344 /></a> </th></thead><tbody></tbody></table>



<h2>Motivation</h2>
Modern electron microscopic staining and imaging technology can be used to highlight intracellular structures, such as vesicles and mitochondria, as well as cellular membranes resulting in complex, textured images. While staining of multiple structures makes it possible to accomplish the identification of most cellular and subcellular tissue components simultaneously, it makes automatic segmentation and identification of these more challenging. When addressing biological problems, automatic segmentation accuracy is critical, as each manual correction requires human effort and ultimately increases the time and cost required for segmentation. Modern three dimensional TEM, SEM, and SBFSEM images involve a large number of objects with various three dimensional shapes. Image intensity alone does not accurately identify a given structure, and identification of objects typically involves a knowledge of various textures and shapes present in the data. Therefore, the numerous segmentation algorithms developed for other biomedical imaging modalities are not directly applicable to thin sections from TEM and serial block face derived SEM images. Cytoseg uses machine learning at multiple steps in the process to address these challenges.<br>
<br>
<br>
<h2>Installation</h2>
<a href='Installation.md'>Installation</a>

<h2>Documentation</h2>
<a href='Usage.md'>Cytoseg User's Guide</a>

<a href='http://cytoseg.blogspot.com/'>Test Results at the Cytoseg Blog</a>

<a href='http://code.google.com/p/cytoseg/wiki/SegmentingMitochondriaWithTrainingDataFromIMOD'>Using Cytoseg with IMOD (make training data, view results, and edit results)</a>

<a href='http://code.google.com/p/cytoseg/wiki/UsingCytosegWithTrakEM2'>Using Cytoseg with TrakEM2 (ImageJ/Fiji) (make training data, view results, and edit results)</a>

<a href='BalancingExamples.md'>Balancing Examples</a>



<h2>Aknowledgement</h2>

We kindly ask users of this software to acknowledge use of Cytoseg their publications and inform us of these publications.<br>
<br>
<h2>Author</h2>
<a href='https://sites.google.com/site/rickgiuly/'>Rick Giuly</a>

<h2>Publications</h2>

<a href='http://www.biomedcentral.com/1471-2105/13/29'>Method: Automatic segmentation of mitochondria utilizing patch classification, contour pair classification, and automatically seeded level sets, Richard J Giuly, Maryann E Martone and Mark H Ellisman, BMC Bioinformatics 2012</a>

<h2>Reports</h2>
<a href='http://cytoseg.googlecode.com/svn-history/r338/trunk/cytoseg/docs/mito_draft.pdf'>Automatic Detection and Segmentation of Mitochondria in 3D Electron Tomographic Images</a>


<h2>Associated Projects</h2>

Scalable Large Analytic Segmentation Hybrid (SLASH) RO1 Grant 1R01NS075314-01<br>
<br>
Cytoseg is part of the <a href='http://openccdb.org/wiki/index.php/Main_Page'>Cell Centered Database</a> tool set.<br>
<br>
<br>
<hr />
<a href='OldDocumentation.md'>Old Documentation</a><br>
<a href='BackgroundReferences.md'>Background References</a>
