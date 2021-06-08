from flask import Flask
import ghhops_server as hs
import rhino3dm

app = Flask(__name__)
hops = hs.Hops(app)

@hops.component(
    "/sample",
    name = "sampleComponent",
    description = "this is sample component",
    inputs = [
        hs.HopsInteger("Input X", "X", "Input X of sample"),
        hs.HopsInteger("Input Y", "Y", "Input Y of sample")
    ],
    outputs = [
        hs.HopsInteger("Output R", "R", "Output R of sample")

    ]

)

def sampleFunction(X, Y):
    #do sth
    add = X + Y

    return add

# add = sampleFunction(10,20)
# print(add)

if __name__ == "__main__":
    app.run(debug=True)