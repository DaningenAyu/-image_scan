#!/usr/bin/env python3
#-*- coding: utf-8 -*

import cv2
import numpy as np
import rospy
import sys
from sensor_msgs.msg import Image
from cv_bridge import CvBridge,CvBridgeError


class ViewColor():

    def __init__(self):
        self.bridge = CvBridge()
        rospy.Subscriber('/camera/color/image_raw',Image,self.listener)
        self.flg = 0

    def listener(self,data):
        try:
            self.bridge_image = self.bridge.imgmsg_to_cv2(data,"bgr8")
            if self.flg == 0:
                cv2.imshow('viewHSV',self.bridge_image)
                cv2.waitKey(1)
            cv2.setMouseCallback('viewHSV',self.call_mouse_pos)
        except CvBridgeError as e:
            print(e)

    def call_mouse_pos(self,event,x,y,flags,params):
        img = np.copy(self.bridge_image)
        if event == cv2.EVENT_LBUTTONDBLCLK:
            hsvclor = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
            cv2.circle(img,center=(x,y),radius=5,color=(0,0,0),thickness=-1)
            h,s,v = hsvclor[y,x,:]
            hsv_str = '(H,S,V)=(' + str(h) + ',' + str(s) +','+ str(v) + ')'
            #cv2.putText(img,hsv_str,(30,50),cv2.FONT_HERSHEY_PLAIN,2,(0,0,0),2,cv2.LINE_AA)
            print(hsv_str)
        cv2.imshow('viewHSV',img)


if __name__ == '__main__':
    try:
        rospy.init_node("view_hsv_color",anonymous=True)
        ViewColor()
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
        cv2.destroyWindow('viewHSV')
