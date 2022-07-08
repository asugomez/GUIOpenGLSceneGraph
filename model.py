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
class BasicShape(ABC):

    def __init__(self, pipeline):
        self.pos_x = 0.0
        self.pos_y = 0.0
        self.pos_z = 0.0
        self.r = 1 # red
        self.g = 1 # green
        self.b = 1 # blue
        self.length = 1 # scale y
        self.width = 1 # scale x 
        self.height = 1 # scale z
        pass

    @abstractmethod
    def draw(self, pipeline):
        """
        draw Scene GraphNode
        """
        pass

class Cube(BasicShape):

    def __init__(self, pipeline):
        super(Cube, self).__init__(pipeline)
        global count_cube
        self.nodeNumber = count_cube
        count_cube += 1
        shape = bs.createColorNormalsCube(0.5,0.5,0.5) #WithNormal
        gpuCube = create_gpu(shape, pipeline)
        self.gpu = gpuCube
        basic_cube = sg.SceneGraphNode('cube')
        basic_cube.childs += [gpuCube]
        cube = sg.SceneGraphNode('cube_' + str(self.nodeNumber)) # the nodenumber will help to have a hierarchy
        cube.childs += [basic_cube]
        self.model = cube

    def draw(self, pipeline, transform = tr.identity()):
        self.model.transform = transform
        #glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, transform)
        #sg.drawSceneGraphNode(self.model, pipeline, "model")
        sg.drawSceneGraphNode(self.model, pipeline, "model")


    def clear(self):
        self.model.clear()

    # def addNode()

class AllModel(object):

    def __init__(self, cube):
        # se comeinza con un cubo básico
        #self.last_child_number = int(cube.nodeNumber)
        #print("cube last number: ", self.last_child_number)
        #first_cube = sg.SceneGraphNode("cube_0")
        #first_cube.childs += [cube.model]
        self.model = cube.model#first_cube

    def addChild(self, pipeline, nodenumber):# buscar por indice
        print(nodenumber)
        node = sg.findNode(self.model, "cube_" + str(nodenumber))
        print("nameeee: ",self.model.name)
        #print("nameeee: ",node.name)
        print(type(node))
        if node == None:
            print("No node founded to add child")
            return
        newCube = Cube(pipeline)
        posy = random.uniform(-0.5,0.5)
        posz = random.uniform(-0.5,0.5)
        newCube.model.transform = tr.translate(0.3, posy, posz)
        node.childs += [newCube.model]


    def draw(self, pipeline, transform, nodenumber):
        node = sg.findNode(self.model, "cube_" + str(nodenumber))
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





