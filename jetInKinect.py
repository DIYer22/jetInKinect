# -*- coding: utf-8 -*-
g=[0]*5
#%%
import gameTool

from gameTool import (allJoint, base64Img, color,
          crun, ctypes, cv2, data, deepResolution,
          dicToObj, dispInfo, drawC, draw_skeleton_data, draw_skeletons,
          floatToUint8, frun, g, getMask, getPlayer,
          getPointMask, getSkeletonPositions, getWindowName, getXyzw, getYx,
          gmtTimeStr, goleft, goright, gos, greyToRgb,
          ignoreWarning, importAllFunCode, io, isScend, itertools,
          joint, jointDic, load_data, localTimeStr, log,
          logTool, loga, lowerFirst, mapp, memo,
          normalizing, np, nui, nuiResolution, onlyShowBody,
          openTime, openread, openwrite, os, plt,
          polt3dSurface, pygame, pyk, pykinect, r,
          random, save_data, screen, setInterval, setMaxMin,
          show, showSpInImg, sk, skeleton_to_depth_image, smoothImg,
          surface_to_array, thread, time, toInd, win32gui,
          yl, ylimg,intToJoint,jo)

from keyboard import doKey,doKeys,releaseKeys
import keyboard
r = (np.random.random((4,4))*5).astype(int)
greyToRgb = lambda grey:grey.repeat(3).reshape(list(grey.shape)+[3])
from gameTool import *
#while 1:time.sleep(1) ;print 8,win32gui.GetWindowText (win32gui.GetForegroundWindow()).decode('gbk')
def depth_frame_ready(frame):
    address = []
    fb = frame.image.bits
    de = np.ndarray(buffer=fb, dtype=np.uint8, shape=DEPTH_WINSIZE[::-1]+(2,))[...,1]
    g[1] = de
    gameTool.DEPTH = de
    if video_display:
        return
#    de = sk.exposure.exposure.equalize_hist(de)
#    de = floatToUint8(de)
    de = de.T
#    de = de.repeat(3).reshape(list(de.shape)+[3])
#    de = np.where(de>0,255,0)
    gameTool.screen.blit(pygame.surfarray.make_surface(de),(0,0))
    pygame.display.update()    

#%%  

def video_frame_ready(frame):
    img4 = np.ndarray(buffer= frame.image.bits, dtype=np.uint8, shape=(480,640, 4))
    img = img4[...,[2,1,0]]
    gameTool.VIDEO = img
    g[0] = (img.copy())
    if setInterval(1,'video'):
        fb = frame.image.bits
#        img = np.ndarray(buffer=fb, dtype=np.uint8, shape=(480,640, 4))
#        show(img4[...,[2,1,0]][::2,::2])
#        print gameTool.PLAYER , gameTool.DEPTH 
        if gameTool.PLAYER is not None and gameTool.DEPTH is not None and 1:
            depth = cv2.resize(gameTool.DEPTH,VIDEO_WINSIZE)
            body = onlyShowBody(gameTool.PLAYER,depth,img,0.3)
            if not video_display:
                print np.mean(depth)
            show(body)
    if video_display:
        if gameTool.PLAYER is not None and gameTool.DEPTH is not None:
            depth = cv2.resize(gameTool.DEPTH,VIDEO_WINSIZE)
            body = onlyShowBody(gameTool.PLAYER,depth,img,0.3)
            gameTool.screen.blit(pygame.surfarray.make_surface(body.transpose(1,0,2)),(0,0))
            pygame.display.update()  
            return 

    if not video_display:
        return

    with screen_lock:
        address = surface_to_array(gameTool.screen)
        
        g[2] = frame
        fb = frame.image.bits
#        img = np.ndarray(buffer=fb, dtype=np.uint8, shape=DEPTH_WINSIZE[::-1]+(4,))
#        show(img[...,[2,1,0]])
        ctypes.memmove(address, frame.image.bits, len(address))
        del address
        if skeletons is not None and draw_skeleton:
            draw_skeletons(skeletons)
        pygame.display.update()

def showPlayerDepthVideo(video, depth, player):
    if player is not None and depth is not None:
        depth = cv2.resize(depth,VIDEO_WINSIZE)
        body = onlyShowBody(player ,depth,video,0.3)
        body = normalizing(body)
        showSpInImg(player, body)
        sp = getSkeletonPositions(player)
