import random
import math
from IVec3 import Vec3, Mat3, Mat4, Color
from RotateVector import rotateVecAAroundVecB

# def getColor(boundingBox, pixelVec3, cameraP):
#     rayDir = pixelVec3.sub(cameraP)
#     candidateFaces = boundingBox.obtainCandidateFaces(cameraP, rayDir)

#     tmin = float('inf')
#     targetFace = None
#     intersectedPoint = None

#     for f in candidateFaces:
#         flag, t, p = f.rayIntersectDetect(cameraP, rayDir)
#         if t < tmin:
#             tmin = t
#             targetFace = f
#     if targetFace:
#         weight = 1
#         depth = 10
#         # todo update intersectedPoint
#         color = pathTracer(targetFace, intersectedPoint, rayDir, weight, depth)
#     else:
#         color = None
#     return color


# def pathTracer(face, intersectedPoint, inDir, weight, depth):
#     depth += 1
#     if depth > 11:
#         return 0
#     if face.material.name == 'initialShadingGroup': # 打到光了 返回
#         return
#     else:
#         ourDir = getOutDir(face, inDir)
#         # 必须与法向同一个方向 cos >1
#         candidateFaces = boundingBox.obtainCandidateFaces(intersectedPoint, ourDir)

#         tmin = float('inf')
#         targetFace = None
#         newIntersectedPoint = None

#         for f in candidateFaces:
#             flag, t, p = f.rayIntersectDetect(cameraP, rayDir)
#             if t < tmin:
#                 tmin = t
#                 targetFace = f
#         if targetFace:
#             pathTracer(targetFace, newIntersectedPoint, ourDir, weight, depth)

def getOutDir(face, intersectedPoint):
    n1 = random.random()
    n2 = random.random()

    # 获取随机方向
    r = math.sqrt(n1)
    theta = 2 * math.pi * n2
    x = r * math.cos(theta)
    z = r * math.sin(theta)
    localDir = Vec3(x, math.sqrt(max(0.0, 1 - n1)), z)

    # get Rotation Matrix
    # normVec3 = Vec3(face.normal[0], face.normal[1], face.normal[2]).normalize() # a
    # normVec3.myPrint('norm')
    # up = Vec3(0, 1, 0) # b

    # v = normVec3.cross(up)
    # s = v.length()
    # c = normVec3.dot(up)
    # v = Mat3(0, -v.z, v.y,
    #         v.z, 0, -v.x,
    #         -v.y, v.x, 0)
    # I = Mat3(1, 0, 0,
    #         0, 1, 0,
    #         0, 0, 1)
    # a = (1.0 - c) / (s * s)
    # rotationMat = I.add(v).add(v.mul(v).scale(a))
    # rotationMat 是正确的
    # outDir = rotationMat.apply(localDir) # wrong

    # 转换成全局方向
    normVec3 = Vec3(face.normal[0], face.normal[1], face.normal[2]).normalize()
    if normVec3.z != 0:
        R = Vec3(0, 0, intersectedPoint.dot(normVec3) / normVec3.z)
    else:
        R = Vec3(0, 0, 0)
    zAxis = R.sub(intersectedPoint).normalize()
    xAxis = zAxis.cross(normVec3).normalize()
    W = Mat4(xAxis.x, xAxis.y, xAxis.z, 0,
            normVec3.x, normVec3.y, normVec3.z, 0,
            zAxis.x, zAxis.y, zAxis.z, 0,
            intersectedPoint.x, intersectedPoint.y, intersectedPoint.z, 1)
    outDir = localDir.rotate(W)

    return outDir


def getColor(boundingBox, pixelVec3, cameraP, maxDepth):
    rayDir = pixelVec3.sub(cameraP)
    weight = 1
    depth = 0
    lightLocation = {
        'center': Vec3(-2.758771896, 1.5246, 0),
        'lefttop': Vec3(-2.758771896, 2.0246, 0.5),
        'righttop': Vec3(-2.758771896, 2.0246, -0.5),
        'leftbottom': Vec3(-2.758771896, 1.0246, 0.5),
        'rightbottom': Vec3(-2.758771896, 1.0246, -0.5)
    }
    color, _, _ = pathTracer(boundingBox, cameraP, rayDir, weight, depth, lightLocation, maxDepth)
    return color


