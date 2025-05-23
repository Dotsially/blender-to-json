import bpy
from mathutils import Vector, Quaternion

def print_armature_keyframes(action_name):
    # Get the action
    action = bpy.data.actions.get(action_name)
    if not action:
        print(f"Action '{action_name}' not found")
        return
        
    # Print header
    print(f"\n=== Keyframe Data for Action: {action_name} ===\n")
    
    # Process each bone's keyframes
    for curve in action.fcurves:
        # Extract bone name from data path
        parts = curve.data_path.split('"')
        if len(parts) < 3:
            continue
            
        bone_name = parts[1]
        channel_type = curve.data_path.split('.')[-1]
        channel_idx = curve.array_index
        
        # Get all keyframe points
        keyframes = [(kp.co[0], kp.co[1]) for kp in curve.keyframe_points]
        
        # Print formatted data
        print(f"BONE: {bone_name}")
        print(f"CHANNEL: {channel_type} (Index: {channel_idx})")
        
        # Format values based on channel type
        formatted_values = []
        for frame, value in keyframes:
            if 'rotation' in channel_type.lower():
                # Rotation values (quaternion components)
                if channel_idx == 0:
                    suffix = "W"
                elif channel_idx == 1:
                    suffix = "X"
                elif channel_idx == 2:
                    suffix = "Y"
                else:
                    suffix = "Z"
                formatted_values.append(f"{value:.4f}")
            else:
                # Position values (XYZ coordinates)
                suffix = ['X', 'Y', 'Z'][channel_idx]
                formatted_values.append(f"{value:.4f}")
                
            print(f"Frame {frame:.0f}: {suffix} = {formatted_values[-1]}")
            
        print()

# Example usage
print_armature_keyframes("UnTpose")