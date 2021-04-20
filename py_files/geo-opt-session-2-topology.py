'''
inputs:
pts - point list
outputs:
a - mesh
'''

import Rhino.Geometry as rg

mesh = rg.Mesh()

for i in pts:
    mesh.Vertices.Add(i)

mesh.Faces.AddFace(0, 1, 2, 3)
a = mesh