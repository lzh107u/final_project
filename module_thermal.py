# -*- coding: utf-8 -*-
"""
Created on Wed Jun 30 21:06:13 2021

@author: user
"""

import cv2
import numpy as np
import queue
import threading

CHILD_DEAD = False # 確認 child thread 是否結束並等待 join
CAM_SAFETY = True # 確認鏡頭是否安全開啟
EXIT = False # 行程是否關閉
queue = queue.Queue( maxsize = 2 ) # 存放 thermal 圖片的佇列

"""
    get_name()
    
    回傳當前模組的代表名稱( 字串 )
"""
def get_name():
    return 'thermal'

"""
    set_image( image )
    
    儲存圖片
"""
def set_image( image ):
    global queue
    
    # 注意：
    # 若在此不進行 blocking 的處理
    # 則會因為 queue 滿溢而 block 在 put 操作上
    # 在這份 code 中，這種情況會發生在因幀數不同而導致取出照片的速度跟不上鏡頭填補的速度
    if queue.full() :
        # 若 queue 已滿，則排出一張圖片
        queue.get()
    
    queue.put( image )
    return 

"""
    open_camera()
    
    開啟鏡頭存取權限( 開檔 )
"""
def open_camera():
    global CAM_SAFETY
    cam = cv2.VideoCapture( 1 ) # 取得紅外線鏡頭以存取資料
    
    if cam.isOpened() :
        print('module_thermal.py: camera open successfully')
        CAM_SAFETY = True
        return cam
    else:
        print('module_thermal.py: camera open failure')
        CAM_SAFETY = False
        return None

"""
    close_camera( cam )
    
    關閉相機鏡頭存取( 關檔 )
"""
def close_camera( cam ):
    cam.release()
    return 

"""
    grab_image( cam )
    
    抓取圖像資料
"""
def grab_image( cam ):
    
    global EXIT
    
    # 在此迴圈中不斷抓取鏡頭，直到 EXIT 為 True 
    while( EXIT == False ):
        ret, image = cam.read() # 讀取圖像
        set_image( image ) # 將影像存入 global_var.py
        
    return 

"""
    worker_function( name )
    
    由 camera_handler 呼叫，為 child thread 執行的工作函數
    流程依序為：開啟鏡頭 => 讀取畫面 => 關閉鏡頭
"""
def worker_function():
    global CAM_SAFETY
    global CHILD_DEAD
    
    cam = open_camera() # 開啟鏡頭
    
    # 若開啟鏡頭失敗，則結束行程操作
    # 在此將 CAM_SAFETY 設為 False 並 return 
    # 由於 worker_function 由同檔案的 worker_start() 作為 child thread 指定函數呼叫
    # 故在此 return 後， child thread 便停止並等待 main thread 回收
    if( cam is None ):
        print('module_thermal, worker_function(): camera open failure, return now')
        CAM_SAFETY = False
        CHILD_DEAD = True
        return 
    
    grab_image( cam ) # 開始抓取圖片
    
    close_camera( cam ) # 關閉鏡頭
    
    return 
"""
    worker_start( name )
    
    開始鏡頭工作的 child thread 
    name: 用於在全域( global_var.py )中識別當前工作
"""
def worker_start( dictionary ):
    global EXIT
    global CAM_SAFETY
    global CHILD_DEAD
    global queue
    
    EXIT = False
    CAM_SAFETY = False
    CHILD_DEAD = False
    # 先設定好共用信號
    # EXIT: 迴圈控制
    # CAM_SAFETY: 鏡頭抓取成功與否
    # CHILD_DEAD: 子執行緒是否已結束並等待 join
    
    name_queue = get_name() + '_queue'
    dictionary[ name_queue ] = queue # 將 original camera 的 queue 放進 _global_dict 內
    
    return

"""
    worker_end( name )
    
    由 camera_handler 呼叫，用於結束 child thread
"""
def worker_end():
    global EXIT
    
    EXIT = True # 結束迴圈工作
    return 

"""
    worker_safety()
    
    確認鏡頭有正常開啟，由主執行續呼叫
"""
def worker_safety():
    global CAM_SAFETY
    
    if CAM_SAFETY == False:
        return False
    elif CAM_SAFETY == True:
        return True
    else:
        return None
"""
    worker_dead()
    
    確認當前 child thread 是否還存活，由主執行緒呼叫
"""
def worker_dead():
    global CHILD_DEAD
    
    if CHILD_DEAD == True:
        print('module_thermal: already dead')
        return True
    else:
        return False

"""
    demo_display()
    
    單獨執行 module_original.py 時，顯示當前的相機功能是否正常
"""
def demo_display():
    global CAM_SAFETY
    global EXIT
    
    while( CAM_SAFETY == False ):
        i = 0
        
    while( True ):
        image = queue.get()
        cv2.imshow( 'module_thermal demo display', image )
        
        if cv2.waitKey( 1 ) & 0xFF == ord('q'):
            break
        
    cv2.destroyAllWindows()
    EXIT = True
    
    return 

"""
    2021-07-04:
    => 可單獨進入 demo mode 
"""
def test():
    worker = threading.Thread( target = demo_display ) # 以 child thread 執行顯示任務
    worker.start() # child thread 開始
    worker_function() # main thread 開始執行主要工作( 開鏡頭、抓圖片、關鏡頭 )
    worker.join() # 回收 child thread
    print('demo finish.')
    return 

if __name__ == '__main__':
    print('module_original: demo mode activated.')
    print('press q to terminate the process.')
    
    test()