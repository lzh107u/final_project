# -*- coding: utf-8 -*-
"""
Created on Tue May 18 17:40:23 2021

@author: user
"""

import cv2

def get_origCam():
    
    cap = cv2.VideoCapture( 0 )
    
    if cap.isOpened():
        ret = 1
        print('camera opened successfully -- ORIG')
    else:
        ret = 0
        print("Unable to open camera")
    
    return ret, cap

def close_origCam( cap ):
    
    cap.release()
    
    return 

def self_test():
    
    ret, cap = get_origCam()
    
    ret, img = cap.read()
    cv2.namedWindow('self_test( orig )', cv2.WINDOW_NORMAL )
    while( ret == 1 ):
        
        ret, img = cap.read()
        cv2.imshow( 'self_test( orig )', img )
        
        if cv2.waitKey( 1 ) & 0xFF == ord('q'):
            print('break out')
            break
    
    cv2.destroyAllWindows()
    close_origCam( cap )
    
    return

if __name__ == "__main__":
    self_test()