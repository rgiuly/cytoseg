import os
import cPickle

class NodeDoesNotExist(Exception):
    pass



#class Node:
#    
#    count = 0
#
#    def __init__(self, name=None):
#        
#        if name != None:
#            self.name = name
#        else:
#            self.name = 'node' + str(Node.count)
#        
#        self.children = [] # this should really be only in GroupNode and not in Node
#        self.valueToSave = None # this should really be only in DataNode and not in Node
#        self.enableRecursiveRendering = False # this should really be only in GroupNode and not in Node
#        
#        Node.count += 1



# node with a list of children

#class GroupNode(Node):
#class GroupNode():
class Node():

#    def __init__(self, name):
#
#        Node.__init__(self, name)
#        #self.children = []
#        self.enableRecursiveRendering = True
    

    count = 0

    def __init__(self, name=None, valueToSave=None):
        
        if name != None:
            self.name = name
        else:
            self.name = 'node' + str(GroupNode.count)
        
        self.children = []
        self.valueToSave = valueToSave
        self.enableRecursiveRendering = True
        self.isGroupNode = False
        
        #Node.count += 1
        GroupNode.count += 1


    def shallowCopy(self):
        
        nodeCopy = GroupNode(self.name)
        nodeCopy.valueToSave = self.valueToSave
        nodeCopy.enableRecursiveRendering = self.enableRecursiveRendering
        return nodeCopy


    # shows children of node
    def __str__(self):
        result = ' %s(' % self.name 
        for child in self.children:
            result += child.__str__() 
        result += ')'
        return result
    
    def addChild(self, node):
        self.children.append(node)

#    def hasChildren(self):
#        return len(self.children) == 0

    def insertChildAt(self, node, index):
        self.children.insert(index, node)


    def addChildren(self, nodeList):
        for node in nodeList:
            self.addChild(node)


    def addObjectList(self, objectList):
        """Add a list of objects as children. A DataNode is created for each object."""
        count = 0
        for object in objectList:
            node = DataNode(str(count), 'object-type', {}, object)
            self.addChild(node)
            count += 1


    def addObject(self, object):
        """Wrap an object in a node and add the node as a child."""

        node = Node(name=str(len(self.children)), valueToSave=object)
        self.addChild(node)


    def makeChildrenObjectList(self):
        """Returns list of children objects. The objects are unwrapped (they are not inside of DataNodes)."""
        list = []
        for child in self.children:
            list.append(child.valueToSave)
        return list
    

    def insertChildrenAt(self, nodeList, index):
        for i in range(len(nodeList)):
            node = nodeList[i]
            self.insertChildAt(node, index + i)

    
    def getChild(self, name):
        for child in self.children:
            if child.name == name:
                return child
        raise NodeDoesNotExist, ("Tried to access node named %s but it wasn't there. (parent node %s.)" % (name, self.name))


    def removeChild(self, name):
        childToRemove = None
        for child in self.children:
            if child.name == name:
                childToRemove = child
                break
        if childToRemove == None:
            raise NodeDoesNotExist, ("Tried to remove node named %s but it wasn't there. (parent node %s.)" % (name, self.name))
        else:
            self.children.remove(childToRemove)


    def __setstate__(self, dict):
        self.__dict__ = dict
        self.guiComponent = None
    
    
    def __getstate__(self):
        result = self.__dict__.copy()
        if 'guiComponent' in result:
            del result['guiComponent']
        return result



class GroupNode(Node):

    def __init__(self, name=None):

        Node.__init__(self, name)
        self.isGroupNode = True



class PersistentDataTree:
    
    def __init__(self, rootNode, rootFolderPath):
        self.rootNode = rootNode
        self.rootFolderPath = rootFolderPath

    # pathToNode identifies the node to be saved
    def writeSubtree(self, pathToSubtree):
        #print pathToSubtree
        node = getNode(self.rootNode, pathToSubtree)
        #print node
        filename = makeFilenameFromNodePath(pathToSubtree)
        f = open(os.path.join(self.rootFolderPath, filename), "wb")
        #cPickle.dump(node, f)
        pickler = cPickle.Pickler(f)
        pickler.fast = True
        pickler.dump(node)
        f.close()

    # reads subtree from file and places it into tree which is specified by rootNode
    def readSubtree(self, pathToSubtree):

        print "reading subtree", pathToSubtree
    
        if nodeExists(self.rootNode, pathToSubtree):
            parent = getNode(self.rootNode, pathToSubtree[0:-1])
            parent.removeChild(pathToSubtree[-1])
        else:
            createPathIfNeeded(self.rootNode, pathToSubtree[0:-1])
    
    
        # read the node from file and insert it into the data tree
    
        filename = makeFilenameFromNodePath(pathToSubtree)
    
        fullFilename = os.path.join(self.rootFolderPath, filename)
        f = open(fullFilename)
        nodeFromFile = cPickle.load(f)
        f.close()
        #self.refreshGUI()
    
        parent = getNode(self.rootNode, pathToSubtree[0:-1])
        parent.addChild(nodeFromFile)


    # todo: this could be a slow operation, it would be good to make it fast
    # todo: give an informative error message if the node is not found, mention the pathToSubtree and the path on disk (the file path)
    def getSubtree(self, pathToSubtree):

        if not(nodeExists(self.rootNode, pathToSubtree)):
            self.readSubtree(pathToSubtree)

        return getNode(self.rootNode, pathToSubtree)

    # todo: this could be a slow operation, it would be good to make it fast
    def subtreeExists(self, pathToSubtree):
        return nodeExists(self.rootNode, pathToSubtree)


    def setSubtree(self, pathToParent, newNode):
        """
        Adds newNode to subtree and saves to file
        """
        parent = getNode(self.rootNode, pathToParent)
        parent.addChild(newNode)
        self.writeSubtree(pathToParent + (newNode.name,))



    # functions in the gui class:
    #def writePersistentBlobs(blobTree, name)
    #def getPersistentBlobs(name)
    #
    ## puts volume in tree and writes it to disk
    #def writePersistentVolume(volume, name)
    #
    #def getPersistentVolume_old(name)



