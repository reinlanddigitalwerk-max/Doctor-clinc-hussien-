"""3D-Version des Praxislogos (Herz aus Händen, Familie, Stethoskop, EKG) – Blender / bpy.

Das vektorisierte Logo (SVG, Ausschnitt-Modus) wird importiert, je Farbe unterschiedlich hoch
aus einer weißen Medaille herausgehoben und beidseitig angebracht.
Aufruf: python praxis3d.py <logo.svg> <ausgabeordner> [--quick] [--spin <bilder>]
"""
import math, os, sys
import bpy
from mathutils import Vector

SVG, OUT = sys.argv[1], sys.argv[2]
QUICK = "--quick" in sys.argv
SPIN = int(sys.argv[sys.argv.index("--spin") + 1]) if "--spin" in sys.argv else 0
os.makedirs(OUT, exist_ok=True)

def lin(h):
    def c(v):
        v /= 255
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    return (c(int(h[1:3], 16)), c(int(h[3:5], 16)), c(int(h[5:7], 16)), 1.0)

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = "CYCLES"; scene.cycles.device = "CPU"
scene.cycles.samples = 32 if QUICK else 48
scene.cycles.use_denoising = True
scene.render.film_transparent = True
scene.view_settings.view_transform = "Standard"; scene.view_settings.look = "None"

