# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os

from logTool import log, ignoreWarning, LogException

def openread(path):
    '''
    返回path文件的文本内容
    '''
    with open(path,'r') as f:
        strr = f.read()
    return strr
def openwrite(strr,path,mode='w'):
    '''
    将strr写入path
    '''
    with open(path,mode) as f:
        f.write(strr)
    return path

def crun(pycode):
    '''测试代码pycode的性能'''
    from cProfile import run
    return run(pycode,sort='time')
def frun(pyFileName=None):
    '''在spyder中 测试pyFileName的性能'''
    if pyFileName:
        if '.py' not in pyFileName:
            pyFileName += '.py'
        crun("runfile('%s',wdir='.')"%pyFileName)
    else:
        crun("runfile(__file__,wdir='.')")
        

#==============================================================================
#%% 保存二进制数据
#==============================================================================

def save_data(data, name='Python_pickle'):  #保存进度
    '''
    保存二进制数据
    '''
    import pickle
    name = name
    f = open(name, "wb")
    print '正在将数据写入',os.path.abspath('.'),'下的文件:“'+name+'”，请稍等。。。'
    pickle.dump(data,f)
    f.close()
    print '\n文件“'+name+'”已保存在',os.path.abspath('.'),'目录下!'

def load_data(name='Python_pickle'):  #载入数据
    import pickle
    name = name
    if not os.path.isfile(name):
        print '在',os.path.abspath('.'),'目录下,“'+name+'”文件不存在，操作失败！'
        return
    print '正在读取',os.path.abspath('.'),'目录下的文件:“'+name+'”\n请稍等。。。'
    f = open(name,"rb")
    data = pickle.load(f)
    f.close()
    print '文件:“'+name+'”读取成功！'
    return data

#==============================================================================
# 动态规划 装饰器
#==============================================================================

 
def memo(func):
    '''
    动态规划 装饰器
    '''
    cache={}
    from functools import wraps
    @wraps(func)
    def wrap(*args):
        if args not in cache:
            cache[args]=func(*args)
        return cache[args]
    return wrap

def importAllFunCode(mod):
    '''
    mod 为包名(type(mod)=='str')或包本身(type(mod)==module)
    自动生成导入所有模块语句 并过滤掉__name__等
    '''
    if isinstance(mod,(str,unicode)):
        exec ('import %s as mod'%mod)

    names = [name for name in dir(mod) if not ((len(name)>2 and name[:2]=='__') or 
                                  name in ['unicode_literals',])]
    n = 5
    lines = []
    while len(names) > n:
        l,names = names[:n],names[n:]
        lines += [', '.join(l)]
    lines += [', '.join(names)]
    lines = ',\n          '.join(lines)
    
    strr = (("from %s import *\nfrom %s import (%s)"%(mod.__name__,mod.__name__,lines)))
    print strr
    
#==============================================================================
# time
#==============================================================================

def localTimeStr():
    '''
    获得本地时间(GM+8 北京时间)
    '''
    import time
    return time.asctime( time.localtime(time.time()))
def gmtTimeStr():
    '''
    获得gmt时间(GM0 格林威治时间)
    '''
    import time
    return time.asctime(time.gmtime(time.time()))
    
def dicToObj(dic):  
    '''
    将 dict 转换为易于调用的 Object
    '''
    top = type(u'MyObject'.encode('utf-8'), (object,), dic)  
    seqs = tuple, list, set, frozenset  
    for i, j in dic.items():  
        if isinstance(j, dict):  
            setattr(top, i, dicToObj(j))  
        elif isinstance(j, seqs):  
            setattr(top, i,   
                type(j)(dicToObj(sj) if isinstance(sj, dict) else sj for sj in j))  
        else:  
            setattr(top, i, j)  
    return top  

def setTimeOut(fun, t):
    '''
    same to setTimeOut in JavaScript
    '''
    from threading import Timer
    thread = Timer(t,fun)
    thread.start()
    return thread

def setInterval(fun, inter, maxTimes=None):
    '''
    same to setInterval in JavaScript
    '''
    maxTimes = [maxTimes]
    def interFun(): 
        fun()
        if maxTimes[0] is not None:
            maxTimes[0] -= 1
            if maxTimes[0] <= 0:
                return 
        setTimeOut(interFun, inter)
    interFun()
    
if __name__ == "__main__":
    def fun():
        for i in range(10):
            print i
            time.sleep(1)
    from threading import Timer
    thread = Timer(0,fun)
    thread.start()
    pass