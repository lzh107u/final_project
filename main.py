# -*- coding: utf-8 -*-
"""
Created on Sun May 16 18:11:37 2021

@author: user
"""

import getCSIcam as CSI
import getThermalCam as THERMAL

if __name__ == '__main__':
    
    retCSI, capCSI = CSI.get_CSIcam()
    retTher, capTher = THERMAL.get_thermal_cam()
    
    
    