def material(name, hexcol, rough, coat=0.0, metallic=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = lin(hexcol)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metallic
    b.inputs["Coat Weight"].default_value = coat
    b.inputs["Coat Roughness"].default_value = 0.05
    return m

MAT = {
    "#124A87": material("Navy", "#124A87", 0.36, coat=0.5),
    "#2A93C6": material("Hellblau", "#2A93C6", 0.34, coat=0.5),
    "#4FD1C9": material("EKG", "#4FD1C9", 0.3, coat=0.5),
    "#FFFFFF": material("Weiß", "#FFFFFF", 0.25, coat=0.6),
}
DEPTH = {"#124A87": 0.05, "#2A93C6": 0.07, "#4FD1C9": 0.075, "#FFFFFF": 0.035}
NORMALIZE = {"#2B94C6": "#2A93C6", "#2B95C6": "#2A93C6", "#319FC6": "#2A93C6", "#4ED0C8": "#4FD1C9"}
mat_disc = material("Medaille", "#F6F7F9", 0.22, coat=0.9)

root = bpy.data.objects.new("Logo", None); scene.collection.objects.link(root)
DISC = 0.16; FRONT = DISC / 2

bpy.ops.mesh.primitive_cylinder_add(vertices=192, radius=1.0, depth=DISC)
disc = bpy.context.object; disc.name = "Medaille"; disc.data.materials.append(mat_disc)
b = disc.modifiers.new("Fase", "BEVEL"); b.width = 0.05; b.segments = 10; b.limit_method = "ANGLE"; b.harden_normals = True
bpy.ops.object.shade_smooth(); disc.parent = root

# ---- SVG lesen: Bezier-Pfade abtasten, gerade/ungerade Füllregel wie im Browser, als Körper extrudieren
import re, bmesh
from shapely.geometry import Polygon
from shapely.ops import unary_union

def sample_path(d, tx, ty, steps=14):
    rings, cur, start, ring = [], None, None, []
    tokens = re.findall(r"[MCLZ]|-?\d*\.?\d+(?:e-?\d+)?", d)
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if t == "M":
            if len(ring) > 2: rings.append(ring)
            cur = (float(tokens[i + 1]), float(tokens[i + 2])); ring = [cur]; i += 3
        elif t == "C":
            i += 1
            while i < len(tokens) and tokens[i] not in "MCLZ":
                c1 = (float(tokens[i]), float(tokens[i + 1])); c2 = (float(tokens[i + 2]), float(tokens[i + 3])); p = (float(tokens[i + 4]), float(tokens[i + 5]))
                for k in range(1, steps + 1):
                    u = k / steps; v = 1 - u
                    ring.append((v**3 * cur[0] + 3 * v*v*u * c1[0] + 3 * v*u*u * c2[0] + u**3 * p[0],
                                 v**3 * cur[1] + 3 * v*v*u * c1[1] + 3 * v*u*u * c2[1] + u**3 * p[1]))
                cur = p; i += 6
        elif t == "L":
            i += 1
            while i < len(tokens) and tokens[i] not in "MCLZ":
                cur = (float(tokens[i]), float(tokens[i + 1])); ring.append(cur); i += 2
        elif t == "Z":
            if len(ring) > 2: rings.append(ring)
            ring = []; i += 1
        else:
            i += 1
    if len(ring) > 2: rings.append(ring)
    return [[(x + tx, y + ty) for x, y in r] for r in rings]

svg = open(SVG).read()
shapes = []  # (farbe, shapely-geometrie)
for m in re.finditer(r"<path ([^>]*)/>", svg):
    attrs = m.group(1)
    col = re.search(r'fill="(#[0-9A-Fa-f]{6})"', attrs).group(1).upper()
    col = NORMALIZE.get(col, col)
    tr = re.search(r"translate\(([-\d.]+),([-\d.]+)\)", attrs)
    tx, ty = (float(tr.group(1)), float(tr.group(2))) if tr else (0.0, 0.0)
    geom = Polygon()
    for r in sample_path(re.search(r'd="([^"]*)"', attrs).group(1), tx, ty):
        pg = Polygon(r).buffer(0)
        geom = geom.symmetric_difference(pg)  # gerade/ungerade Regel
    if not geom.is_empty:
        shapes.append((col, geom))

allg = unary_union([g for _, g in shapes])
minx, miny, maxx, maxy = allg.bounds
cx, cy = (minx + maxx) / 2, (miny + maxy) / 2
scale = 1.94 / max(maxx - minx, maxy - miny)

def to_xy(x, y):  # SVG (y nach unten) -> Blender, zentriert, Radius ~0.97
    return ((x - cx) * scale, -(y - cy) * scale)

front = bpy.data.objects.new("Logo vorne", None); scene.collection.objects.link(front); front.parent = root

def extrude(name, geom, z0, depth, mat):
    mesh = bpy.data.meshes.new(name); obj = bpy.data.objects.new(name, mesh)
    scene.collection.objects.link(obj); obj.parent = front
    bm = bmesh.new()
    polys = list(geom.geoms) if hasattr(geom, "geoms") else [geom]
    for pg in polys:
        pg = pg.simplify(0.35)
        if pg.is_empty or pg.area < 4: continue
        edges = []
        for ring in [pg.exterior] + list(pg.interiors):
            vs = [bm.verts.new((*to_xy(x, y), z0)) for x, y in list(ring.coords)[:-1]]
            edges += [bm.edges.new((vs[k], vs[(k + 1) % len(vs)])) for k in range(len(vs))]
        res = bmesh.ops.triangle_fill(bm, use_beauty=True, use_dissolve=True, edges=edges)
    faces = [f for f in bm.faces]
    for f in faces: f.normal_update()
    bmesh.ops.recalc_face_normals(bm, faces=faces)
    for f in faces:
        if f.normal.z < 0: f.normal_flip()
    ext = bmesh.ops.extrude_face_region(bm, geom=faces)
    top = [e for e in ext["geom"] if isinstance(e, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, verts=top, vec=Vector((0, 0, depth)))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh); bm.free()
    for p in mesh.polygons: p.use_smooth = True
    mesh.materials.append(mat)
    bv = obj.modifiers.new("Fase", "BEVEL"); bv.width = 0.006; bv.segments = 3; bv.limit_method = "ANGLE"; bv.angle_limit = math.radians(50); bv.harden_normals = True
    obj.modifiers.new("Glättung", "WEIGHTED_NORMAL")
    return obj

for i, (col, geom) in enumerate(shapes):
    extrude(f"Logo {i:02d} {col}", geom, FRONT - 0.005 + 0.0012 * i, DEPTH[col] + 0.005, MAT[col])

# Rückseite: Kopie, um 180° um die senkrechte Achse gedreht -> nach halber Drehung seitenrichtig
back = bpy.data.objects.new("Logo hinten", None); scene.collection.objects.link(back); back.parent = root
back.rotation_euler = (0, math.pi, 0)
for o in list(front.children):
    c = o.copy(); c.data = o.data; scene.collection.objects.link(c); c.parent = back

# ---- Licht wie beim bisherigen Emblem
def area(name, loc, energy, size, color=(1, 1, 1)):
    d = bpy.data.lights.new(name, "AREA"); d.energy = energy; d.size = size; d.color = color
    ob = bpy.data.objects.new(name, d); scene.collection.objects.link(ob); ob.location = loc
    t = ob.constraints.new("TRACK_TO"); t.target = root; t.track_axis = "TRACK_NEGATIVE_Z"; t.up_axis = "UP_Y"
    return ob
area("Hauptlicht", (-3.2, 2.6, 4.6), 260, 6.0)
area("Aufhellung", (3.6, -1.0, 2.6), 80, 5.0, (0.94, 0.97, 1.0))
area("Kante", (1.5, 3.8, -0.6), 200, 2.5)
g = area("Glanzstreifen", (2.2, 3.4, 3.8), 240, 1.0); g.data.shape = "RECTANGLE"; g.data.size = 6.0; g.data.size_y = 0.25
world = bpy.data.worlds.new("Studio"); scene.world = world; world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.9, 0.92, 0.95, 1)
world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.22

