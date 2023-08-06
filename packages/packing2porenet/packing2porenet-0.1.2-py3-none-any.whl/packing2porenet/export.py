# -*- coding: future_typing -*-
from typing import Iterable, Callable
from . import Sphere, Mesh, PoreNetwork, Edge

EXT_VTK = ".vtk"
EXT_TXT = ".txt"


def _lines2file(lines: list[str], fileName: str):
    lines = [f"{l}\n" for l in lines]
    with open(fileName, "w") as f:
        f.writelines(lines)


def _fileName2ext(fileName: str, ext: str):
    if not fileName.lower().endswith(ext):
        fileName += ext
    return fileName


def _fileName2txt(fileName: str):
    return _fileName2ext(fileName, EXT_TXT)


def _fileName2vtk(fileName: str):
    return _fileName2ext(fileName, EXT_VTK)


def spheres2txt(spheres: Iterable[Sphere], fileName: str, firstLineComment=True):
    lines = []
    if firstLineComment:
        lines = ["# x y z radius"]
    for sph in spheres:
        x, y, z = sph.center
        r = sph.radius
        lines.append(f"{x} {y} {z} {r}")
    fileName = _fileName2txt(fileName)
    _lines2file(lines, fileName)


def spheres2vtk(spheres: Iterable[Sphere], fileName: str, comment: str = "comment"):
    nSphs = len(spheres)
    lines = [
        "# vtk DataFile Version 3.0.",
        comment,
        "ASCII",
    ]
    #
    lines.extend([
        "",
        "DATASET POLYDATA",
        f"POINTS {nSphs} double",
    ])
    for sph in spheres:
        x, y, z = sph.center
        lines.append(f"{x} {y} {z}")
    #
    lines.extend([
        "",
        f"POINT_DATA {nSphs}",
        "SCALARS radius double 1",
        "LOOKUP_TABLE default",
    ])
    for sph in spheres:
        r = sph.radius
        lines.append(f"{r}")
    #
    fileName = _fileName2vtk(fileName)
    _lines2file(lines, fileName)


def mesh2vtk(mesh: Mesh, fileName: str, comment: str = "comment", edgeData: dict[str, Callable[[Edge], float]] = {}):
    cells = mesh.cells
    cell2id = {cell: i for i, cell in enumerate(cells)}
    points = [cell.asSphere().center for cell in cells]
    nPoints = len(points)
    edges = mesh.edges
    nEdges = len(edges)
    lines = [
        "# vtk DataFile Version 3.0.",
        comment,
        "ASCII",
    ]
    #
    lines.extend([
        "",
        "DATASET POLYDATA",
        f"POINTS {nPoints} double",
    ])
    for point in points:
        x, y, z = list(point)
        lines.append(f"{x} {y} {z}")
    #
    lines.extend([
        "",
        f"LINES {nEdges} {3*nEdges}",
    ])
    for edge in edges:
        id1 = cell2id[edge.cell1]
        id2 = cell2id[edge.cell2]
        lines.append(f"2 {id1} {id2}")
    #
    if edgeData:
        lines.extend([
            "",
            f"CELL_DATA {nEdges}",
        ])
        for key, edge2number in edgeData.items():
            lines.extend([
                "",
                f"SCALARS {key} double 1",
                "LOOKUP_TABLE default",
            ])
            for edge in edges:
                v = edge2number(edge)
                lines.append(str(v))
    #
    fileName = _fileName2vtk(fileName)
    _lines2file(lines, fileName)


def poreNetwork2txt(network: PoreNetwork, fileBase: str):
    spheres = [pore.sphere for pore in network.pores]
    fPores = f"{fileBase}-pores.txt"
    fThroats = f"{fileBase}-throats.txt"
    spheres2txt(spheres, fPores)
    throats = network.edges
    lines = ["# id_pore_1 id_pore_2 radius"]
    for throat in throats:
        cells = throat.getCells()
        id1, id2 = [cell.id for cell in cells]
        r = throat.radius
        lines.append(f"{id1} {id2} {r}")
    _lines2file(lines, fThroats)


def poreNetwork2vtk(network: PoreNetwork, fileBase: str):
    return mesh2vtk(network, fileBase, edgeData=dict(radius=lambda edge: edge.radius))
