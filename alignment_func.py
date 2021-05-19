# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 11:53:47 2021

@author: user
 
    已可觀看對齊結果

"""

import cv2
import numpy as np

MAX_FEATURES = 500
GOOD_MATCH_PERCENT = 0.1

# alignment function
def alignImages( img1, img2 ):
    # print('call function ... ')
    img1Gray = cv2.cvtColor( img1, cv2.COLOR_BGR2GRAY )
    img2Gray = cv2.cvtColor( img2, cv2.COLOR_BGR2GRAY )
    # convert images to grayscale
    # 將圖片轉換成灰階
    
    orb = cv2.ORB_create( MAX_FEATURES )
    keypoints1, descriptors1 = orb.detectAndCompute( img1Gray, None )
    keypoints2, descriptors2 = orb.detectAndCompute( img2Gray, None )
    # detect orb features and compute descriptors
    # 找出關鍵點( keypoints, 多為邊緣高頻區 )
    
    img_tmp1 = cv2.drawKeypoints( img1Gray, keypoints1, None, color=( 0, 255, 0 ), flags = 0 )
    img_tmp2 = cv2.drawKeypoints( img2Gray, keypoints2, None, color=( 0, 255, 0 ), flags = 0 )
    # show orb results
    # 將 orb.detectAndCompute() 之結果( keypoints )繪製於圖片上
    
    # matcher = cv2.DesriptorMatcher_create( cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING )
    matcher = cv2.BFMatcher( cv2.NORM_HAMMING, crossCheck=True )
    matches = matcher.match( descriptors1, descriptors2, None )
    # match features
    # 將前述關鍵點進行匹配
    
    matches.sort( key=lambda x: x.distance, reverse=False )
    # sort matches by score
    # 將配對結果排序( 由好到壞 )
    
    numGoodMatches = int( len( matches ) * GOOD_MATCH_PERCENT )
    matches = matches[ :numGoodMatches ]
    # remove not so good matches
    # 僅保留前方優良配對結果
    # NumGoodMatches 用比例的方式從總匹配數量中得出優良上限
    # 將 matches[] 中優良的組合保留下來
        
    imgMatches = cv2.drawMatches( img1, keypoints1, img2, keypoints2, matches, None )
    # cv2.imwrite( "matches.jpg", imgMatches )
    # draw top matches
    cv2.imshow( 'match result', imgMatches )
    # cv2.waitKey( 1 )
    # 繪製優秀配對結果
    
    points1 = np.zeros( ( len( matches ), 2 ), dtype = np.float32 )
    points2 = np.zeros( ( len( matches ), 2 ), dtype = np.float32 )
    # extract location of good matches
    
    # print( len( matches ) )
    
    for i, match in enumerate( matches ):
        points1[ i, : ] = keypoints1[ match.queryIdx ].pt
        points2[ i, : ] = keypoints2[ match.trainIdx ].pt
        
    h, mask = cv2.findHomography( points1, points2, cv2.RANSAC )
    # find homography
    # 得出轉換結果
    # h 為 3*3 轉換矩陣
    
    cv2.waitKey( 1 )
    # cv2.destroyAllWindows()
    
    return h, mask

def fusionImages( img_bg, img_fusion, h, mask ):
    
    height_fusion, width_fusion, channels_fusion = img_fusion.shape
    height_bg, width_bg, channels_bg = img_bg.shape
    # 取得圖片尺寸
    
    # tmp_fusion = cv2.warpPerspective( img_fusion, h, ( width_fusion, height_fusion ) )
    tmp_bg = cv2.warpPerspective( img_fusion, h, ( width_bg, height_fusion ) )
    # 輸出轉換後結果
    # print( img_tmp.shape )
    # 輸出尺寸為 ( width, height )
    # cv2.imshow( 'tmp', img_tmp )
    
    fusion_result = cv2.addWeighted( img_bg, 0.7, tmp_bg, 0.3, 0 )
    # 注意：cv2.addWeighted() 需要兩畫面等大( 相同寬高 )
    # cv2.imshow( 'img_tmp',img_tmp )
    # cv2.waitKey( 1 )
    # cv2.imshow( 'img_tmp_orig', img_tmp_orig )
    # cv2.waitKey( 1 )
    cv2.imshow( 'fusion result', fusion_result )
    
    cv2.waitKey( 1 )
    # return fusion_result
    

if __name__ == '__main__':
    
    refFilename = 'screen_shot_1.jpg'
    print('reading reference image: ', refFilename )
    imReference = cv2.imread( refFilename, cv2.IMREAD_COLOR )
    # read reference image
    
    imFilename = 'screen_shot_2.jpg'
    print('Reading image to align:', imFilename )
    img = cv2.imread( imFilename, cv2.IMREAD_COLOR )
    # read image to be aligned
    
    print('aligning images ... ')
    # registered image will be restored in imgReg
    # the estimated homography will be stored in h
    
    # imgReg, h = alignImages( img, imReference )
    alignImages( img, imReference )
    cv2.waitKey( 0 )
    cv2.destroyAllWindows()