def getNode(rootNode, nameList):
    currentNode = rootNode
    #print 'nameList'
    #print nameList
    for name in nameList:
        #print name
        currentNode = currentNode.getChild(name)
    return currentNode

    
def nodeExists(rootNode, nameList):

    currentNode = rootNode
    for name in nameList:
        try:
            currentNode = currentNode.getChild(name)
        except NodeDoesNotExist:
            return False

    return True
    

def makeFilenameFromNodePath(nodePath):
    # nodePath is a list of node names
    # return value is a path and a filename like "folder1/folder2/file.pickle"
    baseFilename = ",".join(nodePath)
    extension = ".pickle"
    return baseFilename + extension


def createPathIfNeeded(rootNode, nodePath):

    currentNode = rootNode

    for name in nodePath:
        try:
            currentNode = currentNode.getChild(name)
        except NodeDoesNotExist:
            currentNode.addChild(DataNode(name, 'type of node', None, None))
            currentNode = currentNode.getChild(name)


#def flattenTree(inputRootNode):
#    
#    resultList = []
#    flattenTreeHelper(inputRootNode, resultList)
#    return resultList
#
#
#def flattenTreeHelper(object, resultList):
#
##    if isinstance(object, GroupNode):
##        for o in object.children:
##            flattenTreeHelper(o, resultList)
##    else:
##        resultList.append(object.valueToSave)
#    for o in object.children:
#        flattenTreeHelper(o, resultList)


#def leafObjects(inputRootNode):
#    
#    resultList = []
#    leafObjectsHelper(inputRootNode, resultList)
#    return resultList
#
#
#def leafObjectsHelper(node, resultList):
#
#    if node.hasChildren():
#        for childNode in node.children:
#            leafObjectsHelper(childNode, resultList)
#    else:
#        resultList.append(node.valueToSave)


def nonnullObjects(inputRootNode):
    
    resultList = []
    nonnullObjectsHelper(inputRootNode, resultList)
    return resultList


def nonnullObjectsHelper(node, resultList):
    
    if node.valueToSave != None:
        resultList.append(node.valueToSave)

    for childNode in node.children:
        nonnullObjectsHelper(childNode, resultList)


def nonnullObjectNodes(inputRootNode):
    
    resultList = []
    nonnullObjectNodesHelper(inputRootNode, resultList)
    return resultList


def nonnullObjectNodesHelper(node, resultList):
    
    if node.valueToSave != None:
        resultList.append(node)

    for childNode in node.children:
        nonnullObjectNodesHelper(childNode, resultList)


#def flattenTreeToNodes(inputRootNode):
#
#    resultList = []
#    flattenTreeToNodesHelper(inputRootNode, resultList)
#    return resultList
#
#
#def flattenTreeToNodesHelper(object, resultList):
#
#    if isinstance(object, GroupNode):
#        for o in object.children:
#            flattenTreeToNodesHelper(o, resultList)
#    else:
#        resultList.append(object)


def copyTree(node, filter=None):
    
    newNode = node.shallowCopy()
    copyTreeHelper(node, newNode, filter)
    return newNode


def copyTreeHelper(node, newNode, filter):

    for child in node.children:
        
        print child
        print child.name
        print child.valueToSave
        print child.isGroupNode

        if child.isGroupNode or (filter == None) or (filter.isValid(child) == True):

            newChild = child.shallowCopy()
            newNode.addChild(newChild)

            copyTreeHelper(child, newChild, filter)


# represents a piece of data
# (can be used for gui components)
class DataNode(GroupNode):

    def __init__(self, name, type, params, valueToSave):
        
        GroupNode.__init__(self, name)
        
        self.type = type
        self.params = params
        self.valueToSave = valueToSave
        self.guiComponent = None


    def get(self):
        self.valueToSave = self.guiComponent.GetValue()  #todo: you should really always use set method so this should not be necessary 
        return self.guiComponent.GetValue()
    

    def set(self, value):
        self.valueToSave = value
        self.guiComponent.SetValue(value)


    def test_old(self):
        n1 = DataNode("root","root",10)
        print 'n1 type'
        print type(n1)
        n2 = DataNode("b","boolean",20)
        n3 = DataNode("c","slider",30)
        n4 = DataNode("d","slider",40)
        n5 = DataNode("e","slider",50)

        n1.addChild(n2)
        n1.addChild(n3)
        n2.addChild(n4)
        n2.addChild(n5)
        
        print 'children types'
        for x in n1.children:
            print type(x)
        f = open("temp.pickle", "w")
        cPickle.dump(n1, f)
        f.close()

        f = open("temp.pickle", "r")
        loadedData = cPickle.load(f)
        print "data loaded from file"
        print loadedData
        f.close()
        
        print 'testing get node'
        print getNode(loadedData, ('particleMotionTool', 'd'))
        
        return n1



