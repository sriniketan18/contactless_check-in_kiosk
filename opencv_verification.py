import cv2
import numpy as np
import pytesseract
import ocr_try2
import time
from pymongo import MongoClient
from pprint import pprint
client = MongoClient("mongodb+srv://prasant:prasant1819@pnrdetails.tuofe.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=client.admin
mydb = client["pnrinquiry"]

def checked_in_ver(first_name, last_name):
    mycol = mydb["passengerdetails"]
    myquery = { "first_name": first_name }
    mydoc = mycol.find(myquery)
    for x in mydoc:
        if x["departure_airport"]=="Chandigarh":
            if x["ischeckedin"]==False:
                return False;
            else:
                return True
    return False

 
def verification(fname_or, lname_or, ischecked=False):
    start=time.time()
    while(True):
        cap = cv2.VideoCapture(0)
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

            background[46:420,46:600,:] = added_image
            background[136:170,216:340,:] = added_image1

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
            """
            print("First Name: ",first_name)
            print("Fname: ",fname_or)
            print("Last Name: ",last_name)
            print("Lname: ",lname_or)
            """
            if ischecked==False:
                if first_name==fname_or and last_name==lname_or:
                    cap.release()
                    cv2.destroyAllWindows()
                    return True
            else:
                if checked_in_ver(first_name, last_name)==True:
                    cap.release()
                    cv2.destroyAllWindows()
                    return True

            k = cv2.waitKey(10)
            if k == ord('q') or (time.time()-start)>25:
                cap.release()
                cv2.destroyAllWindows()
                return False
                     
        cap.release()
        cv2.destroyAllWindows()
        

#print(verification("Amitesh", "Garg"))