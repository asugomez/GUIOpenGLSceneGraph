# imports 
import grafica.basic_shapes as bs
import grafica.scene_graph as sg
from model import create_gpu

def createModel(pipeline):
   shape = bs.createColorNormalsCube(0.5,0.5,0.5)
   gpuCube = create_gpu(shape, pipeline)
   basic_cube = sg.SceneGraphNode('basic_cube')
   basic_cube.childs += [gpuCube]

   # writing the cube leaf: cube_3
   shape = bs.createColorNormalsCube(0.5,0.5,0.5)
   gpuCube = create_gpu(shape, pipeline)
   basic_cube_3 = sg.SceneGraphNode('basic_cube_3')
   basic_cube_3.childs += [gpuCube]
   cube_3 = sg.SceneGraphNode('cube_3')
   cube_3.transform =[[1.0, 0.0, 0.0, 0.30000001192092896], [0.0, 1.0, 0.0, 0.10245301574468613], [0.0, 0.0, 1.0, -0.27627167105674744], [0.0, 0.0, 0.0, 1.0]]
   cube_3.childs += [basic_cube_3]

   # writing the cube leaf: cube_4
   shape = bs.createColorNormalsCube(0.5,0.5,0.5)
   gpuCube = create_gpu(shape, pipeline)
   basic_cube_4 = sg.SceneGraphNode('basic_cube_4')
   basic_cube_4.childs += [gpuCube]
   cube_4 = sg.SceneGraphNode('cube_4')
   cube_4.transform =[[1.0, 0.0, 0.0, 0.30000001192092896], [0.0, 1.0, 0.0, 0.4713023602962494], [0.0, 0.0, 1.0, -0.16686812043190002], [0.0, 0.0, 0.0, 1.0]]
   cube_4.childs += [basic_cube_4]

   # writing the cube leaf: cube_5
   shape = bs.createColorNormalsCube(0.5,0.5,0.5)
   gpuCube = create_gpu(shape, pipeline)
   basic_cube_5 = sg.SceneGraphNode('basic_cube_5')
   basic_cube_5.childs += [gpuCube]
   cube_5 = sg.SceneGraphNode('cube_5')
   cube_5.transform =[[1.0, 0.0, 0.0, 0.30000001192092896], [0.0, 1.0, 0.0, 0.21534761786460876], [0.0, 0.0, 1.0, 0.38260650634765625], [0.0, 0.0, 0.0, 1.0]]
   cube_5.childs += [basic_cube_5]

   # writing the cube node: cube_1
   cube_1 = sg.SceneGraphNode('cube_1')
   cube_1.transform = [[0.4420827031135559, -0.22958938777446747, -0.1310693323612213, 0.0], [0.18690957129001617, 0.4029311537742615, -0.6993292570114136, 0.0], [0.14009882509708405, 0.18690957129001617, 1.3465839624404907, 0.0], [0.0, 0.0, 0.0, 1.0]]
   cube_1.childs += [basic_cube]
   cube_1.childs += [cube_3]
   cube_1.childs += [cube_4]
   cube_1.childs += [cube_5]

   # writing the cube leaf: cube_2
   shape = bs.createColorNormalsCube(0.5,0.5,0.5)
   gpuCube = create_gpu(shape, pipeline)
   basic_cube_2 = sg.SceneGraphNode('basic_cube_2')
   basic_cube_2.childs += [gpuCube]
   cube_2 = sg.SceneGraphNode('cube_2')
   cube_2.transform =[[1.0, 0.0, 0.0, 0.30000001192092896], [0.0, 1.0, 0.0, -0.28556910157203674], [0.0, 0.0, 1.0, 0.23049339652061462], [0.0, 0.0, 0.0, 1.0]]
   cube_2.childs += [basic_cube_2]

   # writing the cube node: cube_0
   cube_0 = sg.SceneGraphNode('cube_0')
   cube_0.transform = [[0.38009220361709595, -0.280601441860199, -0.16368483006954193, 0.0], [0.16070041060447693, 0.3813636004924774, -0.280601441860199, 0.0], [0.2823212444782257, 0.16070041060447693, 0.38009220361709595, 0.0], [0.0, 0.0, 0.0, 1.0]]
   cube_0.childs += [basic_cube]
   cube_0.childs += [cube_1]
   cube_0.childs += [cube_2]

   return cube_0
# fun to set up lights
def setUpLightsOutput():
   return (0.7095779776573181, 0.16577742993831635, 0.16577742993831635), (1.0, 1.0, 1.0), (1.0, 1.0, 1.0), (1.0, 1.0, 1.0), (1.0, 1.0, 1.0), (0.8380438089370728, 0.253078818321228, 0.253078818321228), (-5.0, -5.0, 5.0), (-2.0, 0.0, 0.10000000149011612), 200.0, 0.009999999776482582, 0.003000000026077032, 0.009999999776482582, (0.5, 0.5, 0.5)
