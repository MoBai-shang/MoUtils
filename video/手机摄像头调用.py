import cv2
import time

if __name__ == '__main__':

    cv2.namedWindow("camera",1)
    #开启ip摄像头
    video="http://admin:admin@10.120.61.211:8081/"
    capture =cv2.VideoCapture(video)

    num = 0;
    while True:
        success,img = capture.read()
        cv2.imshow("camera",img)

    #按键处理，注意，焦点应当在摄像头窗口，不是在终端命令行窗口
        key = cv2.waitKey(10)

        if key == 27:
        #esc键退出
            print("esc break...")
            break
        if key == ord(' '):
             #保存一张图像
            num = num+1
            filename = "frames_%s.jpg" % num
            cv2.imwrite(filename,img)


    capture.release()
    cv2.destroyWindow("camera")

'''
import cv2
cv2.namedWindow("camera", 1)
# 开启ip摄像头
video = "http://admin:admin@10.120.61.211:8081/"  # 此处@后的ipv4 地址需要改为app提供的地址
cap = cv2.VideoCapture(video)
while True:
    # Start Camera, while true, camera will run

    ret, image_np = cap.read()

    # Set height and width of webcam
    height = 600
    width = 1000

    # Set camera resolution and create a break function by pressing 'q'
    cv2.imshow('object detection', cv2.resize(image_np, (width, height)))
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break
# Clean up
cap.release()
cv2.destroyAllWindows()
'''