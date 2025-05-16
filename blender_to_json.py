import bpy
import json
import os

desktop = os.path.expanduser("~/Desktop")

output_file = desktop + '/file.json'

bpy.ops.object.mode_set(mode='OBJECT')

object = bpy.context.active_object

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
        
        bones = []
        weights = []
        
        for group in v.groups:
            bones.append(group.group)
            weights.append(group.weight)    
            
        vertices_bones.append(bones)
        vertices_weights.append(weights)
        
    
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
        "faces" : faces
    }
    
    with open(output_file, 'w') as file:
        json.dump(data, file)