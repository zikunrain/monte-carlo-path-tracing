from GetBound import getBound

def getOutmostBound(faces):
    maxX = -200
    minX = 200
    maxY = -200
    minY = 200
    maxZ = -200
    minZ = 200
    for f in faces:
        bound = f.bound
        minX = bound['minX'] if bound['minX'] < minX else minX
        maxX = bound['maxX'] if bound['maxX'] > maxX else maxX

        minY = bound['minY'] if bound['minY'] < minY else minY
        maxY = bound['maxY'] if bound['maxY'] > maxY else maxY

        minZ = bound['minZ'] if bound['minZ'] < minZ else minZ
        maxZ = bound['maxZ'] if bound['maxZ'] > maxZ else maxZ
    return minX, maxX, minY, maxY, minZ, maxZ