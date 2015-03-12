# Installation Instructions (Windows) #
  1. Install [pythonxy](http://www.pythonxy.com) with all optional components except opencv
  1. Install opencv http://opencv.willowgarage.com/wiki/ and copy the contents of OpenCV2.0\Python2.6\Lib\site-packages into Python26\Lib\site-packages (or wherever you have python installed)
  1. Install orange for python http://www.ailab.si/orange/
  1. Install [python-graph](http://code.google.com/p/python-graph/)
  1. Download cytoseg from svn (see http://code.google.com/p/cytoseg/source/checkout)


---

# Installation Instructions (Ubuntu Linux) #
  1. Install the following modules with synaptic: python, python-numpy, python-wxgtk2.8, python-scipy, python-matplotlib
  1. Install opencv and opencv python bindings using the Ubuntu Software Center
  1. Install itk for python: sudo apt-get install python-insighttoolkit3
  1. Install orange for python http://www.ailab.si/orange/
    * [Instructions for installing orange in Ubuntu 12.04](http://manojbits.wordpress.com/2012/09/25/installing-orange-in-ubuntu-12-04/)
  1. Install [python-graph](http://code.google.com/p/python-graph/)
  1. Download cytoseg from svn (see http://code.google.com/p/cytoseg/source/checkout)

Optional for experimental features:
  1. Visit http://code.enthought.com/projects/mayavi/docs/development/html/mayavi/installation.html to get the most recent version of mayavi2 and install it



---

# Installation Instruction (Redhat Linux) #

Note: Redhat installation is more time consuming than Windows or Linux due to need for compilation of Wrap ITK and orange

  1. Install enthought python suite version 7.1
  1. Install WrapITK with ITK version 3.17
    * Ensure that `PyBuffer` in installed with `WrapITK` [Discussion about this](http://old.nabble.com/How-to-build-ITK%2BWrapITK-python%2BPyBuffer--td27078096.html)
  1. Install orange data mining module for python
  1. Install opencv for python
  1. Download cytoseg from svn (see http://code.google.com/p/cytoseg/source/checkout)

You'll need to configure environmental variables according to the instructions for each module. Here's an example of how I set my environmental variables assuming that EPD is installed at /usr/local/EPD:

```

export PYTHON_INCLUDE_PATH=/usr/local/EPD/include/python2.7
export PYTHON_LIB_PATH=/usr/local/EPD/lib/python2.7
export LD_LIBRARY_PATH=/usr/lib64:/lib:/lib64:/usr/lib:/usr/local/EPD/lib:/usr/local/lib/InsightToolkit:/usr/local/lib/InsightToolkit/WrapITK/lib
export PATH=/usr/local/EPD/bin:$PATH
```


---

[OptionalInstallation](OptionalInstallation.md)