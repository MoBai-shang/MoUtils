import cv2

cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
# fps = cap.get(cv2.CAP_PROP_FPS)
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
out = cv2.VideoWriter('camera_test.avi', fourcc,10.0, size)
while True:
    ret, frame = cap.read()
    # 横向翻转
    frame = cv2.flip(frame, 1)
    out.write(frame)
    # 在图像上显示 Press Q to save and quit
    cv2.putText(frame,
                "Press Q to save and quit",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                (0, 255, 0), 2)
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.imwrite("/home/pi/Desktop/takephoto6.jpg", frame)
cap.release()
out.release()
cv2.destroyAllWindows()
