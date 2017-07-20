# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os

def log(x):
    print x
    return x
def ignoreWarning():
    from warnings import filterwarnings
    filterwarnings('ignore')

class LogException():
    '''
    用于扑捉和记录函数中的异常错误
    usage:
        loge = LogException(logFilePath,otherFun) # 先实例一个对象
        loge.listen(f,*l,**args) # 用 .listen 运行函数
        @loge.decorator  # 装饰被监听函数
    '''
    def __init__(self,
                 logFilePath=None, 
                 otherFun=None,
                 printOnCmd=True, 
                 logBegin=False,
                 localTime=False):
        '''logFilePath  log文件保存路径,为False时 不写入文件
        otherFun  一个返回字符串的函数，每次错误运行一次，结果写入log
        printOnCmd   时候在屏幕上打印
        logBegin     是否记录开始监听事件
        localTime    是否为当地时间 默认为GMT时间
        '''
        
        self.splitLine = '/*----------*/'
        self.path = logFilePath
        self.fun = otherFun if otherFun else lambda :''
        self.printt = printOnCmd
        self.localTime = localTime
        self.format = (
'''     Index :{index}, {time}
{timeClass} :{timeStr}
 Exception :{exceptionName}
   Message :{message}
      Args :{args}
{otherInfo}
{splitLine}
''')
        self.index = 0
        if logFilePath:
            if os.path.isfile(logFilePath):
                with open(self.path,'r') as f:     
                    strr = f.read()
                self.index = strr.count(self.splitLine)
        if logBegin:
            class beginLogException(Exception):
                pass
            def f ():
                raise beginLogException,'LogException is begin to log Exception!'
            self.listen(f)
        
    def listen(self,f,*l,**args):
        '''
        f        : 监听函数
        *l,**args: 函数f的参数
        '''
        import time
        try:
            f(*l,**args)
        except Exception as e:
            exceptionName = str(type(e))
            exceptionName = exceptionName[exceptionName.index('.')+1:-2]
            
            timeClass = 'Local time' if self.localTime else '  GMT time'
            t = time.asctime( time.localtime(time.time())) if self.localTime  else time.asctime(time.gmtime(time.time()))
            
            otherInfo = self.fun()
            
            erroStr = self.format.format(
                                         index=self.index,
                                         timeStr=t,
                                         timeClass=timeClass,
                                         time=time.time(),
                                         exceptionName=exceptionName,
                                         message=e.message,
                                         args=str(e.args),
                                         otherInfo=otherInfo,
                                         splitLine=self.splitLine,
                                         )
            self.__writeLog(erroStr)
            self.index += 1
            self.last = self.e = e

    def __writeLog(self,strr):
        '''
        判断是否打印和写入
        '''
        if self.printt:
            print strr
        if self.path:
            with open(self.path,'a') as f:     
                f.write(strr)
    def decorator(self,f):
        '''
        函数装饰器封装
        '''
        def ff(*l,**arg):
            r = self.listen(f,*l,**arg)
            return r
        return ff
#    l= LogException('a.txt',logBegin=1)
#    l.listen(lambda :9/0,)
if __name__ == "__main__":

    pass