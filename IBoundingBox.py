from GetBound import getBound
from GetOutmostBound import getOutmostBound


class BoundingBox():
    
    def __init__(self, faces, minX, maxX, minY, maxY, minZ, maxZ):
        self.faces = faces
        self.children = []
        self.minX = minX
        self.maxX = maxX
        self.minY = minY
        self.maxY = maxY
        self.minZ = minZ
        self.maxZ = maxZ
        self.generateBVH()
    
    def generateBVH(self):
        if len(self.faces) < 20:
            return

        childBoundingFaces = [[], [], [], [], [], [], [], []]
        for fi, f in enumerate(self.faces):
            index = self.getBoxIndex(f)
            childBoundingFaces[index - 1].append(f)

        for boxi, faces in enumerate(childBoundingFaces):
            if len(faces) > 0:
                # print(len(faces), boxi)
                if len(faces) == len(self.faces):
                    print('return', len(faces), boxi)
                    return
                minX, maxX, minY, maxY, minZ, maxZ = getOutmostBound(faces)
                self.children.append(BoundingBox(faces, minX, maxX, minY, maxY, minZ, maxZ))

    def getBoxIndex(self, f):
        minX = self.minX
        maxX = self.maxX
        minY = self.minY
        maxY = self.maxY
        minZ = self.minZ
        maxZ = self.maxZ
        midX = (maxX + minX) / 2
        midY = (maxY + minY) / 2
        midZ = (maxZ + minZ) / 2
        bound = f.bound

        v1 = f.vertices[0]
        v2 = f.vertices[1]
        v3 = f.vertices[2]

        if ((minX <= v1[0] and v1[0] <=  midX) and \
            (minY <= v1[1] and v1[1] <=  midY) and \
            (minZ <= v1[2] and v1[2] <=  midZ)):
            return 1
        elif ((midX <= v1[0] and v1[0] <=  maxX) and \
            (minY <= v1[1] and v1[1] <=  midY) and \
            (minZ <= v1[2] and v1[2] <=  midZ)):
            return 2
        elif ((minX <= v1[0] and v1[0] <=  midX) and \
            (midY <= v1[1] and v1[1] <=  maxY) and \
            (minZ <= v1[2] and v1[2] <=  midZ)):
            return 3
        elif ((midX <= v1[0] and v1[0] <=  maxX) and \
            (midY <= v1[1] and v1[1] <=  maxY) and \
            (minZ <= v1[2] and v1[2] <=  midZ)):
            return 4

        elif ((minX <= v1[0] and v1[0] <=  midX) and \
            (minY <= v1[1] and v1[1] <=  midY) and \
            (midZ <= v1[2] and v1[2] <=  maxZ)):
            return 5
        elif ((midX <= v1[0] and v1[0] <=  maxX) and \
            (minY <= v1[1] and v1[1] <=  midY) and \
            (midZ <= v1[2] and v1[2] <=  maxZ)):
            return 6
        elif ((minX <= v1[0] and v1[0] <=  midX) and \
            (midY <= v1[1] and v1[1] <=  maxY) and \
            (midZ <= v1[2] and v1[2] <=  maxZ)):
            return 7
        elif ((midX <= v1[0] and v1[0] <=  maxX) and \
            (midY <= v1[1] and v1[1] <=  maxY) and \
            (midZ <= v1[2] and v1[2] <=  maxZ)):
            return 8
        else:
            return -1

