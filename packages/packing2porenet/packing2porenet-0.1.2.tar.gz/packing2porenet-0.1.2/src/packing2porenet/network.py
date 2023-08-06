# -*- coding: future_typing -*-
from tkinter.messagebox import NO
from typing import cast, Callable
from math import atan, pi, sqrt
import warnings
from .linalg import Vector3
from .geom import Sphere, Circle
from .mesh import Cell, Edge, Tetrahedron, Mesh
from .voronoi import Voronoi


class Pore(Cell):

    def __init__(self, center: Vector3 = None, radius: float = 0, volume: float = 0):
        super().__init__()
        self.sphere = Sphere(center, radius)
        self.volume = volume
        self._EdgeType = Throat
        self._originalSpheres: set[Sphere] = set()

    def asSphere(self):
        s = self.sphere
        c, r = s.center, s.radius
        return Sphere(c, r)

    def fromSpheres(self, spheres: tuple[Sphere, Sphere, Sphere, Sphere], **kw):
        self._originalSpheres = set(spheres)
        centers = [sphere.center for sphere in spheres]
        #
        s12, s13, s14, s23, s24, s34 = [centers[j] - centers[i] for i, j in ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))]
        s21, s31, s41, s32, s42, s43 = [-s for s in (s12, s13, s14, s23, s24, s34)]
        volume = Tetrahedron.points2volume(*centers)
        for sphere, (a, b, c) in zip(spheres, ((s12, s13, s14), (s21, s23, s24), (s31, s32, s34), (s41, s42, s43))):
            a, b, c = [cast(Vector3, v) for v in (a, b, c)]
            abc = a.dot(b.cross(c))
            an, bn, cn = [v.norm() for v in (a, b, c)]
            tanSangle = abc / (an * bn * cn + a.dot(b) * cn + a.dot(c) * bn + b.dot(c) * an)
            sangle = 2 * atan(tanSangle)
            dVolume = sangle * sphere.volume() / (4 * pi)
            volume -= dVolume
        self.volume = volume
        #
        self.sphere = Sphere.inscribedSphere(*spheres, **kw)
        return self


class Throat(Edge):

    def __init__(self, pore1: Pore, pore2: Pore):
        super().__init__(pore1, pore2)
        self.radius = float(0)

    def fromSpheres(self, spheres: tuple[Sphere, Sphere, Sphere]):
        A, B, C = [sphere.center for sphere in spheres]
        rA, rB, rC = [sphere.radius for sphere in spheres]
        a, b, c = B - C, C - A, A - B
        a, b, c = [s.norm() for s in (a, b, c)]
        cA = Circle((0, 0, 0), rA)
        cB = Circle((c, 0, 0), rB)
        x = (b**2 + c**2 - a**2) / (2 * c)
        y = sqrt(b**2 - x**2)
        cC = Circle((x, y, 0), rC)
        r = Circle.inscribedCircleRadius(cA, cB, cC)
        self.radius = r