#        printHandsForDriver(sp)
#        printPlayerInfo(player)
jointsList = [jo.head,jo.handLeft,jo.handRight,jo.hipCenter,jo.kneeLeft,jo.kneeRight]
def saveAll():
    saveList.append([gameTool.VIDEO, gameTool.DEPTH, gameTool.PLAYER])
    showPlayerDepthVideo(gameTool.VIDEO, gameTool.DEPTH, gameTool.PLAYER)
def printPlayerInfo(player,joints=None):
    sp = getSkeletonPositions(player)
    if joints is None:
        joints = intToJoint
    print '\n'.join([(n+': x=%.2f, y=%.2f, z=%.2f, w=%.2f,'%tuple(sp[i])) for i,n in intToJoint.items() if i in joints] )

def bySpine(player,lean=0.14):
    poss = [player.SkeletonPositions[i].x for i in SPINE[::-1]]
    if (poss[0]-poss[-1]) > lean:
        goright()
    elif (poss[0]-poss[-1]) < -lean:
        goleft()
    else:
        gos()
        pass
def byHand(player,diff=0.1):
    poss = [player.SkeletonPositions[i].y for i in [11,7]]
    if (poss[0]-poss[-1]) > diff:
        goleft()
        print 'left'
    elif (poss[0]-poss[-1]) < -diff:
        goright()
    else:
        gos()
        pass
def winterRush(player):
    if 'Winter Rush - Google Chrome' in getWindowName():
#        bySpine()
        byHand(player)
def gta(player):
    if 'GTA: San Andreas' in getWindowName():
#        bySpine()
        byHand(player)
def driver(player):
    sp = getSkeletonPositions(player)
    handYDiff = 0.15
    diff = sp[jo.handLeft][1] - sp[jo.handRight][1]
    handTurnRight = diff > handYDiff
    handTurnLeft = diff < -handYDiff
    
    elbowZThr = -0.08
    elbowZThrBack = 0.05
    elbowMean = (sp[jo.elbowLeft][2]+sp[jo.elbowRight][2])/2
    elbowForward = elbowMean<elbowZThr
    elbowBackward = elbowMean>elbowZThrBack
    print '%.2f'%elbowMean
    
    
    kneeYThr = -0.55
    kneeMean = (sp[jo.kneeLeft][1]+sp[jo.kneeRight][1])/2
    isCrouch = kneeMean > kneeYThr
#   print '%.2f'%kneeMean

    hipTurnRight = False
    hipTurnLeft = False
    
    backDrive = isCrouch or elbowBackward
    backDrive =  elbowBackward
    kvs = {
     'a':handTurnLeft or hipTurnLeft,
     'd':handTurnRight or hipTurnRight,
     'w':elbowForward and not backDrive,
     's':backDrive,
     }
    print [k for k,v in kvs.items() if v]
    if 'GTA: San Andreas' in getWindowName():
        doKeys(kvs)
        
    
#%%
def action(frame):
    player = getPlayer(frame)
    if not player :
        return

    winterRush(player)
#    gta(player)
#    driver(player)
    fly(player)
    if setInterval(0.5,'zs'):
        showPlayerDepthVideo(gameTool.VIDEO, gameTool.DEPTH, gameTool.PLAYER)
    if setInterval(20,'sp'):
        img = np.zeros(VIDEO_WINSIZE[::-1]+(3,))+1
        showSpInImg(player,img)
swich = 0
debug = False
gameTool.openTime = True
gameTool.TIME_DIC['sp'] = None
gameTool.TIME_DIC['video'] = None
gameTool.TIME_DIC['zs'] = None
saveList = []

from yl.tool import setTimeOut
from speech import google,bing,sphinx,baidu,Listen
TIME_DIC = {}
def handleAudio(audio):
#    if not 'GTA: San Andreas' in getWindowName():
#        return
    ti = time.time()
    TIME_DIC[ti] = True
    g = lambda :handleText(google(audio),ti,'google')
    b = lambda :handleText(bing(audio),ti,'bing')
    s = lambda :handleText(sphinx(audio),ti,'sphinx')
    bd = lambda :handleText(baidu(audio),ti,'baidu')
    setTimeOut(g,0)
    setTimeOut(b,0)
