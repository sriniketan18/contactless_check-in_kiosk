import pytesseract
from PIL import Image
import datetime
import cv2
import sys
import os
import os.path
import re
import numpy as np
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
#class to extract text from an image where the image file is passed as an argument

#class to extract text from an image where the image file is passed as an argument
class Text_Extractor():
    #Constructor
    def __init__(self,image_file):
        self.image_file=image_file
        if self is None:
            return 0
        
#Function to extract the text from image as string 
    def extract_text(self): 

        #img=Image.open(self.image_file)
        #img = cv2.imread(self.image_file)
        img=self.image_file
        #resize the image
        #img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        #convert the image to gray
        #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        #the following command uses the tesseract directory path to get the trained data in the config option
        text=pytesseract.image_to_string(img,config='--tessdata-dir "C:/Program Files/Tesseract-OCR/tessdata"') 
        return text
    
#class to validate if  an image is a adhar card where the text is passed as an argument
class Aadhar_Card_Validator():
    #Constructor
    def __init__(self,text):
        self.text=text
#Function to validate if an image contains text showing its an aadhar card
    def is_aadhar_card(self):
               res=self.text.split()
               dates={}           
               if 'GOVERNMENT OF INDIA'  in self.text:
                   print ("Aadhar card is valid and the details are below:")
                   index=res.index('INDIA')
                   name=''
                   if res[index+3].isalpha():
                      name= res[index+3] + " " + res[index+4] + " " + res[index+5]
                   else :
                      name= res[index+4] + " " + res[index+5] + " " + res[index+6]
               else:
                    name=res[0] + " " + res[1]
               if len(name)>1:
                   print("Name:  " + name)
               else:
                    print("Name not read")
               p = re.compile('d+/d+/d+')
               if (p.findall(self.text)):
                    dates=p.findall(self.text)
                    
               if len(dates)>0 and len(dates[0])>1:
                   print("Date of birth:"+ str(dates[0]))
               aadhar_number=''
               for word in res:
                  if 'yob' in word.lower():
                       yob=re.findall('d+', word)
                       if yob:
                           print ('Year of Birth: ' + yob[0])
                  if len(word) == 4 and word.isdigit():
                      aadhar_number=aadhar_number  + word + ' '
               if len(aadhar_number)>=14:
                   print("Aadhar number is :"+ aadhar_number)
               else:
                    print("Aadhar number not read")
                    print("Try again or try  another file")

"""
def main():
    
       
       te= Text_Extractor("sample.jpeg")
       text=te.extract_text()
       print(text)
       #acv=Aadhar_Card_Validator(text)
       #acv.is_aadhar_card()
main()
"""