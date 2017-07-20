# -*- coding: utf-8 -*-

import speech_recognition as sr

r = sr.Recognizer()
# recognize speech using Sphinx
def sphinx(audio):
    try:
#        raise sr.RequestError
        return r.recognize_sphinx(audio)
    except sr.UnknownValueError:
#        print("Sphinx could not understand audio")
        return "not understand audio"
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))
    
def google(audio):    
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        re = r.recognize_google(audio)
#        print("Google:" + re)
        return re
    except sr.UnknownValueError:
#        print("Google Speech Recognition could not understand audio")
        return "NO" and None
    except sr.RequestError as e:
#        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return 'OFF' and None
        pass
    
# recognize speech using Microsoft Bing Voice Recognition
def bing(audio):
    BING_KEY = "b024f6dc6a274b9890ae217a4c8dd2a5"  # Microsoft Bing Voice Recognition API keys 32-character lowercase hexadecimal strings
    try:
         return r.recognize_bing(audio, key=BING_KEY)
#        print("Microsoft Bing:" + r.recognize_bing(audio, key=BING_KEY))
    except sr.UnknownValueError:
#        print("Microsoft Bing Voice Recognition could not understand audio")
        return "NO" and None
    except sr.RequestError as e:
#        print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))
        return 'OFF' and None
def baidu(audio):
    wav = audio.get_wav_data()
    resoult = aipSpeech.asr(wav, 'wav', audio.sample_rate, {
    'lan': 'en',
    })
    if 'err_no' in resoult and not resoult['err_no']:
        return ''.join(resoult['result']).replace(',','')

import time
#crun('sphinx(audio)')
#crun('google(audio)')
#crun('bing(audio)')
from yl.tool import crun,setTimeOut

class Listen():
    def __init__(self, handelAudio,timeLimit=2.3,sample_rate=16000):
        self.fun = handelAudio
        self.timeLimit = timeLimit
        self.sample_rate = sample_rate
    def start(self):
        self.listening = True
        setTimeOut(self.listen,0)
    def listen(self):
        r = sr.Recognizer()
        with sr.Microphone(sample_rate=self.sample_rate) as source:
            print 'voice input device name:',source.audio.get_default_input_device_info()['name']#.decode('gbk')
            while self.listening:
                audio = r.listen(source,phrase_time_limit=self.timeLimit)
                self.audio = audio
                self.fun(audio)
    def stop(self):
        self.listening = False
'''
%time google(audio)
%time bing(audio)
%time sphinx(audio)
'''
# 引入Speech SDK
from aip import AipSpeech

# 定义常量
APP_ID = '9909572'
API_KEY = 'CsclCxNTDWjZur0R7Zl1tHS4'
SECRET_KEY = 'RIFIeFsDsN7RlGYo2rkiRpYyztuULlfi'

# 初始化AipSpeech对象
aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

if __name__ == '__main__':
    r = sr.Recognizer()
    with sr.Microphone(device_index= 0,sample_rate=8000) as source:
        print 'voice input device name:',source.audio.get_default_input_device_info()['name']#.decode('gbk')
#        audio = r.listen(source,phrase_time_limit=3)

#    handleAudio(audio)

    speech = Listen(handleAudio)
    speech.start()
    setTimeOut(lambda :speech.stop(),50)
#    sphinx(audio) 
#    print 'bing',bing(audio)
#    print 'google',google(audio)