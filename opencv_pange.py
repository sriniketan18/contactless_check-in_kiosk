
import cv2
import numpy as np
import pytesseract
import ocr_try2
import time
 
# create an overlay image. You can use any image
foreground = np.ones((100,100,3),dtype='uint8')*255
fore=cv2.imread("rect.png")
# Open the camera
start=time.time()
cap = cv2.VideoCapture(0)
# Set initial value of weights
alpha = 0.4
while True:
    # read the background
    ret, background = cap.read()
    #large box for the id proof
    added_image = cv2.copyMakeBorder(
                 background[50:420,50:600,:], 
                 2, 
                 2, 
                 2, 
                 2, 
                 cv2.BORDER_CONSTANT, 
                 value=[0,0,255]
              )
    #small box for the name
    added_image1 = cv2.copyMakeBorder(
                 background[140:170,220:340,:], 
                 2, 
                 2, 
                 2, 
                 2, 
                 cv2.BORDER_CONSTANT, 
                 value=[0,255,0]
              )
    # Change the region with the result
    background[46:420,46:600,:] = added_image
    background[136:170,216:340,:] = added_image1
    # For displaying current value of alpha(weights)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(background,'Place the identity proof in the box with name in the green box',(10,30), font, 0.6,(0,0,255),1,cv2.LINE_AA)
    cv2.imshow('a',background)
    ######################################################### OCR #############################################
    ocr_img=background[136:170,216:340,:]
    gray = cv2.cvtColor(ocr_img, cv2.COLOR_RGB2GRAY)
    gray, img_bin = cv2.threshold(gray,128,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    te= ocr_try2.Text_Extractor(img_bin)
    text=te.extract_text()
    print(text)
    first_name=""
    last_name=""
    fname=0
    for t in text:
        if ((t>='A' and t<="Z") or (t>='a' and t<='z')) and (fname==0 or fname==1):
            fname=1
            first_name=first_name+t
        elif t==" " and fname==1:
            fname=2
        elif ((t>='A' and t<="Z") or (t>='a' and t<='z')) and (fname==2 or fname==3):
            fname=3
            last_name=last_name+t

    print("first_name: ",first_name)
    print("last_name: ", last_name)


    k = cv2.waitKey(10)

    # Press q to break
    if k == ord('q') or (time.time()-start)>15:
        break
    
# Release the camera and destroy all windows         
cap.release()
cv2.destroyAllWindows()