# imports 
import grafica.basic_shapes as bs
import grafica.scene_graph as sg
from model import create_gpu

def createModel(pipeline):
   shape = bs.createColorNormalsCube(0.5,0.5,0.5)
   gpuCube = create_gpu(shape, pipeline)
   basic_cube = sg.SceneGraphNode('basic_cube')
   basic_cube.childs += [gpuCube]

   # writing the cube leaf: cube_1
   shape = bs.createColorNormalsCube(0.5,0.5,0.5)
   gpuCube = create_gpu(shape, pipeline)
   basic_cube_1 = sg.SceneGraphNode('basic_cube_1')
   basic_cube_1.childs += [gpuCube]
   cube_1 = sg.SceneGraphNode('cube_1')
   cube_1.transform =[[1.0, 0.0, 0.0, 0.30000001192092896], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.30000001192092896], [0.0, 0.0, 0.0, 1.0]]
   cube_1.childs += [basic_cube_1]

   # writing the cube node: cube_0
   cube_0 = sg.SceneGraphNode('cube_0')
   cube_0.transform = [[0.38009220361709595, -0.280601441860199, -0.16368483006954193, 0.0], [0.16070041060447693, 0.3813636004924774, -0.280601441860199, 0.0], [0.2823212444782257, 0.16070041060447693, 0.38009220361709595, 0.0], [0.0, 0.0, 0.0, 1.0]]
   cube_0.childs += [basic_cube]
   cube_0.childs += [cube_1]

   return cube_0