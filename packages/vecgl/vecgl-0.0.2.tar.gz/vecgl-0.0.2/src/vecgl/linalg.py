import functools
import math


# Linear algebra in a 3D coordinate system.


def to_vec3(u):
    assert type(u) is tuple and len(u) in [
        3, 4], f"expect 3D or 4D coordinate tuple but got {u}"
    if len(u) == 3:
        return u
    ux, uy, uz, uw = u
    return ux/uw, uy/uw, uz/uw


def x_vec3(u):
    ux, uy, uz = u
    return ux


def y_vec3(u):
    ux, uy, uz = u
    return uy


def z_vec3(u):
    ux, uy, uz = u
    return uz


def str_vec3(u):
    ux, uy, uz = u
    return f"({ux:.2f}, {uy:.2f}, {uz:.2f})"


def scale_vec3(a, u):
    ux, uy, uz = u
    return a*ux, a*uy, a*uz


def add_vec3(u, v):
    ux, uy, uz = u
    vx, vy, vz = v
    return ux + vx,      uy + vy, uz + vz


def sub_vec3(u, v):
    ux, uy, uz = u
    vx, vy, vz = v
    return tuple([a - b for a, b in zip(u, v)])


def dot_vec3(u, v):
    ux, uy, uz = u
    vx, vy, vz = v
    return ux*vx + uy*vy + uz*vz


def cross_vec3(u, v):
    ux, uy, uz = u
    vx, vy, vz = v
    return uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx


# Linear algebra in a 4D homogenious coordinate system.


def to_vec4(u):
    assert type(u) is tuple and len(u) in [
        3, 4], f"expect 3D or 4D coordinate tuple but got {u}"
    if len(u) == 4:
        return u
    ux, uy, uz = u
    return ux, uy, uz, 1.0


def x_vec4(u):
    ux, uy, uz, uw = u
    return ux


def y_vec4(u):
    ux, uy, uz, uw = u
    return uy


def z_vec4(u):
    ux, uy, uz, uw = u
    return uz


def w_vec4(u):
    ux, uy, uz, uw = u
    return uw


def str_vec4(u):
    ux, uy, uz, uw = u
    return f"({ux:.2f}, {uy:.2f}, {uz:.2f}, {uw:.2f})"


def dot_vec4(u, v):
    ux, uy, uz, uw = u
    vx, vy, vz, vw = v
    return ux*vx + uy*vy + uz*vz + uw*vw


def transform_mat4_vec4(U, v):
    return tuple([dot_vec4(u, v) for u in U])


def mul_mat4_mat4(U, V):
    l = len(U)
    m = len(V)
    n = len(V[0])
    W = []
    for i in range(l):
        Wi = []
        for j in range(n):
            Wij = sum([U[i][k] * V[k][j] for k in range(m)])
            Wi.append(Wij)
        W.append(tuple(Wi))
    return tuple(W)


def mul_mat4(*Us):
    return functools.reduce(mul_mat4_mat4, Us)


def get_unit_mat4():
    return ((1.0, 0.0, 0.0, 0.0),
            (0.0, 1.0, 0.0, 0.0),
            (0.0, 0.0, 1.0, 0.0),
            (0.0, 0.0, 0.0, 1.0))


def get_scale_mat4(ax, ay, az):
    return ((ax,  0.0, 0.0, 0.0),
            (0.0, ay,  0.0, 0.0),
            (0.0, 0.0, az,  0.0),
            (0.0, 0.0, 0.0, 1.0))


def get_translate_mat4(dx, dy, dz):
    return ((1.0, 0.0, 0.0, dx),
            (0.0, 1.0, 0.0, dy),
            (0.0, 0.0, 1.0, dz),
            (0.0, 0.0, 0.0, 1.0))


def get_rotate_x_mat4(da):
    return ((1.0, 0.0, 0.0, 0.0),
            (0.0, math.cos(da), math.sin(da), 0.0),
            (0.0, -math.sin(da), math.cos(da), 0.0),
            (0.0, 0.0, 0.0, 1.0))


def get_rotate_y_mat4(da):
    return ((math.cos(da), 0.0, -math.sin(da), 0.0),
            (0.0, 1.0, 0.0, 0.0),
            (math.sin(da), 0.0, math.cos(da), 0.0),
            (0.0, 0.0, 0.0, 1.0))


def get_rotate_z_mat4(da):
    return ((math.cos(da), -math.sin(da), 0.0, 0.0),
            (math.sin(da), math.cos(da), 0.0, 0.0),
            (0.0, 0.0, 1.0, 0.0),
            (0.0, 0.0, 0.0, 1.0))


def get_ortho_mat4(left, right, bottom, top, near, far):
    return ((2.0/(right-left), 0.0, 0.0, -(right + left)/(right-left)),
            (0.0, 2.0/(top-bottom), 0.0, -(top+bottom)/(top-bottom)),
            (0.0, 0.0, -2.0/(far-near), -(far+near)/(far-near)),
            (0.0, 0.0, 0.0, 1.0))


def get_frustum_mat4(left, right, bottom, top, near, far):
    return ((2.0*near/(right - left), 0.0, (right+left)/(right-left), 0.0),
            (0.0, 2.0*near/(top-bottom), (top+bottom)/(top-bottom), 0.0),
            (0.0, 0.0, -(far+near)/(far-near), -2.0*far*near/(far-near)),
            (0.0, 0.0, -1.0, 0.0))


def get_viewport_mat4(x, y, width, height):
    return ((width/2.0, 0.0, 0.0, x + width/2.0),
            (0.0, height/2.0, 0.0, y + height/2.0),
            (0.0, 0.0, 1.0, 0.0),
            (0.0, 0.0, 0.0, 1.0))
