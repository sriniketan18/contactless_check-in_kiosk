from tkinter import *
import speech_recognition as sr
input_text="Please say Hello to continue"



def speech_to_text(dur):
    r=sr.Recognizer()
    print("Speak up!!")
    try:
        with sr.Microphone() as source:
            aud_data=r.record(source, duration=dur)
            print("recog...")
            text=r.recognize_google(aud_data)
            a1=text.replace(" ", "")
            return a1
    except:
        print("Problem with the microphone")
        return

def openNewWindow():
    
    newWindow = Toplevel(root) 
    newWindow.title("New Window") 
    newWindow.mainloop()
    

def speakInput():
    found = False
    while not found:
        text=speech_to_text(5)
        print(text)
        if(text=="hello"):
            found=True
    if found:
        input_text="Say 1 for english"
        

screen1 = Tk()




class MyFirstGUI:
    def __init__(self,master):
        master.title("A simple GUI")

        label = Label(master, text=input_text)
        label.pack()
        speakInput()
        master.mainloop()
        
      
my_gui = MyFirstGUI(screen1)