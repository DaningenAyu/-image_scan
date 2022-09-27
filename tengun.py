from calendar import c
import cv2
import numpy as np
import resource


WIDTH = 800
HEIGHT = 600
FPS = 30


cap_file = cv2.VideoCapture(2)
count = 1
cap_file.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('H','2','6','4'))
cap_file.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap_file.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
cap_file.set(cv2.CAP_PROP_FPS, FPS)



#前のフレーム
previous_frame = []



#繰り返しのためのwhile文
while True:
    print('あの一瞬（とき）は戻ってこない...',count)
    #カメラからの画像取得
    ret, frame = cap_file.read()
    
    orb = cv2.ORB_create()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    canny = cv2.Canny(gray,5,50)
    
    height = canny.shape[0]
    width = canny.shape[1]
    center = (int(width/2),int(height/2))

    angle = 0
    scale = 1.0
    trans = cv2.getRotationMatrix2D(center,angle,scale)
    image2 = cv2.warpAffine(frame,trans,(width,height))

    previous_frame.append(image2)

    img_src1 = image2
    img_src2 = previous_frame[count - 1]
    img_dst = img_src1


    keypoint1,descript1 = orb.detectAndCompute(img_src1,None) #現在のフレームの写真
    keypoint2,descript2 = orb.detectAndCompute(img_src2,None) #前のフレームの写真をゲット
    bf = cv2.BFMatcher(cv2.NORM_HAMMING,crossCheck=True)
    matches = bf.match(descript1,descript2)
    matches = sorted(matches,key=lambda x:x.distance)
    img3 = cv2.drawMatches(img_src1, keypoint1, img_src2, keypoint2, matches, img_dst, flags=2)
    
    #カメラの画像の出力
    cv2.imshow('camera' , img3)

    #繰り返し分から抜けるためのif文
    key =cv2.waitKey(10)
    if key == 27:
        break
    
    count +=1
#メモリを解放して終了するためのコマンド
cap.release()
cv2.destroyAllWindows()
