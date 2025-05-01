import bpy
import json
import os

desktop = os.path.expanduser("~/Desktop")

output_file = desktop + '/file.json'


obj = bpy.context.active_object

if obj and obj.type == 'MESH':
    vertices = []
    indices = []
        
    for v in obj.data.vertices:
        vertices.append(v.co.x)
        vertices.append(v.co.y)
        vertices.append(v.co.z)
    
    for face in obj.data.polygons:
        indices.append(face.vertices[0])
        indices.append(face.vertices[1])
        indices.append(face.vertices[2])
    
    data = {
        "vertices" : vertices,
        "indices" : indices
    }
    
    with open(output_file, 'w') as file:
        json.dump(data, file)