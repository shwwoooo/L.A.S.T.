from tkinter import *
import os
import threading
from email.mime.text import MIMEText 
import smtplib
import datetime
import spi
import mysql.connector

cardDetected = True
date = datetime.datetime.now().strftime('%Y-%m-%d')

#Generating day number
class workDays():
	def __init__(self, start_date, end_date, days_off=None):
		
		self.start_date = start_date
		self.end_date = end_date
		self.days_off = days_off
		if self.start_date > self.end_date:
			self.start_date, self.end_date = self.end_date, self.start_date
		if days_off is None:
			self.days_off = 5, 6
	  
		self.days_work = [x for x in range(7) if x not in self.days_off]

	def workDays(self):
	   
		# 还没排除法定节假日还有那些teacher trainingday...
		tag_date = self.start_date
		while True:
			if tag_date > self.end_date:
				break
			if tag_date.weekday() in self.days_work:
				yield tag_date
			tag_date += datetime.timedelta(days=1)

	def daysCount(self):
	   
		return len(list(self.workDays()))

era = datetime.date(2019,11,11)
dateinput = date.split('-')
y = int(dateinput[0])
m = int(dateinput[1])
d = int(dateinput[2])

b = datetime.date(y,m,d)
work = workDays(era,b)
global DAYNUM
DAYNUM = work.daysCount()%8


def mainPage():
	value = "\n\n\nWelcome to SWIS Late System: L.A.S.T\n\n\nPlease scan your card if you are late. Detecting..."
	global textLabel
	textLabel = Label(root,text=value)
	textLabel.grid(padx=80,pady=20)
	#stuID = scanner()
	global STUDENT
	STUDENT = sqlconnection(***REMOVED***,DAYNUM)#(stuID)
	#print(cardDetected)
	#print(studentName + ' ' + studentGrade)
	if cardDetected == True:
		timer = threading.Timer(2,confirmPage)
		timer.start()

#Connect to SQL server to get stuname, grade, and email for the ID
def sqlconnection(ID_Number, Day_Number):
	try:
		cnx = mysql.connector.connect(user="root",password="***REMOVED***",\
			database="L.A.S.T.")

		cursor = cnx.cursor()
		query = ("SELECT * FROM `L.A.S.T.`.Day{};".format(Day_Number))

		cursor.execute(query)

		for each in cursor:
			if ID_Number == each[0]:
				return each[1], each[2], each[3]

	except mysql.connector.Error as err:
		print("Error:", err.msg)

#Allow the guards to confirm; protection for trigger by mistake
def confirmPage():
	value2 = "\n{0} from {1}\n\n\tIs this you? Click the buttom to confirm.\t\n".format(STUDENT[0], STUDENT[1])
	textLabel.config(text=value2)
	textLabel.grid(row=0,padx=50)
	global button1
	button1 = Button(text="Confirm",command=sentOutPage)
	button1.grid(row=1,pady=10)
	global button2
	button2 = Button(text="That's not me",command=secMainPage)
	button2.grid(row=2,pady=10)

#append email addresses and call sendEmail function to send emails
def sentOutPage():
	button1.grid_forget()
	button2.grid_forget()
	listEmails = []
	listEmails.append(STUDENT[2])
	listEmails.append("***REMOVED***")
	time = datetime.datetime.now().strftime('%H:%M:%S')
	'''
	sendEmail("LATE STUDENT - " + studentName,\
	"Hello,\n\n" + studentName + " from " + studentGrade + " is late for school on " + date\
	+ ", entering the gates at " + time + ".\n\n\nSWIS Late System",\
	listEmails)
	'''
	value3="\nEmails have sent to admission office and your first class teacher."
	textLabel.config(text=value3)
	timer = threading.Timer(2,secMainPage)
	timer.start()

#Send email function
def sendEmail(title,messages,toAddr):
	fromAddr= r'***REMOVED***'  # sender's email address
	password = r'***REMOVED***'  # sender's email passwords
	smtpServer = '***REMOVED***'  # SMTP server
	server = smtplib.SMTP(smtpServer, 25)
	msg = MIMEText(messages, 'plain', 'utf-8')
	if len(toAddr) == 1: # testing whether there are one or multiple addresses
		toAddr = toAddr[0]
		msg['To'] = toAddr # put the recipients' addresses in the message block
	else:
		msg['To'] = ','.join(toAddr)
	msg['From'] = fromAddr # sender's address
	msg['Subject'] = title # email title

	server.starttls()  # encode the message using TLS
	#server.set_debuglevel(1)
	server.login(fromAddr, password) # login to sender's email sever
	server.sendmail(fromAddr,toAddr, msg.as_string()) # send the email
	print("Email sent.")
	server.quit() 

#Use for looping 
def secMainPage():
	button1.grid_forget()
	button2.grid_forget()
	value = "\n\n\nWelcome to SWIS Late System: L.A.S.T\n\n\nPlease scan your card if you are late. Detecting..."
	textLabel.config(text=value)
	if cardDetected == True:
		timer = threading.Timer(2,confirmPage)
		timer.start()


root = Tk()
root.title("SWIS Late System")
root.geometry("480x240")
root.resizable(width=False,height=False) 
mainPage()
root.mainloop()
