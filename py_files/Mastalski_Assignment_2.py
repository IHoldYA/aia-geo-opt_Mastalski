"""Provides a scripting component.
    Inputs:
        m: a mesh
        s: sun vector
    Output:
        a: List of Vectors
        b: List of Points
        c: list of angles
        d: exploded mesh
        """
        
import Rhino.Geometry as rg

#1.
#compute face normals using rg.Mesh.FaceNormals.ComputeFaceNormals()
#output the vectors to a
m.FaceNormals.ComputeFaceNormals()
a = m.FaceNormals

# print(a)

#2.
#get the centers of each facaes using rg.Mesh.Faces.GetFaceCenter()
#store the centers into a list called centers 
#output that list to b

b = []

# print(m.Faces.Count)

for i in range(m.Faces.Count):
    b.append(m.Faces.GetFaceCenter(i))

#3.
#calculate the angle between the sun and each FaceNormal using rg.Vector3d.VectorAngle()
#store the angles in a list called angleList and output it to c

c = []

for i in b:
    c.append(rg.Vector3d.VectorAngle(s, rg.Vector3d(i)))

#4. explode the mesh - convert each face of the mesh into a mesh
#for this, you have to first copy the mesh using rg.Mesh.Duplicate()
#then iterate through each face of the copy, extract it using rg.Mesh.ExtractFaces
#and store the result into a list called exploded in output d

# from System.Collections.Generic import IEnumerable

d = []

# d = m.Faces.GetFaceVertices(0)[1:]

for i in range(m.Faces.Count):
    m_t = rg.Mesh()
    m_v = m.Faces.GetFaceVertices(i)[1:] #slice to get rid of the boolean
    for j in m_v:
        m_t.Vertices.Add(j)
    m_t.Faces.AddFace(*range(len(m_v)))
    m_t.Normals.ComputeNormals()
    m_t.Compact()
    d.append(m_t)


# for i in range(m.Faces.Count):
#     m_t = rg.Mesh()
#     m_t.Faces.AddFace(m.Faces.GetFace(i))
#     d.append(m_t)

# print(d)
#after here, your task is to apply a transformation to each face of the mesh
#the transformation should correspond to the angle value that corresponds that face to it... 
#the result should be a mesh that responds to the sun position... its up to you!

