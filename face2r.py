import cv2

# Videoサイズ
frameWidth = 640
frameHeight = 480

#学習データの取得
cascade_path = './haarcascades/haarcascade_frontalface_alt.xml'
cascade = cv2.CascadeClassifier(cascade_path)

#カメラからの入力
cap = cv2.VideoCapture(0)
fps = int(cap.get(cv2.CAP_PROP_FPS)) #動画のFPSを取得

while True:

    ret, img = cap.read()       #画像の読み込み
    img = cv2.resize(img, (frameWidth, frameHeight))    #画像サイズを変更
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    #画像のグレースケール化

    
    # 白黒に変換
    ret, thresh = cv2.threshold(img_gray,120, 255, cv2.THRESH_BINARY_INV)
    # 輪郭検出
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, contours, -1, (0, 0, 255), 1)

    face_list = cascade.detectMultiScale(img_gray, minSize = (20, 20))  #顔検出の最小サイズ設定  

    
    #顔の検出
    if len(face_list):
        for (x,y,w,h) in face_list:
            # 顔が見つかった場合赤い四角で囲う
            cv2.rectangle(img, (x,y), (x+w, y+h), (0, 0, 255), thickness=2)
    
    img_flip_lr = cv2.flip(img,1)       #動画を左右反転
    cv2.imshow('Video', img_flip_lr)    #動画を出力
    print('ret=',ret)
    print('fps=',fps)    

    # qを押すと止まる。
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()