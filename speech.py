############################ language barrier

from google_trans_new import google_translator
import os
from playsound import playsound
from gtts import gTTS 
import speech_recognition as sr
from text import text_to_speech

from pymongo import MongoClient
from pprint import pprint

import opencv_verification as ov
import qrcode


client = MongoClient("mongodb+srv://prasant:prasant1819@pnrdetails.tuofe.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=client.admin
serverStatusResult=db.command("serverStatus")

mydb = client["pnrinquiry"]

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

###################################################### PAGE FOR SELECTING LANGUAGES ############################
def start_process():
	initial_text="Speak 1 for english, 3 for hindi, 4 for exit"
	print(initial_text)
	text_to_speech(initial_text, "en")

	count=0
	language="en"
	while(True):
		text=speech_to_text(2)
		print(text)
		if text=='1':
			break
		elif text=='3':
			language="hi"
			break
		elif text=="4":
			return       ####################return
		else:
			text_1="Invalid Input....please retry"
			print(text_1)
			text_to_speech(text_1,"en")
			count=count+1
			if count>=3:
				return ############################return and update failure count


	####################################################### ALREADY CHECKED IN VERIFICATION ##############################3

	text_10="Verifying if you are already checked in."
	print(text_10)
	text_to_speech(text_10,language)
	if ov.verification("","",True)==False:
		text1="Not Checked in or the person is not present in the database.Please continue in the process"
		print(text1)
		text_to_speech(text1, language)
	else:
		text1="Person already checked in...returning to main menu"
		print(text1)
		text_to_speech(text1, language)
		return                ########################## return 

	####################################################### INPUTTING THE PNR ##################

	def input_using_voice():
		text_2="Please speak the PNR Number"
		print(text_2)
		text_to_speech(text_2,language)
		text_3=speech_to_text(8)
		text_3=text_3.upper()
		print(text_3)
		return text_3

	def input_using_barcode():
		output=qrcode.scanQRCode()
		return output

	####################################################### ACCESSING THE DATABASE ##################

	def accessing_database(text_3):
		mycol = mydb["passengerdetails"]
		myquery = { "pnr": text_3 }
		mydoc = mycol.find(myquery)
		list1=[]
		list2=[]
		if mydoc.count()==0:
			return list1,list2
		
		for x in mydoc:
			list1.append(x["first_name"])
			list2.append(x["last_name"])

		return list1, list2
			
		
	def update_database(pnr,fname,lname):
		mycol = mydb["passengerdetails"]
		myquery = { "pnr": pnr , "first_name": fname , "last_name": lname}
		mydoc = mycol.find(myquery)
		for x in mydoc:
			newvalues = { "$set": { "ischeckedin": True } }
			mycol.update_one(myquery, newvalues)


	######################################################### OPTION FOR PNR ENTERING ###############################

	initial_text="Speak 1 for entering your PNR using barcode, 3 for entering using voice, 4 for exit"
	fir_name=[]
	las_name=[]
	text_1="Invalid PNR...Please try again"
	pnr=""
	data_rec=False
	count=0
	while(True):
		print(initial_text)
		text_to_speech(initial_text, language)
		text=speech_to_text(4)
		print(text)

		if text=='1':
			pnr=input_using_barcode()
			################################## check if pnr is empty

			fir_name,las_name=accessing_database(pnr)
			if len(fir_name)==0:
				count=count+1
				if count>=3:
					text_2="Invalid PNR...."
					print(text_2)
					text_to_speech(text_2,language)
					return ############################ return and update failure count
				print(text_1)
				text_to_speech(text_1,language)
			else:
				data_rec=True
				break

		elif text=='3':
			pnr=input_using_voice()

			################################## check if pnr is empty
			fir_name,las_name=accessing_database(pnr)
			if len(fir_name)==0:
				count=count+1
				if count>=3:
					text_2="Invalid PNR...."
					print(text_2)
					text_to_speech(text_2,language)
					return ############################return and update failure count
				print(text_1)
				text_to_speech(text_1,language)
			else:
				data_rec=True
				break

		elif text=="4":
			return        ####################return
		else:
			print(text_1)
			text_to_speech(text_1,language)
			count=count+1
			if count>=3:
				return ############################return and update failure count
		if data_rec==True:
			break

	############################################### RETRIEVEING THE NAMES OF PEOPLE FROM THE DATABASE #####################################
	y=0
	for x in range(len(fir_name)):
		print(y,fir_name[x], las_name[x])
		text_5=str(y)+"for"+fir_name[x]+las_name[x]
		text_to_speech(text_5,language)
		y=y+1

	text_6="Speak out the Number corresponding to the person you want the boarding pass of, for entering all, speak all, if done, speak ok."

	first=False
	check_list=[]
	count=0
	while(True):
		if first==True:
			text_6="For adding more individuals, just speak out the number corresponding to that person, for entering all, speak all, if done, speak ok."
		text_7="Invalid number...please try again."
		print(text_6)
		text_to_speech(text_6,language)
		text_4=speech_to_text(3)
		print(text_4)
		if(text_4=="ok"):
			break
		if(text_4=="all" and first==True):
			check_list.clear()
			for i in range(y):
				check_list.append(i)
			break
		try:
			a=int(text_4)
			if(int(text_4)>=y):
				count=count+1
				if count>=3:
					text_2="Invalid numbers....returning to main menu"
					print(text_2)
					text_to_speech(text_2,language)
					return ############################ return and update failure count
				print(text_7)
				text_to_speech(text_7,language)
			else:
				check_list.append(int(text_4))
				first=True
		except:
			count=count+1
			if count>=3:
				text_2="Invalid numbers....returning to main menu"
				print(text_2)
				text_to_speech(text_2,language)
				return ############################ return and update failure count
			print(text_7)
			text_to_speech(text_7,language)

	if(len(check_list)==0):
		return ################### return to main menu

	print(check_list)

	############################################################################# ID CARD VERIFICATION ##########################

	text_8="Please show the pictures of your aadhar card in the camera in the boxes shown to verify the further process."
	print(text_8)
	text_to_speech(text_8, language)
	ver=False
	for i in range(len(check_list)):
		ver_failure=0
		while(ver_failure<=2):
			if ov.verification(fir_name[check_list[i]], las_name[check_list[i]]):
				ver=True
				text_8= "Verification Successful!"
				print(text_8)
				text_to_speech(text_8, language)
				update_database(pnr,fir_name[check_list[i]],las_name[check_list[i]])
				break

			else:
				ver=False
				ver_failure=ver_failure+1
				text_8="Please retry"
				if ver_failure>2:
					text_8="Verification Failed....Please contact the desk for support!"
				print(text_8)
				text_to_speech(text_8, language)

		if ver_failure>2:
			return ###################################### return and update failure count

		final_ver=False
		if ver==True:
			if i==len(check_list)-1:
				text_8="All verifications successful!"
				print(text_8)
				text_to_speech(text_8, language)
				final_ver=True
				break

			else:
				text_8="Verification Successful....Going to the next person!"
				print(text_8)
				text_to_speech(text_8, language)
		if final_ver==True:
			break

