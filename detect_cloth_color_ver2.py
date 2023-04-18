#!/usr/bin/env python3
# -*- coding: utf-8 -*

import rospy
import cv2
import collections
from std_msgs.msg import Float64
from sensor_msgs.msg import Image
from ros_openpose.msg import Frame
from cv_bridge import CvBridge, CvBridgeError
from happymimi_msgs.srv import SetStr, SetStrResponse

class DetectClothColor(object):
    def __init__(self):
        rospy.Service('/person_feature/cloth_color', SetStr, self.main)
        rospy.Subscriber('/camera/color/image_raw', Image, self.realsenseCB)
        rospy.Subscriber('/frame', Frame, self.openPoseCB)
        self.head_pub = rospy.Publisher('/servo/head', Float64, queue_size=1)

        self.image_res = Image()
        self.pose_res = Frame()

    def realsenseCB(self, res):
        self.image_res = res

    def openPoseCB(self, res):
        self.pose_res = res

    """
    def judgeColor(self, req):
        # hsv色空間で色の判定
        h, s, v = req
        #print h, s, v
        color = ''
        if 0<=v and v<=79: color = 'Black'
        if (0<=s and s<=50) and (190<=v and v<=255): color = 'White'
        elif (0<=s and s<=50) and (80<=v and v<=130): color = 'Gray'
        #elif (50 <= s and s <= 170) and (70 <= v and v <= 150): color = 'Gray'
        elif (50<=s and s<=170) and (80<=v and v<=90): color = 'Gray'
        #elif (0<=s and s<=50) and (80<=v and v<=230): color = 'Gray'
        #elif (5<=h and h<=18) and (20<=s and s<=240) and (70<=v and v<=180): color = 'Brown'
        elif (5<=h and h<=18) and v<=200: color = 'Brown'
        elif (0<=h and h<=4) or (174<=h and h<=180): color = 'Red'
        elif 100<=h and h<=110: color = 'Orange'
        elif 75<=h and h<=99: color = 'Yellow'
        elif 50<=h and h<=74: color = 'Green'
        elif 90<=h and h<=136: color = 'Blue'
        elif 137<=h and h<=159: color = 'Purple'
        elif 160<=h and h<=173: color = 'Pink'
        return color
    """

    def detectcolor(self):
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
        elif self.h < 75:
            color = 'blue green'
        elif self.h < 100:
            color = 'light blue'
        elif self.h < 130:
            color = 'blue'
        elif self.h < 140:
            color = 'purple'
        else:
            color = 'pink'
        return color
    
    def detectBWG(self,req):
        B = 'black'
        W = 'white'
        G = 'gray'

        self.h,self.s,self.v = req

        self.ps = 100 / 255 * self.s
        self.pv = 100 / 255 * self.v

        if self.ps <  5:
            color = self.ifColor(20,B,70,G,W)
        elif self.ps < 10:
            color = self.ifColor(20,B,80,G,W)
        elif self.ps < 20:
            color = self.ifColor(25,B,70,G,W)
        elif self.ps < 30:
            color = self.ifColor(25,B,60,G,W)
        elif self.ps < 40:
            color = self.ifColor(30,B,50,G,self.detectcolor())
        elif self.ps < 50:
            color = self.ifColor(30,B,40,G,self.detectcolor())
        elif self.ps < 60:
            if self.pv < 30:
                color = B
            else:
                color = self.detectcolor()
        else:
            color = self.detectcolor()
        
        if (self.h < 20 or 170 < self.h) and self.ps < 45 and self.pv < 45:
            color = 'brown'

        return color

    def ifColor(self,pv_range1,color1,pv_range2,color2,color3):
        if self.pv  < pv_range1:
            color = color1
        elif self.pv < pv_range2:
            color = color2
        else:
            color = color3
        return color


    def main(self, _):
        response = SetStrResponse()

        self.head_pub.publish(-20.0)
        rospy.sleep(2.5)

        pose = self.pose_res
        if len(pose.persons)==0: return response

        # neckとhipの座標から中点を得る
        neck_x = pose.persons[0].bodyParts[1].pixel.y
        neck_y = pose.persons[0].bodyParts[1].pixel.x
        hip_x = pose.persons[0].bodyParts[8].pixel.y
        hip_y = pose.persons[0].bodyParts[8].pixel.x
        r_shoulder_x = pose.persons[0].bodyParts[2].pixel.y
        r_shoulder_y = pose.persons[0].bodyParts[2].pixel.x
        l_shoulder_x = pose.persons[0].bodyParts[5].pixel.y
        l_shoulder_y = pose.persons[0].bodyParts[5].pixel.x
        print('neck: ', neck_x, neck_y)
        print('hip: ', hip_x, hip_y)
        print('r_shoulder: ', r_shoulder_x, r_shoulder_y)
        print('l_shoulder: ', l_shoulder_x, l_shoulder_y)

        if (neck_x==0.0 and neck_y==0.0) and (hip_x==0.0 and hip_y==0.0):
            return response
        elif neck_x==0.0 and neck_y==0.0:
            body_axis_x = hip_x-10
            body_axis_y = hip_y
            chest_length = 10
        else:
            body_axis_x = neck_x
            body_axis_y = neck_y
            if hip_x==0.0 and hip_y==0.0:
                chest_length = int(479 - neck_x)
            else:
                chest_length = int(hip_x - neck_x)
        if body_axis_x<0: body_axis_x=0
        if body_axis_x>479: body_axis_x=479
        if body_axis_y<0: body_axis_y=0
        if body_axis_y>639: body_axis_y=639

        if (r_shoulder_x==0.0 and r_shoulder_y==0.0) and (l_shoulder_x==0.0 and l_shoulder_y==0.0):
            pass
        elif r_shoulder_x==0.0 and r_shoulder_y==0.0:
            width = int(l_shoulder_y - body_axis_y)
        elif l_shoulder_x==0.0 and l_shoulder_y==0.0:
            width = int(body_axis_y - r_shoulder_y)
        else:
            shoulder_width = l_shoulder_y - r_shoulder_y
            width = int(shoulder_width/2)

        # 画像の変換
        image = CvBridge().imgmsg_to_cv2(self.image_res)
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        color_map = ['']
        for i in range(chest_length+1):
            x = body_axis_x + i
            #if x<0 or x>479: continue
            for j in range(-width, width):
                y = body_axis_y + j
                #if y<0 or y>639: continue
                color = self.judgeColor(hsv_image[int(x), int(y)])
                color_map.append(color)
        print(color_map)
        count_l = collections.Counter(color_map)
        response.result = count_l.most_common()[0][0]

        return response

if __name__ == '__main__':
    rospy.init_node('detect_cloth_color')
    detect_cloth_color = DetectClothColor()
    rospy.spin()
