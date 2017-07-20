# -*- coding: utf-8 -*-
g=[0]*5

import win32gui,time,win32api,win32con
getWindowName = lambda :win32gui.GetWindowText (win32gui.GetForegroundWindow()).decode('gbk')

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

def pussWhile(f,t=1):
    while 1:
        f()
        time.sleep(t)
#%%
if __name__ == '__main__':
    
    
    pass
# direct inputs
# source to this solution and code:
# http://stackoverflow.com/questions/14489013/simulate-python-keypresses-for-controlling-a-game
# http://www.gamespp.com/directx/directInputKeyboardScanCodes.html

import ctypes
import time

SendInput = ctypes.windll.user32.SendInput


W = 0x11
A = 0x1E
S = 0x1F
D = 0x20

NP_2 = 0x50
NP_4 = 0x4B
NP_6 = 0x4D
NP_8 = 0x48

keyToInt = {u"'": 40,
 u',': 51,
 u'-': 12,
 u'.': 52,
 u'/': 53,
 u'0': 11,
 u'1': 2,
 u'2': 3,
 u'3': 4,
 u'4': 5,
 u'5': 6,
 u'6': 7,
 u'7': 8,
 u'8': 9,
 u'9': 10,
 u';': 39,
 u'=': 13,
 u"Numlock_toggle,_using_'clear'_button": 69,
 u'Scroll_lock_(f15)': 70,
 u'[': 26,
 u'\\': 43,
 u']': 27,
 u'^_on_ISO_keyboards': 41,
 u'`_on_ANSI_keyboards_(ISO_key_is_overridden_in_CRDKeyboard)': 41,
 u'a': 30,
 u'b': 48,
 u'backspace': 14,
 u'c': 46,
 u'd': 32,
 u'delete': 211,
 u'down_arrow': 208,
 u'e': 18,
 u'end': 207,
 u'enter': 28,
 u'esc': 1,
 u'f': 33,
 u'f1': 59,
 u'f10': 68,
 u'f11': 87,
 u'f12': 88,
 u'f2': 60,
 u'f3': 61,
 u'f4': 62,
 u'f5': 63,
 u'f6': 64,
 u'f7': 65,
 u'f8': 66,
 u'f9': 67,
 u'g': 34,
 u'h': 35,
 u'home': 199,
 u'i': 23,
 u'insert': 210,
 u'j': 36,
 u'k': 37,
 u'l': 38,
 u'left_arrow': 203,
 u'm': 50,
 u'n': 49,
 u'nu*': 55,
 u'nu+': 78,
 u'nu-': 74,
 u'nu.': 83,
 u'nu/': 181,
 u'nu0': 82,
 u'nu1': 79,
 u'nu2': 80,
 u'nu3': 81,
 u'nu4': 75,
 u'nu5': 76,
 u'nu6': 77,
 u'nu7': 71,
 u'nu8': 72,
 u'nu9': 73,
 u'nuenter': 156,
 u'o': 24,
 u'p': 25,
 u'page_down': 209,
 u'page_up': 201,
 u'q': 16,
 u'r': 19,
 u'return': 28,
 u'right_arrow': 205,
 u's': 31,
 u'space': 57,
 u't': 20,
 u'tab': 15,
 u'u': 22,
 u'up_arrow': 200,
 u'v': 47,
 u'w': 17,
 u'x': 45,
 u'y': 21,
 u'z': 44}
intToKey = dict(zip(keyToInt.values(),keyToInt))
# C struct redefinitions 
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):
    if not isinstance(hexKeyCode,int):
        hexKeyCode = keyDic[hexKeyCode]
        
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    if not isinstance(hexKeyCode,int):
        hexKeyCode = keyDic[hexKeyCode]
        
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def getKvAndKeyDic():
    ords = range(65,90+1)
    chrk = map(chr,[i+32 for i in ords])
    
    keyDic = {
     'up':200,
     'down':208,
     'upWheel':3,
     'rctrl':0x1D,#0xE0,
     'n0':82,
     'n2':80,
     'n4':75,
     'n6':77,
     'n8':72,
     'lalt':0x38,
     }

    ks = chrk
    vs = [keyToInt[i] for i in ks]
    dic = dict(zip(ks,vs))
    keyDic.update(dic)
    import yl
    kv = yl.tool.dicToObj(keyDic)
    return  kv,keyDic

kv,keyDic = getKvAndKeyDic()
pkey = PressKey
rkey = ReleaseKey

def releaseKeys(l):
    for k in l:
        doKey(k,False)
def doKey(key,v):
    k = keyDic[key]
    if v :
        pkey(k)
    else:
        rkey(k)
def doKeys(dic,release=False):
    if release:
        releaseKeys(dic)
    for key in dic:
        doKey(key,dic[key])
        pass

def tapKey(key, t=None):
    if not isinstance(key,int):
        k = keyDic[key]
    pkey(k)
    if t:
        time.sleep(t)
    rkey(k)
def sendWord(ws, t=None):
    [tapKey(w,t) for w in ws]

#%% 
if __name__ == '__main__':
    def f():
        k = 'n4'
        ReleaseKey(k)
        PressKey(k)
        time.sleep(1)
        ReleaseKey(k)
        time.sleep(1)
    def send():
        sendWord('jumpjet',0.05)
    def lctrl():
        k = 'lalt'
        rkey(k)
        time.sleep(0.1)
        pkey(k)
    pussWhile(f,2)
#    f()n4
#    print 



