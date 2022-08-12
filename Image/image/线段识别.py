#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# -*- coding: utf-8 -*-
 
import cv2
import numpy as np
 
#两个回调函数
def HoughLinesP(minLineLength):
    tempIamge = scr.copy()
    lines = cv2.HoughLinesP( edges, 1, np.pi/180,threshold=minLineLength,minLineLength=180,maxLineGap=40)
    i=0
    max_len = 0
    max_x1,max_x2,max_y1,max_y2=0,0,0,0
    if np.any(lines)==None:
        return scr
    for line in lines:
        # newlines1 = lines[:, 0, :]
        #print("line["+str(i)+"]=",line)
        x1,y1,x2,y2 = line[0]   #两点确定一条直线，这里就是通过遍历得到的两个点的数据 （x1,y1）(x2,y2)
        cv2.line(tempIamge,(x1,y1),(x2,y2),(0,0,255),2)     #在原图上画线
        # 转换为浮点数，计算斜率
        x1 = float(x1)
        x2 = float(x2)
        y1 = float(y1)
        y2 = float(y2)
        #print("x1=%s,x2=%s,y1=%s,y2=%s" % (x1, x2, y1, y2))
        if((x2 - x1) > max_len):
            max_len = x2 - x1
            max_x1 = x1
            max_x2 = x2
            max_y1 = y1
            max_y2 = y2
        i = i+1
    print("x1=%s,x2=%s,y1=%s,y2=%s" % (max_x1, max_x2, max_y1, max_y2))
    if max_x2 - max_x1 == 0:
        print("直线是竖直的")
        result=90
    elif max_y2 - max_y1 == 0 :
        print("直线是水平的")
        result=0
    else:
        # 计算斜率
        k = -(max_y2 - max_y1) / (max_x2 - max_x1)
        # 求反正切，再将得到的弧度转换为度
        result = np.arctan(k) * 57.29577
        print("直线倾斜角度为：" + str(result) + "度")

    cv2.imshow(window_name,tempIamge)
 
#临时变量
minLineLength = 20
 
#全局变量
# minLINELENGTH = 20
window_name = "HoughLines Demo"
 
 
#读入图片，模式为灰度图，创建窗口
scr = cv2.imread("test.jpg")
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
scr=frame
gray = cv2.cvtColor(scr,cv2.COLOR_BGR2GRAY)
img = cv2.GaussianBlur(gray,(3,3),0)
edges = cv2.Canny(img, 50, 150, apertureSize = 3)
cv2.namedWindow(window_name)
#初始化
HoughLinesP(minLineLength)
 
if cv2.waitKey(0) == 27:
    cv2.destroyAllWindows()


# In[ ]:




