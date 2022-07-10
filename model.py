from abc import ABC, abstractmethod # Abstract Base Class
from OpenGL.GL import GL_STATIC_DRAW, GL_TRUE, glUniformMatrix4fv, glGetUniformLocation
import glfw
import grafica.basic_shapes as bs
import grafica.scene_graph as sg
import grafica.transformations as tr
import grafica.easy_shaders as es
import grafica.gpu_shape as gs
import random

count_cube = 0

def create_gpu(shape, pipeline):
    gpu = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpu)
    gpu.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    return gpu

class Cube(object):

    def __init__(self, pipeline):
        global count_cube
        self.nodeNumber = count_cube
        count_cube += 1
        shape = bs.createColorNormalsCube(0.5,0.5,0.5) #WithNormal
        gpuCube = create_gpu(shape, pipeline)
        #self.gpu = gpuCube
        basic_cube = sg.SceneGraphNode('basic cube')
        basic_cube.childs += [gpuCube]
        
        cube = sg.SceneGraphNode('cube_' + str(self.nodeNumber)) # the nodenumber will help to have a hierarchy
        cube.childs += [basic_cube] # leaf can not have child nodes

        self.model = cube

    def draw(self, pipeline, transform = tr.identity()):
        self.model.transform = transform
        #glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, transform)
        #sg.drawSceneGraphNode(self.model, pipeline, "model")
        sg.drawSceneGraphNode(self.model, pipeline, "model")

    def addChild(self):
        basic_cube = sg.SceneGraphNode('basic cube')
        basic_cube.childs += [gpuCube]
        cube = sg.SceneGraphNode('cube_' + str(self.nodeNumber)) # the nodenumber will help to have a hierarchy
        cube.childs += [gpuCube]#[basic_cube]

        self.model = cube


    def clear(self):
        self.model.clear()

    # def addNode()

class AllModel(object):

    def __init__(self, cube):
        # se comeinza con un cubo básico
        self.model = cube.model #first_cube

    def addChild(self, pipeline, nodenumber):
        print("call to add child: ", nodenumber)
        print("call to add child: ", self.model.childs[0].childs)
        node = sg.findNode(self.model, "cube_" + str(nodenumber))
        if node == None:
            print("No node founded to add child (addChild function)")
            return
        newCube = Cube(pipeline)
        posy = random.uniform(-0.5,0.5)
        posz = random.uniform(-0.5,0.5)
        newCube.model.transform = tr.translate(0.3, posy, posz)
        node.childs += [newCube.model]
        print("call to add child final: ", self.model.childs)
        print("fin ")


    def draw(self, pipeline, transform, nodenumber):
        node = sg.findNode(self.model, "cube_" + str(nodenumber))
        if node == None:
            print("No node founded to add child (draw function)")
            return
        node.transform = transform
        sg.drawSceneGraphNode(node, pipeline, "model")


    def clear(self):
        self.model.clear()

    
def addChild(node, name, pipeline):
    
    # The name was not found in this path
    if isinstance(node, gs.GPUShape):
        return None

    # This is the requested node
    if node.name == name:
        print("ime here")
        newCube = Cube(pipeline)
        posy = random.uniform(-0.5,0.5)
        posz = random.uniform(-0.5,0.5)
        newCube.model.transform = tr.translate(0.3, posy, posz)
        print(type(newCube.model))
        node.childs += [newCube.model]
        return
    
    # All childs are checked for the requested name
    for child in node.childs:
        print("hello")
        foundNode = addChild(child, name, pipeline)

    # No child of this node had the requested name
    return None





