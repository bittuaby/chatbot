import os
import os.path
import requests
import datetime
import pdfGenerator
import emailSend
def getClassifiedText(userid):
        print "get classified text"
        filename="sessions/"+userid+".tx"
        if os.path.isfile(filename):
                with open(filename) as f:
                        lines = f.readlines()
                        return lines[4].split(',')[1]
        else:
                return "nil"


def setSessionClassification(userid,classification):
        print "set session"
        filename="sessions/"+userid+".tx"
        lines=""
        if os.path.isfile(filename):
                with open(filename) as f:
                        lines = f.readlines()
                        lines[0]=userid+","+classification+"\n"
                with open(filename,'w')as f:
                        f.writelines(lines)
        else:
                file = open(filename,'w')
                file.write(userid+","+classification+"\n")
                file.close()


def setIntentSteps(userid,step,classification):
        print "set session for ",userid,",",step,",",classification
        filename="sessions/"+userid+".tx"
	lines=""
        if os.path.isfile(filename):
                with open(filename) as f:
                        lines = f.readlines()
                        lines[1]=userid+","+step+"\n"
		with open(filename,'w') as f:
			f.writelines(lines)
        else:
                file = open(filename,'w')
                file.write(userid+","+classification+"\n"+userid+",step1\n")
                file.close()




def writeToSummary(userid,key,value):
	filename=userid+"_transaction.sum"
	f=open(filename,"a+")
	f.write(key+" : "+value+"\n")

#this function reads the conversation file based on steps and perform the corresponding action and return the response
def getConversationResponse(userid,username,step,inputText):
	print "inside get Conversation response  ",step," : ",inputText
        with open("proofConversation.cv") as f:
                lines=f.readlines()
                for line in lines:
			print line.split(",")[0]
			print "checking if ",line.split(",")[0]," equals ",step
			checkFile=str(line.split(",")[0]).strip()
			step=step.strip()
                        if(checkFile==step):
                                reply=line.split(",")[1].strip()
				print step," : ",reply
				if(reply=="checkAccount"):
					f=0
					acno=-1
					classifiedText=getClassifiedText(userid)
					print "classified text:",classifiedText
					classifiedText=classifiedText.replace("\n","")
					for each in classifiedText.split(" "):
						print each
						if each.isdigit():
							f=1
							acno=int(each)
							print "yes"
							break
						else:
							print "no"
					if(f==0):
						for each in inputText.split(" "):
							if each.isdigit():
								f=1
								acno=int(each)
								break
					
					if(f==0):
						reply="Sure.. Incoming payments are always good. I have detected that you have multiple debit accounts"
						reply=reply+"\nCan you tell me the debit account no you want the statement for ?"
					elif(f==1):
						reply="Sure.. Incoming payments are always good. I have detected that you have multiple debit accounts"
						pdfGenerator.createAccountConfirmationPDF(userid,str(acno),"LU46034000067895346",username,"USD","CITILUX")
						reply="next"
						stepCount=step[4:]
						stepCount=int(stepCount)
						stepCount=stepCount+1
						setIntentSteps(userid,"step"+str(stepCount),"Account Proof")
					return reply
				
                                elif(reply=="checkMail"):
					if("mail" in inputText.lower()):
						emailSend.sendMail('bittu.raju@cognizant.com','Account Proof.pdf')
						reply="Yeah Sure.. You will recieve a copy of this on your registered email address\n Is there anything else i can help you with ?"
					else:
						reply="ok"					
					setSessionClassification(userid,"nil")
                                        setIntentSteps(userid,"step1","nil")

					return reply
				else:
					stepCount=step[4:]
					stepCount=int(stepCount)
					stepCount=stepCount+1
					setIntentSteps(userid,"step"+str(stepCount),"Account Proof")
					return reply


				



