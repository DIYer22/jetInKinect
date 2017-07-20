# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import numpy as np
import matplotlib.pyplot as plt

def __draw3dSurface(X,Y,Z):

    from matplotlib import cm
    from matplotlib.ticker import LinearLocator, FormatStrFormatter
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    
    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
    #画表面,x,y,z坐标， 横向步长，纵向步长，颜色，线宽，是否渐变
    
    #ax.set_zlim(-1.01, 1.01)#坐标系的下边界和上边界
    ax.zaxis.set_major_locator(LinearLocator(10))#设置Z轴标度
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))#Z轴精度
    fig.colorbar(surf, shrink=0.5, aspect=5)#shrink颜色条伸缩比例（0-1），aspect颜色条宽度（反比例，数值越大宽度越窄）
    
    plt.show()


def polt3dSurface(Z):
    m, n = Z.shape
    X = range(n)
    Y = range(m)
    X, Y = np.meshgrid(X, Y)
    __draw3dSurface(X,Y,Z)

