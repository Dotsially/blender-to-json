import bpy
import json
import os

desktop = os.path.expanduser("~/Desktop")

output_file = desktop + '/file.json'


object = bpy.context.active_object

if object and object.type == 'MESH':
    mesh = object.data
    
    vertices = []
    
    for v in mesh.vertices:
        vertices.append(v.co.x)
        vertices.append(v.co.z)
        vertices.append(v.co.y)
    
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
        "faces" : faces
    }
    
    with open(output_file, 'w') as file:
        json.dump(data, file)