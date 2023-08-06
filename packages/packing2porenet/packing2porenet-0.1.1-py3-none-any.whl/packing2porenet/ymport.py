from . import Sphere


def txt2spheres(fileName: str):

    def _txtLine2sphere(line: str):
        x, y, z, r = line.split()
        x, y, z, r = [float(v) for v in (x, y, z, r)]
        return Sphere((x, y, z), r)

    with open(fileName) as f:
        lines = f.readlines()
    spheres = [_txtLine2sphere(line) for line in lines if not line.startswith("#")]
    return spheres
