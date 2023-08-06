import math

import vecgl.model as vglm
import vecgl.rendering as vglr
import vecgl.linalg as vgll


def test_benchmark_sphere_renderig(benchmark):
    model = vglm.get_sphere_model()
    view_mat4 = vgll.mul_mat4(
        vgll.get_translate_mat4(0.0, 0.0, -3.0),
        vgll.get_rotate_x_mat4(-0.2*math.pi),
        vgll.get_rotate_y_mat4(0.15*math.pi))
    projection_mat4 = vgll.get_frustum_mat4(-1.0, 1.0, -1.0, 1.0, 1.0, 100.0)
    model.transform(vgll.mul_mat4(projection_mat4, view_mat4))
    rendered = benchmark(vglr.render, model)
    assert len(rendered.lines) == 107
    assert len(rendered.triangles) == 256


def test_benchmark_cube_renderig(benchmark):
    model = vglm.get_cube_model()
    view_mat4 = vgll.mul_mat4(
        vgll.get_translate_mat4(0.0, 0.0, -3.0),
        vgll.get_rotate_x_mat4(-0.2*math.pi),
        vgll.get_rotate_y_mat4(0.15*math.pi))
    projection_mat4 = vgll.get_frustum_mat4(-1.0, 1.0, -1.0, 1.0, 1.0, 100.0)
    model.transform(vgll.mul_mat4(projection_mat4, view_mat4))
    rendered = benchmark(vglr.render, model)
    assert len(rendered.lines) == 9
    assert len(rendered.triangles) == 12
