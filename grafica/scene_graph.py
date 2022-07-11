# coding=utf-8
"""A simple scene graph class and functionality"""

from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import grafica.transformations as tr
import grafica.gpu_shape as gs

__author__ = "Daniel Calderon"
__license__ = "MIT"


class SceneGraphNode:
    """
    A simple class to handle a scene graph
    Each node represents a group of objects
    Each leaf represents a basic figure (GPUShape)
    To identify each node properly, it MUST have a unique name
    """
    def __init__(self, name):
        self.name = name
        self.transform = tr.identity()
        self.childs = []

    def clear(self):
        """Freeing GPU memory"""

        for child in self.childs:
            child.clear()

            

    
def findNode(node, name):

    # The name was not found in this path
    if isinstance(node, gs.GPUShape):
        return None

    # This is the requested node
    if node.name == name:
        return node
    
    # All childs are checked for the requested name
    for child in node.childs:
        foundNode = findNode(child, name)
        if foundNode != None:
            return foundNode

    # No child of this node had the requested name
    return None


def findTransform(node, name, parentTransform=tr.identity()):

    # The name was not found in this path
    if isinstance(node, gs.GPUShape):
        return None

    newTransform = np.matmul(parentTransform, node.transform)

    # This is the requested node
    if node.name == name:
        return newTransform
    
    # All childs are checked for the requested name
    for child in node.childs:
        foundTransform = findTransform(child, name, newTransform)
        if isinstance(foundTransform, (np.ndarray, np.generic) ):
            return foundTransform

    # No child of this node had the requested name
    return None


def findPosition(node, name, parentTransform=tr.identity()):
    foundTransform = findTransform(node, name, parentTransform)

    if isinstance(foundTransform, (np.ndarray, np.generic) ):
        zero = np.array([[0,0,0,1]], dtype=np.float32).T
        foundPosition = np.matmul(foundTransform, zero)
        return foundPosition

    return None


def drawSceneGraphNode(node, pipeline, transformName, parentTransform=tr.identity()):
    assert(isinstance(node, SceneGraphNode))

    # Composing the transformations through this path
    newTransform = np.matmul(parentTransform, node.transform)

    # If the child node is a leaf, it should be a GPUShape.
    # Hence, it can be drawn with drawCall
    if len(node.childs) == 1 and isinstance(node.childs[0], gs.GPUShape):
        leaf = node.childs[0]
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, transformName), 1, GL_TRUE, newTransform)
        pipeline.drawCall(leaf)

    # If the child node is not a leaf, it MUST be a SceneGraphNode,
    # so this draw function is called recursively
    else:
        for child in node.childs:
            drawSceneGraphNode(child, pipeline, transformName, newTransform)

# new version 
def drawSceneGraphNodeV2(node, node_to_transform_name, pipeline, transformName, change = False, parentTransform=tr.identity()):
    assert(isinstance(node, SceneGraphNode))

    # Composing the transformations through this path
    newTransform = np.matmul(parentTransform, node.transform)

    # If the child node is a leaf, it should be a GPUShape.
    # Hence, it can be drawn with drawCall
    if len(node.childs) == 1 and isinstance(node.childs[0], gs.GPUShape):
        if change == True:
            leaf = node.childs[0]
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, transformName), 1, GL_TRUE, newTransform)
            pipeline.drawCall(leaf)
        else:
            leaf = node.childs[0]
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, transformName), 1, GL_TRUE, tr.identity())
            pipeline.drawCall(leaf)

    # If the child node is not a leaf, it MUST be a SceneGraphNode,
    # so this draw function is called recursively
    else:
        for child in node.childs:
            if child.name == node_to_transform_name:
                drawSceneGraphNodeV2(child, pipeline, transformName, newTransform, change=True)
            else:
                drawSceneGraphNodeV2(child, node_to_transform_name, pipeline, transformName, newTransform, change=False)


def printSceneGraphNode(node, pipeline):
    assert(isinstance(node, SceneGraphNode))

    # If the child node is a leaf, it should be a GPUShape.
    # Hence, it can be drawn with drawCall
    if len(node.childs) == 1 and isinstance(node.childs[0], gs.GPUShape):
        leaf = node.childs[0]
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, transformName), 1, GL_TRUE, newTransform)
        pipeline.drawCall(leaf)

    # If the child node is not a leaf, it MUST be a SceneGraphNode,
    # so this draw function is called recursively
    else:
        for child in node.childs:
            drawSceneGraphNode(child, pipeline, transformName, newTransform)

def mySceneGraph(node):
    print("call to myscene graph")

    #print(tr.identity().tolist()) # todo transform it with , np.matmul

    if len(node.childs) == 1 and isinstance(node.childs[0].childs[0], gs.GPUShape):
        print("leaf: ", node.name)
        # write it on a python program
        f = open("./modeloutput.py", "a")
        f.write("   # writing the cube leaf: " + node.name + "\n")
        f.write("   shape = bs.createColorNormalsCube(0.5,0.5,0.5)\n")
        f.write("   gpuCube = create_gpu(shape, pipeline)\n")
        f.write("   basic_" + node.name + " = sg.SceneGraphNode('basic_" + node.name + "')\n")
        #f.write("   basic_" + node.name + ".transform =" + str(newTransform.tolist()) + "\n") # new transform to apply to node
        f.write("   basic_" + node.name + ".childs += [gpuCube]\n") # gpu basic cube
        f.write("   " + node.name + " = sg.SceneGraphNode('"+node.name+"')\n") #scenegraphnode with node name
        f.write("   " + node.name + ".transform =" + str(node.transform.tolist()) + "\n") # new transform to apply to node
        f.write("   " + node.name + ".childs += [basic_" + node.name + "]\n")
        f.write("\n")
        f.close()

    else:
        for child in node.childs:
            if not isinstance(child.childs[0], gs.GPUShape):
                mySceneGraph(child)
        f = open("./modeloutput.py", "a")
        f.write("   # writing the cube node: " + node.name + "\n")
        f.write("   " + node.name + " = sg.SceneGraphNode('" + node.name + "')\n")
        f.write("   " + node.name + ".transform = " + str(node.transform.tolist()) + "\n")
        for child in node.childs:
            f.write("   " + node.name + ".childs += [" + child.name + "]\n")
        f.write("\n")
        f.close()


def writeSceneGraph(model):
    f = open("./output.py", "a")
    #f.write("from model import Cube\n")
    mySceneGraph(model)


