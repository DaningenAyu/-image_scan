#!/usr/bin/env python3
#-*- coding: utf-8 -*

class DetectColor():  
    def detectColor(self,hsv_bit_image):
        B = 'black'
        W = 'white'
        G = 'gray'
        self.h,s,v = hsv_bit_image
        self.ps = 100 / 255 * s
        self.pv = 100 / 255 * v
        print('ps:{},pv:{}'.format(self.ps,self.pv))

        if self.ps <  5:
            color = self.if3Color(15,B,60,G,W)
        elif self.ps < 10:
            color = self.if3Color(20,B,65,G,W)
        elif self.ps < 20:
            color = self.if3Color(12,B,20,G,self.putColor())
        elif self.ps < 30:
            color = self.if2Color(11,B,self.putColor())
        elif self.ps < 40:
            color = self.if2Color(10,B,self.putColor())
        elif self.ps < 50:
            color = self.if2Color(9,B,self.putColor())
        elif self.ps < 60:
            color = self.if2Color(8,B,self.putColor())
        else:
            color = self.putColor()

        return color    
     
    def putColor(self):
        if self.h < 5 or 170 < self.h:
            if self.pv < 40:    color = 'brown'
            else:   color = 'red'
        elif self.h < 20:
            if self.pv < 45:    color = 'brown'
            else:   color = 'orange'
        elif self.h < 30:
            if self.pv < 50:    color = 'brown'
            else:   color = 'yellow'
        elif self.h < 40:
            color = 'yellow green'
        elif self.h < 50:
            color = 'green'
        elif self.h < 80:
            if self.pv < 30:    color = 'green'
            else:   color = 'blue green'
        elif self.h < 100:
            if self.pv < 20:    color = 'green'
            else:   color = 'light blue'
        elif self.h < 130:  
            color = 'blue'
        elif self.h < 140:  
            color = 'purple'
        else:   
            color = 'pink'

        return color
    

    def if2Color(self,pv_range1,color1,color2):
        if self.pv < pv_range1:
            color = color1
        else:
            color = color2
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
    dcolor = DetectColor()
    color = dcolor.detectColor()
    print(color)
