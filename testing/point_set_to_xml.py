
from point_set import *
from xml.dom.minidom import Document

doc = Document()

blob = Blob()
blob.addPoint(LabeledPoint((1, 2, 3)))
blob.addPoint(LabeledPoint((4, 5, 6)))
element = blob.getXMLVoxelList(doc)

doc.appendChild(element)
print doc.toprettyxml(indent="  ")

