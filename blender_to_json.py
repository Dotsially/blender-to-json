import bpy
import json
import os

desktop = os.path.expanduser("~/Desktop")

output_file = desktop + '/file.json'

bpy.ops.object.mode_set(mode='OBJECT')

object = bpy.context.active_object

def recursive_traverse(bone, parent=None):
    result = [(bone.name, parent)]
        
    # Only process children if they exist
    if hasattr(bone, 'children'):
        for child in bone.children:
            result.extend(recursive_traverse(child, bone.name))
                
    return result

def get_armature_hierarchy(armature):
    # Start traversal from root bones (bones without parents)
    hierarchy = []
    for bone in armature.bones:
        if not bone.parent:
            hierarchy.extend(recursive_traverse(bone))
            
    return hierarchy


if object and object.type == 'MESH':
    mesh = object.data
    armature = None
    
    if object.parent and object.parent.type == 'ARMATURE':
         armature = object.parent.data
         
    hierarchy = get_armature_hierarchy(armature)
    bones = []
    for bone_name, parent_name in hierarchy:
        bone = []
        bone.append(bone_name)
        bone.append(parent_name)
        bones.append(bone)
    
    vertices = []
    normals = []
    vertices_bones = []
    vertices_weights = []
    
    
    for v in mesh.vertices:
        vertices.append(v.co.x)
        vertices.append(v.co.z)
        vertices.append(v.co.y)
        
        normals.append(v.normal.x)
        normals.append(v.normal.z)
        normals.append(v.normal.y)
        
        vertex_groups = []
        vertex_weights = []
        
        for group in v.groups:
            vertex_groups.append(object.vertex_groups[group.group].name)
            vertex_weights.append(group.weight)    
            
        vertices_bones.append(vertex_groups)
        vertices_weights.append(vertex_weights)
        
    
    faces = []
    uv_layer = mesh.uv_layers.active.data
    for face in mesh.polygons:
        uv_coords = []
        indices = []
        
        for loop_index, vertex_index in enumerate(face.vertices):    
            uv_coord = uv_layer[face.loop_indices[loop_index]].uv
            uv_coords.extend([uv_coord.x, uv_coord.y])
            
            indices.append(vertex_index)
        
        face = {
            "uv_coords" : uv_coords,
            "indices" : indices    
        }
        
        faces.append(face)        
    
    data = {
        "vertices" : vertices,
        "vertices_bones" : vertices_bones,
        "vertices_weights" : vertices_weights,
        "normals" : normals,
        "faces" : faces,
        "bones" : bones
    }
    
    with open(output_file, 'w') as file:
        json.dump(data, file)