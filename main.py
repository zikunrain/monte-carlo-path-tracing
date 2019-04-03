from IModel import Model
from IBoundingBox import BoundingBox
from GetOutmostBound import getOutmostBound

model = Model('VeachMIS', 3)
minX, maxX, minY, maxY, minZ, maxZ = getOutmostBound(model.faces)
boundingBox = BoundingBox(model.faces, minX, maxX, minY, maxY, minZ, maxZ)

