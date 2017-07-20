# -*- coding: utf-8 -*-
g=[0]*5
import numpy as np
from sympy import Plane, Point3D, Line3D
import sympy
import sympy as sy

def choice(listt,listLen,f,r=None):
    if r is None:
        r = []
    deep = len(r)
    if deep == listLen:
        l = [listt[i] for i in r]
        f(tuple(l))
        return 
    for ind in range((r[-1]+1) if r else 0,len(listt)+deep-listLen+1):
        r.append(ind)
        choice(listt,listLen,f,r)
        r.pop()
def vectorToUnitVector(t):
    t = np.array(t)
    for i in t:
        if i>0:
            break
        elif i<0:
            t = -t
            break
    return t/((t**2).sum())**0.5
def pointsToPlanes(points):
    planes = []
    f = lambda x:planes.append(Plane(*x))
    choice(points,3,f)
    return planes
def fitPointsToPlane(points):
#    if not isinstance(points,np.ndarray):
#        points = np.array(points)
    nvs = []
    planes = pointsToPlanes(points)
    nvs = [vectorToUnitVector(p.normal_vector.args) for p in planes]
    nvs = np.array(nvs).astype(float)
    #nvs = nvs/((nvs**2).sum(1)**0.5)[...,None]
    nv = nvs.mean(0)
    uv = vectorToUnitVector(nv)
    points = np.array(points)
    point = points.mean(0)
    plane = Plane(tuple(point),tuple(uv))
    return plane
def toLine(l):
    if isinstance(l,sympy.geometry.line.Line3D):
        return l
    if isinstance(l,np.ndarray):
        if l.shape == (2,3):
            return Line3D(tuple(l[0]),tuple(l[1]))
        l = tuple(l)
    if isinstance(l,(list,tuple,sympy.geometry.point.Point3D,sympy.core.containers.Tuple)):
        return Line3D((0,0,0),l)
def angleBetween(l1,l2):
    l1, l2 = map(toLine,(l1,l2))
    ag = l1.angle_between(l2)
    return float(ag)
toArray = lambda x:np.array(x).astype(float)
def degreeOfVictor(p1,p2):
    p1,p2 = map(toArray,(p1,p2))
    dotProduct = (p1*p2).sum()
    norm = lambda p:(p**2).sum()**0.5
    angle = dotProduct/(norm(p1)*norm(p2))
    arccosDegree = lambda x:np.degrees(np.arccos(x))
    degree = arccosDegree(angle)
    return degree 

#%%
if __name__ == '__main__':
    po = Point3D(0,0,0)
#    print fitPointsToPlane(points)
    a.distance(po)
    
    l = Line3D((0,0,0),(1,0,0))
    l2 = Line3D((0,1,0),(0,1,1))
    
    a = Plane(Point3D(1,1,1), normal_vector=(1,1,1))
    b = a.perpendicular_line(Point3D(0,0,0))
    points = (1,0,0),(0,1,0),(0,0,1),(0.1,0.1,0.1)
    
    a.distance(Point3D(0,0,0))
    pass