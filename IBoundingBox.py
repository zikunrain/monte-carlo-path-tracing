from GetBound import getBound
from GetOutmostBound import getOutmostBound
import math


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
    
    def obtainCandidateFaces(self, rayStart, rayDir):
        candidateFaces = []
        stack = []
        for box in self.children:
            stack.append(box)
        while stack:
            cur = stack.pop()
            # res.append(cur.val)
            if cur.rayIntersectDetect(rayStart, rayDir): # 与光线相交
                if len(cur.children) > 0: # 还有孩子，继续细分
                    for box in cur.children:
                        stack.append(box)
                else: # 没有孩子了
                    candidateFaces += cur.faces

        return candidateFaces

        
    
    def rayIntersectDetect(self, rayStart, rayDir):
        mins = [self.minX, self.minY, self.minZ]
        maxs = [self.maxX, self.maxY, self.maxZ]
        d = [rayDir.x, rayDir.y, rayDir.z]
        sp = [rayStart.x, rayStart.y, rayStart.z]
        tmin = 0.0
        tmax = float('inf')
        eps = 0.000000001

        for i in range(3): # x, y, z
            if math.fabs(d[i]) < eps:
                if (sp[i] < mins[i] or sp[i] > maxs[i]):
                    return False
            else:
                ood = 1.0 / d[i]
                t1 = (mins[i] - sp[i]) * ood
                t2 = (maxs[i] - sp[i]) * ood
                
                if t1 > t2:
                    tmp = t1
                    t1 = t2
                    t2 = tmp
                if t1 > tmin:
                    tmin = t1
                if t2 < tmax:
                    tmax = t2

                if tmin > tmax:
                    return False

        return True
        
    
    def generateBVH(self):
        if len(self.faces) < 2:
            return

        childBoundingFaces = [[], [], [], [], [], [], [], []]
        for fi, f in enumerate(self.faces):
            index = self.getBoxIndex(f)
            childBoundingFaces[index - 1].append(f)

        for boxi, faces in enumerate(childBoundingFaces):
            if len(faces) > 0:
                # print(len(faces), boxi)
                if len(faces) == len(self.faces):
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

