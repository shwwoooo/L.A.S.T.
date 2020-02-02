from tkinter import *
import os
import threading
from email.mime.text import MIMEText 
import smtplib
import datetime
import spi

cardDetected = False
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
	temp = find_name_from_txt(123456)#(stuID)
	global studentName, studentGrade
	studentName = temp[0]
	studentGrade = temp[1]
	#print(cardDetected)
	#print(studentName + ' ' + studentGrade)
	if cardDetected == True:
  		timer = threading.Timer(1,confirmPage)
  		timer.start()

#Use the ID code from card to find student and grade
def find_name_from_txt(stuid):
	global cardDetected
	cardDetected = True
	with open('Table/stuid.txt') as file:
		lines = file.readlines()
	stu_dic = {}
	stu_dic2 = {}
	for line in lines:
		stu_id = int(line.split(',')[0].strip())
		stu_name = line.split(',')[1].strip()
		stu_grade = line.split(',')[2].strip()
		stu_dic[stu_id]=stu_name
		stu_dic2[stu_id]=stu_grade
	return stu_dic[stuid],stu_dic2[stuid]

#Allow the guards to confirm; protection for trigger by mistake
def confirmPage():
    value2 = "\n{0} from {1}\n\n\tIs this you? Click the buttom to confirm.\t\n".format(studentName, studentGrade)
    textLabel.config(text=value2)
    textLabel.grid(row=0,padx=50)
    global button1
    button1 = Button(text="Confirm",command=sentOutPage)
    button1.grid(row=1,pady=10)
    global button2
    button2 = Button(text="That's not me",command=secMainPage)
    button2.grid(row=2,pady=10)

#find class for DP students
def find_class_from_txtDP(stuname,daynum):
    file = open('Table/%s/%d.txt' % (stuname,daynum))
    lines = file.readlines()
    stu_dic2 = {}
    for line in lines:
        stu_name = line.split(',')[0].strip()
        stu_class = line.split(',')[1].strip()
        stu_dic2[stu_name] = stu_class
    return stu_dic2[stuname]

#find class for MYP students
def find_class_from_txtMYP(stugrade,daynum):
    print(DAYNUM)
    print(studentGrade)
    file = open('Table/%s.txt' % (stugrade))
    lines = file.readlines()
    stu_dic2 = {}
    for line in lines:
        day_Num = line.split(',')[0].strip()
        stu_class = line.split(',')[1].strip()
        stu_dic2[day_Num] = stu_class
    print(stu_dic2)
    return stu_dic2[str(daynum)]

#append email addresses and call sendEmail function to send emails
def sentOutPage():
	button1.grid_forget()
	button2.grid_forget()
	listEmails = []
	if int(studentGrade[1:]) <= 10:
		listEmails.append(find_class_from_txtMYP(studentGrade,DAYNUM))
	else:
		listEmails.append(find_class_from_txtDP(studentName,DAYNUM))
	listEmails.append("***REMOVED***")
	print(studentName + ' ' + str(studentGrade) + ' ' + str(DAYNUM))
	print(listEmails)
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
		timer = threading.Timer(5,confirmPage)
		timer.start()

root = Tk()
root.title("SWIS Late System")
root.geometry("480x240")
root.resizable(width=False,height=False) 
mainPage()
root.mainloop()
