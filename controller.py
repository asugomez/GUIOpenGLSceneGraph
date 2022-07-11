import numpy as np
import imgui # see documentation here: https://github.com/ocornut/imgui#demo 
# doc also here: https://pyimgui.readthedocs.io/en/latest/reference/imgui.core.html
import random
import glfw
import grafica.gpu_shape as gs
import grafica.transformations as tr
from utils import mySceneGraph

from model import Cube

class Controller():

    def __init__(self):
        self.fillPolygon = True
        self.scene = None
        self.width = 1000
        self.height = 800
        self.eye = np.array([-2, 0, 0.1])
        self.up = np.array([0, 0, 1])
        self.at = np.array([1, 0, 0.1])
        self.projection = tr.perspective(45, self.width/self.height, 0.1, 100)
        self.name_node_selected = "cube_0" # initial node
        L = 1,1,1 # initial value
        self.La= L
        self.Ld= L
        self.Ls= L
        self.Ka = L
        self.Kd = L
        self.Ks = L
        self.lightPos = -5, -5, 5
        self.shininess = 200
        self.constantAttenuation = 0.01
        self.linearAttenuation = 0.003
        self.quadraticAttenuation = 0.01
        self.modulationColor = 1,1,1

    @property
    def mouseX(self):
        # Getting the mouse location in opengl coordinates
        mousePosX = 2 * (self.mousePos[0] - self.width/2) / self.width
        return mousePosX
    
    @property
    def mouseY(self):
        # Getting the mouse location in opengl coordinates
        mousePosY = 2 * (self.height/2 - self.mousePos[1]) / self.height
        return mousePosY

    def set_shape(self, shape):
        self.scene = shape

    def add_shape(self, pipeline, node_name):
        newCube = Cube(pipeline)
        newCube.model.transform = tr.translate(0.3, 0, 0.3)
        #self.scene.addChildV2(pipeline, node_name, newCube)
        self.scene.addRandomChild(pipeline, node_name)

    def save_setup_lights(self, La, Ld, Ls, Ka, Kd, Ks, lightPos, viewPos, shininess, constantAttenuation, linearAttenuation, quadraticAttenuation, modulationColor):
        """
        Function that saves the light components
        """
        self.La= La
        self.Ld= Ld
        self.Ls= Ls
        self.Ka = Ka
        self.Kd = Kd
        self.Ks = Ks
        self.lightPos = lightPos
        self.viewPos = viewPos
        self.shininess = shininess
        self.constantAttenuation = constantAttenuation
        self.linearAttenuation = linearAttenuation
        self.quadraticAttenuation = quadraticAttenuation
        self.modulationColor = modulationColor
        #print(La, Ld, Ls, Ka, Kd, Ks, lightPos, shininess, constantAttenuation, linearAttenuation, quadraticAttenuation, modulationColor)
        
    def get_setup_lights(self):
        return self.La, self.Ld, self.Ls, self.Ka, self.Kd, self.Ks, self.lightPos, self.viewPos, self.shininess, self.constantAttenuation, self.linearAttenuation, self.quadraticAttenuation, self.modulationColor

    def cursor_pos_callback(self, window, x, y):
        #print("call back cursor")
        self.mousePos = (x,y)

    def on_key(self, window, key, scancode, action, mods):
    
        if action != glfw.PRESS:
            return

        if key == glfw.KEY_SPACE:
            self.fillPolygon = not self.fillPolygon

        elif key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window, True)

        ### perspective (thir camera)
        elif key == glfw.KEY_1 and action == glfw.PRESS:
            print("click on 1")
            self.eye = np.array([-2, 0, 0.1])
            self.at = np.array([1, 0, 0.1])
            self.up = np.array([0, 0, 1])
            self.projection = tr.perspective(45, self.width/self.height, 0.1, 100)

        ### second perspective (from angle)
        elif key == glfw.KEY_2 and action == glfw.PRESS:
            print("click on 2")
            self.eye = np.array([-4, -1, 0.3]) # esquina superior derecha
            self.at = np.array([2, 2, -0.1]) # hacia abajo en diagonal
            self.up = np.array([0, 0, 1])
            self.projection = tr.perspective(80, self.width/self.height, 0.1, 100)

        else:
            print('Unknown key')

    def transformGuiOverlay(self, locationX, locationY, locationZ, scaleX, scaleY, scaleZ, angleX, angleY, angleZ, color, pipeline):
        """
        Create the frame to modify the position, scale, color and angle 
        """
        # open new window context
        imgui.begin("3D Transformations control", False, imgui.WINDOW_ALWAYS_AUTO_RESIZE)
        #imgui.treee
        imgui.text("Transformations and constants")

        # position
        edited, locationX = imgui.slider_float("location X", locationX, -1, 3)
        edited, locationY = imgui.slider_float("location Y", locationY, -1, 1)
        edited, locationZ = imgui.slider_float("location Z", locationZ, -0.5, 0.5)
        # scale
        edited, scaleX = imgui.slider_float("scale X", scaleX, 0, 5)
        edited, scaleY = imgui.slider_float("scale Y", scaleY, 0, 5)
        edited, scaleZ = imgui.slider_float("scale Z", scaleZ, 0, 5)
        # rotations
        edited, angleX = imgui.slider_float("Angle X", angleX, -np.pi, np.pi)
        edited, angleY = imgui.slider_float("Angle Y", angleY, -np.pi, np.pi)
        edited, angleZ = imgui.slider_float("Angle Z", angleZ, -np.pi, np.pi)
        # color
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

        return locationX, locationY, locationZ, scaleX, scaleY, scaleZ, angleX, angleY, angleZ, color

    def lightGuiOverlay(self, La, Ld, Ls, Ka, Kd, Ks, lightPos, viewPos, shininess, constantAttenuation, linearAttenuation, quadraticAttenuation):
        """
        Create the frame to modify the light components (constants, ligh and view position, shininess)
        """
        # window position
        imgui.set_next_window_position(0, 400)

        # open new window context
        imgui.begin("Light Transformations control", False, imgui.WINDOW_ALWAYS_AUTO_RESIZE)

        # white light
        edited, La = imgui.color_edit3("La", La[0], La[1], La[2])
        edited, Ld = imgui.color_edit3("Ld", Ld[0], Ld[1], Ld[2])
        edited, Ls = imgui.color_edit3("Ls", Ls[0], Ls[1], Ls[2])
        # constants K
        edited, Ka = imgui.color_edit3("Ka", Ka[0], Ka[1], Ka[2])
        edited, Kd = imgui.color_edit3("Kd", Kd[0], Kd[1], Kd[2])
        edited, Ks = imgui.color_edit3("Ks", Ks[0], Ks[1], Ks[2])
        # light position
        edited, lightPosX = imgui.slider_float("lightPosX", lightPos[0], -2, 2)
        edited, lightPosY = imgui.slider_float("lightPosY", lightPos[1], -2, 2)
        edited, lightPosZ = imgui.slider_float("lightPosZ", lightPos[2], -2, 2)
        lightPos = lightPosX, lightPosY, lightPosZ
        # view position
        edited, viewPosX = imgui.slider_float("viewPosX", viewPos[0], -2, 2)
        edited, viewPosY = imgui.slider_float("viewPosY", viewPos[1], -2, 2)
        edited, viewPosZ = imgui.slider_float("viewPosZ", viewPos[2], -2, 2)
        viewPos = viewPosX, viewPosY, viewPosZ

        # shine
        edited, shininess = imgui.slider_float("shininess", shininess, 0, 100)
        # constants
        edited, constantAttenuation = imgui.slider_float("constantAttenuation", constantAttenuation, 0, 1)
        edited, linearAttenuation = imgui.slider_float("linearAttenuation", linearAttenuation, 0, 1)
        edited, quadraticAttenuation = imgui.slider_float("quadraticAttenuation", quadraticAttenuation, 0, 1)

        # close current window context
        imgui.end()

        return La, Ld, Ls, Ka, Kd, Ks, lightPos, viewPos, shininess, constantAttenuation, linearAttenuation, quadraticAttenuation

    def sceneGraphGuiOverlay(self, pipeline):
        """
        Create the frame to see the scene graph tree node and the buttons 'save' and 'add'
        """
        # window position
        imgui.set_next_window_position(800, 0)

        # open new window context
        imgui.begin("Scene graph", False, imgui.WINDOW_ALWAYS_AUTO_RESIZE)

        if imgui.button("Save"):
            print("click on save")
            self.create_code_output()

        imgui.same_line()
        if imgui.button("Add"):
            # add a child to the node
            self.add_shape(pipeline, self.name_node_selected)

        visible = True

        self.create_tree_node(self.scene.model)
        
        # close current window context
        imgui.end()

    def clear(self):
        self.scene.clear()

    def create_tree_node(self, model):
        """
        Recursive function that creates the scene graph tree node
        """
        # TODO draw as selected
        if len(model.childs) == 1 and isinstance(model.childs[0].childs[0], gs.GPUShape):
            if imgui.tree_node(model.name, imgui.TREE_NODE_SELECTED): # change to opened
                if imgui.is_item_clicked():
                    #imgui.tree_node.flags(imgui.TREE_NODE_SELECTED)
                    self.name_node_selected = model.name
                imgui.tree_pop() # call tree_pop() to finish.
        else:
            if imgui.tree_node(model.name, imgui.TREE_NODE_SELECTED):
                if imgui.is_item_clicked():
                    #imgui.TREE_NODE_SELECTED
                    self.name_node_selected = model.name

                for child in model.childs:
                    if not isinstance(child.childs[0], gs.GPUShape):
                        self.create_tree_node(child)
                imgui.tree_pop() 

    def create_code_output(self):
        """
        Function that creates the output code to make the model
        It saves all the model and the lights set up
        """
        # fun createModel
        f = open("./modeloutput.py", "w")
        f.write("# imports \n")
        f.write("import grafica.basic_shapes as bs\n")
        f.write("import grafica.scene_graph as sg\n")
        f.write("from model import create_gpu\n")
        f.write("\n")
        f.write("def createModel(pipeline):\n")
        f.write("   shape = bs.createColorNormalsCube(0.5,0.5,0.5)\n")
        f.write("   gpuCube = create_gpu(shape, pipeline)\n")
        f.write("   basic_cube = sg.SceneGraphNode('basic_cube')\n")
        f.write("   basic_cube.childs += [gpuCube]\n")
        f.write("\n")
        f.close()
        # write the model
        mySceneGraph(self.scene.model)
        f = open("./modeloutput.py", "a")
        f.write("   return cube_0\n")
        f.close()
        # fun setUpLights
        La, Ld, Ls, Ka, Kd, Ks, lightPos, viewPos, shininess, constantAttenuation, linearAttenuation, quadraticAttenuation, modulationColor = \
            self.get_setup_lights()
        f = open("./modeloutput.py", "a")
        f.write("# fun to set up lights\n")
        f.write("def setUpLightsOutput():\n")
        f.write("   return " + str(La) + ", " + str(Ld) + ", " + str(Ls) + ", " + str(Ka) + ", " +  str(Kd) + ", " +  str(Ks) + ", " + str(lightPos) + ", " + str(viewPos) + ", " +str(shininess) + ", " +  str(constantAttenuation) + ", " + str(linearAttenuation) + ", " + str(quadraticAttenuation) + ", " + str(modulationColor) + "\n")
        f.close()
