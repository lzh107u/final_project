# -*- coding: utf-8 -*-
"""
Created on Fri Jul 02 20:26:09 2021

@author: user
"""

import sys # stdin
import re # regular expression
import threading # 接收相機模組的回傳值
import cv2
import queue


import module_original as orig_mod # 筆電原始鏡頭
import module_C200 as c200_mod # tapo C200 webcam
import module_CSI as csi_mod # CSI 鏡頭
import module_thermal as ther_mod # 紅外線鏡頭

test = True
module_name = [] # 儲存整個程式所包含的 camera module 的識別名稱
_global_dict = {} # 儲存所有全域對象

"""
    set_value( name, value )
    
    name: 變數名稱
    value: 與之配對的資料
    變數型態不限制
"""
def set_value( name, value ):
    global _global_dict
    _global_dict[ name ] = value
    
"""
    get_value( name, defValue = None )
    
    name: 欲取出的變數名稱
    defValue: 取出 name 相對應的資料，並用這個 reference 回傳
    注意： defValue 預設為 None
"""
def get_value( name, defValue = None ):
    global _global_dict
    try:
        return _global_dict[ name ]
    except KeyError:
        return defValue

"""
    thread_start( name )
    
    執行緒工作開始
"""
def thread_start( name ):
    
    name_function = name + '_function' # dictionary 內索引名稱加長
    camera_function = get_value( name_function )
    worker = threading.Thread( target = camera_function )
    worker.start()
    # 開啟一個新的 child thread 來處理鏡頭工作
    
    name_thread = name + '_thread'
    set_value( name_thread, worker ) # 將 child thread reference 存進全域
    # print('thread_start(): store child thread reference with name:', name )
    
    return 

"""
    thread_end( name ):
        
    執行緒工作結束( 回收 )
"""
def thread_end( name ):
    name_end = name + '_end'
    end_func = get_value( name_end ) # 取得收尾函式指標
    end_func()
    
    name_thread = name + '_thread'
    worker = get_value( name_thread ) # 取得 child thread 指標
    
    worker.join()
    
    return 

"""
    worker_start( name )
    
    指定要開始的平行作業名稱，將相應的工作函數與收尾函數存進 dictionary
    結尾時呼叫 thread_start() 正式開始 child thread 的執行
"""
def worker_start( name = 'default' ):
    global _global_dict
    name_function = name + '_function' # 儲存執行緒工作函數在 dictionary 內的索引
    name_end = name + '_end'
    # 指定 child thread 的工作函數( worker_function )與對應傳入參數( args )
    if re.match( orig_mod.get_name(), name ):
        orig_mod.worker_start( _global_dict ) # 開啟筆電原始鏡頭拍照功能
        
        set_value( name_function, orig_mod.worker_function ) # 將函數指標存進 dictionary
        set_value( name_end, orig_mod.worker_end )
    
    elif re.match( c200_mod.get_name(), name ):    
        c200_mod.worker_start( _global_dict ) # 開啟 Tapo C200 webcam 拍照功能
        
        set_value( name_function, c200_mod.worker_function ) # 將函數指標存進 dictionary
        set_value( name_end, c200_mod.worker_end )
    
    elif re.match( csi_mod.get_name(), name ):    
        csi_mod.worker_start( _global_dict ) # 開啟 CSI 鏡頭拍照功能
        
        set_value( name_function, csi_mod.worker_function ) # 將函數指標存進 dictionary
        set_value( name_end, csi_mod.worker_end )
    elif re.match( ther_mod.get_name(), name ):    
        ther_mod.worker_start( _global_dict ) # 開啟紅外線拍照功能
        
        set_value( name_function, ther_mod.worker_function ) # 將函數指標存進 dictionary
        set_value( name_end, ther_mod.worker_end )
    
    else :
        print('\'name\'(', name, ') is invalid')
        return False
    
    thread_start( name )
    return True

"""
    worker_end( reference of child thread )
    
    傳入要結束的 child_thread 指標並在此結束它的工作
"""
def worker_end():
    
    module_name = get_value( 'module_name' ) 
    # 取得全域 module name 資料
    
    if module_name is None:
        return 
    else:
        # 載入 test
        test = get_value( 'test' )
        
        # 由是否為測試模式決定要關掉誰
        if test:
            thread_end( orig_mod.get_name() )
            thread_end( c200_mod.get_name() )
        else :    
            thread_end( ther_mod.get_name() )
            thread_end( csi_mod.get_name() )
    return

