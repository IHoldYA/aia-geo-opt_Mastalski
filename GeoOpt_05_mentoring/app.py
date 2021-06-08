from flask import Flask
import ghhops_server as hs
import rhino3dm as r

import MeshPaths as mp
import meshutils as mu
    
# register hops app as middleware
app = Flask(__name__)
hops = hs.Hops(app)

@hops.component(
    "/meshwalker",
    name = "meshwalker",
    inputs=[
        hs.HopsMesh("Input Mesh", "M", "Mesh"),
        hs.HopsInteger("face Index 1","f1","Face index one"),
        hs.HopsInteger("face Index 2","f2","Face index two")

    ],
    outputs=[
        hs.HopsPoint("list of points","P","shortest path points", hs.HopsParamAccess.LIST),
        hs.HopsInteger("list of faces indexes","F","shortest path face indexes", hs.HopsParamAccess.LIST)

    ]
)
def meshwalker(mesh, f1, f2):
    #do something with this mesh
    #convert the mesh to a nx graph
    G = mp.graphFromMesh(mesh)
    #print(type(G))
    #print(G.nodes)
    
    #use the graph to find the shortest path between two faces
    SP = mp.shortestPath(G, f1, f2)

    pts = SP[0]
    faceInd = SP[1]

    return pts, faceInd


if __name__ == "__main__":
    app.run(debug=True)
    #app.run()