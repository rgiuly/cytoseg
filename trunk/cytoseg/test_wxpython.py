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

#import wx
#app = wx.PySimpleApp()
#frame = wx.Frame(None, wx.ID_ANY, "Hello World")
#frame.Show(True)
#app.MainLoop()

import Numeric
import numpy

import wx

if 0:
    class App(wx.App):
        def OnInit(self):
            
                   
            frame = wx.Frame(parent=None, title='Bare')
            
            name = 'O:\images\LFong\cropped\8bit_smaller\8bit_smaller0000.tif'
            image = wx.Image(name, type=wx.BITMAP_TYPE_ANY, index=-1)
            #frame.Add(image)  ## try this in separate file
            
            p = wx.Panel(self)
            
            sb1 = wx.StaticBitmap(p, -1, wx.BitmapFromImage(image))
            fgs = wx.FlexGridSizer(cols=2, hgap=10, vgap=10)
            fgs.Add(sb1)
                    
            frame.Show()
            return True
        
    app = App(redirect=False)
    app.MainLoop()
    
    
    

filenames = ['O:\images\LFong\cropped\8bit_smaller\8bit_smaller0000.tif' ]

class TimerHandler(wx.EvtHandler):

    def OnUpTime(self, evt):
         #self.lblUptime.SetLabel('Running ' + (str(myTimerText[0])) + 'hours') # 1/10  hour count
         #myTimerText[0] = myTimerText[0] + .1
         print 'timer'
         print evt
 

class TestFrame(wx.Frame):
    
    def startTimer1(self, handler):
        self.t1 = wx.Timer(handler, id=1)
        self.t1.Start(200)
        handler.Bind(wx.EVT_TIMER, handler.OnUpTime, id=1)
    
    
    
    def __init__(self):

        th = TimerHandler()
        self.startTimer1(th)
        
        wx.Frame.__init__(self, None, title="Loading Images")
        p = wx.Panel(self)
        fgs = wx.FlexGridSizer(cols=2, hgap=10, vgap=10)
        for name in filenames:
            img1 = wx.Image(name, wx.BITMAP_TYPE_ANY)
            w = img1.GetWidth()
            h = img1.GetHeight()
            img2 = img1.Scale(w/2, h/2)
            
            height = 200
            width = 100
            #array = Numeric.ones( (height, width, 3),'c')
            array = numpy.ones( (height, width, 3),numpy.int8)
            
            #array = Numeric.ones( (height, width, 3), Numeric.Int8)
            #array = array + array
            ##for i in range(0,10):
            ##    array = array + array
            #array = array * 200
            #print type(array*200)

            #array = numpy.ones( (height, width, 3),'c')

            #array1 = Numeric.ones( (height, width, 3))
            #array = Numeric.array(int(array1 * 300), 'c')
            #array = Numeric.array(array1 * 300, 'c')
            
            #numpy.multiply(array, 200) 
            #array[:,:,0] = range( 100 )
            array[:,:,0] = 200
            #array = numpy.array(range(200*100*3))
            #array.shape = (200,100,3)
            
            image = wx.EmptyImage(width,height)
            image.SetData( array.tostring())
            bitmap = image.ConvertToBitmap()# wx.BitmapFromImage(image)
            
            #sb1 = wx.StaticBitmap(p, -1, wx.BitmapFromImage(img1))
            #sb2 = wx.StaticBitmap(p, -1, wx.BitmapFromImage(img2))

            sb1 = wx.StaticBitmap(p, -1, wx.BitmapFromImage(img1))
            #sb2 = wx.StaticBitmap(p, -1, wx.BitmapFromImage(bitmap))
            #sb2 = bitmap
            sb2 = wx.StaticBitmap(p, -1, wx.BitmapFromImage(image))


            fgs.Add(sb1)
            fgs.Add(sb2)
            p.SetSizerAndFit(fgs)
            self.Fit()

app = wx.PySimpleApp()
frm = TestFrame()
frm.Show()
app.MainLoop()
    
    