import math

import vecgl.linalg as vgll


# Model and its primitives.


class Point:

    def __init__(self, p, color):
        self.p = vgll.to_vec4(p)
        self.color = color

    def transform(self, U):
        self.p = vgll.transform_mat4_vec4(U, self.p)

    def __str__(self):
        return vgll.str_vec4(self.p)


class Line:

    def __init__(self, p, q, color):
        self.p = vgll.to_vec4(p)
        self.q = vgll.to_vec4(q)
        self.color = color

    def transform(self, U):
        self.p = vgll.transform_mat4_vec4(U, self.p)
        self.q = vgll.transform_mat4_vec4(U, self.q)

    def __str__(self):
        return f"{vgll.str_vec4(self.p)} to {vgll.str_vec4(self.q)}"


class Triangle:

    def __init__(self, p, q, r, color):
        self.p = vgll.to_vec4(p)
        self.q = vgll.to_vec4(q)
        self.r = vgll.to_vec4(r)
        self.color = color

    def transform(self, U):
        self.p = vgll.transform_mat4_vec4(U, self.p)
        self.q = vgll.transform_mat4_vec4(U, self.q)
        self.r = vgll.transform_mat4_vec4(U, self.r)

    def __str__(self):
        return f"{vgll.str_vec4(self.p)}, {vgll.str_vec4(self.q)}, " + \
               f"{vgll.str_vec4(self.r)}"


class Model:

    def __init__(self):
        self.points = []
        self.lines = []
        self.triangles = []
        self.rendered = False

    def add_point(self, p, color):
        self.points.append(Point(p, color))

    def add_line(self, p, q, color):
        self.lines.append(Line(p, q, color))

    def add_triangle(self, p, q, r, color):
        self.triangles.append(Triangle(p, q, r, color))

    def add_model(self, model):
        self.points += model.points
        self.lines += model.lines
        self.triangles += model.triangles

    def transform(self, U):
        for pt in self.points:
            pt.transform(U)
        for ln in self.lines:
            ln.transform(U)
        for tr in self.triangles:
            tr.transform(U)


# A small model library.


DEFAULT_SURFACE_COLOR = "gray"
DEFAULT_LINE_COLOR = "black"


def get_cube_model(surface_color=DEFAULT_SURFACE_COLOR,
                   line_color=DEFAULT_LINE_COLOR, surfaces=True, lines=True):
    cube = Model()

    # Create the 8 points.
    ps = []
    for i in range(8):
        px = 1.0 if i & 0x01 else -1.0
        py = 1.0 if i & 0x02 else -1.0
        pz = 1.0 if i & 0x04 else -1.0
        p = px, py, pz
        ps.append(p)

    # Add the 12 lines if needed.
    if lines:
        for i in range(8):
            for shift in range(3):
                mask = 0x01 << shift
                if not i & mask:
                    j = i | mask
                    cube.add_line(ps[i], ps[j], line_color)

    # Add the 12 triangles if needed.
    if surfaces:
        cube.add_triangle(ps[0], ps[1], ps[2], surface_color)
        cube.add_triangle(ps[0], ps[1], ps[4], surface_color)
        cube.add_triangle(ps[0], ps[2], ps[4], surface_color)
        cube.add_triangle(ps[1], ps[2], ps[3], surface_color)
        cube.add_triangle(ps[1], ps[3], ps[5], surface_color)
        cube.add_triangle(ps[1], ps[4], ps[5], surface_color)
        cube.add_triangle(ps[2], ps[3], ps[6], surface_color)
        cube.add_triangle(ps[2], ps[4], ps[6], surface_color)
        cube.add_triangle(ps[3], ps[5], ps[7], surface_color)
        cube.add_triangle(ps[3], ps[6], ps[7], surface_color)
        cube.add_triangle(ps[4], ps[5], ps[6], surface_color)
        cube.add_triangle(ps[5], ps[6], ps[7], surface_color)

    return cube


def get_sphere_model(n=8, m=16, surface_color=DEFAULT_SURFACE_COLOR,
                     line_color=DEFAULT_LINE_COLOR, surfaces=True,
                     latitude_lines=True, longitude_lines=True):
    sphere = Model()

    # Create the n*m points and a unique north and south pole.
    p_north = 0.0, 1.0, 0.0
    p_south = 0.0, -1.0, 0.0
    ps = []
    for i in range(n):
        angle_latitude = (i+1)/(n+1) * math.pi
        py = math.cos(angle_latitude)
        radius_xz = math.sqrt(1.0 - py ** 2)
        ps_latitude = []
        for j in range(m):
            angle_longitude = j/m * 2.0*math.pi
            px = radius_xz * math.sin(angle_longitude)
            pz = radius_xz * math.cos(angle_longitude)
            p = px, py, pz
            ps_latitude.append(p)
        ps.append(ps_latitude)

    # Add lines and triangles defined by the grid.
    for i in range(n - 1):
        i_next = i+1
        for j in range(m):
            j_next = (j+1) % m
            p = ps[i][j]
            q = ps[i][j_next]
            r = ps[i_next][j]
            s = ps[i_next][j_next]
            if surfaces:
                sphere.add_triangle(p, q, r, surface_color)
                sphere.add_triangle(q, r, s, surface_color)
            if latitude_lines:
                sphere.add_line(p, q, line_color)
            if longitude_lines:
                sphere.add_line(p, r, line_color)

    # Add lines and triangles to connect the north and south poles.
    for j in range(m):
        j_next = (j+1) % m
        p = ps[0][j]
        q = ps[0][j_next]
        r = ps[-1][j]
        s = ps[-1][j_next]
        if surfaces:
            sphere.add_triangle(p_north, p, q, surface_color)
            sphere.add_triangle(p_south, r, s, surface_color)
        if latitude_lines:
            sphere.add_line(r, s, line_color)
        if longitude_lines:
            sphere.add_line(p_north, p, line_color)
            sphere.add_line(p_south, r, line_color)

    return sphere