"""
    open_camera( name )

    用於取得相機鏡頭
    name: 用於區分不同鏡頭，有 CSI 與 thermal 兩種
"""
def open_camera( name = 'default' ):
    global module_name # 儲存所有套件的名稱
    
    ret = worker_start( name )
    
    if ret == True:
        module_name.append( name )
        set_value( 'module_name', module_name ) 
        # 更新 module_name 在全域( global_var.py )的紀錄
    
        return True
    elif ret == False:
        print('name:', name )
        print('main process terminated')
        
        return False

def clean_up():
    
    worker_end()
    # 終止子執行緒
    
    return

def controller():
    global C
    while( True ):
        print( 'command: ', end = '', flush = True )
        # end 項：決定字串結尾，在此指定為空，不額外添加 '\n'
        # flush 項：決定是否使用 buffering ，用 True 表示 unbuffering 
        # ( 預設應為 line buffering )
        line = sys.stdin.readline().strip('\n')
        # 標準輸入，自動去掉結尾空白
        # print( 'line: ', line )
        
        # 以 regular expression 來識別指令
        if re.match( '[Bb][Rr][Ee][Aa][Kk]', line ):
            # 退出程式
            print('break out now ...')
            break
        elif re.match( 'take', line ):
            print('take two photos ...')
            image = get_value( 'CSI_image' )
            cv2.imwrite( 'CSI_image.jpg', image )
            image = get_value( 'thermal_image' )
            cv2.imwrite( 'thermal_image.jpg', image )
            
    return 

def controller_test():
    global test
    if test: 
        queue_orig = get_value( 'orig_queue' ) # 取得 orig 影像
        queue_c200 = get_value( 'C200_queue' ) # 取得 c200 影像
        cv2.namedWindow( 'original camera', cv2.WINDOW_NORMAL )
        cv2.namedWindow( 'Tapo c200', cv2.WINDOW_NORMAL )
        
    else:
        queue_csi = get_value( 'CSI_queue' ) # 取得 CSI 影像
        queue_thermal = get_value( 'thermal_queue' ) # 取得 thermal 影像
        cv2.namedWindow( 'thermal camera', cv2.WINDOW_NORMAL )
        cv2.namedWindow( 'CSI camera', cv2.WINDOW_NORMAL )
    
    counting = 0
    i = 0
    while( True ):
        
        if test:
            
            if queue_c200 is None:
                queue_c200 = get_value( 'C200_queue' )
                continue
            
            
            img_orig = queue_orig.get() # 從 queue 取得影像
            img_c200 = queue_c200.get() 
            
            cv2.imshow( 'original camera', img_orig )
            cv2.imshow( 'Tapo c200', img_c200 )
            
        else:
            
            if queue_thermal is None:
                queue_thermal = get_value( 'thermal_queue' )
                continue
            elif queue_csi is None:
                queue_csi = get_value( 'CSI_queue' )
                continue
            
            if queue_csi.empty():
                continue
            else:
                img_csi = queue_csi.get() # 從 queue 取得影像
            
            if queue_thermal.empty():
                continue
            else:
                img_ther = queue_thermal.get()
            
            cv2.imshow( 'thermal camera', img_ther )
            cv2.imshow( 'CSI camera', img_csi )
            
        
        if cv2.waitKey( 1 ) & 0xFF == ord('q'):
            print('controller end')
            break
        
    cv2.destroyAllWindows()
    
    return 
    
if __name__ == '__main__':
    
    # _init()
    # 初始化全域變數空間
    
    test = False
    
    set_value( 'test', test ) # 是否為測試
    set_value( 'module_name', module_name )
    
    ret1 = True
    ret2 = True
    if test :
        ret1 = open_camera( orig_mod.get_name() ) # 開啟 orig 鏡頭
        ret2 = open_camera( c200_mod.get_name() ) # 開啟 C200 鏡頭
    else :
        ret1 = open_camera( csi_mod.get_name() )
        ret2 = open_camera( ther_mod.get_name() )
    # 初始化環境
    
    # controller()
    # 開始控制器
    if ret1 == True & ret2 == True:
        controller_test()
    
    clean_up()
    # 結束子執行緒
    
    print('all done, end now')