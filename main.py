from IModel import Model
from IBoundingBox import BoundingBox
from GetOutmostBound import getOutmostBound
from InitializeScreen import initializeScreen
import math
from IVec3 import Vec3

rWidth = 512
rHeight = 512
camera = {
    'p': Vec3(0.0, 0.64, 0.52),
    'l': Vec3(0.0, 0.40, 0.30),
    'u': Vec3(0.0, 1.0, 0.0),
    'f': 50
}
near = 0.1
light = {
    'shape': 'quad',
    'center': Vec3(-2.758771896, 1.5246, 0),
    'normal': Vec3(1, 0, 0),
    'size': 1,
    'Le': [40, 40, 40]
}

model = Model('cup', 2)
minX, maxX, minY, maxY, minZ, maxZ = getOutmostBound(model.faces)
boundingBox = BoundingBox(model.faces, minX, maxX, minY, maxY, minZ, maxZ)
screen = initializeScreen(camera, near)

xRange = screen['LT'].x - screen['RT'].x
yRange = screen['LT'].y - screen['LB'].y
widthPerPixel = xRange / rWidth
heightPerPixel = yRange / rHeight

for i in range(rWidth):
    x = screen['LT'].x - i * widthPerPixel
    for j in range(rHeight):
        y = screen['LT'].y - j * heightPerPixel
        z = screen['LT'].z - screen['dz'] * j * heightPerPixel
        # print(x,y,z)




