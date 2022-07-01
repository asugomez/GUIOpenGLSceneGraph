from grafica.scene_graph import drawSceneGraphNode
import output

if __name__ == "__main__":
    # import the out put file
    # save the node 
    # call draw scene fraph node

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    window = glfw.create_window(width, height, "Reading Scene Graph Node", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

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

    finalModel = sg.SceneGraphNode("final_model")
    finalModel.childs = [node_gpu] # TODO FIX IT

    drawSceneGraphNode(finalModel, pipeline, 'transform')