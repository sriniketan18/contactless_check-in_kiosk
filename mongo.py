from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint
# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
client = MongoClient("mongodb+srv://prasant:prasant1819@pnrdetails.tuofe.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=client.admin
serverStatusResult=db.command("serverStatus")

mydb = client["pnrinquiry"]
#pprint(serverStatusResult)
pnr="123456"
language="en"######clear global variables after one process
fir_name=[]
las_name=[]
def accessing_database():
	print(pnr)
	mycol = mydb["passengerdetails"]
	myquery = { "pnr": pnr }
	mydoc = mycol.find(myquery)
	print(mydoc.count)
	if mydoc.count()==0:
		return
	
	for x in mydoc:
		fir_name.append(x["first_name"])
		las_name.append(x["last_name"])

	return
accessing_database()
print(pnr)
print(fir_name)
print(las_name)