def pathTracer(boundingBox, sp, rayDir, weight, depth, lightLocation, maxDepth):
    depth += 1

    # 如果递归深度大于20 返回
    if depth > maxDepth:
        return Color(0, 0, 0), Vec3(0, 0, 0), 1
    
    # 找到第一个相交的面片
    candidateFaces = boundingBox.obtainCandidateFaces(sp, rayDir)
    tmin = float('inf')
    intersectedFace = None
    intersectedPoint = None
    for f in candidateFaces:
        flag, t, p = f.rayIntersectDetect(sp, rayDir)
        candidateNormVec = Vec3(f.normal[0], f.normal[1], f.normal[2]).normalize()
        if (flag and t < tmin and t > 1.0e-10 and candidateNormVec.dot(rayDir.multiple(-1)) > 0):
            tmin = t
            intersectedFace = f
            intersectedPoint = p
    
    # 如果确实与某个面片相交
    if intersectedFace:
        # 不需要的
        r = intersectedPoint.sub(sp).length()

        # 相交面片归一化后的法线
        normVec3 = Vec3(intersectedFace.normal[0], intersectedFace.normal[1], intersectedFace.normal[2]).normalize()

        # 如果打到光了， 返回
        if intersectedFace.material.name == 'initialShadingGroup':
            return Color(0, 0, 0), normVec3, r
        
        ks = intersectedFace.material.Ks
        ns = intersectedFace.material.Ns
        kd = intersectedFace.material.Kd
        kdVec3 = Vec3(kd[0], kd[1], kd[2]) if kd else Vec3(0, 0, 0)
        ksVec3 = Vec3(ks[0], ks[1], ks[2]) if ks else Vec3(0, 0, 0)

        light = Color(0, 0, 0)

        # 检测是否与光源相交
        rayToLightCenter = lightLocation['center'].sub(intersectedPoint) # 当前点到光源中心的射线
        rayToLights = [
            rayToLightCenter,
            lightLocation['lefttop'].sub(intersectedPoint),
            lightLocation['righttop'].sub(intersectedPoint),
            lightLocation['leftbottom'].sub(intersectedPoint),
            lightLocation['rightbottom'].sub(intersectedPoint)
        ]
        intersectedFaceOfLight = None

        for rayToLight in rayToLights:
            intersectedFaceOfLight = None
            candidateFacesContainLight = boundingBox.obtainCandidateFaces(intersectedPoint, rayToLight)
            tmin = float('inf')
            for f in candidateFacesContainLight:
                flag, t, p = f.rayIntersectDetect(intersectedPoint, rayToLight)
                if (flag and t < tmin and t > 1.0e-10):
                    tmin = t
                    intersectedFaceOfLight = f
            if intersectedFaceOfLight and intersectedFaceOfLight.material.name == 'initialShadingGroup':
                break
        
        # candidateFacesContainLight = boundingBox.obtainCandidateFaces(intersectedPoint, rayToLightCenter)
        # tmin = float('inf')
        # for f in candidateFacesContainLight:
        #     flag, t, p = f.rayIntersectDetect(intersectedPoint, rayToLightCenter)
        #     if (flag and t < tmin and t > 1.0e-10):
        #         tmin = t
        #         intersectedFaceOfLight = f

        con_theta_s_direct = 0
        ksVec3_direct = Vec3(0, 0, 0)
        if intersectedFaceOfLight and intersectedFaceOfLight.material.name == 'initialShadingGroup': # 如果与光源直接相交
            distanceToLight = rayToLightCenter.length()
            lightNorm = Vec3(intersectedFaceOfLight.normal[0], intersectedFaceOfLight.normal[1], intersectedFaceOfLight.normal[2]).normalize()
            # RVec = rotateVecAAroundVecB(rayToLightCenter, normVec3)
            # cos_theta_s = RVec.normalize().dot(rayToLight.multiple(-1).normalize())
            cos_theta_light_1 = normVec3.dot(rayToLightCenter.normalize())
            cos_theta_light_2 = rayToLightCenter.normalize().dot(lightNorm.multiple(-1))
            if ns:
                con_theta_s_direct = rotateVecAAroundVecB(rayToLightCenter, normVec3).normalize().multiple(-1).dot(rayDir.normalize())
                con_theta_s_direct = pow(con_theta_s_direct, ns)
                ksVec3_direct = ksVec3.multiple(con_theta_s_direct)

            light = Color(40, 40, 40).dotMul(kdVec3.multiple(cos_theta_light_1).add(ksVec3_direct)).scale(cos_theta_light_1 * cos_theta_light_2 / (distanceToLight * distanceToLight))



        # 获取出射光线
        outDir = getOutDir(intersectedFace, intersectedPoint)

        # 递归光线追踪
        indirect, nextNorm, nextR = pathTracer(boundingBox, intersectedPoint, outDir, weight, depth, lightLocation, maxDepth)
        
        cos_theta_s_indirect = 0
        if ns: # 如果有高光
            cos_theta_s_indirect = rotateVecAAroundVecB(outDir, normVec3).normalize().multiple(-1).dot(rayDir.normalize())
            cos_theta_s_indirect = pow(cos_theta_s_indirect, ns)
        ksVec3_indirect = ksVec3.multiple(cos_theta_s_indirect)

        cos_indirect = normVec3.dot(outDir.normalize())

        return indirect.dotMul(kdVec3.multiple(cos_indirect).add(ksVec3_indirect)).add(light), normVec3, r

    else:
        return Color(0, 0, 0), Vec3(0, 0, 0), 1


