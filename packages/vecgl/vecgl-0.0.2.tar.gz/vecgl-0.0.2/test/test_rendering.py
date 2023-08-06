import vecgl.model as vglm
import vecgl.rendering as vglr
import vecgl.linalg as vgll


def test_render_points_outside_of_clipping_space():
    model = vglm.Model()
    model.add_point((1.25, 0.0, 0.0), "green")
    model.add_point((0.0, 1.0, 0.0), "green")
    model.add_point((0.0, 1.0, 0.5), "green")
    rendered = vglr.render(model)
    assert len(rendered.points) == 2


def test_render_point_behind_triangle():
    model = vglm.Model()
    model.add_triangle((0.0, 0.0, 0.0),
                       (1.0, 0.0, 0.0),
                       (0.0, 1.0, 0.0), "red")
    model.add_point((0.25, 0.25, 1.0), "green")
    rendered = vglr.render(model)
    assert len(rendered.points) == 0
    assert len(rendered.triangles) == 1


def test_render_point_in_front_of_triangle():
    model = vglm.Model()
    model.add_triangle((0.0, 0.0, 0.0),
                       (1.0, 0.0, 0.0),
                       (0.0, 1.0, 0.0), "red")
    model.add_point((0.25, 0.25, -1.0), "green")
    rendered = vglr.render(model)
    assert len(rendered.points) == 1
    assert len(rendered.triangles) == 1


def test_render_point_next_to_triangle():
    model = vglm.Model()
    model.add_triangle((0.0, 0.0, 0.0),
                       (1.0, 0.0, 0.0),
                       (0.0, 1.0, 0.0), "red")
    model.add_point((-0.5, 0.5, 0.0), "green")
    rendered = vglr.render(model)
    assert len(rendered.points) == 1
    assert len(rendered.triangles) == 1


def test_render_point_on_triangle():
    model = vglm.Model()
    model.add_triangle((0.0, 0.0, 0.0),
                       (1.0, 0.0, 0.0),
                       (0.0, 1.0, 0.0), "red")
    model.add_point((0.2, 0.2, 0.0), "green")
    rendered = vglr.render(model)
    assert len(rendered.points) == 1
    assert len(rendered.triangles) == 1


def test_render_point_on_triangle_edge():
    model = vglm.Model()
    model.add_triangle((0.0, 0.0, 0.0),
                       (1.0, 0.0, 0.0),
                       (0.0, 1.0, 0.0), "red")
    model.add_point((0.5, 0.5, 0.0), "green")
    rendered = vglr.render(model)
    assert len(rendered.points) == 1
    assert len(rendered.triangles) == 1


def test_render_lines_outside_of_clipping_space():
    model = vglm.Model()
    model.add_line((-1.0, -1.0, 1.0),
                   (1.0, 1.0, 0.5), "green")
    model.add_line((0.0, 0.0, 0.0),
                   (0.3, 0.4, 0.5), "green")
    model.add_line((-2.3, 0.0, 0.0),
                   (4.5, 0.0, 0.0), "green")
    model.add_line((-2.3, -0.1, 0.4),
                   (4.5, 0.2, -0.3), "green")
    model.add_line((-2.0, -2.0, -2.0),
                   (2.0, 2.0, 2.0), "green")
    model.add_line((2.0, 2.0, -2.0),
                   (2.0, 2.0, 2.0), "green")
    rendered = vglr.render(model)
    assert len(rendered.lines) == 5


def test_render_line_behind_triangle():
    model = vglm.Model()
    model.add_triangle((0.0, 0.0, 0.0),
                       (0.0, 1.0, 0.0),
                       (1.0, 0.0, 0.0), "red")
    model.add_line((-1.0, -1.0, 1.0),
                   (1.0, 1.0, 0.5), "green")
    rendered = vglr.render(model)
    assert len(rendered.lines) == 2
    assert len(rendered.triangles) == 1


def test_render_line_in_front_of_triangle():
    model = vglm.Model()
    model.add_triangle((0.0, 0.0, 0.0),
                       (1.0, 0.0, 0.0),
                       (0.0, 1.0, 0.0), "red")
    model.add_line((-1.0, -1.0, -0.5),
                   (1.0, 1.0, -1.0), "green")
    rendered = vglr.render(model)
    assert len(rendered.lines) == 1
    assert len(rendered.triangles) == 1


def test_render_line_next_to_triangle():
    model = vglm.Model()
    model.add_triangle((0.0, 0.0, 0.0),
                       (1.0, 0.0, 0.0),
                       (0.0, 1.0, 0.0), "red")
    model.add_line((-1.0, 0.0, 0.0),
                   (0.0, -1.0, 0.0), "green")
    rendered = vglr.render(model)
    assert len(rendered.lines) == 1
    assert len(rendered.triangles) == 1


def test_render_line_on_triangle():
    model = vglm.Model()
    model.add_triangle((0.0, 0.0, 0.0),
                       (1.0, 0.0, 0.0),
                       (0.0, 1.0, 0.0), "red")
    model.add_line((0.0, 0.0, 0.0),
                   (0.5, 0.5, 0.0), "green")
    rendered = vglr.render(model)
    assert len(rendered.lines) == 1
    assert len(rendered.triangles) == 1


def test_render_line_on_triangle_edge():
    model = vglm.Model()
    model.add_triangle((0.0, 0.0, 0.0),
                       (1.0, 0.0, 0.0),
                       (0.0, 1.0, 0.0), "red")
    model.add_line((1.0, 0.0, 0.0),
                   (0.0, 1.0, 0.0), "green")
    rendered = vglr.render(model)
    assert len(rendered.lines) == 1
    assert len(rendered.triangles) == 1


def test_render_line_through_triangle_cw():
    model = vglm.Model()
    model.add_triangle((0.0, 0.0, 0.0),
                       (1.0, 0.0, 0.0),
                       (0.0, 1.0, 0.0), "red")
    model.add_line((-0.5, -0.5, 1.0),
                   (1.0, 1.0, -1.0), "green")
    rendered = vglr.render(model)
    assert len(rendered.lines) == 2
    assert len(rendered.triangles) == 1


def test_render_line_through_triangle_ccw():
    model = vglm.Model()
    model.add_triangle((0.0, 0.0, 0.0),
                       (0.0, 1.0, 0.0),
                       (1.0, 0.0, 0.0), "red")
    model.add_line((1.0, 1.0, -1.0),
                   (-0.5, -0.5, 1.0), "green")
    rendered = vglr.render(model)
    assert len(rendered.lines) == 2
    assert len(rendered.triangles) == 1


def test_render_model():
    model = vglm.get_cube_model()
    view_mat4 = vgll.mul_mat4(
        vgll.get_translate_mat4(0.0, 0.0, -3.0),
        vgll.get_rotate_y_mat4(0.5))
    projection_mat4 = vgll.get_frustum_mat4(-1.0, 1.0, -1.0, 1.0, 1.0, 100.0)
    model.transform(vgll.mul_mat4(projection_mat4, view_mat4))
    rendered = vglr.render(model)
    assert len(rendered.lines) == 7
    assert len(rendered.triangles) == 12
