import bpy
import os
import random

# Get animations
actions: list[bpy.types.Action] = [a for a in bpy.data.actions if "Armature" in a.name] # Animations
mesh_actions: list[bpy.types.Action] = [a for a in bpy.data.actions if "Armature" not in a.name] # Blend shape animations

# Scene setup
cameras = ["Left", "Right", "IsoLeft", "IsoRight", "Center"] # Probably should get a list of cameras in the scene instead of hard-coding these :p
camera = random.choice(cameras) # Select random camera to use
action = random.choice(actions) # Select random animation
idx = action.name.split("_")[0] # Get index of animation
action_name = '_'.join(action.name.split('_')[1:-1]) # Get animation name
bpy.data.objects["Armature"].animation_data.action = action # Set animation to randomly selected action
bpy.context.scene.frame_end = int(action.curve_frame_range[1]) # Set length of render to length of action
bpy.context.scene.camera = bpy.data.objects[camera] # Set active camera to randomly selected camera

# Apply blend shape animations (if any)
for mesh_action in mesh_actions:
    if mesh_action.name.startswith(f"{idx}_"):
        part = mesh_action.name.split("_")[-1]
        mesh: bpy.types.Mesh = bpy.data.objects[part].data
        mesh.shape_keys.animation_data.action = mesh_action

# Render to out directory
bpy.context.scene.render.filepath = os.path.join(os.getcwd(), "out", f"{action_name}.mp4")
bpy.ops.render.render(animation=True)
