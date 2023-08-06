# -*- coding: future_typing -*-
from re import T
from typing import Generic, TypeVar, TYPE_CHECKING
from .linalg import Vector3
if TYPE_CHECKING:
    from .geom import Sphere


class Cell:

    def __init__(self):
        super().__init__()
        self.edges: set[Edge] = set()
        self._EdgeType = Edge
        self.id = int(-1)

    def getNeighbors(self):
        return [edge.getSecondCell(self) for edge in self.edges]

    def getCommonEdgeWith(self, cell: "Cell") -> "Edge":
        common = self.edges & cell.edges
        if len(common) == 0:
            return None
        if len(common) == 1:
            return common.pop()
        raise RuntimeError("two cells has more then one common edge")

    def connectWith(self, cell: "Cell"):
        if self is cell:
            return None
        edge = self.getCommonEdgeWith(cell)
        if edge:
            return edge
        else:
            return self._EdgeType(self, cell)

    def asSphere(self) -> "Sphere":
        raise NotImplemented

    def remove(self):
        edges = list(self.edges)
        for edge in edges:
            edge.remove()

    def position(self):
        return self.asSphere().center


class Edge:

    def __init__(self, cell1: Cell, cell2: Cell):
        super().__init__()
        self.cell1 = cell1
        self.cell2 = cell2
        cell1.edges.add(self)
        cell2.edges.add(self)
        self.triangles: set[Triangle] = set()

    def getCells(self):
        return self.cell1, self.cell2

    def getCommonCellWith(self, edge: "Edge") -> Cell:
        scells = self.getCells()
        for ecell in edge.getCells():
            if ecell in scells:
                return ecell
        return None

    def getSecondCell(self, cell: Cell) -> Cell:
        if cell is self.cell1:
            return self.cell2
        if cell is self.cell2:
            return self.cell1
        return None

    def getCommonTriangleWith(self, edge1: "Edge", edge2: "Edge") -> "Triangle":
        common = self.triangles & edge1.triangles & edge2.triangles
        if len(common) == 0:
            return None
        if len(common) == 1:
            return common.pop()
        raise RuntimeError("three edges has more then one common triangle")

    def getTriangles(self):
        cell1, cell2 = self.cell1, self.cell2
        for edge1 in self.cell1.edges:
            if edge1 is self:
                continue
            cell12 = edge1.getSecondCell(cell1)
            for edge2 in self.cell2.edges:
                if edge2 is self:
                    continue
                cell22 = edge2.getSecondCell(cell2)
                if cell12 is cell22:
                    if self.getCommonTriangleWith(edge1, edge2) is None:
                        Triangle(self, edge1, edge2)
        return self.triangles

    def remove(self):
        for cell in self.getCells():
            cell.edges.discard(self)
        for tri in self.triangles:
            tri.remove()
        self.cell1 = self.cell2 = None

    def length(self):
        p1, p2 = [cell.position() for cell in self.getCells()]
        return (p1 - p2).norm()


