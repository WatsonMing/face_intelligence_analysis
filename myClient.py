# -*- coding:UTF-8 -*-
from aip import AipFace
import base64
"""我的秘钥和授权码"""
APP_ID = ''
API_KEY = ''
SECRET_KEY = ''
"""创建新的客户端"""
client = AipFace(APP_ID, API_KEY, SECRET_KEY)
"""          参数设置          """
"""接收参数"""
options = {}
options["face_field"] = "age,gender"
options["face_type"] = "LIVE"
options["max_face_num"] = "10"
'''图片格式'''
imageType = "BASE64"
'''
def getYesterday():
    import datetime
    today=datetime.date.today() 
    oneday=datetime.timedelta(days=1) 
    yesterday=str(today-oneday)  
    return yesterday
# 遍历出结果 返回文件的名字
def readAllImage():
    import os
    try:
        path='/home/pi/face/image/'+getYesterday()
        s = os.listdir(path)
        resultArray = []
        fileName = os.path.basename(path)
        for i in s:
            document = os.path.join(path, i)
            resultArray.append(document)
    except IOError:
        print ("Error")
    else:
        print ("读取成功")
        return resultArray
def ergodicImageToSever():
    pathArray=readAllImage()
    for image in pathArray:
        print(image)
        bdFaceApi(image)
''' 
def bdFaceApi(filePath):
    with open(filePath,"rb") as f:
        """b64encode"""
        base64_data = base64.b64encode(f.read())
    image = str(base64_data)
    """ 调用人脸检测 """
    result = client.detect(image, imageType,options)
    faceResult=result['result']
    print(faceResult)
    #faceList=result['face_list']
    man=str(faceResult).count('male')
    women=str(faceResult).count('female')
    peopleCount=faceResult['face_num']
    print(peopleCount)
    print(man)
    print(women)
    return man,women
    
bdFaceApi('/home/pi/face/test.JPEG')
#readAllImage()
#ergodicImageToSever()
