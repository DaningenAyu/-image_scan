#!/usr/bin/env python3
#-*- coding: utf-8 -*

#モジュールのimport
import cv2
from cv_bridge import CvBridge,CvBridgeError
from sensor_msgs.msg import Image
import rospy
import numpy as np
from mimi_motion_detection.srv import depth_meter


class Show_realsense():
    #初期設定
    def __init__(self):
        rospy.init_node('depsMaskImage',anonymous=True)#ノードを立てる
        self.bridge = CvBridge()
        #Realsenseのカラー画像の情報取得(topicを取得)
        rospy.Subscriber('/camera/color/depth_mask',Image,self.img_listener)
        rospy.wait_for_service("depth_mask")
        self.control_depth_mask = rospy.ServiceProxy("depth_mask",depth_meter)
        self.flg = 0

    #カラー画像を処理
    def img_listener(self,data):
        try:
            #topicで送られてきたROS_Image型の画像をOpenCVで扱える型に変換
            self.color_data = self.bridge.imgmsg_to_cv2(data,"bgr8")
            self.show()
        except CvBridgeError as e:
            print(e)
        
    #画像を表示させる
    def show(self):
        cv2.imshow('View_lis',self.color_data)
        k = cv2.waitKey(1)
        if k == 13:
            if self.flg == 0:
                self.control_depth_mask(1.5)
                self.flg = 1
            else: 
                self.control_depth_mask(2.5)
                self.flg = 0

#main文
if __name__ == '__main__':
    try:
        Show_realsense()    #classを呼び出す
        rospy.spin()    #処理を継続させる
    except rospy.ROSInitException:
        print('Shutting down')
        cv2.destroyAllWindows()
