# -*- coding: utf-8 -*-
"""
Created on Tue May 18 17:53:01 2021

@author: user
"""

import cv2

def get_usbCam():
    
    cap = cv2.VideoCapture( 1 )
    
    if cap.isOpened():
        ret = 1
        print('camera opened successfully -- USB')
    else:
        ret = 0
        print("Unable to open camera")
    
    return ret, cap

def close_usbCam( cap ):
    
    cap.release()
    
    return 

def self_test():
    
    ret, cap = get_usbCam()
    
    ret, img = cap.read()
    cv2.namedWindow('self_test( USB )', cv2.WINDOW_NORMAL )
    while( ret == 1 ):
        
        ret, img = cap.read()
        cv2.imshow( 'self_test( USB )', img )
        
        if cv2.waitKey( 1 ) & 0xFF == ord('q'):
            print('break out')
            break
    
    cv2.destroyAllWindows()
    close_usbCam( cap )
    
    return

if __name__ == "__main__":
    self_test()