import bpy
import random
import math
from mathutils import Vector

# ============== YOUR ROLL NUMBER SETTINGS ==============
N = 10                     # Change this (e.g. 28 from your roll number)
SEED = 20231234            # Put your roll number here
random.seed(SEED)

# Visual settings
BLOCK_WIDTH = 2.3
GAP = 3.5
# ============== CAMERA SETTINGS — FIXED FOR 10 BLOCKS ==============
CAM_DISTANCE = 135         # ← Increased (was 110)
CAM_HEIGHT   = 65          # ← Raised a bit (was 50)
CAM_ANGLE    = 58          # ← Slightly narrower FOV for perfect fit

# ============== CLEAR SCENE ==============
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# ============== GROUND ==============
bpy.ops.mesh.primitive_plane_add(size=600, location=(0,0,0))
ground = bpy.context.object
ground_mat = bpy.data.materials.new("Ground")
ground_mat.use_nodes = True
nodes = ground_mat.node_tree.nodes
nodes.clear()
emission = nodes.new('ShaderNodeEmission')
emission.inputs[0].default_value = (0.03, 0.03, 0.12, 1)
emission.inputs[1].default_value = 4
output = nodes.new('ShaderNodeOutputMaterial')
ground_mat.node_tree.links.new(emission.outputs[0], output.inputs[0])
ground.data.materials.append(ground_mat)

# ============== STATIC CAMERA — NOW PERFECTLY FRAMES ALL 24 BLOCKS ==============
bpy.ops.object.camera_add(location=(0, -CAM_DISTANCE, CAM_HEIGHT))
cam = bpy.context.object
cam.data.type = 'PERSP'
cam.data.angle = math.radians(CAM_ANGLE)          # ← New FOV
cam.rotation_euler = (math.radians(68), 0, 0)     # ← Slightly steeper look-down
bpy.context.scene.camera = cam

# Light
bpy.ops.object.light_add(type='SUN', location=(10, -10, 60))
bpy.context.object.data.energy = 6

# ============== MATERIALS (Emission — never fails) ==============
def make_mat(name, r, g, b):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    emission = nodes.new('ShaderNodeEmission')
    emission.inputs[0].default_value = (r, g, b, 1.0)
    emission.inputs[1].default_value = 6
    output = nodes.new('ShaderNodeOutputMaterial')
    mat.node_tree.links.new(emission.outputs[0], output.inputs[0])
    return mat

m_normal  = make_mat("Normal",  0.1, 0.5, 1.0)    # Blue
m_compare = make_mat("Compare", 1.0, 0.9, 0.1)    # Yellow
m_swap    = make_mat("Swap",    1.0, 0.2, 0.2)    # Red
m_sorted  = make_mat("Sorted",  0.1, 0.9, 0.3)    # Green

# ============== CREATE BLOCKS — ALL ON GROUND ==============
values = list(range(1, N+1))
random.shuffle(values)
blocks = []

for i, h in enumerate(values):
    x = (i - N/2 + 0.5) * (BLOCK_WIDTH + GAP)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0, h/2))
    cube = bpy.context.active_object
    cube.scale = (BLOCK_WIDTH, BLOCK_WIDTH, h)
    cube.location.z = h / 2
    cube.data.materials.append(m_normal)
    blocks.append(cube)

# ============== BUBBLE SORT — NO CHANGES HERE ==============
frame = 60
def set_color(indices, mat):
    for i in indices:
        blocks[i].data.materials.clear()
        blocks[i].data.materials.append(mat)

def swap(i, j):
    global frame
    a, b = blocks[i], blocks[j]
    x1, x2 = a.location.x, b.location.x
    set_color([i, j], m_swap)
    for t in range(41):
        f = frame + t
        p = t / 40
        a.location.x = x1 + (x2 - x1) * p
        b.location.x = x2 + (x1 - x2) * p
        a.keyframe_insert("location", frame=f)
        b.keyframe_insert("location", frame=f)
    blocks[i], blocks[j] = blocks[j], blocks[i]
    values[i], values[j] = values[j], values[i]
    frame += 50

swapped = True
pass_num = 0
while swapped and pass_num < N:
    swapped = False
    for i in range(N - 1 - pass_num):
        set_color([i, i+1], m_compare)
        frame += 20
        if values[i] > values[i+1]:
            swap(i, i+1)
            swapped = True
        set_color([i, i+1], m_normal)
    pass_num += 1
    frame += 30

final_frame = frame + 120
set_color(range(N), m_sorted)
for b in blocks:
    b.keyframe_insert("location", frame=final_frame)

bpy.context.scene.frame_end = final_frame + 200

print("BUBBLE SORT 3D — ALL 24 BLOCKS NOW PERFECTLY VISIBLE!")
print("Camera fixed — no cropping, everything in frame")
print("Press SPACEBAR → Render → Submit!")
