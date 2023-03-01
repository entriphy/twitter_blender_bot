import bpy
import os
import random
import sys

# Get animations and cameras
actions: list[bpy.types.Action] = [a for a in bpy.data.actions if "Armature" in a.name] # Animations
cameras: list[bpy.types.Object] = [c for c in bpy.data.objects if c.type == "CAMERA"]
if sys.argv[-1] == "action_count":
    print(len(actions))
    exit(0)

# Scene setup
action = random.choice(actions) # Select random animation
camera = random.choice(cameras) # Select random camera to use
action_name = action.name # Get animation name
bpy.data.objects["Armature"].animation_data.action = action # Set animation to randomly selected action
bpy.context.scene.frame_end = int(action.curve_frame_range[1]) # Set length of render to length of action
bpy.context.scene.camera = camera # Set active camera to randomly selected camera

# Klonoa-specific stuff. Comment or delete this code if you do not need it.
split = action.name.split("_")
idx = split[0]
action_name = "_".join(split[1:-1])
mesh_actions: list[bpy.types.Action] = [a for a in bpy.data.actions if "Armature" not in a.name]
for mesh_action in mesh_actions:
    # Apply blend shape animations (if any)
    if mesh_action.name.startswith(f"{idx}_"):
        part = mesh_action.name.split("_")[-1]
        mesh: bpy.types.Mesh = bpy.data.objects[part].data
        mesh.shape_keys.animation_data.action = mesh_action

# Render to out directory
bpy.context.scene.render.filepath = os.path.join(os.getcwd(), "out", f"{action_name}.mp4")
bpy.ops.render.render(animation=True)
