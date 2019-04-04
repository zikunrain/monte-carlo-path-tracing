import math

class Vec3():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
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
    
    def myPrint(self, name):
        print(name)
        print('x: ', self.x, ', y: ', self.y, ', z: ', self.z)