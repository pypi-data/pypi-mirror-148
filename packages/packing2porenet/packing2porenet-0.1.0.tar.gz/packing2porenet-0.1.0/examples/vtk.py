from packing2porenet import Voronoi, PoreNetwork, export, ymport

spheres = ymport.txt2spheres("spheres1.txt")
export.spheres2vtk(spheres, "vtk-packing")
voro = Voronoi(spheres)
export.network2vtk(voro, "vtk-voro")
network = PoreNetwork().fromVoronoi(voro)
export.spheres2vtk([pore.asSphere() for pore in network.cells], "vtk-pores")
export.network2vtk(network, "vtk-throats")
network.mergeIntersectingPores()
export.spheres2vtk([pore.asSphere() for pore in network.cells], "vtk-pores-merged")
export.network2vtk(network, "vtk-throats-merged")

print("see exported files in Paraview")
