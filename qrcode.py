

import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import pyqrcode
from pyqrcode import QRCode
import png

def generateQRCode(pnr,fname, lname):
    qr = pyqrcode.create(pnr+'_'+fname+' '+lname)
   
    qr.png("PNR_"+pnr+"_"+fname+lname+".png", scale = 10)


def scanQRCode():
    cap = cv2.VideoCapture(0)
   
    curTime = 0
   
    decodedQRData = ''

    destroyWindowFlag = False
   
    while True:
        _, frame = cap.read()
       
        curTime+=1
       
        decodedObj = pyzbar.decode(frame)
       
        for obj in decodedObj:
            destroyWindowFlag = True
           
            decodedQRData = obj.data.decode("ascii")
           
            print(decodedQRData)
           
        if (destroyWindowFlag and len(decodedQRData) > 0) or curTime == 350:
            #this means we have got the QRcode info successfully OR the timer has timed out
            #we return this data if returned value is empty string show timeout error and ask if they want to try again
            #Once we get valid info use this data to query the db and get passeneger/flight details
            cap.release()
           
            cv2.destroyAllWindows()
           
            return decodedQRData
       
        cv2.imshow("Frame", frame)
       
        key = cv2.waitKey(1)


