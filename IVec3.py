import math

class Vec3():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def normalize(self):
        l = self.length()
        return Vec3(self.x / l, self.y / l, self.z / l)
    
    def add(self, vec3):
        return Vec3(self.x + vec3.x, self.y + vec3.y, self.z + vec3.z)
    
    def sub(self, vec3):
        return Vec3(self.x - vec3.x, self.y - vec3.y, self.z - vec3.z)
    
    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def perpend(self, i): # i = 0, 1, 2
        if i == 0:
            return Vec3(self.x, -self.z, self.y)
        elif i == 1:
            return Vec3(-self.z, self.y, self.x)
        else:
            return Vec3(self.x, -self.y, self.z)

    def cross(self, vec3):
        a1 = self.x
        b1 = self.y
        c1 = self.z
        a2 = vec3.x
        b2 = vec3.y
        c2 = vec3.z
        return Vec3(b1 * c2 - b2 * c1, a2 * c1 - a1 * c2, a1 * b2 - a2 * b1)
    
    def dot(self, vec3):
        return self.x * vec3.x + self.y * vec3.y + self.z * vec3.z
    
    def multiple(self, k):
        return Vec3(self.x * k, self.y * k, self.z * k)
    
    def myPrint(self, name):
        print('x: ', self.x, ', y: ', self.y, ', z: ', self.z, name)

    def rotate(self, mat3):
        a = self.dot(Vec3(mat3.m[0][0], mat3.m[1][0], mat3.m[2][0]))
        b = self.dot(Vec3(mat3.m[0][1], mat3.m[1][1], mat3.m[2][1]))
        c = self.dot(Vec3(mat3.m[0][2], mat3.m[1][2], mat3.m[2][2]))
        return Vec3(a, b, c)

class Mat3():
    def __init__(self, m11=0.0, m12=0.0, m13=0.0, m21=0.0, m22=0.0, m23=0.0, m31=0.0, m32=0.0, m33=0.0):
        m = [[], [], []]
        m[0] = [m11, m12, m13]
        m[1] = [m21, m22, m23]
        m[2] = [m31, m32, m33]
        self.m = m
    
    def mul(self, mat3):
        res = Mat3()
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    res.m[i][j] += self.m[i][k] * mat3.m[k][j]
        return res
    
    def add(self, mat3):
        res = Mat3()
        for i in range(3):
            for j in range(3):
                res.m[i][j] = self.m[i][j] + mat3.m[i][j]
        return res

    def scale(self, k):
        res = Mat3()
        for i in range(3):
            for j in range(3):
                res.m[i][j] = self.m[i][j] * k
        return res
    
    def apply(self, vec3):
        m1v = Vec3(self.m[0][0], self.m[0][1], self.m[0][2])
        m2v = Vec3(self.m[1][0], self.m[1][1], self.m[1][2])
        m3v = Vec3(self.m[2][0], self.m[2][1], self.m[2][2])
        return Vec3(m1v.dot(vec3), m2v.dot(vec3), m3v.dot(vec3))

class Mat4():
    def __init__(self, m11=0.0, m12=0.0, m13=0.0, m14=0.0,
                        m21=0.0, m22=0.0, m23=0.0, m24=0.0,
                        m31=0.0, m32=0.0, m33=0.0, m34=0.0,
                        m41=0.0, m42=0.0, m43=0.0, m44=0.0):
        m = [[], [], [], []]
        m[0] = [m11, m12, m13, m14]
        m[1] = [m21, m22, m23, m24]
        m[2] = [m31, m32, m33, m34]
        m[3] = [m41, m42, m43, m44]
        self.m = m

class Color():
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
    
    def add(self, c):
        return Color(self.r + c.r, self.g + c.g, self.b + c.b)
    
    def scale(self, k):
        return Color(self.r * k, self.g * k, self.b * k)
    
    def dotMul(self, vec3):
        return Color(self.r * vec3.x, self.g * vec3.y, self.b * vec3.z)
    
    def colorPrint(self, name):
        print(name + '_rgb: ', self.r, self.g, self.b)
    
    def dump(self):
        r = 1.0 if self.r > 1.0 else self.r
        g = 1.0 if self.g > 1.0 else self.g
        b = 1.0 if self.b > 1.0 else self.b
        return Color(r, g, b)
    
    def removeComplex(self):
        if (type(self.r) == type(complex(1,2))) or (type(self.g) == type(complex(1,2))) or (type(self.b) == type(complex(1,2))):
            return Color(0, 0, 0)
        else:
            return self
    
    def gamma(self, v):
        return Color(pow(self.r, v), pow(self.g, v), pow(self.b, v))
    
    def absColor(self):
        return Color(abs(self.r), abs(self.g), abs(self.b))