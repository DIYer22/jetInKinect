# -*- coding: utf-8 -*-
g=[0]*5
#%%
import yl,time,cv2
from yl import ylimg
from yl.ylimg import show
from yl.ylimg import *
from yl.tool import *
from yl.ylnp import *
from pylab import np


import win32gui 
getWindowName = lambda :win32gui.GetWindowText (win32gui.GetForegroundWindow()).decode('gbk')
#%%
from pykeyboard import PyKeyboard
pyk = PyKeyboard()
def goleft():
    pyk.release_key(pyk.right_key)
    pyk.press_key(pyk.left_key)
def goright():
    pyk.release_key(pyk.left_key)
    pyk.press_key(pyk.right_key)
def gos():
    pyk.release_key(pyk.left_key)
    pyk.release_key(pyk.right_key)
#%%
isScend = lambda : not time.time().is_integer()
def __draw3dSurface(X,Y,Z):

    from matplotlib import cm
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib.ticker import LinearLocator, FormatStrFormatter
    fig = plt.figure()
#    ax = fig.gca(projection='3d')
    ax = Axes3D(fig)
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
r = (np.random.random((4,4))*5).astype(int)
greyToRgb = lambda grey:grey.repeat(3).reshape(list(grey.shape)+[3])
getXyzw = lambda it:(it.x,it.y)+(it.z,it.w)
import thread
import itertools
import ctypes

import pykinect
from pykinect import nui
from pykinect.nui import JointId

import pygame
from pygame.color import THECOLORS
from pygame.locals import *


deepResolution = 320

if deepResolution == 320:
    DEPTH_WINSIZE = 320,240
    nuiResolution = nui.ImageResolution.Resolution320x240
    
if deepResolution == 640:
    DEPTH_WINSIZE = 640,480
    nuiResolution = nui.ImageResolution.Resolution640x480


KINECTEVENT = pygame.USEREVENT

VIDEO_WINSIZE = 640,480
pygame.init()
dispInfo = None
screen = None
def getSkeletonPositions(player):
    l = [getXyzw(player.SkeletonPositions[idd]) for idd in range(20)]+\
    [getXyzw(player.get_position())]
    sp = np.array(l)
    sp[-1,-1] = 0
    x = np.mean(sp[[jo.shoulderCenter,jo.hipCenter,jo.spine]],0)
    sp[:-1] -= x
    return sp
SKELETON_COLORS = [THECOLORS["red"], 
                   THECOLORS["blue"], 
                   THECOLORS["green"], 
                   THECOLORS["orange"], 
                   THECOLORS["purple"], 
                   THECOLORS["yellow"], 
                   THECOLORS["violet"]]

LEFT_ARM = (JointId.ShoulderCenter, 
            JointId.ShoulderLeft, 
            JointId.ElbowLeft, 
            JointId.WristLeft, 
            JointId.HandLeft)
RIGHT_ARM = (JointId.ShoulderCenter, 
             JointId.ShoulderRight, 
             JointId.ElbowRight, 
             JointId.WristRight, 
             JointId.HandRight)
LEFT_LEG = (JointId.HipCenter, 
            JointId.HipLeft, 
            JointId.KneeLeft, 
            JointId.AnkleLeft, 
            JointId.FootLeft)
RIGHT_LEG = (JointId.HipCenter, 
             JointId.HipRight, 
             JointId.KneeRight, 
             JointId.AnkleRight, 
             JointId.FootRight)
SPINE = (JointId.HipCenter, 
         JointId.Spine, 
         JointId.ShoulderCenter, 
         JointId.Head)

allJoint = set(LEFT_ARM+LEFT_LEG+RIGHT_ARM+RIGHT_LEG+SPINE)
lowerFirst = lambda s :s[0].lower()+s[1:]
jointDic =  {lowerFirst(i.name):(i.value) for i in allJoint}
intToJoint = dict(zip(jointDic.values(),jointDic.keys()))
import yl
joint = yl.tool.dicToObj(jointDic)
jo = joint
#jointDic = dict(zip(map(lowerFirst,jointDic.values()),jointDic.keys()))
skeleton_to_depth_image = nui.SkeletonEngine.skeleton_to_depth_image



# recipe to get address of surface: http://archives.seul.org/pygame/users/Apr-2008/msg00218.html
if hasattr(ctypes.pythonapi, 'Py_InitModule4'):
   Py_ssize_t = ctypes.c_int
elif hasattr(ctypes.pythonapi, 'Py_InitModule4_64'):
   Py_ssize_t = ctypes.c_int64
else:
   raise TypeError("Cannot determine type of Py_ssize_t")

_PyObject_AsWriteBuffer = ctypes.pythonapi.PyObject_AsWriteBuffer
_PyObject_AsWriteBuffer.restype = ctypes.c_int
_PyObject_AsWriteBuffer.argtypes = [ctypes.py_object,
                                  ctypes.POINTER(ctypes.c_void_p),
                                  ctypes.POINTER(Py_ssize_t)]

def surface_to_array(surface):
   buffer_interface = surface.get_buffer()
   address = ctypes.c_void_p()
   size = Py_ssize_t()
   _PyObject_AsWriteBuffer(buffer_interface,
                          ctypes.byref(address), ctypes.byref(size))
   bytes = (ctypes.c_byte * size.value).from_address(address.value)
   bytes.object = buffer_interface
   return bytes

