# Example of using packing2porenet with [YADE](https://yade-dem.org/)
# Very simple compression test, default materials, default engines
#
# usage:
# YADE example-yade.py
# where YADE can be yade, yadedaily, yade-some-extension etc.

from packing2porenet import export, Sphere, Voronoi, PoreNetwork, Pore

dimensions = (12, 12, 18)
# spheres

pred = pack.inAlignedBox((0, 0, 0), dimensions)
sp = pack.randomDensePack(pred, radius=1, rRelFuzz=0.2, returnSpherePack=True, spheresInCell=200)
sp.toSimulation()

# walls
walls = aabbWalls()
top = walls[5]
O.bodies.append(walls)

# apply oedometric compression
top.state.vel = (0, 0, -0.05)

# pores code
O.engines += [PyRunner(command="pores()", iterPeriod=5000, initRun=True)]  # runs pores() function every 5000 iterations


def poreFilter(pore: Pore):
    sph = pore.sphere
    c = sph.center
    r = sph.radius
    x, y, z = c
    (xmi, ymi, zmi), (xma, yma, zma) = aabbExtrema(centers=True)
    return x - r > xmi and x + r < xma and y - r > ymi and y + r < yma and z - r > zmi and z + r < zma


def fileBase(key, iteration):
    return f"yade-{key}-{iteration:06d}"


def pores():
    print()
    print("pores() function start")
    spheres = [Sphere(b.state.pos, b.shape.radius) for b in O.bodies if isinstance(b.shape, yade.Sphere)]
    i = O.iter
    print("computing pores")
    voro = Voronoi(spheres)
    network = PoreNetwork().fromVoronoi(voro, warn=False, limitTetraQuality=0.8)
    network.filterPores(poreFilter)
    print("export 1")
    export.spheres2vtk(spheres, fileBase("packing", i))
    export.network2vtk(voro, fileBase("voro", i))
    print("merging pores")
    network.mergeIntersectingPores()
    print("export 2")
    pspheres = [pore.sphere for pore in network.cells]
    export.spheres2txt(pspheres, fileBase("pores", i))
    export.spheres2vtk(pspheres, fileBase("pores", i))
    export.network2vtk(network, fileBase("throats", i))
    print("pores() function end")
    print()


# 3D view
try:
    view = yade.qt.View()
    view.eyePosition = (-20, -20, 20)
    view.upVector = (0, 0, 1)
    view.viewDir = (1, 1, -.5)
except:
    pass

# run
O.stopAtIter = 15100
O.run()
