from OpenGL.GL import *

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