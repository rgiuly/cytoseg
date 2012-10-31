# Utility functions


from ctypes import *
from ctypes.wintypes import *

def subtractDictionary(d1, d2):
    """Subtract dictionary, subtracts each element from corresponding element"""

    result = odict()
    for key in d1.keys():
        result[key] = d1[key] - d2[key]
    return result


def flatten(inputList):
    """Flatten tree"""
    
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
    """Output memory status"""
    x = MEMORYSTATUS()
    windll.kernel32.GlobalMemoryStatus(byref(x))
    return x

