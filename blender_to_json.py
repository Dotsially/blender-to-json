import bpy
import json
import os

desktop = os.path.expanduser("~/Desktop")

output_file = desktop + '/file.json'

bpy.ops.object.mode_set(mode='OBJECT')

object = bpy.context.active_object

def recursive_traverse(bone, parent=None):
    bone_location  = bone.head_local
    
    
    result = [(bone.name, bone_location, None)] 
    if parent:
        result = [(bone.name, bone_location, parent.name)] 
        
    # Only process children if they exist
    if hasattr(bone, 'children'):
        for child in bone.children:
            result.extend(recursive_traverse(child, bone))
                
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
        
        
    armature = None
    bones = []
    if object.parent and object.parent.type == 'ARMATURE':
        armature = object.parent.data 
        hierarchy = get_armature_hierarchy(armature)
        for bone_name, bone_location, parent_name in hierarchy:
            bone = {
                "name" : bone_name,
                "location" : [bone_location.x, bone_location.z, bone_location.y],
                "parent" : parent_name
            }
            
            bones.append(bone)
    
            
    
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