import speech
from text import text_to_speech
def final_1():
	while(True):
		text="Say Hello!"
		print(text)
		text_to_speech(text,"en")
		out=speech.speech_to_text(3)
		if out is not None:
			out.lower()
		print(out)
		if out=="hello": 
			speech.start_process()