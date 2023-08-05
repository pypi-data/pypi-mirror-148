# -*- coding: future_typing -*-
from typing import overload


class Vector3:

    @overload
    def __init__(self, x: float, y: float, z: float):
        pass

    @overload
    def __init__(self, vector: "Vector3"):
        pass

    def __mul__(self, other: float):
        return Vector3()

    def __rmul__(self, other: float):
        return Vector3()

    def __add__(self, other: "Vector3"):
        return Vector3()

    def __sub__(self, other: "Vector3"):
        return Vector3()

    def norm(self):
        return float()

    def dot(self, other: "Vector3"):
        return float()

    def cross(self, other: "Vector3"):
        return Vector3()


class Matrix3:

    @overload
    def __init__(self, m11: float, m12: float, m13: float, m21: float, m22: float, m23: float, m31: float, m32: float, m33: float):
        pass

    @overload
    def __init__(self, matrix: "Matrix3"):
        pass

    def inverse(self):
        return Matrix3()

    def determinant(self):
        return float()

    @overload
    def __mul__(self, other: Vector3):
        return Vector3()


class MatrixX:

    @overload
    def __init__(self, values: list[list[float]]):
        pass

    @overload
    def __init__(self, matrix: "MatrixX"):
        pass

    def determinant(self):
        return float()


from minieigen import Vector3, Matrix3, MatrixX
