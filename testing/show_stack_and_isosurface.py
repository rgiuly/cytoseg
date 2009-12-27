import numpy


from cytoseg_classify import *
#from mitochondria import *



import sys

from enthought.mayavi.scripts import mayavi2


#@mayavi2.standalone
def display3D(gui):
    """Example showing how to view a 3D numpy array in mayavi2.
    """
    
    from enthought.mayavi.sources.array_source import ArraySource
    from enthought.mayavi.modules.outline import Outline
    from enthought.mayavi.modules.image_plane_widget import ImagePlaneWidget
    from enthought.mayavi.modules.iso_surface import IsoSurface

    from enthought.mayavi import mlab as enthought_mlab
    
    # 'mayavi' is always defined on the interpreter.
    #mayavi.new_scene()
    from enthought.mayavi.api import Engine
    e = Engine()
    e.start()
    s = e.new_scene()

    # Make the data and add it to the pipeline.
    # todo: load this from the data tree of cytoseg
    originalVolume = loadImageStack("data/3D-blob-data", None)
    #originalVolume = loadImageStack("O:/images/3D-blob-data/small_crop", None)
    
    gui.addVolumeAndRefreshDataTree(originalVolume, "numpyArray")

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
    
    enthought_mlab.contour3d(originalVolume, contours=3)


temporaryDataFolder = "c:/temp"

app = wx.PySimpleApp()
gui = ClassificationControlsFrame(makeClassifyGUITree(), temporaryDataFolder)
gui.Show()

display3D(gui)

app.MainLoop()
