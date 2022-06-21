'''
Code from ex_transform_imgui.py example
'''
import imgui
import numpy as np

class Controller:
    fillPolygon = True


    def on_key(window, key, scancode, action, mods):
    
        if action != glfw.PRESS:
            return
        
        global controller

        if key == glfw.KEY_SPACE:
            controller.fillPolygon = not controller.fillPolygon

        elif key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window, True)

        else:
            print('Unknown key')


    def transformGuiOverlay(self, locationX, locationY, angle, color):
        
        # start new frame context
        imgui.new_frame()

        # open new window context
        imgui.begin("2D Transformations control", False, imgui.WINDOW_ALWAYS_AUTO_RESIZE)

        # draw text label inside of current window
        imgui.text("Configuration sliders")

        edited, locationX = imgui.slider_float("location X", locationX, -1.0, 1.0)
        edited, locationY = imgui.slider_float("location Y", locationY, -1.0, 1.0)
        edited, angle = imgui.slider_float("Angle", angle, -np.pi, np.pi)
        edited, color = imgui.color_edit3("Modulation Color", color[0], color[1], color[2])
        if imgui.button("Random Modulation Color!"):
            color = (random.uniform(0.0, 1.0), random.uniform(0.0, 1.0), random.uniform(0.0, 1.0))
        imgui.same_line()
        if imgui.button("White Modulation Color"):
            color = (1.0, 1.0, 1.0)

        edited, checked = imgui.checkbox("wireframe", not self.fillPolygon)
        if edited:
            self.fillPolygon = not checked

        # close current window context
        imgui.end()

        # pass all drawing comands to the rendering pipeline
        # and close frame context
        imgui.render()
        imgui.end_frame()

        return locationX, locationY, angle, color

