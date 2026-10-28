"""3D-Logo der Hausarzt Praxis Hilden Nord (Blender / bpy).

Medaille mit Dach und medizinischem Kreuz – aus denselben Koordinaten wie das SVG-Logo (64er-Raster).
Aufruf: python logo3d.py <ausgabeordner> [--quick] [--spin <frames>]
  --spin: rendert eine volle Drehung (Einzelbilder in <ausgabeordner>/spin/) statt der Standbilder.
"""
import math, sys, os
import bpy, bmesh
from mathutils import Vector
from shapely.geometry import LineString, Polygon

OUT = sys.argv[1]
QUICK = "--quick" in sys.argv
SPIN = int(sys.argv[sys.argv.index("--spin") + 1]) if "--spin" in sys.argv else 0
os.makedirs(OUT, exist_ok=True)

PALETTES = {  # Primärfarbe je Farbpalette der Website
    "p1": "#1A6FB5", "p2": "#0B4F8A", "p3": "#0E7490", "p4": "#4F5BD5", "p5": "#2563A8",
}

def srgb_to_linear(h):
    def c(v):
        v /= 255
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    return (c(int(h[1:3], 16)), c(int(h[3:5], 16)), c(int(h[5:7], 16)), 1.0)

def svg_xy(px, py):  # 64er-SVG-Raster -> Einheitskreis (Radius 1)
    return ((px - 32) / 32, (32 - py) / 32)

# ---------------------------------------------------------------- Szene
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.device = "CPU"
scene.cycles.samples = 48 if QUICK else 192
scene.cycles.use_denoising = True
scene.render.film_transparent = True
scene.view_settings.view_transform = "Standard"  # Markenfarben unverfälscht
scene.view_settings.look = "None"

# ---------------------------------------------------------------- Materialien
def material(name, color, rough, coat=0.0, metallic=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = color
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metallic
    b.inputs["Coat Weight"].default_value = coat
    b.inputs["Coat Roughness"].default_value = 0.18
    return m

mat_blue = material("Praxisblau", srgb_to_linear(PALETTES["p1"]), 0.32, coat=0.9)
mat_blue.node_tree.nodes["Principled BSDF"].inputs["Coat Roughness"].default_value = 0.04
mat_white = material("Weiß", (0.97, 0.975, 0.985, 1), 0.22, coat=0.6)
mat_ring = material("Siegelring", (0.86, 0.89, 0.93, 1), 0.12, metallic=1.0)

# ---------------------------------------------------------------- Geometrie
root = bpy.data.objects.new("Logo", None)
scene.collection.objects.link(root)

DISC_DEPTH = 0.22
FRONT = DISC_DEPTH / 2
RELIEF = 0.075

bpy.ops.mesh.primitive_cylinder_add(vertices=192, radius=1.0, depth=DISC_DEPTH, location=(0, 0, 0))
disc = bpy.context.object
disc.name = "Medaille"
disc.data.materials.append(mat_blue)
bev = disc.modifiers.new("Fase", "BEVEL"); bev.width = 0.055; bev.segments = 10; bev.limit_method = "ANGLE"; bev.harden_normals = True
bpy.ops.object.shade_smooth()
disc.parent = root

def extrude_polygon(name, poly, height, mat, bevel=0.016):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    scene.collection.objects.link(obj)
    bm = bmesh.new()
    coords = list(poly.exterior.coords)[:-1]
    if Polygon(coords).exterior.is_ccw is False:
        coords.reverse()
    verts = [bm.verts.new((x, y, FRONT - 0.01)) for x, y in coords]
    face = bm.faces.new(verts)
    ext = bmesh.ops.extrude_face_region(bm, geom=[face])
    top = [e for e in ext["geom"] if isinstance(e, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, verts=top, vec=Vector((0, 0, height + 0.01)))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh); bm.free()
    for p in mesh.polygons: p.use_smooth = True
    mesh.materials.append(mat)
    b = obj.modifiers.new("Fase", "BEVEL"); b.width = bevel; b.segments = 5; b.limit_method = "ANGLE"; b.angle_limit = math.radians(40); b.harden_normals = True
    obj.modifiers.new("Glättung", "WEIGHTED_NORMAL")
    obj.parent = root
    return obj

# Dach: Linie (15,31)-(32,16.5)-(49,31), Strichstärke 4.5, runde Enden
roof_line = LineString([svg_xy(15, 31), svg_xy(32, 16.5), svg_xy(49, 31)])
roof = roof_line.buffer(4.5 / 32 / 2, quad_segs=24, cap_style="round", join_style="round")
extrude_polygon("Dach", roof, RELIEF, mat_white)

# Kreuz: SVG-Pfad mit 1.5er runder Kontur
cross_pts = [(29, 28), (35, 28), (35, 35), (42, 35), (42, 41), (35, 41), (35, 48), (29, 48), (29, 41), (22, 41), (22, 35), (29, 35)]
cross = Polygon([svg_xy(*p) for p in cross_pts]).buffer(1.5 / 32 / 2, quad_segs=12, join_style="round")
extrude_polygon("Kreuz", cross, RELIEF, mat_white)

# Siegelring
bpy.ops.mesh.primitive_torus_add(major_radius=0.875, minor_radius=0.016, major_segments=192, minor_segments=24, location=(0, 0, FRONT))
ring = bpy.context.object; ring.name = "Siegelring"; ring.data.materials.append(mat_ring); bpy.ops.object.shade_smooth(); ring.parent = root

# Rückseite: dasselbe Motiv, um 180° gedreht – nach einer halben Drehung seitenrichtig lesbar
for name in ("Dach", "Kreuz", "Siegelring"):
    src = bpy.data.objects[name]
    back = src.copy(); back.data = src.data
    back.name = name + " (Rückseite)"
    scene.collection.objects.link(back)
    back.parent = root
    back.rotation_euler = (0, math.pi, 0)
    if name == "Siegelring":
        back.location = (0, 0, -FRONT)

# ---------------------------------------------------------------- Licht
def area(name, loc, energy, size, color=(1, 1, 1)):
    d = bpy.data.lights.new(name, "AREA"); d.energy = energy; d.size = size; d.color = color
    o = bpy.data.objects.new(name, d); scene.collection.objects.link(o); o.location = loc
    t = o.constraints.new("TRACK_TO"); t.target = root; t.track_axis = "TRACK_NEGATIVE_Z"; t.up_axis = "UP_Y"
    return o

area("Hauptlicht", (-3.2, 2.6, 4.6), 300, 6.0)
area("Aufhellung", (3.6, -1.0, 2.6), 90, 5.0, (0.92, 0.96, 1.0))
area("Kante", (1.5, 3.8, -0.6), 220, 2.5)
glint = area("Glanzstreifen", (2.2, 3.4, 3.8), 260, 1.0)
glint.data.shape = "RECTANGLE"; glint.data.size = 6.0; glint.data.size_y = 0.25
world = bpy.data.worlds.new("Studio"); scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.9, 0.92, 0.95, 1)
world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.22

