# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 16:36:33 2021

@author: user

functions:
    
    tH, tW, found = matching( img_sample, img_template )
    => moved into match_found.py
    
    startX, startY, endX, endY = get_coordinate( tH, tW, found )
    
    image_copy = get_result_img( img_sample, img_template, found )
    
    leftX, leftY, rightX, rightY = upper_coordinate( tH, tW, found )
    leftX, leftY, rightX, rightY = lower_coordinate( tH, tW, found )
    
    leftX, leftY, rightX, rightY = get_upper( img_sample, img_template )
    leftX, leftY, rightX, rightY = get_lower( img_sample, img_template )

"""

import cv2
import numpy as np
import imutils
import match_found as mf

"""
    tH: template height
    tW: template width
    found: maxVal, maxLoc, r
    
    回傳矩形的左上與右下座標
"""
def get_coordinate( tH, tW, found ):
    
    ( _, maxLoc, r ) = found
    # unpeck the maximum value data
    
    ( startX, startY ) = ( int( maxLoc[ 0 ] * r ), int( maxLoc[ 1 ] * r ) )
    # 將起始座標( 矩形左上座標 )乘上比例 r 
    
    ( endX, endY ) = ( int( ( maxLoc[ 0 ] + tW ) * r ), int( ( maxLoc[ 1 ] + tH ) * r ) )
    
    return startX, startY, endX, endY


"""
    輸入 matching() 回傳的結果 ( found )
    回傳經 found 運算後框出的符合區
    
    found: ( maxVal, maxLoc, r )
    r: 最佳縮放比例
    maxVal: 最佳匹配值
    maxLoc: 最佳匹配位置
    可參考 cv2.minMaxLoc()
"""
def get_result_img( img_sample, img_template, found ):
    
    ( tH, tW ) = img_template.shape[ : 2 ]
    
    # unpack the bookkeeping variable and compute the 
    # ( x, y ) coordinates of the bounding box based 
    # on the resized ratio
    startX, startY, endX, endY = get_coordinate( tH, tW, found )
    
    # draw a bounding box around the detected result and
    # display the image
    image_copy = img_sample.copy()
    cv2.rectangle( image_copy, ( startX, startY ), ( endX, endY ), ( 0, 0, 255 ), 2 )
    
    return image_copy


"""
    解析 found 取得雙手向上的約略座標
"""
def upper_coordinate( tH, tW, found ):
    
    ( _, maxLoc, r ) = found
    # unpeck the maximum value data
    
    ( leftX, leftY ) = ( int( maxLoc[ 0 ] * r ), int( maxLoc[ 1 ] * r ) )
    # 將起始座標( 矩形左上座標 )乘上比例 r 
    
    ( rightX, rightY ) = ( int( ( maxLoc[ 0 ] + tW ) * r ), leftY )
    
    return leftX, leftY, rightX, rightY


"""
    解析 found 取得雙手向下的約略座標
"""
def lower_coordinate( tH, tW, found ):
    
    ( _, maxLoc, r ) = found
    
    ( leftX, leftY ) = ( int( maxLoc[ 0 ] * r ), int( ( maxLoc[ 1 ] + tH ) * r ) )
    ( rightX, rightY ) = ( int( ( maxLoc[ 0 ] + tW ) * r ), int( ( maxLoc[ 1 ] + tH ) * r ) )
    
    return leftX, leftY, rightX, rightY
            
"""
    輸入圖片，得出雙手向上的座標
"""
def get_upper( img_sample, img_template ):
    
    tH, tW, found = mf.matching( img_sample, img_template )
    # 將原圖與模板丟進 matching 得出最大位置資訊與模板長寬
    leftX, leftY, rightX, rightY = upper_coordinate( tH, tW, found )
    # 輸入 matching 的回傳 得出左右座標
    
    return leftX, leftY, rightX, rightY

"""
    輸入圖片，得出雙手向下的座標
"""
def get_lower( img_sample, img_template ):
    
    tH, tW, found = mf.matching( img_sample, img_template )
    # 將原圖與模板丟進 matching 得出最大位置資訊與模板長寬
    leftX, leftY, rightX, rightY = lower_coordinate( tH, tW, found )
    # 輸入 matching 的回傳 得出左右座標
    
    return leftX, leftY, rightX, rightY
    

if __name__ == '__main__':
    
    img_sample = cv2.imread( 'sample2.jpg' )
    img_template = cv2.imread( 'template_thermal2.jpg' )
    
    tH, tW, result = mf.matching( img_sample, img_template )
    img_result = get_result_img( img_sample, img_template, result )
    
    cv2.namedWindow( 'self_test', cv2.WINDOW_NORMAL )
    cv2.imshow( 'self_test', img_result )
    cv2.waitKey( 0 )
    
    cv2.destroyAllWindows()

    
    
    
    