def draw_skeleton_data(pSkelton, index, positions, width = 4):
    start = pSkelton.SkeletonPositions[positions[0]]
       
    for position in itertools.islice(positions, 1, None):
        next = pSkelton.SkeletonPositions[position.value]
        
        curstart = skeleton_to_depth_image(start, dispInfo.current_w, dispInfo.current_h) 
        curend = skeleton_to_depth_image(next, dispInfo.current_w, dispInfo.current_h)
#        print (screen, SKELETON_COLORS[index], curstart, curend, width)
#        (<Surface(320x240x16 SW)>, (160, 32, 240, 255), 
#         (161.33431098117978, 118.00078981553618), (149.86954440126942, 87.68447313512536), 10)
        pygame.draw.line(screen, SKELETON_COLORS[index], curstart, curend, width)
        
        start = next
        
def draw_skeletons(skeletons):
    for index, data in enumerate(skeletons):
        # draw the Head
        HeadPos = skeleton_to_depth_image(data.SkeletonPositions[JointId.Head], dispInfo.current_w, dispInfo.current_h) 
         
        draw_skeleton_data(data, index, SPINE, 10)
        pygame.draw.circle(screen, SKELETON_COLORS[index], (int(HeadPos[0]), int(HeadPos[1])), 20, 0)
    
        # drawing the limbs
        draw_skeleton_data(data, index, LEFT_ARM)
        draw_skeleton_data(data, index, RIGHT_ARM)
        draw_skeleton_data(data, index, LEFT_LEG)
        draw_skeleton_data(data, index, RIGHT_LEG)



#%%  
toInd = lambda x:[i.value for i in x]
def setMaxMin(x,ma,mi):
    ma -= 1
    x[x>ma]=ma
    x[x<mi]=mi
    return x
def drawC(ps,img,v=0,r=10):
    ps = np.array(ps)
    if ps.ndim == 1:
        ps = np.array([ps])
    rrcc = [sk.draw.circle(p[0],p[1],r) for p in ps]
    rr,cc = [rr for rr,cc in rrcc], [cc for rr,cc in rrcc]
    rr,cc = np.array(reduce(np.append,rr)),np.array(reduce(np.append,cc))
    rr,cc = setMaxMin(rr,img.shape[0],0),setMaxMin(cc,img.shape[1],0)
    img[rr,cc] = v
#%%
openTime = True
TIME_DIC = {}
def setInterval(inter=5,idd=0):
    if not openTime or (idd in TIME_DIC and not TIME_DIC[idd]):
        return False
    t = int(time.time()/inter)
    if idd in TIME_DIC and t == TIME_DIC[idd]:
        return False
    else:
        TIME_DIC[idd]=t
        return True

PLAYER = None
DEPTH = None
VIDEO = None
def getPlayer(skframe):
    skeletonData = skframe.SkeletonData
    players = filter(lambda x:x.get_position().x and 0.9<x.get_position().z<3,skeletonData)
    g[-1] = players
    if not len(players):
        return 
    player = min(players,key=lambda x:x.get_position().z)
    g[3] = player
    global PLAYER
    PLAYER = player
    return player

def getYx(player,img):
    xy = [skeleton_to_depth_image(sp, img.shape[1],img.shape[0]) for sp in player.SkeletonPositions]
    yx = np.array(xy)[...,[1,0]].astype(int)
    setMaxMin(yx[:,0],VIDEO_WINSIZE[1],0)
    setMaxMin(yx[:,1],VIDEO_WINSIZE[0],0)
    return yx
def showSpInImg(player,img):
    yx = getYx(player,img)
    drawC(yx[[15,19]],img,v=[0,0,1])
    drawC(yx[[7,11]],img,v=[0,0,.5])
    drawC(yx[toInd(SPINE)],img,v=[0.5,0,0])
    drawC(yx[[3,]],img,v=[1,0,0],r=15)
#    drawC(yx[-1],img,v=[0,0,0],r=15)
    show(img)
    print yx[3]
    
    
#onlyShowBody(player,depth,rgb)

def getPointMask(p,depth,r):
    diff = 5
    cmask  = np.zeros(depth.shape,np.bool)
    drawC(p,cmask,v=True,r=r)
    dv = depth[p[0],p[1]]
    gt,lt = dv + diff,max(1,dv - diff)
    mask = (depth>lt)*(depth<gt)*cmask
    return mask
def getMask(player,depth,rgb):
    yxs = getYx(player,rgb)
    r = max(yxs[:,0])-min(yxs[:,0])
    r = r*0.2
    mask = reduce(np.add,[getPointMask(p,depth,r) for p in yxs])
#    [depth[p[0],p[1]] for p in yxs]
    smask = smoothImg(mask)
    return smask
    
def smoothImg(img,size=5):
    img = img.astype(np.uint8)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(size, size))  
    eroded = cv2.erode(img,kernel)  
    
    kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT,(size*2, size*2))  
    dilated = cv2.dilate(eroded,kernel2)  
    new = dilated
    kernel3 = cv2.getStructuringElement(cv2.MORPH_RECT,(int(size), int(size)))
    new = cv2.erode(dilated,kernel3)
    return new
    

def onlyShowBody(player,depth,rgb,dark=None):
    smask = getMask(player,depth,rgb)
    if dark:
        smask = smask.astype(float)
        smask[smask==0] = dark
    body = smask[:,:,None]*rgb
    return body.astype(np.uint8)
if __name__ == '__main__':
    
    pass