class Triangle:

    def __init__(self, edge1: Edge, edge2: Edge, edge3: Edge):
        super().__init__()
        self.edge1 = edge1
        self.edge2 = edge2
        self.edge3 = edge3
        edge1.triangles.add(self)
        edge2.triangles.add(self)
        edge3.triangles.add(self)
        self.tetrahedrons: set[Tetrahedron] = set()

    def getEdges(self):
        return self.edge1, self.edge2, self.edge3

    def getCells(self):
        return set(cell for edge in self.getEdges() for cell in edge.getCells())

    def getRestEdges(self, edge: Edge) -> tuple[Edge, Edge]:
        if edge is self.edge1:
            return self.edge2, self.edge3
        if edge is self.edge2:
            return self.edge3, self.edge1
        if edge is self.edge3:
            return self.edge1, self.edge2
        return None

    def getThirdCell(self, edge: Edge) -> Cell:
        e1e2 = self.getRestEdges(edge)
        if e1e2 is None:
            return None
        e1, e2 = e1e2
        c1 = e1.getCommonCellWith(e2)
        return e2.getSecondCell(c1)

    def getCommonEdgeWith(self, tri: "Triangle") -> Edge:
        sedges = self.getEdges()
        for tedge in tri.getEdges():
            if tedge in sedges:
                return tedge
        return None

    def getCommonTetrahedronWith(self, tri1: "Triangle", tri2: "Triangle", tri3: "Triangle") -> "Tetrahedron":
        common = self.tetrahedrons & tri1.tetrahedrons & tri2.tetrahedrons & tri3.tetrahedrons
        if len(common) == 0:
            return None
        if len(common) == 1:
            return common.pop()
        raise RuntimeError("four triangles has more then one common tetrahedron")

    def getTetrahedrons(self):
        for tri1 in self.edge1.triangles:
            if tri1 is self:
                continue
            for tri2 in self.edge2.triangles:
                if tri2 is self:
                    continue
                if tri2.getCommonEdgeWith(tri1) is None:
                    continue
                for tri3 in self.edge3.triangles:
                    if tri3 is self:
                        continue
                    if tri3.getCommonEdgeWith(tri1) is None:
                        continue
                    if tri3.getCommonEdgeWith(tri2) is None:
                        continue
                    if self.getCommonTetrahedronWith(tri1, tri2, tri3) is None:
                        Tetrahedron(self, tri1, tri2, tri3)
        return self.tetrahedrons

    def getSecondTetrahedron(self, t: "Tetrahedron"):
        ts = list(self.tetrahedrons)
        if len(ts) != 2:
            return None
        t1, t2 = ts
        if t is t1:
            return t2
        elif t is t2:
            return t1
        else:
            return None

    def remove(self):
        for edge in self.getEdges():
            edge.triangles.discard(self)
        for tetra in self.tetrahedrons:
            tetra.remove()

    def area(self):
        p1, p2, p3 = [cell.position() for cell in self.getCells()]
        s1 = p2 - p1
        s2 = p3 - p1
        return 0.5 * s1.cross(s2).norm()


class Tetrahedron:

    def __init__(self, face1: Triangle, face2: Triangle, face3: Triangle, face4: Triangle):
        super().__init__()
        self.face1 = face1
        self.face2 = face2
        self.face3 = face3
        self.face4 = face4
        face1.tetrahedrons.add(self)
        face2.tetrahedrons.add(self)
        face3.tetrahedrons.add(self)
        face4.tetrahedrons.add(self)

    def getFaces(self):
        return self.face1, self.face2, self.face3, self.face4

    def getCells(self):
        return set(cell for face in self.getFaces() for cell in face.getCells())

    def remove(self):
        for face in self.getFaces():
            face.tetrahedrons.discard(self)

    def volume(self):
        p1, p2, p3, p4 = [cell.position() for cell in self.getCells()]
        return Tetrahedron.points2volume(p1, p2, p3, p4)

    @staticmethod
    def points2volume(p1: Vector3, p2: Vector3, p3: Vector3, p4: Vector3, absoluteValue=True):
        s1 = p2 - p1
        s2 = p3 - p1
        s3 = p4 - p1
        v = 1 / 6. * s1.dot(s2.cross(s3))
        if absoluteValue:
            v = abs(v)
        return v


CellType = TypeVar("CellType", bound=Cell)
EdgeType = TypeVar("EdgeType", bound=Edge)


class Mesh(Generic[CellType, EdgeType]):

    def __init__(self):
        super().__init__()
        self.cells: list[CellType] = []
        self.edges: set[EdgeType] = set()
        self.triangles: set[Triangle] = set()
        self.tetrahedrons: set[Tetrahedron] = set()

    def _buildEdges(self):
        self.edges = set(edge for cell in self.cells for edge in cell.edges)

    def _buildTriangles(self):
        self.triangles = set(tri for edge in self.edges for tri in edge.getTriangles())

    def _buildTetrahedrons(self):
        self.tetrahedrons = set(tetra for tri in self.triangles for tetra in tri.getTetrahedrons())

    def _numberCells(self):
        for i, cell in enumerate(self.cells):
            cell.id = i
