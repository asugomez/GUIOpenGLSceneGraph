from abc import ABC, abstractmethod # Abstract Base Class
from OpenGL.GL import GL_STATIC_DRAW, GL_TRUE, glUniformMatrix4fv, glGetUniformLocation
import glfw
import grafica.basic_shapes as bs
import grafica.scene_graph as sg
import grafica.transformations as tr
import grafica.easy_shaders as es


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

    def __init__(self, pipeline, nodeNumber):
        super(Cube, self).__init__(pipeline)
        shape = bs.createColorNormalsCube(0.5,0.5,0.5) #WithNormal
        gpuCube = create_gpu(shape, pipeline)
        self.gpu = gpuCube
        cube = sg.SceneGraphNode('cube_' + str(nodeNumber)) # the nodenumber will help to have a hierarchy
        cube.childs += [gpuCube]
        self.model = cube
        self.nodeNumber = nodeNumber

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
        self.last_child_number = int(cube.nodeNumber)
        first_cube = sg.SceneGraphNode("cube")
        first_cube.childs += [cube.model]
        self.model = first_cube
        #self.cubes = cubepu

    def addChild(self, pipeline, nodenumber):# buscar por indice
        # find node
        #target_node = sg.findNode(node, 'cube_'+str(nodenumber))
        #if target_node == None:
        #    print("No node founded!")
        #    return

        self.last_child_number += 1 # cada nodo está indexado
        newCube = Cube(pipeline, self.last_child_number)
        newCube.model.transform = tr.translate(0.3, 0.2, 0.4)
        #newCube.model.childs += [newCube.gpu]
        #print("type: ", type(newCube.model))
        self.model.childs += [newCube.model]
        # update last child numebr

    def draw(self, pipeline, transform = tr.identity()):
        self.model.transform = transform
        #glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, transform)
        #sg.drawSceneGraphNode(self.model, pipeline, "model")
        sg.drawSceneGraphNode(self.model, pipeline, "model")


    def clear(self):
        self.model.clear()

    





