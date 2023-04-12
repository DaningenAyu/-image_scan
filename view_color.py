#!/usr/bin/env python3
#-*- coding: utf-8 -*

import cv2
import numpy as np
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge,CvBridgeError


class View_realsense_color():
    def __init__(self):
        rospy.init_node("view_hsv_color",anonymous=True)
        self.bridge = CvBridge()
        rospy.Subscriber('/camera/color/image_raw',Image,self.listener)
        cv2.namedWindow("viewHSV",cv2.WINDOW_NORMAL)
        cv2.setMouseCallback("viewHSV",self.call_mouse_pos) 
    
    def listener(self,data):
        try:
            self.cv_image = self.bridge.imgmsg_to_cv2(data,"bgr8")
            cv2.imshow("viewHSV",self.cv_image)
        except CvBridgeError as e:
            print(e)

    def call_mouse_pos(self,event,x,y,flags,params):
        print("eee")
        if event == cv2.EVENT_MOUSEMOVE:
            self.img = np.copy(self.cv_image)
            self.img = cv2.cvtColor(self.img,cv2.COLOR_BGR2HSV_FULL)
            H,S,V = self.img[y,x,:]
            hsv_str = '(H,S,V)=(' + str(H) + ',' + str(S) +','+ str(V) + ')'
            cv2.putText(self.img,hsv_str,(30,50),cv2.FONT_HERSHEY_PLAIN,2,(0,0,0),2,cv2.LINE_AA)
            print("fff")
            cv2.imshow('viewHSV',self.img)

if __name__ == '__main__':
    try:
        view = View_realsense_color()
        rospy.spin()
    except rospy.ROSInterruptException as e:
        print(e)
