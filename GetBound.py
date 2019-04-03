def getBound(f):
    v1 = f.vertices[0]
    x1 = v1[0]
    y1 = v1[1]
    z1 = v1[2]
    v2 = f.vertices[1]
    x2 = v2[0]
    y2 = v2[1]
    z2 = v2[2]
    v3 = f.vertices[2]
    x3 = v3[0]
    y3 = v3[1]
    z3 = v3[2]

    maxX = -200
    minX = 200
    maxY = -200
    minY = 200
    maxZ = -200
    minZ = 200

    minX = min(x1, x2, x3) if min(x1, x2, x3) < minX else minX
    maxX = max(x1, x2, x3) if max(x1, x2, x3) > maxX else maxX

    minY= min(y1, y2, y3) if min(y1, y2, y3) < minY else minY
    maxY = max(y1, y2, y3) if max(y1, y2, y3) > maxY else maxY

    minZ= min(z1, z2, z3) if min(z1, z2, z3) < minZ else minZ
    maxZ = max(z1, z2, z3) if max(z1, z2, z3) > maxZ else maxZ

    return {
        'minX': minX, 'maxX': maxX, 'minY': minY, 'maxY': maxY, 'minZ': minZ, 'maxZ': maxZ
    }
    