#!/usr/bin/env python3
#-*- coding: utf-8 -*

import cv2
import numpy as np
import rospy
import sys
from sensor_msgs.msg import Image
from cv_bridge import CvBridge,CvBridgeError
import mimi_color


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
            self.h,self.s,self.v = hsvclor[y,x,:]
            hsv_str = '(H,S,V)=(' + str(self.h) + ',' + str(self.s) +','+ str(self.v) + ')'
            #cv2.putText(img,hsv_str,(30,50),cv2.FONT_HERSHEY_PLAIN,2,(0,0,0),2,cv2.LINE_AA)
            print(hsv_str)
            self.ps = 100 / 255 * self.s
            self.pv = 100 / 255 * self.v
            dcolor = mimi_color.DetectColor()
            color = dcolor.detectColor(hsvclor[y,x,:])
            #color = self.detectBWG()
            print(color)
        cv2.imshow('viewHSV',img)

    def putColor(self):
        if self.h < 5 or 170 < self.h:
            if self.pv < 40:
                color = 'brown'
            else:
                color = 'red'
        elif self.h < 20:
            if self.pv < 45:
                color = 'brown'
            else:
                color = 'orange'
        elif self.h < 30:
            if self.pv < 50:
                color = 'brown'
            else:
                color = 'yellow'
        elif self.h < 40:
            color = 'yellow green'
        elif self.h < 50:
            color = 'green'
        elif self.h < 80:
            if self.pv < 30:
                color = 'green'
            else:
                color = 'blue green'
        elif self.h < 100:
            if self.pv < 20:
                color = 'green'
            else:
                color = 'light blue'
        elif self.h < 130:
            color = 'blue'
        elif self.h < 140:
            color = 'purple'
        else:
            if self.h < 160 and self.pv < 30:
                color = 'purple'
            else: 
                color = 'pink'
        return color

    def detectBWG(self):
        B = 'black'
        W = 'white'
        G = 'gray'
        print('ps:{},pv:{}'.format(self.ps,self.pv))

        if self.ps <  5:
            color = self.if3Color(15,B,60,G,W)
        elif self.ps < 10:
            color = self.if3Color(20,B,65,G,W)
        elif self.ps < 20:
            color = self.if3Color(15,B,20,G,self.putColor())
        elif self.ps < 60:
            color = self.if3Color(20,B,25,G,self.putColor())
        else:
            color = self.putColor()

        return color

    def if3Color(self,pv_range1,color1,pv_range2,color2,color3):
        if self.pv  < pv_range1:
            color = color1
        elif self.pv < pv_range2:
            color = color2
        else:
            color = color3
        return color
    

if __name__ == '__main__':
    try:
        rospy.init_node("view_hsv_color",anonymous=True)
        ViewColor()
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
        cv2.destroyWindow('viewHSV')
