def _is_point_in_bbox(p, bbox_lb, bbox_ub):
    k = len(p)
    for i in range(k):
        if p[i] < bbox_lb[i] or p[i] > bbox_ub[i]:
            return False
    return True


class KDTree:

    def __init__(self, i, p, lhs, rhs):
        self.i = i
        self.p = p
        self.lhs = lhs
        self.rhs = rhs

    def find_point(self, p):

        # Check if the point is here.
        if self.p == p:
            return True

        # For points that are less or equal in dimension i, recur left.
        if p[self.i] <= self.p[self.i]:
            if self.lhs == None:
                return False
            return self.lhs.find_point(p)

        # For points that are greater in dimension i, recur right.
        if self.rhs == None:
            return False
        return self.rhs.find_point(p)

    def find_points(self, bbox_lb, bbox_ub):
        ps = []

        # Collect point if in bounding box.
        if _is_point_in_bbox(self.p, bbox_lb, bbox_ub):
            ps.append(self.p)

        # If the bounding box reaches into the left subtree, recur.
        if bbox_lb[self.i] <= self.p[self.i]:
            if self.lhs != None:
                ps.extend(self.lhs.find_points(bbox_lb, bbox_ub))

        # If the bounding box reaches into the right subtree, recur.
        if bbox_ub[self.i] > self.p[self.i]:
            if self.rhs != None:
                ps.extend(self.rhs.find_points(bbox_lb, bbox_ub))

        return ps


def make_kdtree(ps, i=0):

    # Return empty tree if no points given.
    if len(ps) == 0:
        return None

    # Find a good separating point for the root.
    # This is the last point that is equal to the median in dimension i.
    ps.sort(key=lambda p: p[i])
    j = len(ps)//2
    while j < len(ps) - 1 and ps[j][i] == ps[j+1][i]:
        j += 1

    # Find points to push into the left and right subtree.
    p = ps[j]
    ps_lhs = ps[:j]
    ps_rhs = ps[j+1:]

    # Recursively build the subtrees.
    k = len(p)
    i_next = (i+1) % k
    lhs = make_kdtree(ps_lhs, i_next)
    rhs = make_kdtree(ps_rhs, i_next)

    return KDTree(i, p, lhs, rhs)
