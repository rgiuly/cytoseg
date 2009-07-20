
from ctypes import *
from ctypes.wintypes import *


def flatten(inputList):
    
    resultList = []
    flattenHelper(inputList, resultList)
    return resultList


def flattenHelper(object, resultList):

    if isinstance(object, list):
        for o in object:
            flattenHelper(o, resultList)
    else:
        resultList.append(object)

#print "test"
#def test1():
#    print "test1"



#http://bytes.com/forum/thread20586.html
class MEMORYSTATUS(Structure):
    _fields_ = [
                ('dwLength', DWORD),
                ('dwMemoryLoad', DWORD),
                ('dwTotalPhys', DWORD),
                ('dwAvailPhys', DWORD),
                ('dwTotalPageFile', DWORD),
                ('dwAvailPageFile', DWORD),
                ('dwTotalVirtual', DWORD),
                ('dwAvailVirtual', DWORD),
                ]

def winmem():
    x = MEMORYSTATUS()
    windll.kernel32.GlobalMemoryStatus(byref(x))
    return x
#---- in your code[color=blue][color=green][color=darkred]
#>>> from winmem import winmem
#>>> m = winmem()
#>>> print '%d MB physical RAM left.' %

