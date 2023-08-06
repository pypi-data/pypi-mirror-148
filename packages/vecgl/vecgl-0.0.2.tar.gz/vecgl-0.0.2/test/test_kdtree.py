import vecgl.kdtree as vglk


def test_find_single_point():
    p = 1.2, 3.4, 5.6
    tree = vglk.make_kdtree([p])
    assert tree.find_point(p) == True


def test_find_point():
    ps = []
    for i in range(3):
        for j in range(3):
            p = 1.0 * i, 1.0 * j
            ps.append(p)
    tree = vglk.make_kdtree(ps)
    for p in ps:
        assert tree.find_point(p) == True


def test_find_points():
    ps = []
    for i in range(8):
        for j in range(8):
            p = 1.0 * i, 1.0 * j
            ps.append(p)
    tree = vglk.make_kdtree(ps)
    bbox_lb = 2.0, 4.0
    bbox_ub = 4.0, 5.0
    ps_in_bbox = tree.find_points(bbox_lb, bbox_ub)
    assert len(ps_in_bbox) == 6
