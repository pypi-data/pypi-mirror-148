import tkinter as tk

import vecgl.linalg as vgll
import vecgl.model as vglm
import vecgl.kdtree as kdtree

# Rendering helper functions.

DEFAULT_EPS = 0.00001


def _get_clipping_space_volume():

    # Collect the 6 boundary planes.
    # Ensure that normals point away from the clipping space volume.
    boundary_planes = []
    for i in range(3):
        for a in [-1.0, 1.0]:
            u = [0.0, 0.0, 0.0]
            u[i] = a
            p = tuple(u)
            n = tuple(u)
            pl = p, n
            boundary_planes.append(pl)
    return boundary_planes


def _get_covered_triangle_volume(tr):
    p, q, r = tr.p, tr.q, tr.r

    # Do this in non-homogenious coordinates.
    p = vgll.to_vec3(p)
    q = vgll.to_vec3(q)
    r = vgll.to_vec3(r)

    # Get the triangle plane.
    pq = vgll.sub_vec3(q, p)
    pr = vgll.sub_vec3(r, p)
    n = vgll.cross_vec3(pq, pr)

    # Derive boundary plane.
    # Ensure that normals point away from the covered volume.
    ccwise = -1.0 if vgll.z_vec3(n) > 0.0 else 1.0
    n = vgll.scale_vec3(ccwise, n)
    boundary_planes = [(p, n)]

    # Collect the three remaining boundary planes per side of the triangle.
    n_pq = -ccwise * vgll.y_vec3(pq), ccwise * vgll.x_vec3(pq), 0.0
    boundary_planes.append((p, n_pq))
    qr = vgll.sub_vec3(r, q)
    n_qr = -ccwise * vgll.y_vec3(qr), ccwise * vgll.x_vec3(qr), 0.0
    boundary_planes.append((q, n_qr))
    rp = vgll.sub_vec3(p, r)
    n_rp = -ccwise * vgll.y_vec3(rp), ccwise * vgll.x_vec3(rp), 0.0
    boundary_planes.append((r, n_rp))

    return boundary_planes


def _get_plane_side(pl, q):
    p, n = pl
    pq = vgll.sub_vec3(q, p)
    return vgll.dot_vec3(pq, n)


def _get_plane_line_intersection(pl, q, r, eps=DEFAULT_EPS):
    p, n = pl
    qr = vgll.sub_vec3(r, q)
    qp = vgll.sub_vec3(p, q)
    denom = vgll.dot_vec3(qr, n)
    if abs(denom) < eps:
        return None
    return vgll.dot_vec3(qp, n) / denom


def _get_point_on_line(a, p, q):
    return vgll.add_vec3(vgll.scale_vec3(1.0 - a, p), vgll.scale_vec3(a, q))


# Point-specific rendering functions.


def _is_point_visible_wrt_clipping_space(pt):

    # Do this in non-homogenious coordinates.
    p = vgll.to_vec3(pt.p)

    px, py, pz = p
    if px < -1.0 or py < -1.0 or pz < -1.0:
        return False
    if px > 1.0 or py > 1.0 or pz > 1.0:
        return False
    return True


def _is_point_visible_wrt_triangle(pt, tr, eps=DEFAULT_EPS):

    # Do this in non-homogenious coordinates.
    p = vgll.to_vec3(pt.p)

    # If point is on or outside of any boundary plane then it is visible.
    boundary_planes = _get_covered_triangle_volume(tr)
    for pl in boundary_planes:
        if _get_plane_side(pl, p) >= -eps:
            return True
    return False


def _get_visible_points(points, triangles):

    # Find visible points wrt. clipping space.
    points_in_clipping_space = []
    for pt in points:
        if _is_point_visible_wrt_clipping_space(pt):
            points_in_clipping_space.append(pt)

    # Find actualy visible points within the clipping space.
    visible_points = []
    for pt in points_in_clipping_space:
        rel_triangles = triangles
        if all(_is_point_visible_wrt_triangle(pt, tr) for tr in rel_triangles):
            visible_points.append(pt)
    return visible_points


# Line-specific rendering functions.


