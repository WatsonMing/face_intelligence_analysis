# -*- coding:UTF-8 -*-
from Tkinter import *
import cv2
from PIL import Image,ImageTk
import threading
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
################################################################################################
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
path="test.JPEG"
###############################################################################################
def getYesterday():
    import datetime
    today=datetime.date.today() 
    oneday=datetime.timedelta(days=1) 
    yesterday=str(today-oneday)  
    return yesterday
###############################################
def dataRead():
    from Temp_Humi import Dht11
    tempertureAndHumidity =Dht11(1)
    temperture,humidity=tempertureAndHumidity.GetResult()
    temp.set(temperture)
    humi.set(humidity)
####################################################################################
timeFlag=True
def clockTimerThread():
    global clockTimer,count
    if timeFlag:
        import time
        # 格式化成2016-03-20 11:45形式
        time=str(time.strftime("%Y-%m-%d %H:%M", time.localtime()))
        clock.set(time)
        print '当前时间为:'+time
        #dataRead()
        clockTimer=threading.Timer(10,clockTimerThread)
        clockTimer.start()
    else:
        clockTimer.cancel()
def getClockThread():
    clockTimer=threading.Timer(2,clockTimerThread)
    clockTimer.start()
    timeFlag=True
######################################################################################
def video_loop():
    success, img = camera.read()  # 从摄像头读取照片
    if success:
        flag = False
        try:
            gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray,1.3,4)
            if len(faces)>0:
                people.set(len(faces))################################人数
                flag=True
                saveimg=img
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + h, y + w), (0,0,255), 2)  # 在人脸区域画一个正方形出来
            ################################################################################################
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)#转换颜色从BGR到RGBA
            imgtk = ImageTk.PhotoImage(image=Image.fromarray(img))#将图像转换成Image对象
            panel.imgtk = imgtk
            panel.config(image=imgtk)
            ################################################################################################
            print flag
            if flag==True:
                save=cv2.cvtColor(saveimg, cv2.COLOR_BGR2RGBA) # 转换颜色从BGR到RGBA
                saveImage = Image.fromarray(save)
                print saveImage
                saveImage.save(path)

                print "开始写入"

                #cv2.imwrite(path,saveImage)
                print "写入成功"
                imageTobd()
                imageTobdThread.start()
            root.after(33, video_loop)
        except:
            root.after(33, video_loop)
def imageTobd():
    from myClient import bdFaceApi
    man,women=bdFaceApi(path)
    import os
    os.remove(path)
    print "删除成功"
    from connect import MyWSDLClient
    myWsdlClient=MyWSDLClient()
    if man!=0:
        myWsdlClient.SendSoapToServer(int(time.time()),str(int(time.time())),man,1,temp.get(),humi.get())
    if women!=0:
        myWsdlClient.SendSoapToServer(int(time.time()),str(int(time.time())),women,2,temp.get(),humi.get())
        
if __name__ == '__main__':

    camera = cv2.VideoCapture(0)    #摄像头
    root = Tk()
    root.title(u"睿逍客人流检测窗口")
    panel = Label(root)
    panel.pack(padx=10, pady=10)
    root.config(cursor="arrow")
    nowTimeLabel = Label(root,text='当前时间:').pack(padx=10)

    clock=StringVar()
    clock.set('2018-01-01 00:00:00')
    Label(root,textvariable=clock).pack(padx=10)
    
    TempLabel = Label(root,text='室内温度:').pack(padx=10)

    temp=DoubleVar()
    temp.set(0.0)
    Label(root,textvariable=temp).pack(padx=10)
    
    HumiLabel = Label(root,text='室内湿度:').pack(padx=10)

    
    humi=DoubleVar()
    humi.set(0.0)
    Label(root,textvariable=humi).pack(padx=10)
    #textvariable

    peopleLabel = Label(root, text='当前人数:').pack(padx=10)
    people=IntVar()
    people.set(0)
    Label(root,textvariable=people).pack(padx=10)
######################################################################################################
    imageTobdThread = threading.Thread(target=imageTobd, name='imageTobdThread')
    getClockThread()
    video_loop()
    root.mainloop()
    # 当一切都完成后，关闭摄像头并释放所占资源
camera.release()
cv2.destroyAllWindows()