from PIL import Image
class vec3:
    def __init__(self,x:float,y:float,z:float):
        self.x = x
        self.y = y
        self.z = z
    def __str__(self):
        return f"x: {self.x}, y: {self.y}, z: {self.z}"

    def __repr__(self):
        return f"vec3(x={self.x}, y={self.y}, z={self.z})"

class texture:
    def __init__(self, location:str):
        self.location = location
        self.img = Image.open(location).convert("RGB")
        
class triangle:
    def __init__(self, point1:vec3,point2:vec3,point3:vec3, texture:texture, texture_points:tuple[tuple[int,int],tuple[int,int],tuple[int,int]]):
        self.p1 = point1
        self.p2 = point2
        self.p3 = point3
        self.texture = texture
        self.texture_points = texture_points

class hexahedron:
    FACES = [
        (0, 1, 2, 3),   # face 0
        (4, 5, 6, 7),   # face 1
        (0, 1, 5, 4),   # face 2
        (1, 2, 6, 5),   # face 3
        (2, 3, 7, 6),   # face 4
        (3, 0, 4, 7),   # face 5
    ]

    def __init__(self, points: tuple[vec3, vec3, vec3, vec3, vec3, vec3, vec3, vec3],
                 textures: tuple[texture, texture, texture, texture, texture, texture]):
        self.points = points
        self.textures = textures

    def get_triangles(self) -> list[triangle]:
        tris = []
        for indices, tex in zip(self.FACES, self.textures):
            pa, pb, pc, pd = (self.points[i] for i in indices)

            w = tex.img.width  - 1
            h = tex.img.height - 1
            ua, ub, uc, ud = (0, 0), (w, 0), (w, h), (0, h)

            tris.append(triangle(pa, pb, pc, tex, (ua, ub, uc)))
            tris.append(triangle(pa, pc, pd, tex, (ua, uc, ud)))
        return tris