# Schattenfänger hinter der Medaille (nur für das große Motiv)
bpy.ops.mesh.primitive_plane_add(size=12, location=(0, 0, -0.9))
catcher = bpy.context.object; catcher.name = "Schattenfaenger"; catcher.is_shadow_catcher = True

# ---------------------------------------------------------------- Kamera
cam_data = bpy.data.cameras.new("Kamera"); cam = bpy.data.objects.new("Kamera", cam_data); scene.collection.objects.link(cam); scene.camera = cam
tc = cam.constraints.new("TRACK_TO"); tc.target = root; tc.track_axis = "TRACK_NEGATIVE_Z"; tc.up_axis = "UP_Y"

def render(path, res, cam_loc, lens, rot=(0, 0, 0), shadow=False, samples=None):
    scene.render.resolution_x, scene.render.resolution_y = res
    scene.render.resolution_percentage = 100
    cam.location = cam_loc; cam_data.lens = lens
    root.rotation_euler = [math.radians(a) for a in rot]
    catcher.hide_render = not shadow
    if samples: scene.cycles.samples = samples
    scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print("rendered", path)

def set_blue(hexcolor):
    mat_blue.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = srgb_to_linear(hexcolor)

if SPIN:
    # Volle Drehung um die senkrechte Achse, gleichmäßig und nahtlos (Bild N+1 = Bild 1)
    scene.render.resolution_x = scene.render.resolution_y = 560
    scene.render.resolution_percentage = 100
    scene.render.use_persistent_data = True
    scene.cycles.samples = 40
    catcher.hide_render = True
    cam.location = (0, -1.0, 6.6); cam_data.lens = 100
    scene.frame_start, scene.frame_end = 1, SPIN
    root.rotation_euler = (0, 0, 0); root.keyframe_insert("rotation_euler", index=1, frame=1)
    root.rotation_euler = (0, 2 * math.pi, 0); root.keyframe_insert("rotation_euler", index=1, frame=SPIN + 1)
    action = root.animation_data.action
    for fc in getattr(action, "fcurves", []):
        for kp in fc.keyframe_points: kp.interpolation = "LINEAR"
    if not getattr(action, "fcurves", None):  # Blender 5: Kanäle in Layern/Slots
        for layer in action.layers:
            for strip in layer.strips:
                for bag in strip.channelbags:
                    for fc in bag.fcurves:
                        for kp in fc.keyframe_points: kp.interpolation = "LINEAR"
    os.makedirs(f"{OUT}/spin", exist_ok=True)
    scene.render.filepath = f"{OUT}/spin/frame_"
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    bpy.ops.render.render(animation=True)
    print("spin done")
    sys.exit(0)

# 1) Hauptmotiv: leicht gedreht, mit weichem Schatten
render(f"{OUT}/logo-3d-hero.png", (1600, 1200) if not QUICK else (800, 600), (0, -2.4, 7.0), 70, rot=(0, 18, -6), shadow=True)
# 2) Frontansicht (für Kopfzeile) – je Farbpalette, ohne Schatten
for key, hexcolor in PALETTES.items():
    set_blue(hexcolor)
    render(f"{OUT}/logo-3d-{key}.png", (256, 256), (0, -1.0, 6.6), 100, rot=(0, 0, 0), samples=48 if QUICK else 96)
    if QUICK: break
set_blue(PALETTES["p1"])
# 3) Großes App-/Social-Bild, Frontansicht
if not QUICK:
    render(f"{OUT}/logo-3d-1024.png", (1024, 1024), (0, -1.0, 6.6), 100, samples=160)

bpy.ops.wm.save_as_mainfile(filepath=f"{OUT}/logo-3d.blend")
bpy.data.objects.remove(catcher, do_unlink=True)
bpy.ops.export_scene.gltf(filepath=f"{OUT}/logo-3d.glb", export_format="GLB", use_selection=False, export_lights=False, export_cameras=False)
print("done")
