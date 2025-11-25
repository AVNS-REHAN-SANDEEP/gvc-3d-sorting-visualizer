# GVC-3d-sorting-visualizer
(GRAPHICS AND VISUAL COMPUTING).

Visualizing sorting algorithms as animated 3D blocks using Python scripting in Blender. Demonstrates GVC concepts: modeling pipeline, transformations, projections, lighting, shading, animation, and rendering. 

- Developed as an individual project for the Graphics and Visual Computing (GVC) course.

- Thanks to the course instructors for introducing the underlying computer graphics concepts used in this project.


# 3D Sorting Visualization in Blender (Bubble Sort) – GVC Project

This project visualizes the **Bubble Sort** algorithm as an animated 3D block arrangement using **Python scripting inside Blender**.  
It is an individual project for the **Graphics and Visual Computing (GVC)** course, showcasing key concepts like modeling, transformations, shading, lighting, animation, and rendering.

---

## 1. Objective

- Represent an array of numbers as a row of 3D blocks (bars).
- Animate **Bubble Sort** step-by-step:
  - element comparisons,
  - swaps,
  - final sorted configuration.
- Use Blender’s 3D pipeline and Python (`bpy`) to demonstrate:
  - modeling pipeline,
  - viewing transformation (camera setup),
  - perspective projection,
  - lighting and shading,
  - keyframe-based animation,
  - final rendering for demo video.

---

## 2. GVC Concepts Demonstrated

### 2.1 Modeling Pipeline

- The scene is built **procedurally** using Python (no manual placement):
  - The entire scene is cleared with:
    ```python
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    ```
  - A **ground plane** is added:
    ```python
    bpy.ops.mesh.primitive_plane_add(size=600, location=(0,0,0))
    ```
  - A list of integer values `1..N` is shuffled using Python’s `random` module.
  - For each value, a **cube** is created and scaled in Z to represent the value:
    ```python
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0, h/2))
    cube.scale = (BLOCK_WIDTH, BLOCK_WIDTH, h)
    cube.location.z = h / 2
    ```
- The blocks are **evenly spaced** along the X-axis using `BLOCK_WIDTH` and `GAP`.

### 2.2 Viewing Transformation (Camera Setup)

- A **single static camera** is created and positioned so all blocks are visible:

  ```python
  bpy.ops.object.camera_add(location=(0, -CAM_DISTANCE, CAM_HEIGHT))
  cam = bpy.context.object
  cam.data.type = 'PERSP'
  cam.data.angle = math.radians(CAM_ANGLE)
  cam.rotation_euler = (math.radians(68), 0, 0)
  bpy.context.scene.camera = cam

### Parameters:

    CAM_DISTANCE – controls how far the camera is from the blocks.

    CAM_HEIGHT – controls how high above the ground the camera is.

    CAM_ANGLE – controls the field of view (FOV).

- This implements the viewing transformation (camera position + orientation) and ensures the full sorting animation remains in frame.


 ### 2.3 Projection

- The camera uses perspective projection:
   ```python
             cam.data.type = 'PERSP'
            cam.data.angle = math.radians(CAM_ANGLE) 

- The effect of perspective (near blocks appearing larger) is visible in the animation and is discussed in the poster/demo video.

- (Orthographic mode can also be shown by manually switching the camera type in Blender to ORTHO for comparison during the demo.)


### 2.4 Lighting & Shading

A Sun light is added to the scene:  
 
            bpy.ops.object.light_add(type='SUN', location=(10, -10, 60))
            bpy.context.object.data.energy = 6


- All materials use emission shaders for bright, clean visuals that are easy to see in a demo:

   ```python
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


- Different materials encode algorithm states:

       m_normal – default blue blocks

      m_compare – yellow blocks when two elements are being compared

      m_swap – red blocks while swapping two elements

      m_sorted – green for the final sorted array

- This satisfies the shading and lighting requirement using material changes and a light source.

 ### 2.5 Animation (Sorting + Keyframes)

- The Bubble Sort algorithm is implemented directly in the script using a list values and a while loop:
  ```python
  values = list(range(1, N+1))
   random.shuffle(values)

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


### Keyframe-based animation:

- frame controls the current frame in the timeline.

- Comparisons and swaps advance the frame count to create smooth timing.

- The swap(i, j) function interpolates X-locations of two cubes over multiple frames:
  ```python
      for t in range(41):
       f = frame + t
      p = t / 40
        a.location.x = x1 + (x2 - x1) * p
      b.location.x = x2 + (x1 - x2) * p
       a.keyframe_insert("location", frame=f)
       b.keyframe_insert("location", frame=f)


### After sorting finishes:

- All blocks are colored with the sorted material.

- A final keyframe is inserted, and frame_end is set:
  ```python
      final_frame = frame + 120
      set_color(range(N), m_sorted)
      for b in blocks:
       b.keyframe_insert("location", frame=final_frame)
      bpy.context.scene.frame_end = final_frame + 200


- This implements the animation pipeline: algorithm → object transforms → keyframes → playback.

### 2.6 Rendering

- The script prepares the animation timeline (start at frame 1, end at frame_end).

- Rendering is done from the camera view using Blender’s Render → Render Animation.

- The resulting output is used to create the 3–5 minute demo video required by the course.

### 3. Roll Number Based Customization

- The project instructions require using the roll number to define parameters such as number of blocks and camera configuration.

In the script:

     N = 10
    SEED = 20231234
    random.seed(SEED)


    N – number of blocks (array size).

    SEED – random seed for shuffling, derived from roll number.

     Example strategy (explained in poster/demo):

    Let roll number (numeric part) = XXXXXXXX.

    Use:

    SEED = <full roll number digits>

    N = 8 + (last_digit % 8) → ensures between 8 and 15 blocks.

    Use another digit to tweak CAM_ANGLE or CAM_DISTANCE.

    In the final submission, the chosen mapping between roll number and:

    N,

    SEED,

- camera FOV / distance
- is documented and mentioned clearly in the poster and demo.

### 4 Tools & Environment

- Primary Tool: Blender (version X.X – fill in your exact version)

- Language: Python (Blender’s built-in interpreter)

- API: bpy and mathutils.Vector

- Standard Library: random, math

- No external Python libraries or plugins are used beyond Blender’s built-in tools.
