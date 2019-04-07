from IVec3 import Vec3
import math

def initializeScreen(camera, near):
    lookDir = camera['l'].sub(camera['p'])
    d = lookDir.length()
    sWidth = 2 * near * math.tan(30 * math.pi / 180)
    screenCenter = Vec3(
        0,
        camera['p'].y + (camera['l'].y - camera['p'].y) * near / d,
        camera['p'].z + (camera['l'].z - camera['p'].z) * near / d
    )
    screenPlaneVector = lookDir.perpend(0)
    alpha = sWidth / 2 / screenPlaneVector.length()
    screenPlaneVector.myPrint('screenPlaneVector')

    screenLeftTop = screenCenter.add(Vec3(sWidth / 2, alpha * screenPlaneVector.y, alpha * screenPlaneVector.z))
    screenLeftBottom = screenCenter.add(Vec3(sWidth / 2, -alpha * screenPlaneVector.y, -alpha * screenPlaneVector.z))
    screenRightTop = screenCenter.add(Vec3(-sWidth / 2, alpha * screenPlaneVector.y, alpha * screenPlaneVector.z))
    screenRightBottom = screenCenter.add(Vec3(-sWidth / 2, -alpha * screenPlaneVector.y, -alpha * screenPlaneVector.z))

    screenLeftTop.myPrint('screenLeftTop')
    screenLeftBottom.myPrint('screenLeftBottom')
    screenRightTop.myPrint('screenRightTop')
    screenRightBottom.myPrint('screenRightBottom')

    return {
        'LT': screenLeftTop,
        'LB': screenLeftBottom,
        'RT': screenRightTop,
        'RB': screenRightBottom,
        'sw': sWidth,
        'sh': sWidth,
        'dz': screenPlaneVector.z / screenPlaneVector.y # y增加1 z增加多少
    }

