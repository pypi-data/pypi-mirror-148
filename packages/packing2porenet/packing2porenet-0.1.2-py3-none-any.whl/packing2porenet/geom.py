# -*- coding: future_typing -*-
from math import pow, pi, sqrt
import warnings
from .linalg import Vector3, Matrix3, MatrixX
from .mesh import Tetrahedron


class Sphere:

    def __init__(self, center: Vector3 = None, radius: float = 0):
        super().__init__()
        if center is None:
            center = Vector3(0, 0, 0)
        self.center = Vector3(center)
        self.radius = radius

    def volume(self):
        return Sphere.radius2volume(self.radius)

    def distanceFromPoint(self, point: Vector3) -> float:
        return (self.center - point).norm() - self.radius

    def containsPoint(self, point: Vector3):
        return self.distanceFromPoint(point) <= 0

    def __str__(self):
        return f"Sphere({self.center},{self.radius:g})"

    @staticmethod
    def radius2volume(radius: float):
        return 4 / 3. * pi * radius**3

    @staticmethod
    def volume2radius(volume: float):
        return (3 * volume / (4 * pi))**(1 / 3.)

    @staticmethod
    def volumeOfIntersection(sphere1: "Sphere", sphere2: "Sphere"):
        if sphere2.radius > sphere1.radius:
            sphere2, sphere1 = sphere1, sphere2
        center1, center2 = sphere1.center, sphere2.center
        d = (center1 - center2).norm()
        rA, rB = sphere1.radius, sphere2.radius
        vI = pi * (rA + rB - d)**2 * (d**2 + 2 * d * rB - 3 * rB**2 + 2 * d * rA + 6 * rB * rA - 3 * rA**2) / (12 * d)
        return vI

    @staticmethod
    def intersection(sphere1: "Sphere", sphere2: "Sphere"):
        if sphere2.radius > sphere1.radius:
            sphere1, sphere2 = sphere2, sphere1
        spheres = (sphere1, sphere2)
        c1, c2 = [sphere.center for sphere in spheres]
        r1, r2 = [sphere.radius for sphere in spheres]
        direction = c2 - c1
        d = direction.norm()
        if d > r1 + r2:
            return None
        normal = direction / d
        #
        x = (d**2 - r2**2 + r1**2) / (2 * d)
        center = c1 + x * normal
        radius = 1 / (2 * d) * sqrt((-d + r1 - r2) * (-d - r1 + r2) * (-d + r1 + r2) * (d + r1 + r2))
        #
        plane = Plane(center, normal)
        return plane, radius

    @staticmethod
    def circumSphere(p1: Vector3, p2: Vector3, p3: Vector3, p4: Vector3):
        x1, y1, z1 = p1
        x2, y2, z2 = p2
        x3, y3, z3 = p3
        x4, y4, z4 = p4
        d1 = x1**2 + y1**2 + z1**2
        d2 = x2**2 + y2**2 + z2**2
        d3 = x3**2 + y3**2 + z3**2
        d4 = x4**2 + y4**2 + z4**2
        a = MatrixX([
            [x1, y1, z1, 1],
            [x2, y2, z2, 1],
            [x3, y3, z3, 1],
            [x4, y4, z4, 1],
        ]).determinant()
        Dx = +MatrixX([
            [d1, y1, z1, 1],
            [d2, y2, z2, 1],
            [d3, y3, z3, 1],
            [d4, y4, z4, 1],
        ]).determinant()
        Dy = -MatrixX([
            [d1, x1, z1, 1],
            [d2, x2, z2, 1],
            [d3, x3, z3, 1],
            [d4, x4, z4, 1],
        ]).determinant()
        Dz = +MatrixX([
            [d1, x1, y1, 1],
            [d2, x2, y2, 1],
            [d3, x3, y3, 1],
            [d4, x4, y4, 1],
        ]).determinant()
        c = MatrixX([
            [d1, x1, y1, z1],
            [d2, x2, y2, z2],
            [d3, x3, y3, z3],
            [d4, x4, y4, z4],
        ]).determinant()
        x = Dx / (2 * a)
        y = Dy / (2 * a)
        z = Dz / (2 * a)
        r = sqrt(Dx**2 + Dy**2 + Dz**2 - 4 * a * c) / (2 * abs(a))
        return Sphere((x, y, z), r)

    @staticmethod
    def inscribedSphere(
        sphere1: "Sphere",
        sphere2: "Sphere",
        sphere3: "Sphere",
        sphere4: "Sphere",
        tol: float = 1e-6,
        maxIter: int = 100,
        limitTetraQuality: float = 0.0,
        warn=True,
    ):
        spheres = (sphere1, sphere2, sphere3, sphere4)
        centers = c1, c2, c3, c4 = [sphere.center for sphere in spheres]
        c1234 = .25 * (c1 + c2 + c3 + c4)
        radii = r1, r2, r3, r4 = [sphere.radius for sphere in spheres]
        circumsphere = Sphere.circumSphere(c1, c2, c3, c4)
        circumr = circumsphere.radius
        tetrav = Tetrahedron.points2volume(c1, c2, c3, c4)
        tetraQuality = (9 * sqrt(3) / 8 * tetrav)**(1 / 3) / circumr
        if tetraQuality < limitTetraQuality:
            if warn:
                warnings.warn(f"Tetrahedron of low quality ({tetraQuality}<{limitTetraQuality}", RuntimeWarning)
            return Sphere(c1234, 0)
        lim = tol * circumr
        ss = s1, s2, s3, s4 = [Sphere(c, r) for c, r in zip(centers, radii)]
        cs = c2, c3, c4
        rs = r2, r3, r4
        vs = [c - c1 for c in cs]
        ds = [v.norm() for v in vs]
        nvs = [v / d for v, d in zip(vs, ds)]
        rrs = [r1 + r for r in rs]
        gs = [d - rr for d, rr in zip(ds, rrs)]
        tMax = 1.0 * circumr
        tMin = .5 * max(gs) + circumr * 1e-6
        tMin = max(tMin, 0)

        #
        def computeIntersectionAndDistances(t: float) -> tuple[Vector3, float]:
            s1.radius = r1 + t
            s2.radius = r2 + t
            s3.radius = r3 + t
            s4.radius = r4 + t
            i1 = Sphere.intersection(s1, s2)
            i2 = Sphere.intersection(s1, s3)
            i3 = Sphere.intersection(s1, s4)
            if any(i is None for i in (i1, i2, i3)):
                return None
            plane1, _ = i1
            plane2, _ = i2
            plane3, _ = i3
            intersection = Plane.intersection3(plane1, plane2, plane3)
            ds = [s.distanceFromPoint(intersection) for s in (s1, s2, s3, s4)]
            dMax = max(ds)
            return intersection, dMax

        id0 = computeIntersectionAndDistances(0)
        if id0 is not None:
            center, v0 = id0
            if v0 <= 0:
                if warn:
                    warnings.warn("Zero volume pore", RuntimeWarning)
                return Sphere(center, 0)
        #
        _, vMin = computeIntersectionAndDistances(tMin)
        if vMin <= 0:
            return Sphere(center, 0)
        while True:
            _, vMax = computeIntersectionAndDistances(tMax)
            if tMax > 2 * circumr:
                if warn:
                    warnings.warn("Degenerate tetrahedron", RuntimeWarning)
                return Sphere(c1234, 0)
            if vMax >= 0:
                tMax *= 1.2
            else:
                break
        assert vMax < 0, vMax
        #
        t1, t2 = tMin, tMax
        iteration = 0
        while True:
            tc = .5 * (t1 + t2)
            center, v = computeIntersectionAndDistances(tc)
            if abs(v) < lim:
                break
            if t2 - t1 < lim:
                break
            if v < 0:
                t2 = tc
            else:
                t1 = tc
            iteration += 1
            if iteration > maxIter:
                raise RuntimeError(f"Sphere.inscribedSphere: bisection method failed\nDebug info: circumr {circumr} tMin {tMin} tMax {tMax} lim {lim} v {v} t2-t1 {t2-t1}")
        #
        radius = (center - c1).norm() - r1
        return Sphere(center, radius)