cam_d = bpy.data.cameras.new("Kamera"); cam = bpy.data.objects.new("Kamera", cam_d); scene.collection.objects.link(cam); scene.camera = cam
tc = cam.constraints.new("TRACK_TO"); tc.target = root; tc.track_axis = "TRACK_NEGATIVE_Z"; tc.up_axis = "UP_Y"
cam.location = (0, -1.0, 6.6); cam_d.lens = 100

def render_still(path, size, rot_y=0.0, samples=None):
    scene.render.resolution_x = scene.render.resolution_y = size; scene.render.resolution_percentage = 100
    root.rotation_euler = (0, math.radians(rot_y), 0)
    if samples: scene.cycles.samples = samples
    scene.render.filepath = path
    bpy.ops.render.render(write_still=True); print("rendered", path)

if SPIN:
    scene.render.resolution_x = scene.render.resolution_y = 560; scene.render.resolution_percentage = 100
    scene.render.use_persistent_data = True
    scene.frame_start, scene.frame_end = 1, SPIN
    root.rotation_euler = (0, 0, 0); root.keyframe_insert("rotation_euler", index=1, frame=1)
    root.rotation_euler = (0, 2 * math.pi, 0); root.keyframe_insert("rotation_euler", index=1, frame=SPIN + 1)
    act = root.animation_data.action
    for layer in getattr(act, "layers", []):
        for strip in layer.strips:
            for bag in strip.channelbags:
                for fc in bag.fcurves:
                    for kp in fc.keyframe_points: kp.interpolation = "LINEAR"
    for fc in getattr(act, "fcurves", []):
        for kp in fc.keyframe_points: kp.interpolation = "LINEAR"
    os.makedirs(f"{OUT}/spin", exist_ok=True)
    scene.render.filepath = f"{OUT}/spin/frame_"
    scene.render.image_settings.file_format = "PNG"; scene.render.image_settings.color_mode = "RGBA"
    bpy.ops.render.render(animation=True)
    print("spin done")
else:
    render_still(f"{OUT}/praxis-3d-front.png", 512 if QUICK else 1024, 0, 48 if QUICK else 128)
    render_still(f"{OUT}/praxis-3d-angle.png", 512, 32, 48 if QUICK else 96)
    if not QUICK:
        bpy.ops.wm.save_as_mainfile(filepath=f"{OUT}/praxis-logo-3d.blend")
        bpy.ops.export_scene.gltf(filepath=f"{OUT}/praxis-logo-3d.glb", export_format="GLB", export_lights=False, export_cameras=False)
    print("stills done")
