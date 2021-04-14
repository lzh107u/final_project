# MIT License
# Copyright (c) 2019 JetsonHacks
# See license
# Using a CSI camera (such as the Raspberry Pi Version 2) connected to a
# NVIDIA Jetson Nano Developer Kit using OpenCV
# Drivers for the camera and OpenCV are included in the base image

import cv2
import numpy as np


# gstreamer_pipeline returns a GStreamer pipeline for capturing from the CSI camera
#s Defaults to 1280x720 @ 60fps
# Flip the image by setting the flip_method (most common values: 0 and 2)
# display_width and display_height determine the size of the window on the screen

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


def show_camera():
    # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
    
    print(gstreamer_pipeline(flip_method=0))
    
    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0),cv2.CAP_GSTREAMER)
    thermal = cv2.VideoCapture( 1 )
    reth, image_th = thermal.read()
    if cap.isOpened():
        window_handle = cv2.namedWindow("CSI Camera", cv2.WINDOW_AUTOSIZE)

        ret_val, img = cap.read()
        keyCode = 0

        while( ret_val != 0 ):

            ret_val, img = cap.read()
            reth, image_th = thermal.read()
            cv2.imshow("CSI Camera", img )
            if cv2.waitKey( 1 ) & 0xFF == ord('q'):
                print('break out!')
                break
            cv2.imshow("thermal camera", image_th )
            if cv2.waitKey( 1 ) & 0xFF == ord( 'q' ):
                print('break out!!')
                break
        
        thermal.release()
        cap.release()
        cv2.destroyAllWindows()
    else:
        print("Unable to open camera")

if __name__ == "__main__":
    show_camera()
    print('last line')


