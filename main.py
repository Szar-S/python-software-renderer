import math

import objects
from PIL import Image

FOLDERS = {"textures": "textures/",
           "output":"output/"}
WIDTH = 720
HEIGHT = 720
FRAME_COUNT = 36
FRAME_DURATION = 60
OUTPUT = "cube.gif"

NEAR = 0.01

def from_3D_to_Image2D(point: objects.vec3) -> tuple[int,int]|None:
    if point.z < NEAR:
        return None
    x = point.x / point.z
    y = point.y / point.z
    pixel_x = int((x + 1) * WIDTH / 2)
    pixel_y = int((1 - y) * HEIGHT / 2)
    return (pixel_x, pixel_y)

def edge(a, b, p):
    return (p[0] - a[0]) * (b[1] - a[1]) - (p[1] - a[1]) * (b[0] - a[0])

def facing_camera(tri, center) -> bool:
    a, b, c = tri.p1, tri.p2, tri.p3
    ux, uy, uz = b.x - a.x, b.y - a.y, b.z - a.z
    vx, vy, vz = c.x - a.x, c.y - a.y, c.z - a.z
    nx = uy * vz - uz * vy
    ny = uz * vx - ux * vz
    nz = ux * vy - uy * vx

    fx = (a.x + b.x + c.x) / 3.0
    fy = (a.y + b.y + c.y) / 3.0
    fz = (a.z + b.z + c.z) / 3.0

    if nx * (fx - center.x) + ny * (fy - center.y) + nz * (fz - center.z) < 0.0:
        nx, ny, nz = -nx, -ny, -nz

    return nx * (-fx) + ny * (-fy) + nz * (-fz) > 0.0

def render_triangle(tri, pixels, zbuffer):
    p0 = from_3D_to_Image2D(tri.p1)
    p1 = from_3D_to_Image2D(tri.p2)
    p2 = from_3D_to_Image2D(tri.p3)
    if p0 is None or p1 is None or p2 is None:
        return

    min_x = max(0, int(math.floor(min(p0[0], p1[0], p2[0]))))
    max_x = min(WIDTH - 1, int(math.ceil(max(p0[0], p1[0], p2[0]))))
    min_y = max(0, int(math.floor(min(p0[1], p1[1], p2[1]))))
    max_y = min(HEIGHT - 1, int(math.ceil(max(p0[1], p1[1], p2[1]))))
    if min_x > max_x or min_y > max_y:
        return

    area = edge(p0, p1, p2)
    if abs(area) < 1e-9:
        return

    uv0, uv1, uv2 = tri.texture_points
    tex_img = tri.texture.img
    tex_pixels = tex_img.load()
    tex_w, tex_h = tex_img.size

    inv_z0 = 1.0 / tri.p1.z
    inv_z1 = 1.0 / tri.p2.z
    inv_z2 = 1.0 / tri.p3.z

    for y in range(min_y, max_y + 1):
        row = y * WIDTH
        for x in range(min_x, max_x + 1):
            p = (x + 0.5, y + 0.5)

            w0 = edge(p1, p2, p) / area
            w1 = edge(p2, p0, p) / area
            w2 = edge(p0, p1, p) / area

            if w0 < 0.0 or w1 < 0.0 or w2 < 0.0:
                continue

            inv_z = w0 * inv_z0 + w1 * inv_z1 + w2 * inv_z2
            idx = row + x

            if inv_z <= zbuffer[idx]:
                continue

            u = (w0 * uv0[0] * inv_z0 +
                 w1 * uv1[0] * inv_z1 +
                 w2 * uv2[0] * inv_z2) / inv_z
            v = (w0 * uv0[1] * inv_z0 +
                 w1 * uv1[1] * inv_z1 +
                 w2 * uv2[1] * inv_z2) / inv_z

            tu = min(tex_w - 1, max(0, int(u)))
            tv = min(tex_h - 1, max(0, int(v)))

            zbuffer[idx] = inv_z
            pixels[x, y] = tex_pixels[tu, tv]

def rotate_point(p, angle, tilt, center):
    x, y, z = p.x, p.y, p.z - center.z

    ct, st = math.cos(tilt), math.sin(tilt)
    y, z = ct * y - st * z, st * y + ct * z

    ca, sa = math.cos(angle), math.sin(angle)
    x, z = ca * x + sa * z, -sa * x + ca * z

    return objects.vec3(x, y, z + center.z)

def main():
    white_t = objects.texture(f"{FOLDERS['textures']}white_t.png")#
    textures = tuple([objects.texture(f"{FOLDERS['textures']}/RGB_cube/cubeside{i}.png") for i in range(6)]) # (white_t,)*6

    s = 0.5
    cz = 2.0
    CENTER = objects.vec3(0.0, 0.0, cz)
    TILT = math.radians(-20.0)

    base_points = (
        objects.vec3(-s, -s, cz - s),
        objects.vec3( s, -s, cz - s),
        objects.vec3( s, -s, cz + s),
        objects.vec3(-s, -s, cz + s),
        objects.vec3(-s,  s, cz - s),
        objects.vec3( s,  s, cz - s),
        objects.vec3( s,  s, cz + s),
        objects.vec3(-s,  s, cz + s),
    )
    
    frames = []

    for i in range(FRAME_COUNT):
        angle = 2.0 * math.pi * i / FRAME_COUNT

        points = tuple(rotate_point(p, angle, TILT, CENTER) for p in base_points)
        cube = objects.hexahedron(points, textures)

        img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
        pixels = img.load()
        zbuffer = [0.0] * (WIDTH * HEIGHT)

        for tri in cube.get_triangles():
            if not facing_camera(tri, CENTER):
                continue
            render_triangle(tri, pixels, zbuffer)

        frames.append(img)
        print(f"frame {i + 1}/{FRAME_COUNT}")

    palette_source = frames[0].quantize(colors=256, method=Image.MEDIANCUT)
    gif_frames = [f.quantize(palette=palette_source) for f in frames]

    gif_frames[0].save(
        FOLDERS["output"]+OUTPUT,
        save_all=True,
        append_images=gif_frames[1:],
        duration=FRAME_DURATION,
        loop=0,
        optimize=False,
    )
    
if __name__ == "__main__":
    main()