class Plane:

    def __init__(self, point: Vector3 = None, normal: Vector3 = None):
        super().__init__()
        if point is None:
            point = Vector3(0, 0, 0)
        self.point = Vector3(point)
        if normal is None:
            normal = Vector3(0, 0, 0)
        self.normal = Vector3(normal)

    def toGeneralForm(self):
        a, b, c = self.normal
        d = -self.point.dot(self.normal)
        return a, b, c, d

    @staticmethod
    def intersection3(plane1: "Plane", plane2: "Plane", plane3: "Plane"):
        a1, b1, c1, d1 = plane1.toGeneralForm()
        a2, b2, c2, d2 = plane2.toGeneralForm()
        a3, b3, c3, d3 = plane3.toGeneralForm()
        m = Matrix3(a1, b1, c1, a2, b2, c2, a3, b3, c3)
        rhs = Vector3(-d1, -d2, -d3)
        ret = m.inverse() * rhs
        return ret


class Line:

    def __init__(self, point: Vector3 = None, normal: Vector3 = None):
        super().__init__()
        if point is None:
            point = Vector3(0, 0, 0)
        self.point = Vector3(point)
        if normal is None:
            normal = Vector3(0, 0, 0)
        self.normal = Vector3(normal)

    def toGeneralForm(self):
        a, b, _ = self.normal
        c = -self.point.dot(self.normal)
        return a, b, c

    @staticmethod
    def intersection(line1: "Line", line2: "Line"):
        a1, b1, c1 = line1.toGeneralForm()
        a2, b2, c2 = line2.toGeneralForm()
        m = Matrix3(a1, b1, 0, a2, b2, 0, 0, 0, 1)
        rhs = Vector3(-c1, -c2, 0)
        ret = m.inverse() * rhs
        return ret