#    setTimeOut(s,0)
    setTimeOut(bd,0)
from keyboard import sendWord,pkey,rkey,kv,keyDic,tapKey
#222
def handleText(text, ti, name):
    if not text or ti not in TIME_DIC:
        return 
    t = text.lower()
    get = 'get' in t
    plan = 'plan' in t or 'air' in t
    car = 'car' in t
    out = 'out' in t
    inn = ('in' in t and (car or plan )) or('drive' in t)
    lock = 'lock' in t
    flash = 'flash' in t
    fire = 'fire' in t
    radio = 'radio' in t
    wheel = ('wheel' in t or 'well' in t or 'will' in t or
             'apple' in t or 'vail' in t or 'up' in t or 
             'down' in t)
    
    if (get and plan and(not inn) and(not out) )or( not get and plan and(not inn) and(not out) ) :
        del TIME_DIC[ti]
        sendWord('jumpjet',0.05)
#    elif( not get and plan and(not inn) and(not out) ):
#        del TIME_DIC[ti]
#        sendWord('jumpjet',0.05)
    elif( (inn) and (car or plan) ) or((out ) and (car or plan)) or( inn or out or car) :
        del TIME_DIC[ti]
        tapKey('f',0.09)
#    elif (out ) and (car or plan) :2
#        del TIME_DIC[ti]
#        tapKey('f',0.09)
#    elif inn or out or car:
#        del TIME_DIC[ti]
#        tapKey('f',0.09)
    elif flash:
        del TIME_DIC[ti]
        rkey('rctrl')
        time.sleep(0.09)
        pkey('rctrl')
    elif lock:
        del TIME_DIC[ti]
        rkey('lalt')
        time.sleep(0.09)
        pkey('lalt')
    elif fire:
        del TIME_DIC[ti]
        tapKey('n0',0.09)
    elif wheel:
        del TIME_DIC[ti]
        tapKey('upWheel',0.09)
    elif radio:
        del TIME_DIC[ti]
        tapKey('r',0.09)
    else:
        print '%.2f'%(time.time()-ti),'[%s]'%name,'[Faile]:',t
        return
    
    print '[%s]'%name,'%.2f'%(time.time()-ti),t

PUSED_LIST = None
from geo import degreeOfVictor,fitPointsToPlane
def fly(player):
    rsp = getSkeletonPositions(player)
    sp = rsp[:,:3]
    spineVector = (sp[jo.shoulderCenter] - sp[jo.spine])
    shoulderVector = sp[jo.shoulderRight] - sp[jo.shoulderLeft]
    
    elbowWristLeft = sp[jo.wristLeft] - sp[jo.elbowLeft]
    elbowWristRight = sp[jo.wristRight] - sp[jo.elbowRight]
    
    #A/D
    elbowVector = sp[jo.elbowRight] - sp[jo.elbowLeft]
    AD = 90-degreeOfVictor(elbowVector,(0,1,0))
    adTre = 15
    
    #W
    shoulderElhowLeft = sp[jo.elbowLeft]-sp[jo.shoulderLeft]
    shoulderElhowRight = sp[jo.elbowRight]-sp[jo.shoulderRight]
    W = degreeOfVictor(shoulderElhowLeft,shoulderElhowRight)
    wTre = 100
    
    #S
    hipKneeRight = sp[jo.kneeRight]-sp[jo.hipRight]
    hipKneeLeft = sp[jo.kneeLeft]-sp[jo.hipLeft]
    Sleft = 90-degreeOfVictor(hipKneeLeft,(0,0,-1))
    Sright = 90-degreeOfVictor(hipKneeRight,(0,0,-1))
    S = (Sleft+Sright)/2
    sThre = 8
    
    #Q/E
    QE = 90-degreeOfVictor(shoulderVector,(0,0,1))
    qeThre = 15
    
    #n8/n2
    n82 = 90-degreeOfVictor(elbowWristLeft,shoulderVector),90-degreeOfVictor(elbowWristRight,shoulderVector)
    n82 += (n82[0]-n82[1],)
    n8Thre = -30
    n2Thre = 40
    
    #up/down
    updown = (90-degreeOfVictor(elbowWristLeft,spineVector),
              90-degreeOfVictor(elbowWristRight,spineVector))
    updown += (sum(updown)/2,)
    upThre = 10
    downThre = -30
    
    #n4/n6
    n46 = n82[:2]
