import os
import os.path
import datetime
import requests

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
        filename=userid+"_transfer.sum"
        f=open(filename,"a+")
        f.write(key+" : "+value+"\n")


def getConversationResponse(userid,step,inputText):
        print "inside get Conversation response  ",step," : ",inputText
        with open("accountConversation.cv") as f:
                lines=f.readlines()
                for line in lines:
                        print line.split(",")[0]
                        print "checking if ",line.split(",")[0]," equals ",step
                        checkFile=str(line.split(",")[0]).strip()
                        step=step.strip()
                        if(checkFile==step):
                                reply=line.split(",")[1].strip()
                                print step," : ",reply
                                if(reply=="checkAccountType"):
					if("saving" in inputText.lower() or "savings" in inputText.lower() or "debit" in inputText.lower()):
						reply="your savings account balance is 10000"
						setSessionClassification(userid,"nil")
                                                setIntentSteps(userid,"step1","nil")
                                                
                                        elif("credit" in inputText.lower()):
						reply="your credit account balance is 12000"
 						setSessionClassification(userid,"nil")
                                                setIntentSteps(userid,"step1","nil")
					else:
						reply="Please specify the account type"


					return reply				

def getReply(userid,step,inputText):
	if("saving" in inputText.lower() or "savings" in inputText.lower() or "debit" in inputText.lower()):
        	reply="your savings account balance is 10000"
                setSessionClassification(userid,"nil")
                setIntentSteps(userid,"step1","nil")
        elif("credit" in inputText.lower()):
        	reply="your credit account balance is 12000"
                setSessionClassification(userid,"nil")
                setIntentSteps(userid,"step1","nil")
        else:
                reply="Please specify the account type"


        return reply

