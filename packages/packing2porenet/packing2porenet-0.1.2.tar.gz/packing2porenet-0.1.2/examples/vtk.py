from packing2porenet import Voronoi, PoreNetwork, export, ymport

spheres = ymport.txt2spheres("spheres1.txt")
export.spheres2vtk(spheres, "vtk-packing")
voro = Voronoi(spheres)
export.mesh2vtk(voro, "vtk-voro")
network = PoreNetwork().fromVoronoi(voro)
export.spheres2vtk([pore.asSphere() for pore in network.cells], "vtk-pores")
export.poreNetwork2vtk(network, "vtk-throats")
export.poreNetwork2txt(network, "vtk-network")
network.mergeIntersectingPores()
export.spheres2vtk([pore.asSphere() for pore in network.cells], "vtk-pores-merged")
export.poreNetwork2vtk(network, "vtk-throats-merged")
export.poreNetwork2txt(network, "vtk-network-merged")

print("see exported files in Paraview")