#    print '%.2f, %.2f, %.2f,'% n82
    n46Thre = 20
    n4 = n46[0] < -n46Thre and n46[1] < -n46Thre 
    n6 = n46[0] > n46Thre and n46[1] > n46Thre 
    
    #F/wheel
    Fwheel = updown[0] - updown[1]
#    print '%.2f, %.2f, %.2f,'% updown
#    print Fwheel
    fWheelThre = 100
    F = Fwheel > fWheelThre
    wheel = Fwheel < - fWheelThre
    #fire
#    points = [tuple(p) for p in (sp[jo.shoulderCenter],sp[jo.spine],sp[jo.shoulderLeft], sp[jo.shoulderRight])]
#    bodyPlane = fitPointsToPlane(points)
#    bodyz = bodyPlane.normal_vector.args
    bodyz = np.cross(spineVector,elbowVector)
    fires = 90-degreeOfVictor(bodyz,shoulderElhowLeft),90-degreeOfVictor(bodyz,shoulderElhowRight)
    n0 = sum(fires)/2
    n0Thre = 35
    #switchOff
    playerz = sp[-1,-1]
    qeIn = -80<QE<80
    bxIn = -0.4<sp[-1][0]<0.4
    byIn = -0.4<sp[-1][1]<0.4
    bzIn =  1.4<sp[-1][2]<2.7
    handDown = max(sp[jo.handLeft][1],sp[jo.handRight][1])<sp[jo.head][1]
    handsDistan = sp[jo.handRight][0]-sp[jo.handLeft][0] > 0.1
    swichOn = bxIn and byIn and bzIn and qeIn and handDown and handsDistan
#    print 'body= %.2f,  %.2f,  %.2f, '%tuple(sp[-1])

    kvs = {
     'a':AD>adTre,
     'd':AD<-adTre,
     'w':W>wTre,
     's':Sleft>sThre and Sright>sThre,
     'q':QE<-qeThre,
     'e':QE>qeThre,
     'n8':n82[-1] < n8Thre,
     'n2':n82[-1] > n2Thre,
     'n0':n0>n0Thre,
     'up':updown[0]<downThre and updown[1]<downThre,
     'down':updown[0]>upThre and updown[1]>upThre,
     'n4':n4,
     'n6':n6,
     
     'upWheel':wheel,
     'f':F,
#     'rctrl':0,
     }
    
    if 'GTA: San Andreas' in getWindowName() :
        changeDic={
                'up':'i',
                'down':'k',
                'n8':'o',
                'n2':'l',
                }
                
        kvsToGame = {(changeDic[k] if k in changeDic else k):v for k,v in kvs.items()}
        if not swichOn:
            kvsToGame = {k:False for k in kvsToGame}
        doKeys(kvsToGame)
    
    ks = [k for k,v in kvs.items() if v]
    strr = ', '.join(ks)
    global PUSED_LIST
    if strr != PUSED_LIST:
        PUSED_LIST = strr
        print '[%s]'%strr if strr else "NULL"
    return 
    print '''switchOff = %.2f, 
    A/D = %.2f
    W = %.2f
    up/down:left = %.2f,right = %.2f,mean = %.2f,
    n8/n2:left = %.2f,right = %.2f,sub = %.2f,
    Q/E = %.2f
    n0 = %.2f
    S = %.2f
    swichOn = %s
    '''%(playerz,AD,W,
    updown[0],updown[1],updown[2],
    n82[0],n82[1],n82[2],
    QE,n0,S,str(swichOn))
    
swich = 0
#swich = 3
#swich = 4
if swich == 4:
    speech = Listen(handleAudio)
    speech.start() # 
    setTimeOut(lambda :speech.stop(),50)
if swich == 3:
#%%
    jointsList = [jo.elbowRight,jo.elbowLeft]
    jointsList = [jo.kneeLeft,jo.kneeRight]
    jointsList = [jo.handLeft,jo.handRight,jo.elbowLeft,jo.elbowRight,jo.hipLeft,jo.hipRight]
    saveList = load_data('fly2')
    #saveList = [saveList[1]]
    for save in  saveList:
        video,depth,player=(save)
        show(video)
