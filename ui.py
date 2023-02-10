import streamlit as st
from text import text_to_speech, speech_to_text
import speech_recognition as sr
from pymongo import MongoClient
from pprint import pprint
import opencv_verification as ov
import qrcode
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os
from PIL import Image


language="en"######clear global variables after one process
fir_name=[]
las_name=[]

client = MongoClient("mongodb+srv://prasant:prasant1819@pnrdetails.tuofe.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=client.admin
serverStatusResult=db.command("serverStatus")

mydb = client["pnrinquiry"]

image = Image.open('touchMeNot.png')
st.image(image,width=250)

st.title("Touch Me not")

st.sidebar.title("ContactLess CheckIn")
st.sidebar.subheader("Team HetroTech")


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

def accessing_database(text_3):
		mycol = mydb["passengerdetails"]
		myquery = { "pnr": text_3 }
		mydoc = mycol.find(myquery)
		if mydoc.count()==0:
			return
		
		for x in mydoc:
			fir_name.append(x["first_name"])
			las_name.append(x["last_name"])

		return
			
		
def update_database(pnr1,fname,lname):
	mycol = mydb["passengerdetails"]
	myquery = {"pnr":pnr1,"first_name": fname , "last_name": lname}
	mydoc = mycol.find(myquery)
	for x in mydoc:
		newvalues = { "$set": { "ischeckedin": True } }
		mycol.update_one(myquery, newvalues)


def sendConfirmationEmail(pnrData, emailid, fname,lname):
	sender_email = "testhackblitz@gmail.com"
	receiver_email = emailid
	password = 'chirag12345'

	message = MIMEMultipart("alternative")
	message["Subject"] = "Checkin Confirmation"
	message["From"] = sender_email
	message["To"] = receiver_email
	img_data = open("PNR_"+pnrData+"_"+fname+lname+".png", 'rb').read()



	# Turn these into plain/html MIMEText objects
	part1 = MIMEText("Hello "+ fname + "," + "\n Thank you for completing checkin process for your PNR : "+pnrData+"\n Please find your Virtual Boarding Pass attached", "plain")
	part2 = MIMEImage(img_data, name=os.path.basename("PNR_"+pnrData+"_"+fname+lname+".png"))
	# Add HTML/plain-text parts to MIMEMultipart message
	# The email client will try to render the last part first
	message.attach(part1)
	message.attach(part2)

	# Create secure connection with server and send email
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
	    server.login(sender_email, password)
	    server.sendmail(
	        sender_email, receiver_email, message.as_string()
	    )


def aadhar_validation(check_list,pnr1):
	print(pnr1)
	text_8="Please show the pictures of your id proof in the camera in the boxes shown to verify the further process."
	st.markdown(text_8)
	text_to_speech(text_8, language)
	ver=False
	print(fir_name)
	print(las_name)
	for i in range(len(check_list)):
		ver_failure=0
		while(ver_failure<=2):
			if ov.verification(fir_name[check_list[i]], las_name[check_list[i]]):
				ver=True
				
				update_database(pnr1,fir_name[check_list[i]],las_name[check_list[i]])
				qrcode.generateQRCode(pnr1,fir_name[check_list[i]],las_name[check_list[i]])
				mycol = mydb["passengerdetails"]
				myquery = {"pnr":pnr1,"first_name": fir_name[check_list[i]] , "last_name": las_name[check_list[i]]}
				mydoc = mycol.find(myquery)
				email=""
				for x in mydoc:
					email=x["mail_id"]
				text_12="Virtual Boarding Pass sent to the mail. "
				st.text(text_12)
				text_to_speech(text_12, language)
				sendConfirmationEmail(pnr1, email , fir_name[check_list[i]],las_name[check_list[i]])

				break

			else:
				ver=False
				ver_failure=ver_failure+1
				text_8="Please retry"
				if ver_failure>2:
					text_8="Verification Failed....Please contact the desk for support!"
				st.text(text_8)
				text_to_speech(text_8, language)

		if ver_failure>2:
			return ###################################### return and update failure count

		final_ver=False
		if ver==True:
			if i==len(check_list)-1:
				text_8="All verifications successful!"
				st.markdown(text_8)
				text_to_speech(text_8, language)
				final_ver=True
				break

			else:
				text_8="Verification Successful....Going to the next person!"
				st.text(text_8)
				text_to_speech(text_8, language)
		if final_ver==True:
			break


def already_check_in():
	text_10="Verifying if you are already checked in."
	print(text_10)
	text_to_speech(text_10,language)
	if ov.verification("","",True)==False:
		text1="Not Checked in or the person is not present in the database.Please continue in the process"
		st.markdown(text1)
		text_to_speech(text1, language)
		return False
	else:
		text1="Person already checked in...returning to main menu"
		st.markdown(text1)
		text_to_speech(text1, language)
		return True


def pnr_entering():
	st.title("PNR Entering")
	initial_text="Speak 1 for entering your PNR using barcode, 3 for entering using voice, 4 for exit"
	check_list=[]
	text_1="Invalid PNR...Please try again"
	pnr=""
	data_rec=False
	count=0
	while(True):
		st.markdown(initial_text)
		text_to_speech(initial_text, language)
		text=speech_to_text(3)
		st.text(text)

		if text=='1':
			pnr=input_using_barcode()
			################################## check if pnr is empty

			accessing_database(pnr)
			if len(fir_name)==0:
				count=count+1
				if count>=3:
					text_2="Invalid PNR...."
					st.markdown(text_2)
					text_to_speech(text_2,language)
					return check_list,pnr############################ return and update failure count
				st.text(text_1)
				text_to_speech(text_1,language)
			else:
				data_rec=True
				break

		elif text=='3':
			pnr=input_using_voice()

			################################## check if pnr is empty
			accessing_database(pnr)
			if len(fir_name)==0:
				count=count+1
				if count>=3:
					text_2="Invalid PNR...."
					st.markdown(text_2)
					text_to_speech(text_2,language)
					return check_list,pnr############################return and update failure count
				st.text(text_1)
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
				return check_list,pnr############################return and update failure count
		if data_rec==True:
			break
	if pnr=="":
		return check_list,pnr
	y=0
	for x in range(len(fir_name)):
		st.write(y,fir_name[x], las_name[x])
		text_5=str(y)+"for"+fir_name[x]+las_name[x]
		text_to_speech(text_5,language)
		y=y+1

	text_6="Speak out the Number corresponding to the person you want the boarding pass of, for entering all, speak all, if done, speak ok."
	neg=False
	first=False
	count=0
	while(True):
		if first==True:
			text_6="For adding more individuals, just speak out the number corresponding to that person, if done, speak ok."
		text_7="Invalid number...please try again."
		if neg==True:
			st.markdown(text_6)
			text_to_speech(text_6,language)
		neg=False
		text_4=speech_to_text(3)
		print(text_4)
		if(text_4=="ok"):
			break
		if(text_4=="all" and first==False):
			check_list.clear()
			for i in range(y):
				check_list.append(i)
			break
		try:
			a=int(text_4)
			if(int(text_4)>=y):
				neg=True
				count=count+1
				if count>=3:
					text_2="Invalid numbers....returning to main menu"
					st.text(text_2)
					text_to_speech(text_2,language)
					return check_list,pnr############################ return and update failure count
				st.text(text_7)
				text_to_speech(text_7,language)
			else:
				check_list.append(int(text_4))
				first=True
		except:
			neg=True
			count=count+1
			if count>=3:
				text_2="Invalid numbers....returning to main menu"
				st.text(text_2)
				text_to_speech(text_2,language)
				return check_list,pnr############################ return and update failure count
			st.text(text_7)
			text_to_speech(text_7,language)

	

	print(check_list)
	return check_list,pnr

def start_process():
	st.title("Select Language")
	initial_text="Speak 1 for english, 3 for hindi, 4 for exit"
	st.markdown(initial_text)
	text_to_speech(initial_text, "en")

	count=0
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
	if already_check_in():
		return
	else:
		check_list=[]
		check_list,pnr1=pnr_entering()
		if(len(check_list)==0):
			return 
		else:
			st.markdown(check_list)
			aadhar_validation(check_list,pnr1)
			return

def board():
	ans=input_using_barcode()
	pnr=""
	finame=""
	laname=""
	
	pnr=ans.split("_")[0]
	finame=ans.split("_")[1].split(" ")[0]
	laname=ans.split("_")[1].split(" ")[0]
	print(pnr)
	print(name)
	print(ans)
	mycol = mydb["passengerdetails"]
	myquery = {"pnr":pnr}
	mydoc = mycol.find(myquery)
	for x in mydoc:
		newvalues = { "$set": { "ischeckedin": True } }
		mycol.update_one(myquery, newvalues)

	out=pnr+": "+finame+' '+laname + ": boarding successful"
	print(out)
	st.success(out)

def final_1():
	st.header("Say Hello or Say Embark!")

	while(True):
		text="Say Hello or Say Embark!"
		print(text)
		text_to_speech(text,"en")
		out=speech_to_text(2)
		if out is not None:
			out.lower()
		print(out)
		if out=="hello": 
			st.text("Starting the process")
			start_process()
			break
		if out=="embark":
			board()
			break
		if out=="exit":
			break
	return


final_1()