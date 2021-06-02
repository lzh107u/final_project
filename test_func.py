# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 18:44:02 2021

@author: user
"""

import cv2
import numpy as np
import template_matching_thermal as tmt
import template_matching_CSI as tmc

def circle_keypoint():
    
    upper_sample = cv2.imread('sample2.jpg')
    lower_sample = cv2.imread('sample7.jpg')
    
    upper_template = cv2.imread('template_thermal2.jpg')
    lower_template = cv2.imread('template_thermal.jpg')
    
    upperleftX, upperleftY, upperrightX, upperrightY = tmt.get_upper( upper_sample, upper_template )
    lowerleftX, lowerleftY, lowerrightX, lowerrightY = tmt.get_lower( lower_sample, lower_template )
    
    cv2.circle( upper_sample, ( upperleftX, upperleftY ), 1, ( 0, 255, 0 ), 1 )
    cv2.circle( upper_sample, ( upperrightX, upperrightY ), 1, ( 0, 255, 0 ), 1 )
    
    cv2.circle( lower_sample, ( lowerleftX, lowerleftY ), 1, ( 0, 255, 0 ), 1 )
    cv2.circle( lower_sample, ( lowerrightX, lowerrightY ), 1, ( 0, 255, 0 ), 1 )
    
    
    cv2.namedWindow( 'upper sample', cv2.WINDOW_NORMAL )
    cv2.imshow( 'upper sample', upper_sample )
    cv2.waitKey( 0 )
    
    cv2.namedWindow( 'lower sample', cv2.WINDOW_NORMAL )
    cv2.imshow( 'lower sample', lower_sample )
    cv2.waitKey( 0 )
    
    cv2.destroyAllWindows()
    
    return 

def CSI_matching():
    
    upper_sample = cv2.imread('sample4.jpg')
    lower_sample = cv2.imread('sample8.jpg')
    
    upper_left = cv2.imread('template4.jpg')
    upper_right = cv2.imread('template10.jpg')
    lower_left = cv2.imread('template5.jpg')
    lower_right = cv2.imread('template9.jpg')
    
    
    upperleftX, upperleftY, upperrightX, upperrightY = tmc.get_upper( upper_sample, upper_left, upper_right )
    lowerleftX, lowerleftY, lowerrightX, lowerrightY = tmc.get_lower( lower_sample, lower_left, lower_right )
    
    cv2.circle( upper_sample, ( upperleftX, upperleftY ), 5, ( 0, 255, 0 ), 1 )
    cv2.circle( upper_sample, ( upperrightX, upperrightY ), 5, ( 0, 255, 0 ), 1 )
    
    cv2.circle( lower_sample, ( lowerleftX, lowerleftY ), 5, ( 0, 255, 0 ), 1 )
    cv2.circle( lower_sample, ( lowerrightX, lowerrightY ), 5, ( 0, 255, 0 ), 1 )
    
    
    cv2.namedWindow( 'upper sample', cv2.WINDOW_NORMAL )
    cv2.imshow( 'upper sample', upper_sample )
    cv2.waitKey( 0 )
    
    cv2.namedWindow( 'lower sample', cv2.WINDOW_NORMAL )
    cv2.imshow( 'lower sample', lower_sample )
    cv2.waitKey( 0 )
    
    cv2.destroyAllWindows()
    
    return 

def align_upper():
    
    # template
    upper_template = cv2.imread('template_thermal2.jpg')
    
    upper_left = cv2.imread('template4.jpg')
    upper_right = cv2.imread('template10.jpg')
    
    
    
    
    return 


if __name__ == '__main__':
    
    circle_keypoint()
    CSI_matching()