#        showPlayerDepthVideo(video, depth, player)
#        printPlayerInfo(player,jointsList)
        fly(player)
        sp = getSkeletonPositions(player)
        
#        io.imsave('img/%s.jpg'%PUSED_LIST,video)
#        print PUSED_LIST
    #printHandsForDriver
    
    video,depth,player= saveList[0]


#%%
#if __name__ == '__main__2':
if swich == 0:
    speech = Listen(handleAudio,3)
    speech.start()
    full_screen = False
    draw_skeleton = True
    video_display = True

    screen_lock = thread.allocate()

    gameTool.screen = pygame.display.set_mode(VIDEO_WINSIZE if video_display else DEPTH_WINSIZE,0,16)    
    pygame.display.set_caption('Python Kinect GTA')
    skeletons = None
    gameTool.screen.fill(THECOLORS["black"])
    try:
        kinect = nui.Runtime()
        
        kinect.skeleton_engine.enabled = True
        def post_frame(frame):
            action(frame)
            try:
                g[2]=frame
                pygame.event.post(pygame.event.Event(KINECTEVENT, skeletons = frame.SkeletonData))
            except:
                # event queue fullffjumpjet2
                pass
    
        kinect.skeleton_frame_ready += post_frame
        
        kinect.depth_frame_ready += depth_frame_ready    
        kinect.video_frame_ready += video_frame_ready    
        
        kinect.video_stream.open(nui.ImageStreamType.Video, 2, nui.ImageResolution.Resolution640x480, nui.ImageType.Color)
        kinect.depth_stream.open(nui.ImageStreamType.Depth, 2, nuiResolution, nui.ImageType.Depth)

    except Exception as e:
        print 'Error!!!!!!\n',e
        pygame.quit()
    print('Controls: ')
    print('     d - Switch to depth view')
    print('     v - Switch to video view')
    print('     s - Toggle displaing of the skeleton')
    print('     u - Increase elevation angle')
    print('     j - Decrease elevation angle')

    # main game loop
    done = False
#    8/0
    try:
        while not done:
            e = pygame.event.wait()
            gameTool.dispInfo = pygame.display.Info()
            if e.type == pygame.QUIT:
                done = True
                break
            elif e.type == KINECTEVENT:
                skeletons = e.skeletons
    #            skeletons = 1
                if draw_skeleton:
                    draw_skeletons(skeletons)
                    pygame.display.update()
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    done = True
                    break
                elif e.key == K_d:
                    with screen_lock:
                        gameTool.screen = pygame.display.set_mode(DEPTH_WINSIZE,0,16)
                        video_display = False
                elif e.key == K_v:
                    with screen_lock:
                        gameTool.screen = pygame.display.set_mode(VIDEO_WINSIZE,0,32)    
                        video_display = True
                elif e.key == K_s:
                    draw_skeleton = not draw_skeleton
                elif e.key == K_u:
                    kinect.camera.elevation_angle = kinect.camera.elevation_angle + 2
                elif e.key == K_j:
                    kinect.camera.elevation_angle = kinect.camera.elevation_angle - 2
                elif e.key == K_x:
                    kinect.camera.elevation_angle = 2
                elif e.key in (K_a, MOUSEBUTTONUP,K_F1):
                    saveAll()
        pygame.quit()
        kinect.close()
        speech.stop()
    except KeyboardInterrupt:
        print e
        pygame.quit()
        kinect.close()
        speech.stop()
#%%
    rgb = g[0]
    player = g[3]
    depthr = g[1]
    depth = cv2.resize(depthr,VIDEO_WINSIZE)
    sp = getSkeletonPositions(player) if g[3] else 0
#    save_data(g)
#%%
#show(depth,rgb)
#de = greyToRgb(depth)
#showSpInImg(player,normalizing(de))
#depth = cv2.resize(gameTool.DEPTH,VIDEO_WINSIZE)
#body = onlyShowBody(player,depth,rgb,0.3)
#show(body)
#%%
#if __name__ == '__main__':
if swich == 1:
    kinect = nui.Runtime()
    cam = nui.Camera(kinect)
    print cam.get_elevation_angle()
    ske = nui.SkeletonEngine(kinect)
    dv = ske.get_next_frame()





