import numpy as np
import cv2
from tkinter import filedialog
import tkinter as tk
from tkinter import messagebox
root = tk.Tk()
root.withdraw()
messagebox.showinfo("提示", "按下空格键为你抓拍画面，按下Esc或q键结束监控！\n选择数据保存文件夹路径，否则默认为当前文件夹!")
filepath = filedialog.askdirectory()  # 获得选择好的文件夹
if filepath:
    filepath=filepath+'/'
##选择摄像头
videoLeftUp = cv2.VideoCapture('rtsp://admin:admin@192.168.2.177:8554/live')
width = (int(videoLeftUp.get(cv2.CAP_PROP_FRAME_WIDTH)))
height = (int(videoLeftUp.get(cv2.CAP_PROP_FRAME_HEIGHT)))
num=0

if videoLeftUp.isOpened():
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    # 第三个参数则是镜头快慢的，10为正常，小于10为慢镜头
    #out = cv2.VideoWriter(filepath + '监控.avi', fourcc, 10, (width*2, height))
    out = cv2.VideoWriter(filepath + '监控1.avi', fourcc, 10, (width, height))
    while 1:
        retLeftUp, frameLeftUp = videoLeftUp.read()
        frameLeftUp = cv2.resize(frameLeftUp, (int(width), int(height)), interpolation=cv2.INTER_CUBIC)
        if retLeftUp:
            #frameUp = np.hstack((frameLeftUp, frameRightUp))
            '''
            flip(src_img,des_img,1);//1代表水平方向旋转180度
            //flip(src_img,des_img,0);//0代表垂直方向旋转180度
            //flip(src_img,des_img,-1);//-1代表垂直和水平方向同时旋转
            '''
            #a = out.write(frameUp)
            #frameUp = np.hstack((frameLeftUp, frameRightUp))
            b=out.write(frameLeftUp)
            cv2.imshow("frame", frameLeftUp)
            key = cv2.waitKey(10)
            if key == 27 or key == ord('q'):
                # esc键退出
                print("esc break...")
                break

            elif key == ord('1') or key == ord(' '):
                # 保存一张图像
                num = num + 1
                filename = "抓拍%s.png" % num
                # cv2.imwrite(filepath+filename, frame)
                cv2.imencode('.png', frameLeftUp)[1].tofile(filepath + filename)
        else:
            messagebox.showinfo("提示", "video.read操作失败")
            break
else:
    messagebox.showinfo("提示", "cv2.VideoCapture操作失败")

videoLeftUp.release()
'''
#上下拼接
frameUp = np.hstack((frameLeftUp, frameRightUp))
frameDown = np.hstack((frameLeftDown, frameRightDown))
frame = np.vstack((frameUp, frameDown))
'''