class PoreNetwork(Mesh[Pore, Throat]):

    def __init__(self):
        super().__init__()
        self._tetra2pore: dict[Tetrahedron, Pore] = None
        self._voro: Voronoi = None

    def fromVoronoi(self, voro: Voronoi, **kw):
        voro._buildTriangles()
        voro._buildTetrahedrons()
        self._voro = voro
        #
        self._reset()
        self._tetras2pores(**kw)
        self._connectPores()
        self.filterPores(lambda pore: pore.sphere.radius > 0)
        self._postproThroats()
        #
        return self

    def _reset(self):
        self.cells = []
        self._tetra2pore = {}

    def _tetras2pores(self, **kw):
        for tetra in self._voro.tetrahedrons:
            vcells = tetra.getCells()
            spheres = [vcell.sphere for vcell in vcells]
            pore = Pore().fromSpheres(spheres, **kw)
            self.cells.append(pore)
            self._tetra2pore[tetra] = pore

    def _connectPores(self):
        for tetra in self._voro.tetrahedrons:
            pore = self._tetra2pore[tetra]
            for face in tetra.getFaces():
                tetra2 = face.getSecondTetrahedron(tetra)
                if tetra2 is None:
                    continue
                pore2 = self._tetra2pore[tetra2]
                pore.connectWith(pore2)

    def _postproThroats(self):
        for throat in self.throats:
            pore1, pore2 = cast(tuple[Pore, Pore], throat.getCells())
            spheres = pore1._originalSpheres & pore2._originalSpheres
            throat.fromSpheres(spheres)

    def mergeIntersectingPores(self, limit: float = 0):
        someMerge = False
        for edge in self.edges:
            pore1, pore2 = edge.cell1, edge.cell2
            if pore1 is None or pore2 is None:
                continue
            pore1pore2merged = self._mergeTwoPores(edge, pore1, pore2, limit)
            someMerge = someMerge or pore1pore2merged
        self.filterPores(lambda pore: len(pore.edges) > 0)
        #
        if someMerge:
            return self.mergeIntersectingPores(limit)
        #
        return self

    def checkPoresOverlaps(self, limit: float = 0.0):
        ret = False
        for edge in self.edges:
            cell1, cell2 = edge.getCells()
            sphere1, sphere2 = [cell.sphere for cell in (cell1, cell2)]
            center1, center2 = [sphere.center for sphere in (sphere1, sphere2)]
            radius1, radius2 = [sphere.radius for sphere in (sphere1, sphere2)]
            distance = (center1 - center2).norm()
            overlap = radius1 + radius2 - distance
            lim = min(radius1, radius2) * limit
            if overlap >= lim:
                warnings.warn(f"pores {cell1.id} and {cell2.id} overlap (r1={radius1},r2={radius2},overlap={overlap})", RuntimeWarning)
                ret = True
        return ret

    def _mergeTwoPores(self, edge: Edge, pore1: Pore, pore2: Pore, limit: float):
        s1, s2 = pore1.sphere, pore2.sphere
        c1, c2 = s1.center, s2.center
        r1, r2 = s1.radius, s2.radius
        d = (c1 - c2).norm()
        overlap = r1 + r2 - d
        lim = limit * min(r1, r2)
        if overlap < lim:
            return False
        #
        if pore2.sphere.radius > pore1.sphere.radius:
            poreA, poreB = pore2, pore1
        else:
            poreA, poreB = pore1, pore2
        #
        sA, sB = poreA.sphere, poreB.sphere
        vA, vB = sA.volume(), sB.volume()
        cA, cB = sA.center, sB.center
        vI = Sphere.volumeOfIntersection(sA, sB)
        center = cA + (cB - cA) * vB / (vA + vB)
        v = vA + vB - vI
        r = Sphere.volume2radius(v)
        #
        poreA.volume += poreB.volume
        poreA.sphere.center = center
        poreA.sphere.radius = r
        #
        for poreC in poreB.getNeighbors():
            if poreC is poreA:
                continue
            oldEdge = poreB.connectWith(poreC)
            newEdge = poreA.connectWith(poreC)
            newArea = Circle.radius2area(newEdge.radius)
            oldArea = Circle.radius2area(oldEdge.radius)
            area = newArea + oldArea
            newEdge.radius = Circle.area2radius(area)
        poreB.remove()
        return True

    def filterPores(self, conditon: Callable[[Pore], bool]):
        remaining: list[Pore] = []
        toBeRemoved: list[Pore] = []
        for pore in self.cells:
            condResult = conditon(pore)
            if condResult:
                remaining.append(pore)
            else:
                toBeRemoved.append(pore)
        for pore in toBeRemoved:
            pore.remove()
        self.cells = remaining
        self._buildEdges()
        self._numberCells()
        return self

    @property
    def pores(self):
        return self.cells

    @property
    def throats(self):
        return self.edges
