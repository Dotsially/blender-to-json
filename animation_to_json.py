import bpy
from collections import defaultdict
import json
import os


action_name = "UnTpose"
desktop = os.path.expanduser("~/Desktop")
output_file = desktop + "/" + action_name + ".json"


def print_armature_keyframes(action_name):
    action = bpy.data.actions.get(action_name)
    if not action:
        print(f"Action '{action_name}' not found")
        return

    bones = defaultdict(lambda: defaultdict(lambda: {
        "position": [0.0, 0.0, 0.0],
        "rotation": [0.0, 0.0, 0.0, 0.0],
        "scale": [1.0, 1.0, 1.0]
    }))

    for curve in action.fcurves:
        # Parse bone name and channel type
        parts = curve.data_path.split('"')
        if len(parts) < 3:
            continue

        bone_name = parts[1]
        property_type = curve.data_path.split('.')[-1]
        array_index = curve.array_index

        for kp in curve.keyframe_points:
            frame = int(kp.co[0])
            value = kp.co[1]

            if property_type == "location":
                bones[bone_name][frame]["position"][array_index] = value
            elif property_type == "rotation_quaternion":
                bones[bone_name][frame]["rotation"][array_index] = value
            elif property_type == "scale":
                bones[bone_name][frame]["scale"][array_index] = value

    # Convert to desired structure
    final_output = {}
    for bone, frames in bones.items():
        frame_list = []
        for frame_number in sorted(frames.keys()):
            frame_data = frames[frame_number]
            frame_list.append({
                "frame_number": frame_number,
                "position": frame_data["position"],
                "rotation": frame_data["rotation"],
                "scale": frame_data["scale"]
            })
        final_output[bone] = frame_list

    return final_output


animation_string = print_armature_keyframes(action_name)

with open(output_file, 'w') as file:
        json.dump(animation_string, file)