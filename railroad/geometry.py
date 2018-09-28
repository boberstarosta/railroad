
import math
from collections import namedtuple
from .vec import Vec

def bezier3(p0, p1, p2, p3, t):
    return p0*(1 - t)**3 + p1*3*(1 - t)**2*t + p2*3*(1 - t)*t**2 + p3*t**3

def nearest_t_on_line(pos, point1, point2):
    length_sq = (point2 - point1).length_sq
    if length_sq == 0:
        return 0.0
    return Vec.dot(point2 - point1, pos - point1) / length_sq

def nearest_point_on_segment(pos, point1, point2):
    t = nearest_t_on_line(pos, point1, point2)
    t = min(1, max(0, t))
    return point1 + (point2 - point1) * t

def nearest_point_on_line(pos, point1, point2):
    t = nearest_t_on_line(pos, point1, point2)
    return point1 + (point2 - point1) * t

def dist_to_segment(pos, point1, point2):
    return (nearest_point_on_segment(pos, point1, point2) - pos).length

def shortest_side_of_triangle(points):
    min_len_sq = None
    shortest = None
    for i in range(len(points)):
        j = (i + 1) % len(points)
        len_sq = (points[i] - points[j]).length_sq
        if min_len_sq is None or len_sq < min_len_sq:
            min_len_sq = len_sq
            shortest = (i, j)
    return shortest

def farthest_point(pos, points):
    max_dist_sq = None
    farthest = None
    for index, point in enumerate(points):
        dist_sq = (pos - point).length_sq
        if max_dist_sq is None or dist_sq > max_dist_sq:
            max_dist_sq = dist_sq
            farthest = index
    return farthest

def point_in_rect(point, x, y, w, h):
    return point[0] >= x and point[1] >= y and point[0] < x + w and point[1] < y + h

def angle_difference(a, b, longer=False):
    if longer:
        if abs(b - a) < 180:
            if a < b:
                a += 360
            elif b < a:
                b += 360
    else:
        if abs(b - a) > 180:
            if a < b:
                a += 360
            elif b < a:
                b += 360
        
    return b - a

def arc(center, radius, a, b, t, longer=False):
    difference = angle_difference(a, b, longer)
    angle = a + t * difference
    radians = math.radians(angle)
    return center + Vec(math.cos(radians), math.sin(radians)) * radius

def intersect_param(p0, d0, p1, d1):
    determinant = d0.y*d1.x - d0.x*d1.y
    if determinant == 0:
        return float("inf")
    return (p1.y*d1.x + p0.x*d1.y - p1.x*d1.y - p0.y*d1.x) / determinant

def intersect_point(p0, d0, p1, d1):
    t = intersect_param(p0, d0, p1, d1)
    if t == float("inf"):
        return None
    else:
        return p0 + d0 * t

def generate_circular_arc(p0, d0, p1, d1, precision=10):
    curve = []
    
    t0 = intersect_param(p0, d0, p1, d1)
    t1 = intersect_param(p1, d1, p0, d0)
    convergent = (t0 > 0 and t1 > 0)
    
    intersect = intersect_point(p0, d0, p1, d1)
    
    if intersect is None:
        return generate_bezier(p0, d0, p1, d1, precision)
    
    pni0 = p0
    pni1 = p1
    
    intdist0 = (intersect - p0).length
    intdist1 = (intersect - p1).length

    if convergent:
        if intdist0 > intdist1:
            pni0 = intersect + (p0 - intersect).normalized * intdist1
            curve.append(pni0)
        elif intdist1 > intdist0:
            pni1 = intersect + (p1 - intersect).normalized * intdist0
    else:
        if intdist0 < intdist1:
            pni0 = intersect + (p0 - intersect).normalized * intdist1
            curve.append(pni0)
        elif intdist1 < intdist0:
            pni1 = intersect + (p1 - intersect).normalized * intdist0
    
    dir0 = (pni0 - intersect).normalized
    d0 = (intersect - pni1).normalized
    perp0 = Vec(-dir0.y, dir0.x)
    perp1 = Vec(-d0.y, d0.x)
    center = intersect_point(pni0, perp0, pni1, perp1)
    if center is None:
        return generate_bezier(p0, d0, p1, d1, precision)
    
    cangle0 = (pni0 - center).angle
    cangle1 = (pni1 - center).angle
    radius = (pni0 - center).length
    
    steps = int(abs(angle_difference(cangle0, cangle1, not convergent)) // precision)
    for i in range(1, steps):
        t = i / steps
        pt = arc(center, radius, cangle0, cangle1, t, not convergent)
        curve.append(pt)
    
    if convergent:
        if intdist1 > intdist0:
            curve.append(pni1)
    else:
        if intdist1 < intdist0:
            curve.append(pni1)
    
    return curve

def generate_bezier(p0, d0, p1, d1, precision=10):
    curve = []
    length = (p1 - p0).length / 2
    steps = 90 // precision
    for i in range(1, steps):
        t = i / steps
        curve.append( bezier3(p0, p0 + d0*length, p1 + d1*length, p1, t) )
    return curve

def generate_curve(p0, d0, p1, d1, precision=10):
    curve = []
    
    t0 = intersect_param(p0, d0, p1, d1)
    t1 = intersect_param(p1, d1, p0, d0)
    
    mint = 50.0
    
    if (t0 > mint and t1 > mint) or (t0 < mint and t1 < mint):
        curve = generate_circular_arc(p0, d0, p1, d1, precision)
    else:
        curve = generate_bezier(p0, d0, p1, d1, precision)
    
    return curve

