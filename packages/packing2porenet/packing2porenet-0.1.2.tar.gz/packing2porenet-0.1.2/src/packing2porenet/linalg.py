# -*- coding: future_typing -*-
from typing import overload, cast
import numpy


class Vector3:

    @overload
    def __init__(self, x: float, y: float, z: float):
        pass

    @overload
    def __init__(self, vector: "Vector3"):
        pass

    def __init__(self, x: float | "Vector3", y: float = 0, z: float = 0):
        if not isinstance(x, (float, int)):
            x, y, z = tuple(x)
            x = cast(float, x)
        self._data = numpy.array([x, y, z], numpy.double)

    def __str__(self):
        x, y, z = self
        return f"Vector3({x:g},{y:g},{z:g})"

    def __eq__(self, other: any):
        return tuple(self) == tuple(other)

    def __ne__(self, other: any):
        return not (self == other)

    def __getitem__(self, i: int) -> float:
        return self._data[i]

    def __setitem__(self, i: int, v: float):
        self._data[i] = v

    def __iter__(self):
        for v in self._data:
            yield v

    def __pos__(self):
        return Vector3(self)

    def __neg__(self):
        return self * -1

    def __imul__(self, f: float):
        self._data *= f
        return self

    def __mul__(self, f: float):
        return Vector3(self).__imul__(f)

    def __itruediv__(self, f: float):
        self._data /= f
        return self

    def __truediv__(self, f: float):
        return Vector3(self).__itruediv__(f)

    def __rmul__(self, f: float):
        return self * f

    def __iadd__(self, other: "Vector3"):
        self._data += tuple(other)
        return self

    def __add__(self, other: "Vector3"):
        return Vector3(self).__iadd__(other)

    def __isub__(self, other: "Vector3"):
        self._data -= tuple(other)
        return self

    def __sub__(self, other: "Vector3"):
        return Vector3(self).__isub__(other)

    def norm(self):
        return float(numpy.linalg.norm(self._data))

    def dot(self, other: "Vector3") -> float:
        return self._data.dot(tuple(other))

    def cross(self, other: "Vector3"):
        return Vector3(numpy.cross(self._data, tuple(other)))


class Matrix3:

    @overload
    def __init__(
        self,
        m11: float,
        m12: float,
        m13: float,
        m21: float,
        m22: float,
        m23: float,
        m31: float,
        m32: float,
        m33: float,
    ):
        pass

    @overload
    def __init__(self, matrix: "Matrix3"):
        pass

    def __init__(
        self,
        m11: float | "Matrix3",
        m12: float = 0,
        m13: float = 0,
        m21: float = 0,
        m22: float = 0,
        m23: float = 0,
        m31: float = 0,
        m32: float = 0,
        m33: float = 0,
    ):
        if not isinstance(m11, (int, float)):
            (m11, m12, m13), (m21, m22, m23), (m31, m32, m33) = tuple(row for row in m11)
        m11 = cast(float, m11)
        self._data = numpy.array([
            [m11, m12, m13],
            [m21, m22, m23],
            [m31, m32, m33],
        ], numpy.double)

    def __str__(self):
        (m11, m12, m13), (m21, m22, m23), (m31, m32, m33) = self
        return f"Matrix3({m11:g},{m12:g},{m13:g}, {m21:g},{m22:g},{m23:g}, {m31:g},{m32:g},{m33:g}"

    def __getitem__(self, ij: tuple[int, int]) -> float:
        return self._data[ij]

    def __setitem__(self, ij: tuple[int, int], v: float):
        self._data[ij] = v

    def inverse(self):
        return Matrix3(numpy.linalg.inv(self._data))

    def determinant(self) -> float:
        return numpy.linalg.det(self._data)

    @overload
    def __mul__(self, other: Vector3):
        return Vector3()

    def __mul__(self, other: Vector3):
        return Vector3(self._data @ tuple(other))


class MatrixX:

    def __init__(self, data: list[list[float]]):
        self._data = numpy.array(data, numpy.double)

    def determinant(self) -> float:
        return numpy.linalg.det(self._data)


def use_minieigen():
    import minieigen
    global Vector3
    Vector3 = minieigen.Vector3
    global Matrix3
    Matrix3 = minieigen.Matrix3
    global MatrixX
    MatrixX = minieigen.Matrix3
