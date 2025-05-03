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
    
    for face in mesh.polygons:
        if len(face.vertices) == 3:
            indices.extend([face.vertices[0], face.vertices[1], face.vertices[2]])
        elif len(face.vertices) > 3:
            vertex_1 = face.vertices[0]
            for i in range(len(face.vertices)-2):
                vertex_2 = face.vertices[i+1]
                vertex_3 = face.vertices[i+2]
                indices.extend([vertex_1, vertex_2, vertex_3])
    
    data = {
        "vertices" : vertices,
        "indices" : indices
    }
    
    with open(output_file, 'w') as file:
        json.dump(data, file)