import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.lighting_shaders as ls
import grafica.performance_monitor as pm
from grafica.assets_path import getAssetPath

__author__ = "Ivan Sipiran"
__license__ = "MIT"


# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True


# We will use the global controller as communication with the callback function
controller = Controller()


def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return
    
    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)

def readOFF(filename, color):
    vertices = []
    normals= []
    faces = []

    with open(filename, 'r') as file:
        line = file.readline().strip()
        assert line=="OFF"

        line = file.readline().strip()
        aux = line.split(' ')

        numVertices = int(aux[0])
        numFaces = int(aux[1])

        for i in range(numVertices):
            aux = file.readline().strip().split(' ')
            vertices += [float(coord) for coord in aux[0:]]
        
        vertices = np.asarray(vertices)
        vertices = np.reshape(vertices, (numVertices, 3))
        print(f'Vertices shape: {vertices.shape}')

        normals = np.zeros((numVertices,3), dtype=np.float32)
        print(f'Normals shape: {normals.shape}')

        for i in range(numFaces):
            aux = file.readline().strip().split(' ')
            aux = [int(index) for index in aux[0:]]
            faces += [aux[1:]]
            
            vecA = [vertices[aux[2]][0] - vertices[aux[1]][0], vertices[aux[2]][1] - vertices[aux[1]][1], vertices[aux[2]][2] - vertices[aux[1]][2]]
            vecB = [vertices[aux[3]][0] - vertices[aux[2]][0], vertices[aux[3]][1] - vertices[aux[2]][1], vertices[aux[3]][2] - vertices[aux[2]][2]]

            res = np.cross(vecA, vecB)
            normals[aux[1]][0] += res[0]  
            normals[aux[1]][1] += res[1]  
            normals[aux[1]][2] += res[2]  

            normals[aux[2]][0] += res[0]  
            normals[aux[2]][1] += res[1]  
            normals[aux[2]][2] += res[2]  

            normals[aux[3]][0] += res[0]  
            normals[aux[3]][1] += res[1]  
            normals[aux[3]][2] += res[2]  
        #print(faces)
        norms = np.linalg.norm(normals,axis=1)
        normals = normals/norms[:,None]

        color = np.asarray(color)
        color = np.tile(color, (numVertices, 1))

        vertexData = np.concatenate((vertices, color), axis=1)
        vertexData = np.concatenate((vertexData, normals), axis=1)

        print(vertexData.shape)

        indices = []
        vertexDataF = []
        index = 0

        for face in faces:
            vertex = vertexData[face[0],:]
            vertexDataF += vertex.tolist()
            vertex = vertexData[face[1],:]
            vertexDataF += vertex.tolist()
            vertex = vertexData[face[2],:]
            vertexDataF += vertex.tolist()
            
            indices += [index, index + 1, index + 2]
            index += 3        



        return bs.Shape(vertexDataF, indices)


if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 1000
    height = 1000
    title = "Reading a *.obj file"
    window = glfw.create_window(width, height, title, None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Defining shader programs
    pipeline = ls.SimpleFlatShaderProgram()
    mvpPipeline = es.SimpleModelViewProjectionShaderProgram()

    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Convenience function to ease initialization
    def createGPUShape(pipeline, shape):
        gpuShape = es.GPUShape().initBuffers()
        pipeline.setupVAO(gpuShape)
        gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
        return gpuShape

    # Creating shapes on GPU memory
    gpuAxis = createGPUShape(mvpPipeline, bs.createAxis(7))

    shapePlane = readOFF(getAssetPath('avion.off'), (0.9, 0.6, 0.2))
    gpuPlane = createGPUShape(pipeline, shapePlane)

    shapeHelix = readOFF(getAssetPath('helice.off'), (0.6, 0.9, 0.5))
    gpuHelix = createGPUShape(pipeline, shapeHelix)

    # Setting uniforms that will NOT change on each iteration
    glUseProgram(pipeline.shaderProgram)
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "La"), 1.0, 1.0, 1.0)
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls"), 1.0, 1.0, 1.0)

    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ka"), 0.2, 0.2, 0.2)
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Kd"), 0.9, 0.9, 0.9)
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "lightPosition"), 3, 3, 3)
    
    glUniform1ui(glGetUniformLocation(pipeline.shaderProgram, "shininess"), 100)
    glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "constantAttenuation"), 0.001)
    glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "linearAttenuation"), 0.1)
    glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "quadraticAttenuation"), 0.01)

    # Setting up the projection transform
    projection = tr.perspective(60, float(width)/float(height), 0.1, 100)
    glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

    glUseProgram(mvpPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
    modelTransform = tr.uniformScale(0.5)
    glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "model"), 1, GL_TRUE, modelTransform)

    t0 = glfw.get_time()
    
    perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)

    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)
    dx = 0

    while not glfw.window_should_close(window):

        # Measuring performance
        perfMonitor.update(glfw.get_time())
        glfw.set_window_title(window, title + str(perfMonitor))

        # Using GLFW to check for input events
        glfw.poll_events()

        viewPos = np.array([5,5,5])
        view = tr.lookAt(
            viewPos,
            np.array([0,0,0]),
            np.array([0,1,0])
        )

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        modelTransformPlane = tr.identity()
        modelTransformHelix = tr.identity()

        # Drawing shapes
        glUseProgram(pipeline.shaderProgram)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), viewPos[0], viewPos[1], viewPos[2])
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, modelTransformPlane)
        pipeline.drawCall(gpuPlane)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE,modelTransformHelix)
        pipeline.drawCall(gpuHelix)
        
        glUseProgram(mvpPipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        mvpPipeline.drawCall(gpuAxis, GL_LINES)

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)
        dx += 0.1

    # freeing GPU memory
    gpuAxis.clear()
    gpuPlane.clear()
    gpuHelix.clear()

    glfw.terminate()
        




