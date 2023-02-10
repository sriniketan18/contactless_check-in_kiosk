from google_trans_new import google_translator
import os
from playsound import playsound
from gtts import gTTS 
import speech_recognition as sr

def text_to_speech(text, language):
	translator = google_translator()  
	translate_text = translator.translate(text,lang_src='en', lang_tgt=language)  
	speak = gTTS(text=translate_text, lang=language, slow= False)  
	speak.save("captured_voice2.mp3")
	playsound("captured_voice2.mp3") 
	os.remove("captured_voice2.mp3")

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