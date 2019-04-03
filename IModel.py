import re
from GetBound import getBound

class Model(object):

    patterns = {
        'get_value': re.compile(r'\w+ (.+)\n'),
        'get_list': re.compile(r'\w+ ([0-9\.-]+) ([0-9\.-]+) ([0-9\.-]+)\n'),
        'get_vertice_info': re.compile(r'(\d+)/\d+/(\d+)')
    }
        
    
    def __init__(self, name, i):
        self.filenames = ['note&scenes/Scene0' + str(i) + '/' + name + '.obj', 'note&scenes/Scene0' + str(i) + '/' + name + '.mtl']
        self.materials = []
        self.faces = []

        self.processFiles()

        print('Model %s loaded: %d faces, %d materials' % (name, len(self.faces), len(self.materials)))
        print(self.materials[0])

    def processFiles(self):
        self.processMTLFile()
        self.processOBJFile()

    # mtl 文件处理
    def processMTLFile(self):
        f = open(self.filenames[1], 'r')

        materials = []
        for line in f.readlines():
            if line[0:6] == 'newmtl':
                materials.append(Material())
                value = self.patterns['get_value'].match(line).group(1)
                materials[len(materials) - 1].name = value
            elif line[0] == 'K':
                search_obj = self.patterns['get_list'].match(line)
                light = [float(search_obj.group(1)), float(search_obj.group(2)), float(search_obj.group(3))]

                if line[1] == 'a':
                    materials[len(materials) - 1].Ka = light
                elif line[1] == 'd':
                    materials[len(materials) - 1].Kd = light
                elif line[1] == 's':
                    materials[len(materials) - 1].Ks = light
            elif line[0] == 'N':
                search_obj = self.patterns['get_value'].match(line)
                value = float(search_obj.group(1))

                if line[1] == 'i':
                    materials[len(materials) - 1].Ni = value
                elif line[1] == 's':
                    materials[len(materials) - 1].Ns = value

        # for m in materials:                 
        #     m.print()
        self.materials = materials
        f.close()

    # obj 文件处理
    def processOBJFile(self):
        f = open(self.filenames[0], 'r')
        faces = []
        vertices = []
        normals = []
        curr_mtl_id = -1

        for line in f.readlines():
            if line[0:2] == 'v ':
                search_obj = self.patterns['get_list'].match(line)
                vertice_pos = [float(search_obj.group(1)), float(search_obj.group(2)), float(search_obj.group(3))]
                vertices.append(vertice_pos)
            elif line[0:2] == 'vn':
                search_obj = self.patterns['get_list'].match(line)
                normal = [float(search_obj.group(1)), float(search_obj.group(2)), float(search_obj.group(3))]
                normals.append(normal)
            elif line[0:6] == 'usemtl':
                name = self.patterns['get_value'].match(line).group(1)
                curr_mtl_id = self.getMTLIdByName(name)
                if curr_mtl_id == -1:
                    print('Material Not Found: ', name)           
            elif line[0:2] == 'f ':
                face_vertices_strlist = line[2:-1].split()
                face_vertices = []
                face_normal = None

                for s in face_vertices_strlist:
                    search_obj = self.patterns['get_vertice_info'].match(s)
                    vertice_id = int(search_obj.group(1)) - 1
                    face_vertices.append(vertices[vertice_id])

                    if face_normal == None:
                        normal_id = int(search_obj.group(2)) - 1
                        face_normal = normals[normal_id]

                # 分割多边形
                vertices_count = len(face_vertices)
                for i in range(vertices_count):
                    if i > 0 and i < vertices_count - 1:
                        triangle = [face_vertices[0], face_vertices[i], face_vertices[i + 1]]
                        face = Face(triangle, face_normal, self.materials[curr_mtl_id])
                        faces.append(face)

        self.faces = faces
        f.close()

    def getMTLIdByName(self, name):
        for id, mtl in enumerate(self.materials):
            if mtl.name == name:
                return id
        return -1

class Face(object):

    def __init__(self, triangle, normal, material):
        self.vertices = triangle  # 三角形 [number, number, number][]
        self.bound = getBound(self)
        self.normal = normal # 法线 [number, number, number]
        self.material = material  # Material

    def print(self):
        print('-------------- Face --------------')
        print('Vertices: ', self.vertices)
        print('Normal: ', self.normal)
        print('Material: ', self.material.name)


class Material(object):

    def __init__(self):
        self.name = ''
        self.Ka = None
        self.Kd = None
        self.Ks = None
        self.Ns = None
        self.Ni = None

    def print(self):
        print('-------------- Material --------------')
        print('Name: ' + self.name)
        print('Ka: ', self.Ka)
        print('Kd: ', self.Kd)
        print('Ks: ', self.Ks)
        print('Ns: ', self.Ns)
        print('Ni: ', self.Ni)