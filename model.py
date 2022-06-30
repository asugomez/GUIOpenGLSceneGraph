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
        cube = sg.SceneGraphNode('cube_' + nodeNumber) # the nodenumber will help to have a hierarchy
        cube.childs += [gpuCube]
        self.model = cube

    def draw(self, pipeline, transform = tr.identity()):
        self.model.transform = transform
        #glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, transform)
        #sg.drawSceneGraphNode(self.model, pipeline, "model")
        sg.drawSceneGraphNode(self.model, pipeline, "model")

    def clear(self):
        self.model.clear()

    # def addNode()

#class AllModel():

