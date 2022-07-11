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
        shape = bs.createColorNormalsCube(0.5,0.5,0.5) # WithNormal
        gpuCube = create_gpu(shape, pipeline)
        basic_cube = sg.SceneGraphNode('basic_cube')
        basic_cube.childs += [gpuCube]
        cube = sg.SceneGraphNode('cube_' + str(self.nodeNumber)) # the nodenumber will help to have a hierarchy
        cube.childs += [basic_cube] # leaf can not have child nodes
        self.model = cube

    def clear(self):
        self.model.clear()


class AllModel(object):

    def __init__(self, cube):
        # we start with a basic cube
        self.model = cube.model #first_cube
       

    def addRandomChild(self, pipeline, node_name):
        """
        Add a random newCube to the node_name node
        """
        global count_cube
        count_cube += 1
        node = sg.findNode(self.model, node_name)
        if node == None:
            print("No node founded to add child (addChild function)")
            return
        newCube = Cube(pipeline)
        posy = random.uniform(-0.5,0.5)
        posz = random.uniform(-0.5,0.5)
        newCube.model.transform = tr.translate(0.3, posy, posz)
        node.childs += [newCube.model]

    def addChildV2(self, pipeline, node_name, newCube):
        """
        Add newCube as a child node to node_name node
        """
        global count_cube
        count_cube += 1
        node = sg.findNode(self.model, node_name)
        if node == None:
            print("No node founded to add child (addChild function)")
            return
        node.childs += [newCube.model]


    def draw(self, pipeline, transform, node_name):
        node = sg.findNode(self.model, node_name)
        if node == None:
            print("No node founded to add child (draw function)")
            return
        node.transform = transform
        sg.drawSceneGraphNode(self.model, pipeline, "model")


    def clear(self):
        self.model.clear()

    




