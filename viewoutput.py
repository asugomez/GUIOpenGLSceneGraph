import numpy as np
import glfw
import sys
import random
import imgui
from imgui.integrations.glfw import GlfwRenderer
from OpenGL.GL import *
import grafica.transformations as tr
import grafica.lighting_shaders as ls
import grafica.easy_shaders as es
import grafica.basic_shapes as bs
import grafica.scene_graph as sg

from modeloutput import createModel, setUpLightsOutput
from utils import setUpLights

if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 1200
    height = 800

    window = glfw.create_window(width, height, "Scene Graph Node OUTPUT", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)
        print("Could not initialize Window")
        exit(1)

    glfw.make_context_current(window)

    # Creating our shader program and telling OpenGL to use it
    pipeline = ls.SimplePhongShaderProgram()
    glUseProgram(pipeline.shaderProgram)
    
    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)
     # Enabling transparencies
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)

    final_model = createModel(pipeline)

    # ilumination
    La, Ld, Ls, Ka, Kd, Ks, lightPos, viewPos, shininess, constantAttenuation, linearAttenuation, quadraticAttenuation, modulationColor = setUpLightsOutput()

    setUpLights(pipeline, La, Ld, Ls, Ka, Kd, Ks, lightPos, viewPos, shininess, constantAttenuation, linearAttenuation, quadraticAttenuation)
    
    eye = np.array([-2, 0, 0.1])
    up = np.array([0, 0, 1])
    at = np.array([1, 0, 0.1])

    viewPos = eye[0], eye[1], eye[2]
    view = tr.lookAt(eye, at, up)
    projection = tr.perspective(45, width/height, 0.1, 100)

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "modulationColor"),
            *modulationColor)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), eye[0], eye[1], eye[2])
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

        # setting up the model
        sg.drawSceneGraphNode(final_model, pipeline, "model")

        #glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)
    
    glfw.terminate()