class Circle:

    def __init__(self, center: Vector3 = None, radius: float = 0):
        super().__init__()
        if center is None:
            center = Vector3(0, 0, 0)
        self.center = Vector3(center)
        self.radius = radius

    def distanceFromPoint(self, point: Vector3) -> float:
        return (self.center - point).norm() - self.radius

    def containsPoint(self, point: Vector3):
        return self.distanceFromPoint(point) <= 0

    @staticmethod
    def radius2area(radius: float):
        return pi * radius**2

    @staticmethod
    def area2radius(area: float):
        return sqrt(area / pi)

    @staticmethod
    def circumCircleRadius(p1: Vector3, p2: Vector3, p3: Vector3):
        a, b, c = [(v1 - v2).norm() for v1, v2 in ((p1, p2), (p2, p3), (p3, p1))]
        s = .5 * (a + b + c)
        A = sqrt(s * (s - a) * (s - b) * (s - c))
        r = A / s
        R = a * b * c / (4 * r * s)
        return R

    @staticmethod
    def intersection(circle1: "Circle", circle2: "Circle"):
        if circle2.radius > circle1.radius:
            circle1, circle2 = circle2, circle1
        circles = (circle1, circle2)
        c1, c2 = [circle.center for circle in circles]
        r1, r2 = [circle.radius for circle in circles]
        direction = c2 - c1
        d = direction.norm()
        if d > r1 + r2:
            return None
        normal = direction / d
        #
        x = (d**2 - r2**2 + r1**2) / (2 * d)
        center = c1 + x * normal
        radius = 1 / (2 * d) * sqrt((-d + r1 - r2) * (-d - r1 + r2) * (-d + r1 + r2) * (d + r1 + r2))
        #
        line = Line(center, normal)
        return line, radius

    @staticmethod
    def inscribedCircleRadius(
        circle1: "Circle",
        circle2: "Circle",
        circle3: "Circle",
        tol: float = 1e-6,
        maxIter: int = 100,
    ):
        spheres = (circle1, circle2, circle3)
        centers = c1, c2, c3 = [circle.center for circle in spheres]
        radii = r1, r2, r3 = [circle.radius for circle in spheres]
        circumr = Circle.circumCircleRadius(c1, c2, c3)
        lim = tol * circumr
        cis = ci1, ci2, ci3 = [Circle(c, r) for c, r in zip(centers, radii)]
        cs = c2, c3
        rs = r2, r3
        vs = [c - c1 for c in cs]
        ds = [v.norm() for v in vs]
        nvs = [v / d for v, d in zip(vs, ds)]
        rrs = [r1 + r for r in rs]
        gs = [d - rr for d, rr in zip(ds, rrs)]
        tMax = 1.0 * circumr
        tMin = .5 * max(gs) + circumr * 1e-6
        tMin = max(tMin, 0)

        #
        def computeIntersectionAndDistances(t: float) -> tuple[Vector3, float]:
            ci1.radius = r1 + t
            ci2.radius = r2 + t
            ci3.radius = r3 + t
            i1 = Circle.intersection(ci1, ci2)
            i2 = Circle.intersection(ci1, ci3)
            if any(i is None for i in (i1, i2)):
                return None
            line1, _ = i1
            line2, _ = i2
            intersection = Line.intersection(line1, line2)
            ds = [s.distanceFromPoint(intersection) for s in (ci1, ci2, ci3)]
            dMax = max(ds)
            return intersection, dMax

        id0 = computeIntersectionAndDistances(0)
        if id0 is not None:
            center, v0 = id0
            if v0 <= 0:
                return 0
        #
        _, vMin = computeIntersectionAndDistances(tMin)
        if vMin <= 0:
            return 0
        while True:
            _, vMax = computeIntersectionAndDistances(tMax)
            if tMax > 2 * circumr:
                return 0
            if vMax >= 0:
                tMax *= 1.2
            else:
                break
        assert vMax < 0, vMax
        #
        t1, t2 = tMin, tMax
        iteration = 0
        while True:
            tc = .5 * (t1 + t2)
            center, v = computeIntersectionAndDistances(tc)
            if abs(v) < lim:
                break
            if t2 - t1 < lim:
                break
            if v < 0:
                t2 = tc
            else:
                t1 = tc
            iteration += 1
            if iteration > maxIter:
                raise RuntimeError(f"Sphere.inscribedSphere: bisection method failed\nDebug info: circumr {circumr} tMin {tMin} tMax {tMax} lim {lim} v {v} t2-t1 {t2-t1}")
        #
        radius = (center - c1).norm() - r1
        return radius
