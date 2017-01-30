import os
import os.path
import requests
import datetime
import emailSend
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
def getConversationResponse(userid,step,inputText):
	print "inside get Conversation response  ",step," : ",inputText
        with open("videoConversation.cv") as f:
                lines=f.readlines()
                for line in lines:
			print line.split(",")[0]
			print "checking if ",line.split(",")[0]," equals ",step
			checkFile=str(line.split(",")[0]).strip()
			step=step.strip()
                        if(checkFile==step):
                                reply=line.split(",")[1].strip()
				print step," : ",reply
                                if(reply=="checkMail"):
					if("mail" in inputText.lower()):
						emailSend.sendMail('bittu.raju@cognizant.com','Account Proof.pdf')
						reply="next"
						stepCount=step[4:]
						stepCount=int(stepCount)
						stepCount=stepCount+1
						setIntentSteps(userid,"step"+str(stepCount),"Start video")
					else:
						setSessionClassification(userid,"nil")
	                                        setIntentSteps(userid,"step1","nil")
						reply="ok"					

					return reply
				elif (reply=="checkConfirmation"):
					if("yes" in inputText.lower() or "proceed" in inputText.lower()):
						reply="Ok"
                     				setSessionClassification(userid,"nil")
                                                setIntentSteps(userid,"step1","nil")

					elif("no" in inputText.lower()):
						reply="Got it. You can still get your account statement from the above link and you can see video on how to do it.\n\nIs there anything else i can do ?"
						setSessionClassification(userid,"nil")
                                                setIntentSteps(userid,"step1","nil")

					else:
						reply="Do you want to proceed (yes/no)"
					return reply
				else:
					stepCount=step[4:]
					stepCount=int(stepCount)
					stepCount=stepCount+1
					setIntentSteps(userid,"step"+str(stepCount),"Start video")
					return reply


				



