import math

def rotateVecAAroundVecB(a, b, angle=math.pi):
    aparallelb = b.multiple(a.dot(b) / b.dot(b))
    aorthogonalb = a.sub(aparallelb)
    omega = b.cross(aorthogonalb)
    x1 = math.cos(angle) / aorthogonalb.length()
    x2 = math.sin(angle) / omega.length()
    return (
        aorthogonalb.multiple(x1)
    ).add(
        omega.multiple(x2)
    ).multiple(aorthogonalb.length())