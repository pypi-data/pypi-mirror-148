import unittest
from math import pi
from packing2porenet import *


class TestLinalg(unittest.TestCase):

    def test_vector3(self):
        v1 = Vector3(1, 2, 3)
        v2 = Vector3(4, 5, 6)
        self.assertEqual(tuple(v1), (1, 2, 3))
        self.assertEqual(tuple(Vector3(v1)), (1, 2, 3))
        self.assertEqual(tuple(2 * v1), (2, 4, 6))
        self.assertEqual(tuple(v1 * 2), (2, 4, 6))
        self.assertEqual(tuple(v1 + v2), (5, 7, 9))
        self.assertEqual(tuple(v2 - v1), (3, 3, 3))
        self.assertEqual(v1.norm(), 14**0.5)
        self.assertEqual(v1.dot(v2), 32)
        self.assertEqual(tuple(v1.cross(v1)), (0, 0, 0))
        self.assertEqual(tuple(v1.cross(v2)), (-3, 6, -3))


class TestSphere(unittest.TestCase):

    def test_sphereVolumeRadius(self):
        s = Sphere((0, 0, 0), 1)
        v = s.volume()
        self.assertEqual(v, 4 / 3 * pi)
        r = Sphere.volume2radius(v)
        self.assertEqual(r, 1)

    def test_sphereOverlap(self):
        f = Sphere.volumeOfIntersection
        s1 = Sphere((0, 0, 0), 4)
        s2 = Sphere((8, 0, 0), 4)
        self.assertEqual(f(s1, s2), 0)
        s3 = Sphere((3, 0, 0), 1)
        vs3 = s3.volume()
        self.assertEqual(f(s1, s3), vs3)
        s4 = Sphere((5, 0, 0), 2)
        v = f(s1, s4)
        self.assertTrue(v > 0 and v < vs3)

    def test_point(self):
        s = Sphere((1, 2, 3), 4)
        p1 = Vector3(8, 2, 3)
        p2 = Vector3(4, 2, 3)
        p3 = Vector3(3, 4, 5)
        self.assertEqual(s.distanceFromPoint(p1), 3)
        self.assertEqual(s.distanceFromPoint(p2), -1)
        self.assertFalse(s.containsPoint(p1))
        self.assertTrue(s.containsPoint(p2))
        self.assertTrue(s.containsPoint(p3))

    def test_intersection(self):
        f = Sphere.intersection
        s1 = Sphere((0, 0, 0), 1)
        s2 = Sphere((4, 0, 0), 2)
        self.assertIsNone(f(s1, s2))
        s1 = Sphere((0, 0, 0), 5)
        s2 = Sphere((8, 0, 0), 5)
        p, r = f(s1, s2)
        self.assertEqual(r, 3)
        self.assertEqual(p.point, Vector3(4, 0, 0))
        s1 = Sphere((0, 0, 0), 5)
        s2 = Sphere((6, 0, 0), 5)
        p, r = f(s1, s2)
        self.assertEqual(r, 4)
        self.assertEqual(p.point, Vector3(3, 0, 0))
        s1 = Sphere((0, 0, 0), 20)
        s2 = Sphere((25, 0, 0), 15)
        p, r = f(s1, s2)
        self.assertEqual(r, 12)
        self.assertEqual(p.point, Vector3(16, 0, 0))


class TestPlane(unittest.TestCase):

    def test_intersection3(self):
        f = Plane.intersection3
        p1 = Plane((0, 0, 0), (1, 0, 0))
        p2 = Plane((0, 0, 0), (0, 1, 0))
        p3 = Plane((0, 0, 0), (0, 0, 1))
        self.assertEqual(f(p1, p2, p3), Vector3(0, 0, 0))
        p2 = Plane((2, 3, 1), (2, 2, 2))
        p1 = Plane((3, 4, 5), (1, -1, 0))
        p3 = Plane((5, 4, 3), (0, 0, 3))
        self.assertEqual(f(p1, p2, p3), Vector3(1, 2, 3))
