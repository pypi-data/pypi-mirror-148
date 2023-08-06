# -*- coding: future_typing -*-
import pyvoro
from .geom import Sphere
from .mesh import Cell, Edge, Mesh


class VoronoiCell(Cell):

    def __init__(self, sphere: Sphere):
        super().__init__()
        self.sphere = sphere
        self._voro = None

    def _fromSphereVoro(self, id: int, voro):
        self.id = id
        self._voro = voro
        return self

    def asSphere(self):
        s = self.sphere
        c, r = s.center, s.radius
        return Sphere(c, r)


class Voronoi(Mesh[VoronoiCell, Edge]):

    def __init__(self, spheres: list[Sphere], blockSize: float = None):
        super().__init__()
        points = [tuple(sph.center) for sph in spheres]
        radii = [sph.radius for sph in spheres]
        rMax = max(radii)
        xs, ys, zs = [[p[index] for p in points] for index in (0, 1, 2)]
        mi = lambda vs: min(vs) - rMax
        ma = lambda vs: max(vs) + rMax
        limits = [[mi(vs), ma(vs)] for vs in (xs, ys, zs)]
        if blockSize is None:
            mi = min(sphere.radius for sphere in spheres)
            ma = max(sphere.radius for sphere in spheres)
            blockSize = 1.0 * (mi + ma)
        voro = pyvoro.compute_voronoi(points, limits, blockSize, radii)
        #
        self._spheres = spheres
        self._voro = voro
        self.cells: list[Cell] = []
        for i, (sph, voroCell) in enumerate(zip(spheres, voro)):
            self.cells.append(VoronoiCell(sph)._fromSphereVoro(i, voroCell))
        for cell in self.cells:
            for face in cell._voro["faces"]:
                i = face["adjacent_cell"]
                if i < 0:
                    continue
                cell2 = self.cells[i]
                cell.connectWith(cell2)
        self._buildEdges()
        self._numberCells()
