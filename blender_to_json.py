import bpy
import json
import os

desktop = os.path.expanduser("~/Desktop")

output_file = desktop + '/file.json'


object = bpy.context.active_object

if object and object.type == 'MESH':
    mesh = object.data
    
    vertices = []
    indices = []
        
    for v in mesh.vertices:
        vertices.append(v.co.x)
        vertices.append(v.co.z)
        vertices.append(v.co.y)
    
    uv_layer = mesh.uv_layers.active.data
    uv_coords = [None] * int((len(vertices)/3)*2)
    
    looked_at = {}
    for face in mesh.polygons:
        for vertex_index in face.vertices:
            if vertex_index in looked_at:
                continue
            looked_at[vertex_index] = 0
            
            uv_coords[vertex_index*2] = uv_layer[vertex_index].uv.x
            uv_coords[vertex_index*2+1] = uv_layer[vertex_index].uv.y
        
        if len(face.vertices) == 3:
            indices.extend([face.vertices[0], face.vertices[1], face.vertices[2]])
        elif len(face.vertices) > 3:
            vertex_1 = face.vertices[0]
            for i in range(len(face.vertices)-2):
                vertex_2 = face.vertices[i+1]
                vertex_3 = face.vertices[i+2]
                indices.extend([vertex_1, vertex_2, vertex_3])
    
    print(len(vertices))
    print(len(uv_coords))
    
    data = {
        "vertices" : vertices,
        "uv_coords" : uv_coords,
        "indices" : indices
    }
    
    with open(output_file, 'w') as file:
        json.dump(data, file)