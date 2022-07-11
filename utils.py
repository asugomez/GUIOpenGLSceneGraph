from OpenGL.GL import *
import grafica.gpu_shape as gs

def setUpLightsDefault(pipeline):
    """
    Function that sets up the light components by the default values
    """
    # Setting all uniform shader variables 
    L = 1,1,1
    La= L
    Ld= L
    Ls= L
    Ka = L
    Kd = L
    Ks = L

    # White light in all components: ambient, diffuse and specular.
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "La"), *La)
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld"), *Ld )
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls"), *Ls)

    # Object is barely visible at only ambient. Bright white for diffuse and specular components.
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ka"), *Ka)
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Kd"), *Kd)
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ks"), *Ks)
    
    lightPos = -5, -5, 5
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "lightPosition"), *lightPos)
    #glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), controller.eye[0], controller.eye[1], controller.eye[2])
    shininess = 200
    glUniform1ui(glGetUniformLocation(pipeline.shaderProgram, "shininess"), shininess)

    constantAttenuation = 0.01
    linearAttenuation = 0.003
    quadraticAttenuation = 0.01
    glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "constantAttenuation"), constantAttenuation)
    glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "linearAttenuation"), linearAttenuation)
    glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "quadraticAttenuation"), quadraticAttenuation)

    return La, Ld, Ls, Ka, Kd, Ks, lightPos, shininess, constantAttenuation, linearAttenuation, quadraticAttenuation

def setUpLights(pipeline, La, Ld, Ls, Ka, Kd, Ks, lightPos, viewPos, shininess, constantAttenuation, linearAttenuation, quadraticAttenuation):
    """
    Function that sets up the light components
    """
    # White light in all components: ambient, diffuse and specular.
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "La"), *La)
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld"), *Ld )
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls"), *Ls)

    # Object is barely visible at only ambient. Bright white for diffuse and specular components.
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ka"), *Ka)
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Kd"), *Kd)
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ks"), *Ks)
    
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "lightPosition"), *lightPos)
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), *viewPos)
    glUniform1ui(glGetUniformLocation(pipeline.shaderProgram, "shininess"), int(shininess))

    glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "constantAttenuation"), constantAttenuation)
    glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "linearAttenuation"), linearAttenuation)
    glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "quadraticAttenuation"), quadraticAttenuation)

def mySceneGraph(node):
    """
    Recursive function that writes in the modeloutput.py file the model (shape, gpu and scene graph node)
    """
    if len(node.childs) == 1 and isinstance(node.childs[0].childs[0], gs.GPUShape):
        # write it on a python program
        f = open("./modeloutput.py", "a")
        f.write("   # writing the cube leaf: " + node.name + "\n")
        f.write("   shape = bs.createColorNormalsCube(0.5,0.5,0.5)\n")
        f.write("   gpuCube = create_gpu(shape, pipeline)\n")
        f.write("   basic_" + node.name + " = sg.SceneGraphNode('basic_" + node.name + "')\n")
        #f.write("   basic_" + node.name + ".transform =" + str(newTransform.tolist()) + "\n") # new transform to apply to node
        f.write("   basic_" + node.name + ".childs += [gpuCube]\n") # gpu basic cube
        f.write("   " + node.name + " = sg.SceneGraphNode('"+node.name+"')\n") #scenegraphnode with node name
        f.write("   " + node.name + ".transform =" + str(node.transform.tolist()) + "\n") # new transform to apply to node
        f.write("   " + node.name + ".childs += [basic_" + node.name + "]\n")
        f.write("\n")
        f.close()

    else:
        for child in node.childs:
            if not isinstance(child.childs[0], gs.GPUShape):
                mySceneGraph(child)
        f = open("./modeloutput.py", "a")
        f.write("   # writing the cube node: " + node.name + "\n")
        f.write("   " + node.name + " = sg.SceneGraphNode('" + node.name + "')\n")
        f.write("   " + node.name + ".transform = " + str(node.transform.tolist()) + "\n")
        for child in node.childs:
            f.write("   " + node.name + ".childs += [" + child.name + "]\n")
        f.write("\n")
        f.close()

    

