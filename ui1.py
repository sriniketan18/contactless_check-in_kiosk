import streamlit as st

from text import text_to_speech,speech_to_text
from pymongo import MongoClient
from pprint import pprint

#import opencv_verification as ov
#import qrcode
client = MongoClient("mongodb+srv://prasant:prasant1819@pnrdetails.tuofe.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=client.admin
serverStatusResult=db.command("serverStatus")

mydb = client["pnrinquiry"]



def start_process():
	st.title("Select Language")
	initial_text="Speak 1 for english, 3 for hindi, 4 for exit"
	st.markdown(initial_text)
	text_to_speech(initial_text, "en")

	count=0
	language="en"
	while(True):
		text=speech_to_text(2)
		st.text(text)
		if text=='1':
			break
		elif text=='3':
			language="hi"
			break
		elif text=="4":
			return       ####################return
		else:
			text_1="Invalid Input....please retry"
			st.text(text_1)
			text_to_speech(text_1,"en")
			count=count+1
			if count>=3:
				text_1="Returning to main menu"
				st.text(text_1)
				text_to_speech(text_1,"en")
				return ############################return and update failure count
	return language
