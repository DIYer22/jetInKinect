# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import numpy as np
import matplotlib.pyplot as plt
import cv2
import skimage as sk
from skimage import io
from skimage import data 

# random((m, n), max) => m*n matrix
# random(n, max) => n*n matrix
random = lambda shape,maxx:(np.random.random(
shape if (isinstance(shape,tuple) or isinstance(shape,list)
)else (shape,shape))*maxx).astype(int)

normalizing = lambda a:(a.astype(float)-a.min())/(a.max() - a.min())

floatToUint8 = lambda img:(normalizing(img)*255.999999).astype(np.uint8)

def mapp(f, matrix, need_i_j=False):
    '''
    for each item of a 2-D matrix
    return a new matrix consist of f:f(it) or f(it, i, j)
    '''
    m, n = matrix.shape[:2]
    listt = [[None]*n for i in range(m)]
    for i in range(m):
        for j in range(n):
            it = matrix[i][j]
            listt[i][j] = f(it,i,j) if need_i_j else f(it)
    return np.array(listt)

def show(*imgs):
    '''
    do io.imshow to a list of imgs or one img
    '''
    if len(imgs)>1:
        l = imgs
    else:
        l = imgs[0]
    if isinstance(l,dict):
        l = l.values()
#    if not isinstance(l,list) and (not isinstance(l,tuple) ) :
#        l = [l]
    if isinstance(l,np.ndarray):
        if l.ndim>=3 and l.shape[-1]==1:
            l = l[...,0]
        if l.ndim==2 or (l.ndim ==3 and l.shape[-1]==3):
            l = [l]
        else:
            l = list(l)
        
    n = len(l)
    if n > 3:
        show(l[:3])
        show(l[3:])
        return 
    fig, axes = plt.subplots(ncols=n)
    count = 0
    axes = [axes] if n==1 else axes 
    for img in l:
        axes[count].imshow(img,cmap='gray')
        count += 1
    plt.show()
    
def loga(array):
    '''
    Analysis np.array with a graph. include shape, max, min, distribute
    '''
    if isinstance(array,list):
        array = np.array(array)
    if isinstance(array,str) or isinstance(array,unicode):
        print 'info and histogram of',array
        l=[]
        eval('l.append('+array+')')
        array = l[0]
    print 'shape:%s ,max: %s, min: %s'%(str(array.shape),str(array.max()),str(array.min()))
    
    unique = np.unique(array)
    if len(unique)<10:
        dic=dict([(i*1,0) for i in unique])
        for i in array.ravel():
            dic[i] += 1
        listt = dic.items()
        listt.sort(key=lambda x:x[0])
        data,x=[v for k,v in listt],np.array([k for k,v in listt]).astype(float)
        if len(x) == 1:
            print 'All value is',x[0]
            return
        width = (x[0]-x[1])*0.7
        x -=  (x[0]-x[1])*0.35
    else:
        data, x = np.histogram(array.ravel(),8)
        x=x[1:]
        width = (x[0]-x[1])
    plt.plot(x, data, color = 'orange')
    plt.bar(x, data,width = width, alpha = 0.5, color = 'b')
    plt.show()
    return 
    
def base64Img(arr):
    import base64,sys
    py3 = sys.version_info.major == 3
    cnt = cv2.imencode('.jpg',arr[:,:,[2,1,0]])[1]
    if py3:
        return base64.encodebytes(cnt[...,0]).decode('utf-8')
    return base64.encodestring(cnt)



