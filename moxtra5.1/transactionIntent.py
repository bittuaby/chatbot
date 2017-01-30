import os
import os.path
import requests
import datetime
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
        with open("transactionConversation.cv") as f:
                lines=f.readlines()
                for line in lines:
			print line.split(",")[0]
			print "checking if ",line.split(",")[0]," equals ",step
			checkFile=str(line.split(",")[0]).strip()
			step=step.strip()
                        if(checkFile==step):
                                reply=line.split(",")[1].strip()
				print step," : ",reply
                                if(reply=="checkPreFormat"):
					r=requests.get('http://vsgupta.in/IoT/xcbivnmit445lizqTTly/viewallpreformat.php')
				        var=r.json()
        				code_list=[]
        				for i in var['preformatcode']:
	    					code_list.append(i['code'])
					f=0
                                        for code in code_list:
                                                if code in inputText.lower():
							f=1
                                                        writeToSummary(userid,"Pre Format Code",code)
                                                        reply="next"
                                                        stepCount=step[4:]
                                                        stepCount=int(stepCount)
                                                        stepCount=stepCount+1
                                                        setIntentSteps(userid,"step"+str(stepCount),"Transaction intent")
							break
					if (f==1):
						reply="next"
                                        else:
						reply="Sorry it didn't match. Enter preformat code again"
                                        return reply
                                elif(reply=="checkBeneficiary"):
					ben_list=[]
        				r=requests.get('http://vsgupta.in/IoT/xcbivnmit445lizqTTly/viewcorporatepayee.php')
        				var=r.json()

        				for i in var['corporatepayee']:
            					ben_list.append(i['benename'])
					f=0
                                        for ben in ben_list:
                                                if ben.lower() in inputText.lower():
                                                        f=1
                                                        writeToSummary(userid,"Beneficiary",ben)
                                                        reply="next"
                                                        stepCount=step[4:]
                                                        stepCount=int(stepCount)
                                                        stepCount=stepCount+1
                                                        setIntentSteps(userid,"step"+str(stepCount),"Transaction intent")
                                                        break
                                        if (f==1):
                                                reply="next"
                                        else:
                                                reply="Sorry it didn't match. Enter Beneficiary Name again"
                                        return reply
				elif(reply=="checkCurrency"):
					cur_list=[]
    	
    					r=requests.get('http://www.vsgupta.in/IoT/xcbivnmit445lizqTTly/viewcurrency.php')
        				var=r.json()

    					for i in var['currencyavailable']:
    	    					cur_list.append(i['curr'].lower())
					f=0
					for cur in cur_list:
                                                if cur.lower() in inputText.lower():
                                                        f=1
                                                        writeToSummary(userid,"Currency",cur)
                                                        reply="next"
                                                        stepCount=step[4:]
                                                        stepCount=int(stepCount)
                                                        stepCount=stepCount+1
                                                        setIntentSteps(userid,"step"+str(stepCount),"Transaction intent")
                                                        break
                                        if (f==1):
                                                reply="next"
                                        else:
                                                reply="Sorry it didn't match. Enter Currency again"
                                        return reply
				elif(reply=="checkDate"):
					if ("today" in inputText.lower() or "now" in inputText.lower()):
						date=datetime.datetime.now()
						writeToSummary(userid,"Date",str(date))
                                                reply="next"
                                                stepCount=step[4:]
                                                stepCount=int(stepCount)
                                                stepCount=stepCount+1
                                                setIntentSteps(userid,"step"+str(stepCount),"Transaction intent")
					else:
						writeToSummary(userid,"Date",inputText)
                                                reply="next"
                                                stepCount=step[4:]
                                                stepCount=int(stepCount)
                                                stepCount=stepCount+1
                                                setIntentSteps(userid,"step"+str(stepCount),"Transaction intent")

					return reply

				elif(reply=="checkDetails"):
                                	writeToSummary(userid,"Details",inputText)
                                        reply="next"
                                        stepCount=step[4:]
                                        stepCount=int(stepCount)
                                        stepCount=stepCount+1
                                        setIntentSteps(userid,"step"+str(stepCount),"Transaction intent")

                                        return reply

				elif(reply=="checkAmount"):
					text=inputText.lower().split(" ")
					amount=0
					f=0
					for word in text:
						if str(word).isdigit():
							amount=word
							f=1
							break
					if(f==1):
						writeToSummary(userid,"Amount",amount)
                                                reply="next"
						stepCount=step[4:]
						stepCount=int(stepCount)
						stepCount=stepCount+1
						setIntentSteps(userid,"step"+str(stepCount),"Transaction intent")

                                        else:
                                                reply="Please specify the amount"
                                        return reply
				elif (reply=="checkConfirmation"):
					if("yes" in inputText.lower() or "ok" in inputText.lower()):
					 	reply="next"
                                                stepCount=step[4:]
                                                stepCount=int(stepCount)
                                                stepCount=stepCount+1
                                                setIntentSteps(userid,"step"+str(stepCount),"Transaction intent")
					elif("no" in inputText.lower()):
						reply="Transaction cancelled. Thanks for using Citi Bank."
                                        	setSessionClassification(userid,"nil")
                                        	setIntentSteps(userid,"step1","nil")
                                        	delname=userid+"_transaction.sum"
                                        	os.remove(delname)
					else:
						reply="please confirm the payment (yes/no)"
						
					return reply

				else:
					stepCount=step[4:]
					stepCount=int(stepCount)
					stepCount=stepCount+1
					setIntentSteps(userid,"step"+str(stepCount),"Transaction intent")
					if (stepCount==14):
						fname="sessions/"+userid+".tx"
						with open(fname) as f:
							lines=f.readlines()
							username=lines[2].split(",")[1]
							writeToSummary(userid,"Account Name",username)
							acno=lines[3].split(",")[1]
							writeToSummary(userid,"Account Number",acno)
                                        	filename=userid+"_transaction.sum"
                                        	with open(filename) as f:
                                                	reply=reply+"\n\n"+str(f.readlines())
					if(stepCount==16):
                                        	setSessionClassification(userid,"nil")
                                        	setIntentSteps(userid,"step1","nil")
                                        	delname=userid+"_transaction.sum"
                                        	os.remove(delname)

					return reply


				



