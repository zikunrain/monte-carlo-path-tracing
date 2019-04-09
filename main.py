from IModel import Model
from IBoundingBox import BoundingBox
from GetOutmostBound import getOutmostBound
from InitializeScreen import initializeScreen
import math
from IVec3 import Vec3
from PathTracer import pathTracer
from PathTracer import getColor
import cv2
import numpy as np
from IVec3 import Color
import sys

canvas = np.zeros((512, 512, 3), dtype = 'uint8')
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

maxDepth = 4
sample = 4
if len(sys.argv) > 1:
    sample = int(sys.argv[1])
if len(sys.argv) > 2:
    maxDepth = int(sys.argv[2])


for i in range(rWidth):
    print(i, 512)
    x = screen['LT'].x - i * widthPerPixel
    for j in range(rHeight):
        y = screen['LT'].y - j * heightPerPixel
        z = screen['LT'].z - screen['dz'] * j * heightPerPixel
        pixelVec3 = Vec3(x, y, z)
        cameraP = camera['p']

        colorSum = Color(0, 0, 0)
        for k in range(sample):
            color = getColor(boundingBox, pixelVec3, cameraP, maxDepth)
            colorSum = colorSum.add(color.absColor())
        avgColor = colorSum.scale(1/sample).gamma(1/2.2).dump()
        canvas[j][i] = [int(avgColor.b*255), int(avgColor.g*255), int(avgColor.r*255)]

# print(sample, maxDepth)

cv2.imshow("Canvas", canvas)
cv2.imwrite( "result.jpg", canvas)
cv2.waitKey(0)





