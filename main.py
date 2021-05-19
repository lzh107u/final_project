# -*- coding: utf-8 -*-
"""
Created on Sun May 16 18:11:37 2021

@author: user
"""

import getCSIcam as CSI
import getThermalCam as THERMAL
import getOrigCam as ORIG
import getUsbCam as USB
import alignment_func as ALIGN

import cv2
import threading
import numpy as np
import time

END_SAFELY = 0
CAM_EXIST = 0
TEST = 0
MAIN = 0

capOrig = 0
capUsb = 0
capCSI = 0
capTher = 0

img1 = 0
img2 = 0

frameName = 'default'
arg = 0
argImg = 0

"""
    show_image()
    由子執行緒執行的函數
    => 抓照片
    => 顯示照片
    => 由 localName 判別該更新哪個全域照片
    
"""
def show_image():
    
    global END_SAFELY
    global arg
    global frameName
    global argImg
    global img1
    global img2
    
    cap = arg
    localName = frameName
    
    if cap.isOpened():
        print('camera opened')
        print('localName:', localName )
        
        
        
        while( True ):
            
            ret, img = cap.read()
            
            # 判別 localName 後更新資料
            if ( 'USB' in localName ) or ( 'Thermal' in localName ):
                img2 = img 
            elif ( 'original' in localName ) or ( 'CSI' in localName ):
                img1 = img
            
            cv2.imshow( localName, img )
            cv2.waitKey( 1 )
            
            if END_SAFELY == 1:
                break
        
        cv2.destroyWindow( localName )
        
    else :
        print('camera not opened')
    
    return 

def unsharp_mask( img, kernel_size = ( 5, 5 ), sigma = 1.0, amount = 1.0, threshold = 0 ):
    blurred = cv2.GaussianBlur( img, kernel_size, sigma )
    sharpened = float( amount + 1 ) * img - float( amount ) * blurred 
    sharpened = np.maximum( sharpened, np.zeros( sharpened.shape ) )
    sharpened = np.minimum( sharpened, 255 * np.ones( sharpened.shape ) )
    sharpened = sharpened.round().astype( np.uint8 )
    
    if threshold > 0:
        low_contrast_mask = np.absolute( img - blurred ) < threshold
        np.copyto( sharpened, img, where = low_contrast_mask )
    
    return img

"""
    更新全域鏡頭物件( videoCapture object )
"""
def getCams():
    
    global MAIN
    global CAM_EXIST
    
    MAIN = 1
    
    retCSI, capCSI = CSI.get_CSIcam()
    retTher, capTher = THERMAL.get_thermal_cam()
    
    if( ( retCSI == 1 ) & ( retTher == 1 ) ):
        CAM_EXIST = 1
    
    return 

def test_getCams():
    
    global CAM_EXIST
    global TEST
    global capOrig
    global capUsb
    
    TEST = 1
    
    retOrig, capOrig = ORIG.get_origCam()
    retUsb, capUsb = USB.get_usbCam()
    
    if( ( retOrig == 1 ) & ( retUsb == 1 ) ):
        CAM_EXIST = 1
    
    return 
"""
    釋放全域鏡頭物件( videoCapture object )
"""
def closeCams( capOrig, capTher ):
    
    global CAM_EXIST
    CAM_EXIST = 0
    
    ORIG.close_origCam( capOrig )
    USB.close_usbCam( capUsb )
    cv2.destroyAllWindows()
    return 

"""
    test_proc( videoCapture_obj1, videoCapture_obj2 )
    
    先呼叫兩個 child thread 顯示畫面
"""
def test_proc( capOrig, capUsb ):
    global END_SAFELY
    global arg
    global frameName
    global img1
    global img2
    global argImg
    
    # 填入 videoCapture object 與 frameName 後呼叫子程序
    arg = capOrig
    argImg = img1
    frameName = 'original cam'
    t1 = threading.Thread( target = show_image )
    t1.start()
    
    time.sleep( 1 )
    
    arg = capUsb
    argImg = img2
    frameName = 'USB cam'
    t2 = threading.Thread( target = show_image )
    t2.start()
    
    time.sleep( 1 )
    
    while( True ):
        # 可成功收到子執行緒儲存的最新影像資料
        # cv2.imshow('main proc img1', img1 )
        # cv2.imshow('main proc img2', img2 )
        img1 = unsharp_mask( img1 )
        h, mask = ALIGN.alignImages( img1, img2 )
        ALIGN.fusionImages( img1, img2, h, mask )
        
        k = 0xFF & cv2.waitKey( 1 )
        
        if k == ord('q'):
            END_SAFELY = 1
            print('break out')
            break
        elif CAM_EXIST == 0:
            END_SAFELY = 1
            print('camera closed accidentally')
            break
            
        
    # 結束執行緒
    t1.join()
    t2.join()
    
    return 
def main_proc():
    global END_SAFELY
    global arg
    global frameName
    global img1
    global img2
    global argImg
    global capCSI
    global capTher
    
    # 填入 videoCapture object 與 frameName 後呼叫子程序
    arg = capCSI
    argImg = img1
    frameName = 'CSI cam'
    t1 = threading.Thread( target = show_image )
    t1.start()
    
    time.sleep( 1 )
    
    arg = capTher
    argImg = img2
    frameName = 'Thermal cam'
    t2 = threading.Thread( target = show_image )
    t2.start()
    
    time.sleep( 1 )
    
    while( True ):
        # 可成功收到子執行緒儲存的最新影像資料
        # cv2.imshow('main proc img1', img1 )
        # cv2.imshow('main proc img2', img2 )
        img1 = unsharp_mask( img1 )
        h, mask = ALIGN.alignImages( img1, img2 )
        ALIGN.fusionImages( img1, img2, h, mask )
        
        k = 0xFF & cv2.waitKey( 1 )
        
        if k == ord('q'):
            END_SAFELY = 1
            print('break out')
            break
        elif CAM_EXIST == 0:
            END_SAFELY = 1
            print('camera closed accidentally')
            break
            
        
    # 結束執行緒
    t1.join()
    t2.join()
    return 

"""
    結束程式：
    => 釋放鏡頭物件( videoCapture object )
    => 關閉所有視窗( window )
"""
def endProc():
    global capOrig
    global capUsb
    
    closeCams(capOrig, capTher)
    
    return 
"""
    直接執行本檔案時，從此開始執行：
    
    注意：在此處使用全域變數不用宣告
"""
if __name__ == '__main__':
    
    test_getCams()
    # getCams()
    # getCams()
    
    if ( ( TEST == 1 ) & ( CAM_EXIST == 1 ) ):
        print('test start...')
        test_proc( capOrig, capUsb )
        
    elif ( ( MAIN == 1 ) & ( CAM_EXIST == 1 ) ):
        print('main start...')
        main_proc( capCSI, capTher )
    else:
        print('no return camera, end process')
        
    
    endProc()
    print('\n\n===============================\nfinal status check:')
    print('CAM_EXIST:', CAM_EXIST )
    print('TEST:', TEST )
    print('MAIN:', MAIN )
    print('END_SAFELY:', END_SAFELY )    