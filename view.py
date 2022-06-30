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
from ModulationTransformShaderProgram import ModulationTransformShaderProgram
from controller import Controller
from model import Cube, create_gpu, AllModel
from utils import *


if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    controller = Controller()

    width = 1200
    height = 800

    window = glfw.create_window(width, height, "Scene Graph Node", None, None)

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

    # Creating shapes on GPU memory
    initial_cube = Cube(pipeline, "1")
    all_model = AllModel(initial_cube)


    controller.set_shape(all_model) # todo change with many shapes

    # initiliaze imgui context (see documentation)
    imgui.create_context()
    impl = GlfwRenderer(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, controller.on_key)
    # Connecting the callback function 'cursor_pos_callback' to handle mouse events
    glfw.set_cursor_pos_callback(window, controller.cursor_pos_callback)

    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0) # TODO: buscar por qué

    locationX = 0.0
    locationY = 0.0
    locationZ = 0.0
    scaleX = 0.5
    scaleY = 0.5
    scaleZ = 0.5
    angleX = 0.4
    angleY = -0.6
    angleZ = 0.4
    color = (0.5, 0.5, 0.5)

    # ilumination
    La, Ld, Ls, Ka, Kd, Ks, lightPos, shininess, constantAttenuation, linearAttenuation, quadraticAttenuation = \
        setUpLightsDefault(pipeline)

    viewPos = controller.eye[0], controller.eye[1], controller.eye[2]

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()
        # imgui function
        impl.process_inputs()

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # 3D transformation
        locationX, locationY, locationZ, scaleX, scaleY, scaleZ, angleX, angleY, angleZ, color= \
            controller.transformGuiOverlay(locationX, locationY, locationZ, scaleX, scaleY, scaleZ, angleX, angleY, angleZ, color, pipeline, controller.scene.model)
        
        #impl.render(imgui.get_draw_data()) 

        ###############

        #La, Ld, Ls, Ka, Kd, Ks, lightPos, viewPos, shininess, constantAttenuation, linearAttenuation, quadraticAttenuation =\
        #    controller.lightGuiOverlay(La, Ld, Ls, Ka, Kd, Ks, lightPos, viewPos, shininess, constantAttenuation, linearAttenuation, quadraticAttenuation)
        
        #impl.render(imgui.get_draw_data()) 

        #controller.sceneGraphGuiOverlay(pipeline)

        #impl.render(imgui.get_draw_data()) 


        # Setting uniforms and drawing the Quad
        rotationMatrixXY = np.matmul(
            tr.rotationY(angleY),
            tr.rotationX(angleX),
        )

        rotationMatrixXYZ = np.matmul(
            tr.rotationZ(angleZ),
            rotationMatrixXY
        )

        rotationAndScale = np.matmul(
            rotationMatrixXYZ,
            tr.scale(scaleX, scaleY, scaleZ)
        )

        transformMatrix = np.matmul(
                tr.translate(locationX, locationY, locationZ),
                rotationAndScale
            )
        
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "modulationColor"), #modulationColor
            color[0], color[1], color[2])
        
        view = tr.lookAt(controller.eye, controller.at, controller.up)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), controller.eye[0], controller.eye[1], controller.eye[2])
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, controller.projection)
  
        # Setting up the model
        all_model.draw(pipeline, transformMatrix)

        # Drawing the imgui texture over our drawing
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        impl.render(imgui.get_draw_data())

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    # freeing GPU memory
    #controller.clear()

    impl.shutdown()
    glfw.terminate()
