# -*- coding: utf-8 -*-
"""
Created on Sun May 16 20:01:45 2021

@author: user
"""

import cv2

def get_thermal_cam():
    
    thermal_cam = cv2.VideoCapture( 1 )

    ret, img = thermal_cam.read
    
    return ret, thermal_cam

def self_test():
    
    ret, thermal_cam = get_thermal_cam()
    
    while( ret ):
        
        ret, img = thermal_cam.read()
        cv2.imshow( 'thermal self-test', img )
        
        if cv2.waitKey( 1 ) & 0xFF == ord('q'):
            print('break loop')
            break
        
    
    return 
        


if __name__ == '__main__':
    self_test()