import bpy
import json
import os

desktop = os.path.expanduser("~/Desktop")

output_file = desktop + '/file.json'


object = bpy.context.active_object

if object and object.type == 'MESH':
    mesh = object.data
    
    vertices = []
    uv_coords = []
    indices = []
    
    uv_layer = mesh.uv_layers.active.data
    
    index_count = 0
    for face in mesh.polygons:
        
        for loop_index, vertex_index in enumerate(face.vertices):
            vertex = mesh.vertices[vertex_index]
            vertices.append(vertex.co.x)
            vertices.append(vertex.co.z)
            vertices.append(vertex.co.y)
            
            uv_coord = uv_layer[face.loop_indices[loop_index]].uv
            uv_coords.extend([uv_coord.x, uv_coord.y])
            
        if len(face.vertices) == 3:
            indices.extend([face.vertices[0] + index_count, face.vertices[1] + index_count, face.vertices[2] + index_count])
        elif len(face.vertices) > 3:
            vertex_1 = face.vertices[0] + index_count
            for i in range(len(face.vertices)-2):
                vertex_2 = face.vertices[i+1] + index_count
                vertex_3 = face.vertices[i+2] + index_count
                indices.extend([vertex_1, vertex_2, vertex_3])
        
        index_count += 4
    
    print(len(vertices))
    print(len(indices))
    print(len(vertices))
    
    data = {
        "vertices" : vertices,
        "uv_coords" : uv_coords,
        "indices" : indices
    }
    
    with open(output_file, 'w') as file:
        json.dump(data, file)