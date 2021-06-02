# -*- coding: utf-8 -*-
"""
Created on Sat May 29 22:04:44 2021

@author: user
"""

import numpy as np
import argparse
import imutils
import glob
import cv2  

# load the image, convert it to grayscale, and detect edges
template = cv2.imread( 'template5.jpg' )
# 熱影像 template : template_thermal.jpg
# 左手掌( 張開 )template: template5.jpg
template = cv2.cvtColor( template, cv2.COLOR_BGR2GRAY )
template = cv2.Canny( template, 50, 200 )
# cv2.Canny( image, threshold1, threshold2 )
# 用於邊緣銳化
( tH, tW ) = template.shape[ : 2 ]
# template height, template width
cv2.imshow( "Template", template )
cv2.waitKey( 1 )


# load the image, convert it to grayscale, and initialize the
# bookkeeping variable to keep track of the matched region
image = cv2.imread( 'sample8.jpg' )
# 雙手向下 sample:
#       => sample6.jpg
#       => sample8.jpg
gray = cv2.cvtColor( image, cv2.COLOR_BGR2GRAY )
found = None 
    
# loop over the scales of the image 
for scale in np.linspace( 0.2, 1.0, 20 ) [ : : -1 ]:
    
    # np.linspace( start, end, num [, ... ] )
    # start: 起始點、 end: 結束點、 num: 元素數目
    # 回傳：介於 start ~ end 間共 num 個均勻分布的數字
    
    # resize the image according to the scale, and keep 
    # track of the ratio of the resizing
    resized = imutils.resize( gray, width = int( gray.shape[ 1 ] * scale ) )
    # scale 從 0.2 ~ 1 ，調整 gray( sample.jpg 的黑白化結果 )
    
    r = gray.shape[ 1 ] / float( resized.shape[ 1 ] )
    # r: 原圖與當前比較圖( resized )的比例
    # r = 1 : scale, scale = 0.2 ~ 1.0 
        
    # if the resized image is smaller than the template, 
    # then break from the loop
    if resized.shape[ 0 ] < tH or resized.shape[ 1 ] < tW:
        print('too small !!')
        break
        
    # detect edges in the resized, grayscale image and 
    # apply template matching to find the template in 
    # the image
    edged = cv2.Canny( resized, 50, 200 )
    # edged: 原圖縮放後的邊緣銳化版
    
    result = cv2.matchTemplate( edged, template, cv2.TM_CCOEFF )
    # 拿 edged 對 template 做 template matching
    ( _, maxVal, _, maxLoc ) = cv2.minMaxLoc( result )
    # minMaxLoc() 回傳最大( 小 )值與其位置
    
    
    # draw a bounding box around the detected region
    clone = np.dstack( [ edged, edged, edged ] )
    cv2.rectangle( clone, ( maxLoc[ 0 ], maxLoc[ 1 ] ), ( maxLoc[ 0 ] + tW, maxLoc[ 1 ] + tH ), ( 0, 0, 255 ), 2 )
    # cv2.namedWindow( 'Visualize', cv2.WINDOW_NORMAL )
    # cv2.imshow("Visualize", clone )
    # cv2.waitKey( 0 )
            
    # if we have found a new maximum correlation value,
    # then update the bookkeeping variable
    if found is None or maxVal > found[ 0 ]:
        print('bigger result found !!')
        found = ( maxVal, maxLoc, r )
            
    # unpack the bookkeeping variable and compute the 
    # ( x, y ) coordinates of the bounding box based 
    # on the resized ratio
    ( _, maxLoc, r ) = found
    ( startX, startY ) = ( int( maxLoc[ 0 ] * r ), int( maxLoc[ 1 ] * r ) )
    # 將起始座標( 矩形左上座標 )乘上比例 r 
    ( endX, endY ) = ( int( ( maxLoc[ 0 ] + tW ) * r ), int( ( maxLoc[ 1 ] + tH ) * r ) )
    
    # draw a bounding box around the detected result and
    # display the image
    image_copy = image.copy()
    cv2.rectangle( image_copy, ( startX, startY ), ( endX, endY ), ( 0, 0, 255 ), 2 )
    # cv2.namedWindow( "image", cv2.WINDOW_NORMAL )
    # cv2.imshow( "image", image_copy )
    # cv2.waitKey( 0 )
    
    # cv2.destroyAllWindows()

cv2.namedWindow( 'final result', cv2.WINDOW_NORMAL )
cv2.imshow( 'final result', image_copy )
cv2.waitKey( 1 )
# cv2.waitKey( 0 )

cv2.destroyAllWindows()






