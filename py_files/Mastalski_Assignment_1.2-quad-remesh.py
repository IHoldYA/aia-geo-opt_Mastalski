import Rhino.Geometry as rg
import ghpythonlib.treehelpers as th
import math

pt_list1 = []
pt_list2 = []
x = int(x)
y = int(y)
div = int(div)


for i in range(x):    
    p1 = rg.Point3d(i, 0, 0)
    pt_list1.append(p1)

for i in range(x):    
    p2 = rg.Point3d(i, y, 0)
    pt_list2.append(p2)

#create lines
line = []

for i in range(len(pt_list1)):
    l = rg.LineCurve(pt_list1[i], pt_list2[i])
    line.append(l)

#get div parameters
div_par = []

for i in line:
    div_par.append(i.DivideByCount(div, True))

#print(div_par)
#print(len(div_par))

#create div points
div_pt = []

#flat list method

for i in range(len(line)):
    for j in range(len(div_par[i])):
        div_pt.append(line[i].PointAt(div_par[i][j]))

#nested list method

#for i in range(len(line)):
#    t = []
#    for j in range(len(div_par[i])):
#        t.append(line[i].PointAt(div_par[i][j]))
#    div_pt.append(t)

#print(len(div_pt))

#translate points into vectors

v1 = []

for i in div_pt:
    v1.append(rg.Vector3d(i))

#get vector length

v1_len = []

for i in v1:
    v1_len.append(i.Length)

v1_len_sin = []

for i in v1_len:
    v1_len_sin.append(math.sin(i))

#print(v1_len_sin)

#create vector z

v_z = []

for i in v1_len_sin:
    v_z.append(rg.Vector3d(0,0,i))

#move points using vectors

div_pt_moved = []

for i in range(len(div_pt)):
    div_pt_moved.append(div_pt[i] - v_z[i])

#print(div_pt_moved)

#create nurbs curve

#nested_pt = []
#
#for i in range(len(line)):
#    t = []
#    t.append(div_pt_moved[:len(div_par[i])])
#    nested_pt.append(t)
#test tree transition
#a = th.list_to_tree(nested_pt)

deg = int(deg)
nurbs_crv = []
t = div_pt_moved[:]

for i in range(len(line)):
    t = div_pt_moved[i*(len(div_par[i])):len(div_par[i])*(i+1)]
    c = rg.NurbsCurve.Create(False, deg, t)
    nurbs_crv.append(c)

#print(nurbs_crv)

#create loft

norm_loft = rg.LoftType.Normal
no_pt = rg.Point3d.Unset
loft = rg.Brep.CreateFromLoft(nurbs_crv, no_pt, no_pt, norm_loft, False)

#create mesh

m_param = rg.MeshingParameters(m_den, m_min_e)
mesh = rg.Mesh.CreateFromBrep(loft[0], m_param)

#evaluate srf and get U V mesh output
pta = rg.Point3d(0, 0, 0)
ptb = rg.Point3d(0, 1, 0)


srf = loft[0].Faces[0]

pts = {}
srfs = []
grid = []
nrows = m_U
ncolumns = m_V

u_domain = rg.Interval(0, m_U)
v_domain = rg.Interval(0, m_V)
srf.SetDomain(0, u_domain)
srf.SetDomain(1, v_domain)

for i in range(0, m_U + 1):
    gcolumn = []
    for j in range(0, m_V + 1):
        pts[(i, j)] = rg.Surface.PointAt(srf, i, j)
        gcolumn.append(rg.Surface.PointAt(srf, i, j))
    grid.append(gcolumn)


for i in range(0, m_U):
    pcolumn = []
    for j in range(0, m_V):
        panel = rg.NurbsSurface.CreateFromCorners(pts[i,j], pts[i+1,j], pts[i+1,j+1], pts[i,j+1])
        pcolumn.append(panel)
    srfs.append(pcolumn)

srfs = th.list_to_tree(srfs)
grid = th.list_to_tree(grid)

#planarize points to create quad mesh based on UV

planar_pts = {}
planes = []

for i in range(0, m_U):
    pcolumn = []    
    plane = rg.Plane.Unset
    for j in range(0, m_V):
        if i == 0 and j == 0:            
            pts_ie = [pts[i,j], pts[i+1,j], pts[i+1,j+1], pts[i,j+1]]
            p_fit = plane.FitPlaneToPoints(pts_ie)
            planar_pts[(i,j)] = p_fit[1].ClosestPoint(pts[i,j])
            planar_pts[(i+1,j)] = p_fit[1].ClosestPoint(pts[i+1,j])
            planar_pts[(i+1,j+1)] = p_fit[1].ClosestPoint(pts[i+1,j+1])
            planar_pts[(i,j+1)] = p_fit[1].ClosestPoint(pts[i,j+1])
        elif i == 0:            
            pts_ie = [planar_pts[i,j], planar_pts[i+1,j], pts[i+1,j+1], pts[i,j+1]]
            p_fit = plane.FitPlaneToPoints(pts_ie)
            planar_pts[(i+1,j+1)] = p_fit[1].ClosestPoint(pts[i+1,j+1])
            planar_pts[(i,j+1)] = p_fit[1].ClosestPoint(pts[i,j+1])
        else:
            pts_ie = [planar_pts[i,j], pts[i+1,j], pts[i+1,j+1], planar_pts[i,j+1]]
            p_fit = plane.FitPlaneToPoints(pts_ie)
            planar_pts[(i+1,j)] = p_fit[1].ClosestPoint(pts[i+1,j])
            planar_pts[(i+1,j+1)] = p_fit[1].ClosestPoint(pts[i+1,j+1])

#print(planar_pts)

#create plines

m_plines = []

for i in range(0, m_U):
    pcolumn = []
    for j in range(0, m_V):
        panel = rg.Polyline([planar_pts[i,j], planar_pts[i+1,j], planar_pts[i+1,j+1], planar_pts[i,j+1], planar_pts[i,j]])
        pcolumn.append(panel)
    m_plines.append(pcolumn)


#print(planes)
#mesh creation using Vertices.Add and Faces.AddFace

m_p_mesh_test = rg.Mesh()
m_v_n = {}
a = -1

for i in range(0, m_U+1):    
    for j in range(0, m_V+1):
        m_p_mesh_test.Vertices.Add(planar_pts[i,j])
        a += 1
        m_v_n[(i,j)] = a

print(m_v_n)

for i in range(0, m_U):    
    for j in range(0, m_V):
        m_p_mesh_test.Faces.AddFace(m_v_n[i,j], m_v_n[i+1,j], m_v_n[i+1,j+1], m_v_n[i,j+1])

m_p_mesh_test.Normals.ComputeNormals()
m_p_mesh_test.Compact()

print(m_p_mesh_test)

#for i in m_plines:
#    for j in i:
#        m_p_mesh.append([rg.Mesh.CreateFromClosedPolyline(j)])

#m_joined = rg.Mesh()

#for i in m_p_mesh:
#    m_joined.Append(i)
#
##print(m_joined)
##m_joined_w = m_joined.Weld(math.pi/2)
#m_joined_w = m_joined.UnifyNormals()
#
#print(m_joined_w)
#
#m_p_mesh = th.list_to_tree(m_p_mesh)
#m_plines = th.list_to_tree(m_plines)

