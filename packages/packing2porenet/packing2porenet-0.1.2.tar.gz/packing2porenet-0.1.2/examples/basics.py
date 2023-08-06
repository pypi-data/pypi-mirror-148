from packing2porenet import PoreNetwork, Voronoi, ymport

spheres = ymport.txt2spheres("spheres1.txt")
voro = Voronoi(spheres)
network = PoreNetwork().fromVoronoi(voro)

print()
print("pores (actual volue, spherical volume):")
for pore in network.cells:
    v1 = pore.asSphere().volume()
    v2 = pore.volume
    print(v2, v1, v2 > v1)

print()
print("check pores overlap 1:")
network.checkPoresOverlaps()

print()
print("check pores overlap 1 - with limit=1.5:")
network.checkPoresOverlaps(limit=1.5)

print()
print("merging coinciding pores")
network.mergeIntersectingPores(limit=1.5)

print()
print("check pores overlap 2:")
network.checkPoresOverlaps()

print()
print("check pores overlap 2 - with limit=1.5:")
network.checkPoresOverlaps(limit=1.5)
