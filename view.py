import glfw
import numpy as np
import sys
import random
import imgui
from imgui.integrations.glfw import GlfwRenderer
from OpenGL.GL import *
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.transformations as tr
import grafica.lighting_shaders as ls
from ModulationTransformShaderProgram import ModulationTransformShaderProgram
from controller import Controller


if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 1000
    height = 800

    controller = Controller()

    window = glfw.create_window(width, height, "Solid DIY", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Creating our shader program and telling OpenGL to use it
    pipeline = ModulationTransformShaderProgram() #ls.SimpleTexturePhongShaderProgram()
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)

    # Creating shapes on GPU memory
    shapeQuad = bs.createRainbowQuad()
    gpuQuad = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuQuad)
    gpuQuad.fillBuffers(shapeQuad.vertices, shapeQuad.indices, GL_STATIC_DRAW)


    # initilize imgui context (see documentation)
    imgui.create_context()
    impl = GlfwRenderer(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    # It is important to set the callback after the imgui setup
    glfw.set_key_callback(window, controller.on_key)

    locationX = 0.0
    locationY = 0.0
    angle = 0.0
    color = (1.0, 1.0, 1.0)

    while not glfw.window_should_close(window):

        impl.process_inputs()
        # Using GLFW to check for input events

        glfw.poll_events()

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        # imgui function
        impl.process_inputs()

        locationX, locationY, angle, color = \
            controller.transformGuiOverlay(locationX, locationY, angle, color)

        # Setting uniforms and drawing the Quad
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE,
            np.matmul(
                tr.translate(locationX, locationY, 0.0),
                tr.rotationZ(angle)
            )
        )
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "modulationColor"),
            color[0], color[1], color[2])
        pipeline.drawCall(gpuQuad)

        # Drawing the imgui texture over our drawing
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        impl.render(imgui.get_draw_data())

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    # freeing GPU memory
    gpuQuad.clear()

    impl.shutdown()
    glfw.terminate()