def _get_line_fragments_outside_convex_volume(
    ln, boundary_planes, inverted=False, eps=DEFAULT_EPS
):

    # Do this in non-homogenious coordinates.
    p, q = vgll.to_vec3(ln.p), vgll.to_vec3(ln.q)

    # For convex volumes, the line fragments outside of the volume will be at
    # most two:
    #   - a head fragment starting in p, and
    #   - a tail fragment ending in q.
    # For a line fragment to be outside of the volume, it must be on the outer
    # side of one of the boundary planes. Start with empty head and tail
    # fragments as an under approximation.
    head_fragment_ub = 0.0
    tail_fragment_lb = 1.0

    # Find the complete line fragments by updating them per boundary plane.
    pq = vgll.sub_vec3(q, p)
    for pl in boundary_planes:
        intersection = _get_plane_line_intersection(pl, p, q)
        if intersection is not None:

            # Line and boundary plane intersect. Update head and tail fragment.
            _, n = pl
            is_same_direction = vgll.dot_vec3(n, pq) > 0
            if is_same_direction:
                tail_fragment_lb = min(intersection, tail_fragment_lb)
            else:
                head_fragment_ub = max(intersection, head_fragment_ub)
        else:

            # Line and boundary plane are parallel to each other. Return the
            # line unchanged if it is entirely outside of the volume.
            is_outside_volume = _get_plane_side(pl, p) >= -eps
            if is_outside_volume:
                intersects = False
                return intersects, [ln] if not inverted else []

    # If head and tail fragment are overlapping, the line does not intersect the
    # volume and we can return it as is.
    if head_fragment_ub + eps >= tail_fragment_lb:
        intersects = False
        return intersects, [ln] if not inverted else []

    # Otherwise, the line and triangle intersect, resulting in up to two line
    # fragments.
    intersects = True
    lines = []
    if not inverted:
        if head_fragment_ub >= eps:
            head_fragment_q = _get_point_on_line(head_fragment_ub, p, q)
            head_fragment = vglm.Line(p, head_fragment_q, ln.color)
            lines.append(head_fragment)
        if tail_fragment_lb <= 1.0 - eps:
            tail_fragment_p = _get_point_on_line(tail_fragment_lb, p, q)
            tail_fragment = vglm.Line(tail_fragment_p, q, ln.color)
            lines.append(tail_fragment)
    else:
        center_fragment_p = _get_point_on_line(head_fragment_ub, p, q)
        center_fragment_q = _get_point_on_line(tail_fragment_lb, p, q)
        center_fragment = vglm.Line(
            center_fragment_p, center_fragment_q, ln.color)
        lines.append(center_fragment)
    return intersects, lines


def _get_visible_line_fragment_wrt_clipping_space(ln):

    boundary_planes = _get_clipping_space_volume()
    intersects, line_fragments = _get_line_fragments_outside_convex_volume(
        ln, boundary_planes, inverted=True
    )
    assert len(line_fragments) <= 1
    if len(line_fragments) == 1:
        return line_fragments[0]
    return None


def _get_visible_line_fragments_wrt_triangle(ln, tr, eps=DEFAULT_EPS):
    boundary_planes = _get_covered_triangle_volume(tr)
    return _get_line_fragments_outside_convex_volume(ln, boundary_planes)


def _get_visible_line_fragments(lines, triangles):

    # Find visible line fragments wrt. clipping space.
    line_fragments_in_clipping_space = []
    for ln in lines:
        ln_fragment = _get_visible_line_fragment_wrt_clipping_space(ln)
        if ln_fragment is not None:
            line_fragments_in_clipping_space.append(ln_fragment)

    # Find visible line fragments within clipping space.
    visible_line_fragments = []
    worklist = line_fragments_in_clipping_space
    while len(worklist) > 0:
        ln = worklist.pop()
        rel_triangles = triangles
        is_fully_visible = True
        for tr in rel_triangles:
            intersects, ln_fragments = _get_visible_line_fragments_wrt_triangle(
                ln, tr)
            if intersects:
                worklist.extend(ln_fragments)
                is_fully_visible = False
                break
        if is_fully_visible:
            visible_line_fragments.append(ln)
    return visible_line_fragments


# Render an entire model.


def render(model):
    rendered = vglm.Model()
    rendered.points = _get_visible_points(model.points, model.triangles)
    rendered.lines = _get_visible_line_fragments(model.lines, model.triangles)
    rendered.triangles = model.triangles  # Not yet implemented.
    rendered.rendered = True
    return rendered


# Show models and render them if needed.


def show(model, size=600, stroke_width=2):

    # Render the model to find all the visible points, line fragments, and
    # triangle fragments.
    if not model.rendered:
        model = render(model)

    # Transform the model to window space.
    model.transform(vgll.get_viewport_mat4(0.0, size, size, -size))

    # Create a canvas.
    frame = tk.Tk()
    canvas = tk.Canvas(frame, bg="white", height=size, width=size)

    # Draw the triangle fragments, which are fully visible.
    for tr in model.triangles:
        px, py, pz = vgll.to_vec3(tr.p)
        qx, qy, qz = vgll.to_vec3(tr.q)
        rx, ry, rz = vgll.to_vec3(tr.r)
        canvas.create_polygon([px, py, qx, qy, rx, ry], fill=tr.color)

    # Draw the lines fragments, which are fully visible.
    for ln in model.lines:
        px, py, pz = vgll.to_vec3(ln.p)
        qx, qy, qz = vgll.to_vec3(ln.q)
        canvas.create_line(
            px,
            py,
            qx,
            qy,
            width=stroke_width,
            fill=ln.color,
            capstyle=tk.ROUND,
            joinstyle=tk.ROUND,
        )

    # Draw the points, which are fully visible.
    for pt in model.points:
        px, py, pz = vgll.to_vec3(pt.p)
        canvas.create_line(
            px,
            py,
            px,
            py,
            width=stroke_width,
            fill=pt.color,
            capstyle=tk.ROUND,
            joinstyle=tk.ROUND,
        )

    # Display the hard work.
    canvas.pack()
    frame.mainloop()
