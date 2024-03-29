# import flask, ghhops_server, and rhino3dm
# rhino3dm is automatically installed with ghhops_server
from flask import Flask
import ghhops_server as hs
import rhino3dm
import numpy as np


# register hops app as middleware
app = Flask(__name__)
hops = hs.Hops(app)

@hops.component(
    "/pointat",
    name="PointAt",
    description="Get point along curve",
    icon="examples/pointat.png",
    inputs=[
        hs.HopsCurve("Curve", "C", "Curve to evaluate"),
        hs.HopsNumber("t", "t", "Parameter on Curve to evaluate"),
    ],
    outputs=[
        hs.HopsPoint("P", "P", "Point on curve at t")
    ]
)
def pointat(curve, t):
    pt = curve.PointAt(t)
    n = np.array([pt.X, pt.Y, pt.Z])
    print(n)
    return curve.PointAt(t)

if __name__ == "__main__":
    app.run()

