from tkinter import *
import pyaudio
import speech_recognition as sr
r = sr.Recognizer()
with sr.Microphone() as source:
    audio = r.listen(source) 
try:
    a=(r.recognize(audio))
    print (a)
except LookupError:                            
    a=("Could not understand audio")
    print (a)
class App(object):

    def __init__(self,root):
        self.root = root

    # create a Frame for the Text and Scrollbar
        txt_frm = tki.Frame(self.root, width=900, height=900)
        txt_frm.pack(fill="both", expand=True)
        # ensure a consistent GUI size
        txt_frm.grid_propagate(False)

    # create first Text label, widget and scrollbar
        self.lbl1 = tki.Label(txt_frm, text="Type")
        self.lbl1.grid(row=0,column=0,padx=2,pady=2)

        self.txt1 = tki.Text(txt_frm, borderwidth=3, relief="sunken", height=4,width=55)
        self.txt1.config(font=("consolas", 12), undo=True, wrap='word')
        self.txt1.grid(row=25, column=7, sticky="nsew", padx=2, pady=2)
        self.txt1.insert(0.0,a)

    def clearBox(self):
        if a == "clear":
            self.txt1.delete('1.0', 'end')        
root = tki.Tk()
app = App(root)
root.mainloop()