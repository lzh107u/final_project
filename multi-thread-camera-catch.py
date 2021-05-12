# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 16:40:53 2021

以多執行緒將取圖與顯示功能分割

"""

import threading
import time
import cv2
import numpy as np

cap = 0
# 可見光鏡頭代號
# 設置為全域
CSI_img = 0
# 可見光影像

END_SAFELY = 0
# 脫離主迴圈
ret_val = 1


# 參考自 cameratest.py
def gstreamer_pipeline(
    
    # width : height = 16 : 9

    capture_width = 1920,
    capture_height = 1080,
    # depend on the setting of camera
    
    display_width = 960,
    display_height = 540,
    # window size
    
    framerate = 30,
    flip_method = 0,
):
    return (    
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

def child_latest_image():
    
    global CSI_img 
    # 將全域 CSI_img 宣告在此
    global ret_val
    # CSI cam 的回傳值為安全變數之一
    global END_SAFELY
    # 安全離開迴圈
    
    print(gstreamer_pipeline(flip_method=0))
    
    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0),cv2.CAP_GSTREAMER)
    
    
    if cap.isOpened():
        window_handle = cv2.namedWindow("CSI Camera", cv2.WINDOW_AUTOSIZE)

        ret_val, CSI_img = cap.read()
        keyCode = 0
        
        while( ret_val != 0 & END_SAFELY == 0 ):

            ret_val, CSI_img = cap.read()
            
        if( ret_val == 0 & END_SAFELY == 0 ):
            print('break out loop accidentally')          
        
        cap.release()
        cv2.destroyAllWindows()
    else:
        print("Unable to open camera")

def show_image():
    
    global CSI_img
    global cap
    global END_SAFELY
    
    
    while( ret_val == 1 ):
        
        
        # main process here
        
        
        CSI_img_process = CSI_img
        # 為避免在操作中 CSI_img 更新，在此將圖片固定在 show_image() 中
        # show images
        cv2.imshow( 'CSI image', CSI_img_process )
        if cv2.waitKey( 1 ) & 0xFF == ord('q'):
            print('break out!')
            END_SAFELY = 1
            # 透過更動此全域變數讓 child thread 停止運作
            break
        
        
    return 
    # 離開 返回 main 等待 child thread 結束
    
t = threading.Thread( target = child_latest_image )
# 由此定義 子執行緒開始後的第一個函數

if __name__ == '__main__':
    
    t.start()
    show_image()
    t.join()
