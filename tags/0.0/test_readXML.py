#Copyright (c) 2008 by individual cytoseg contributors
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

import xml.dom.minidom
import string
from visual import *
import numpy

#doc = xml.dom.minidom.Document()


def remove_whitespace_nodes(node, unlink=False):
    """Removes all of the whitespace-only text decendants of a DOM node.
    
    When creating a DOM from an XML source, XML parsers are required to
    consider several conditions when deciding whether to include
    whitespace-only text nodes. This function ignores all of those
    conditions and removes all whitespace-only text decendants of the
    specified node. If the unlink flag is specified, the removed text
    nodes are unlinked so that their storage can be reclaimed. If the
    specified node is a whitespace-only text node then it is left
    unmodified."""
    
    remove_list = []
    for child in node.childNodes:
        if child.nodeType == xml.dom.Node.TEXT_NODE and \
           not child.data.strip():
            remove_list.append(child)
        elif child.hasChildNodes():
            remove_whitespace_nodes(child, unlink)
    for node in remove_list:
        node.parentNode.removeChild(node)
        if unlink:
            node.unlink()

doc = xml.dom.minidom.parse('reconstruct_file.1')
#doc = remove_whitespace_nodes(doc1)

remove_whitespace_nodes(doc)

transformIndex = 1
contourIndex = 0
print doc.childNodes[1].childNodes[transformIndex].childNodes[contourIndex].attributes['points'].value
#print doc.childNodes[1].childNodes[1].childNodes[3].attributes['points'].value


contourIndex = 0
for transformNode in doc.childNodes[1].childNodes:
    for node in transformNode.childNodes:
        if node.nodeName == 'Contour':
            contourNode = node
            print contourNode
            str = contourNode.attributes['points'].value
            
            # replace commas with spaces
            str = str.replace(',',' ')
            
            lst = string.split(str)
            #print lst
            #print float(lst[0])
            numberList = map(float, lst)
    
            pointList = []
            while len(numberList) >= 2:
                # read three numbers from the list and make them a point
                point = numpy.array((numberList.pop(0), numberList.pop(0), contourIndex))
                pointList.append(point)
            
            if len(numberList) > 0:
                # todo: this  should be a warning, like if there some way python reports a warning it should use that
                print  'number of points in contour was not divisible by 2, they come in x y pairs of 2, so this is probably an error'
            
            c = curve( pos=pointList, color=color.red )
                
            print pointList
            
            contourIndex = contourIndex + 1
        
#print doc.childNodes[1].childNodes[1].attributes['points'].name
#print doc.childNodes[1].childNodes[1].attributes['points'].value


#print doc.childNodes[1].childNodes[1].nodeType