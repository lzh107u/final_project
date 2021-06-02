# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 19:24:45 2021

@author: user
"""

import cv2
import numpy as np
import match_found as mf


def upper_right_coor( tH, tW, found ):
    
    ( _, maxLoc, r ) = found
    # unpeck the maximum value data
    ( leftX, leftY ) = ( int( maxLoc[ 0 ] * r ), int( maxLoc[ 1 ] * r ) )
    # 將起始座標( 矩形左上座標 )乘上比例 r 
    return leftX, leftY

def upper_left_coor( tH, tW, found ):
    
    ( _, maxLoc, r ) = found
    # unpeck the maximum value data
    ( rightX, rightY ) = ( int( ( maxLoc[ 0 ] + tW ) * r ), int( maxLoc[ 1 ] * r ) )
    
    return rightX, rightY

def lower_right_coor( tH, tW, found ):
    
    ( _, maxLoc, r ) = found
    # unpeck the maximum value data
    ( leftX, leftY ) = ( int( maxLoc[ 0 ] * r ), int( ( maxLoc[ 1 ] + tH ) * r ) )
    
    return leftX, leftY

def lower_left_coor( tH, tW, found ):
    
    ( _, maxLoc, r ) = found
    # unpeck the maximum value data
    ( rightX, rightY ) = ( int( ( maxLoc[ 0 ] + tW ) * r ), int( ( maxLoc[ 1 ] + tH ) * r ) )
    
    return rightX, rightY

"""
    解析 found 取得雙手向上的約略座標
"""
def upper_coordinate( tH, tW, found ):
    
    leftX, leftY = upper_left_coor( tH, tW, found )
    rightX, rightY = upper_right_coor( tH, tW, found )
    
    return leftX, leftY, rightX, rightY


"""
    解析 found 取得雙手向下的約略座標
"""
def lower_coordinate( tH, tW, found ):
    
    leftX, leftY = lower_left_coor( tH, tW, found )
    rightX, rightY = lower_right_coor( tH, tW, found )
    
    return leftX, leftY, rightX, rightY



"""
    輸入圖片，得出雙手向上的座標
"""
def get_upper( img_sample, img_left_template, img_right_template ):
    
    tH, tW, found = mf.matching( img_sample, img_left_template )
    # 將原圖與模板丟進 matching 得出最大位置資訊與模板長寬
    leftX, leftY = upper_left_coor( tH, tW, found )
    
    tH, tW, found = mf.matching( img_sample, img_right_template )
    rightX, rightY = upper_right_coor( tH, tW, found )
    # 輸入 matching 的回傳 得出左右座標
    
    return leftX, leftY, rightX, rightY

"""
    輸入圖片，得出雙手向下的座標
"""
def get_lower( img_sample, img_left_template, img_right_template ):
    
    tH, tW, found = mf.matching( img_sample, img_left_template )
    # 將原圖與模板丟進 matching 得出最大位置資訊與模板長寬
    leftX, leftY = lower_left_coor( tH, tW, found )
    
    tH, tW, found = mf.matching( img_sample, img_right_template )
    rightX, rightY = lower_right_coor( tH, tW, found )
    # 輸入 matching 的回傳 得出左右座標
    
    return leftX, leftY, rightX, rightY