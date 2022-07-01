from OpenGL.GL import *
import grafica.gpu_shape as gs


def setUpLightsDefault(pipeline):
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


def saveSceneGraphNode(node):
    """ 
    Save the graph node into a python file
    """
    print("sgname: ", node.name)
    print(len(node.childs))
    # All childs are checked for the requested name
    #for child in sgNode.childs:
    #    print(child.name)
    #for child in node.childs:
    #    if child != None:
    #        return foundNode
    if len(node.childs) == 1 and isinstance(node.childs[0], gs.GPUShape):
        print("name: ",node.name)
        print("transform: ", node.transform)
        # TODO: ver algun arbol mas complejo como ejemplo
        # shape = 
        # gpu_cube_3 = 
        # cube_3 = sg.SceneGraphNode(node.name)
        # cube_3.transform = node.transform
        # cube_3.childs += [gpu]

    # If the child node is not a leaf, it MUST be a SceneGraphNode,
    # so this draw function is called recursively
    else:
        for child in node.childs:
            saveSceneGraphNode(child)

    

