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
   cube_1.transform =[[1.0, 0.0, 0.0, 0.30000001192092896], [0.0, 1.0, 0.0, -0.06304548680782318], [0.0, 0.0, 1.0, -0.24004562199115753], [0.0, 0.0, 0.0, 1.0]]
   cube_1.childs += [basic_cube_1]

   # writing the cube leaf: cube_5
   shape = bs.createColorNormalsCube(0.5,0.5,0.5)
   gpuCube = create_gpu(shape, pipeline)
   basic_cube_5 = sg.SceneGraphNode('basic_cube_5')
   basic_cube_5.childs += [gpuCube]
   cube_5 = sg.SceneGraphNode('cube_5')
   cube_5.transform =[[1.0, 0.0, 0.0, 0.30000001192092896], [0.0, 1.0, 0.0, -0.36779528856277466], [0.0, 0.0, 1.0, 0.22758957743644714], [0.0, 0.0, 0.0, 1.0]]
   cube_5.childs += [basic_cube_5]

   # writing the cube leaf: cube_6
   shape = bs.createColorNormalsCube(0.5,0.5,0.5)
   gpuCube = create_gpu(shape, pipeline)
   basic_cube_6 = sg.SceneGraphNode('basic_cube_6')
   basic_cube_6.childs += [gpuCube]
   cube_6 = sg.SceneGraphNode('cube_6')
   cube_6.transform =[[-0.28079429268836975, 2.945014715194702, 0.05796497315168381, 0.0], [-0.1591329723596573, -0.8048288226127625, 0.42107242345809937, 0.0], [0.5882790684700012, 1.1879879236221313, 0.1415701061487198, 0.03999999910593033], [0.0, 0.0, 0.0, 1.0]]
   cube_6.childs += [basic_cube_6]

   # writing the cube node: cube_2
   cube_2 = sg.SceneGraphNode('cube_2')
   cube_2.transform = [[0.29727408289909363, 0.224104642868042, 0.3616945445537567, 0.0], [0.12568546831607819, -0.5295300483703613, 0.15312010049819946, 0.0], [0.5882790684700012, -0.00011265102511970326, -0.2154885232448578, 0.03999999910593033], [0.0, 0.0, 0.0, 1.0]]
   cube_2.childs += [basic_cube]
   cube_2.childs += [cube_5]
   cube_2.childs += [cube_6]

   # writing the cube leaf: cube_3
   shape = bs.createColorNormalsCube(0.5,0.5,0.5)
   gpuCube = create_gpu(shape, pipeline)
   basic_cube_3 = sg.SceneGraphNode('basic_cube_3')
   basic_cube_3.childs += [gpuCube]
   cube_3 = sg.SceneGraphNode('cube_3')
   cube_3.transform =[[1.0, 0.0, 0.0, 0.30000001192092896], [0.0, 1.0, 0.0, -0.15570810437202454], [0.0, 0.0, 1.0, 0.13616685569286346], [0.0, 0.0, 0.0, 1.0]]
   cube_3.childs += [basic_cube_3]

   # writing the cube leaf: cube_4
   shape = bs.createColorNormalsCube(0.5,0.5,0.5)
   gpuCube = create_gpu(shape, pipeline)
   basic_cube_4 = sg.SceneGraphNode('basic_cube_4')
   basic_cube_4.childs += [gpuCube]
   cube_4 = sg.SceneGraphNode('cube_4')
   cube_4.transform =[[1.0, 0.0, 0.0, 0.30000001192092896], [0.0, 1.0, 0.0, 0.4777291417121887], [0.0, 0.0, 1.0, -0.17892108857631683], [0.0, 0.0, 0.0, 1.0]]
   cube_4.childs += [basic_cube_4]

   # writing the cube node: cube_0
   cube_0 = sg.SceneGraphNode('cube_0')
   cube_0.transform = [[-0.30666056275367737, -0.38530030846595764, -0.2620379626750946, 0.0], [-0.12965400516986847, 0.41209760308265686, -0.3001992106437683, 0.0], [0.5825719833374023, -0.11110439896583557, -0.20474505424499512, 0.03999999910593033], [0.0, 0.0, 0.0, 1.0]]
   cube_0.childs += [basic_cube]
   cube_0.childs += [cube_1]
   cube_0.childs += [cube_2]
   cube_0.childs += [cube_3]
   cube_0.childs += [cube_4]

   return cube_0
# fun to set up lights
def setUpLightsOutput():
   return (0.8831571936607361, 0.4926327168941498, 0.4926327168941498), (1.0, 1.0, 1.0), (1.0, 1.0, 1.0), (1.0, 1.0, 1.0), (1.0, 1.0, 1.0), (1.0, 1.0, 1.0), (-5.0, -5.0, 5.0), (-2.0, 0.0, 0.10000000149011612), 200.0, 0.009999999776482582, 0.003000000026077032, 0.009999999776482582, (0.8828507661819458, 0.6538639068603516, 0.6517414450645447)
