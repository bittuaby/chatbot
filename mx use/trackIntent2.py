import os
import os.path
import requests
from datetime import datetime
import re
import emailSend
import citiService
import pickle
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


def hasNumbers(inputString):
        return any(char.isdigit() for char in inputString)


def writeToSummary(userid,key,value):
	filename=userid+"_transaction.sum"
	f=open(filename,"a+")
	f.write(key+" : "+value+"\n")

#this function reads the conversation file based on steps and perform the corresponding action and return the response
def getConversationResponse(userid,step,inputText):
	print "inside get Conversation response  ",step," : ",inputText
        with open("trackConversation.cv") as f:
                lines=f.readlines()
                for line in lines:
			print line.split(",")[0]
			print "checking if ",line.split(",")[0]," equals ",step
			checkFile=str(line.split(",")[0]).strip()
			step=step.strip()
                        if(checkFile==step):
                                reply=line.split(",")[1].strip()
				print step," : ",reply
                                if(reply=="checkNumbers"):
					if(hasNumbers(inputText)):
						#check 2 conditions
						#i want to know status of payment made to abc holdings for 2000 eur last month
						r1 = re.compile('(.*?)to(.*?)to(.*?)for(.*?)last month')
						m1 = r1.search(inputText.lower())
						r2 = re.compile('(.*?)to(.*?)for(.*?)last month')
						m2 = r2.search(inputText.lower())

						if("last month" in inputText.lower())or("lastmonth" in inputText.lower()):
							if (m1):
								benef=m.group(3).strip()
								amount=m.group(4).strip()
								amount=amount.split(" ")[0]
								now=datetime.datetime.now()
								if(now.month!=1)
									fromDate="01-"+str(now.month-1)+"-"+str(now.year)	
								else
									fromDate="01-12-"+str(now.year-1)	
								from datetime import datetime as dt
								fromDate = dt.strptime(str(fromDate), "%d/%m/%Y")
								print fromDate
	
				
						print "2"
					else:
						reply="Got it.I would first like to locate your payment.How would you like to search for this payment\n"
						reply=reply+"\n1.Most Recent\n2.Largest\n3.Direct Search"
						stepCount=step[4:]
						stepCount=int(stepCount)
						stepCount=stepCount+1
						setIntentSteps(userid,"step"+str(stepCount),"Track payment")
					return reply
				elif(reply=="checkEntry"):
					if("3" in inputText.lower()):
						reply= "Okay.How would you further like to search this.Select one of the following\n"
						reply=reply+"\n1.By Value Date\n2.Input Data"
						stepCount=step[4:]
						stepCount=int(stepCount)
						stepCount=stepCount+1
						setIntentSteps(userid,"step"+str(stepCount),"Track payment")
					elif("2" in inputText.lower() or "1" in inputText.lower()):
						reply="Sorry. I am not able to handle this request at the moment"
						setSessionClassification(userid,"nil")
                                                setIntentSteps(userid,"step1","nil")
					else:
						reply="Please select a valid number (1-3)\n1.Most Recent\n2.Largest\n3.Direct Search"
					return reply
				elif(reply=="checkSearchType"):
					if("1" in inputText.lower()):
						reply= "Sure.. Enter the date range to search from (max 90 days)"
						stepCount=step[4:]
						stepCount=int(stepCount)
						stepCount=stepCount+1
						setIntentSteps(userid,"step"+str(stepCount),"Track payment")
					elif("2" in inputText.lower()):
						reply="Sorry. I am not able to handle this request at the moment"
						setSessionClassification(userid,"nil")
                                                setIntentSteps(userid,"step1","nil")
					else:
						reply="Please select a valid number (1-2)\n1.By Value Date\n2.Input Data"
					return reply
				elif(reply=="checkDateRange"):
					r = re.compile('(.*?)to(.*?)from(.*?)to(.*)')
                                        m = r.search(inputText.lower())
					r1 = re.compile('(.*?)to(.*?)for(.*?)last month')
					m1 = r1.search(inputText.lower())
					transactionList=citiService.getTransaction("jd12345")
                                        if m:
						benef=m.group(2).strip()
						fromDate=m.group(3).strip()
						toDate=m.group(4).strip()
						print "beneficiary : ",benef
						print "from : ",fromDate
						print "to : ",toDate
						try:
							dateObj=datetime.strptime(fromDate, '%d-%b-%Y')
							fromDate=dateObj.strftime('%d/%m/%Y')
							dateObj=datetime.strptime(toDate, '%d-%b-%Y')
							toDate=dateObj.strftime('%d/%m/%Y')
							print fromDate,toDate
						except:
							reply="please enter valid dates"
							return reply
						paymentList=[]
						from datetime import datetime as dt
						fromDate = dt.strptime(str(fromDate), "%d/%m/%Y")
						toDate = dt.strptime(str(toDate), "%d/%m/%Y")
						count=0
						for transaction in transactionList:
							transDate=transaction['date'].split(" ")[0]
							transDate=transDate.strip()
							print "tRANS dTAE :",transDate
							from datetime import datetime as dt
							transDate = dt.strptime(transDate, "%d/%m/%Y")
							if(transDate>=fromDate and transDate<=toDate):
								transaction["no"]=count+1		
								paymentList.append(transaction)
								count=count+1
						if len(paymentList)==0:
							reply="Sorry. i cant find a payment in this date range. Thanks for using Hello Citi."
							setSessionClassification(userid,"nil")
                	                                setIntentSteps(userid,"step1","nil")
						else:
							reply="Found "+str(len(paymentList))+" payments according to your search criteria.Select one of these"
							reply=reply+"\n"

							#Serializing the list object to check option next time
							output = open(userid+'.pkl', 'wb')
						        pickle.dump(paymentList, output)
						        output.close()

							for each in paymentList:
								ans="\n"+str(each["no"])+"\n Beneficiary Name : "+str(each["beneficiaryName"])
								ans=ans+"\n Account : "+str(each["account"])
								ans=ans+"\n Date : "+str(each["date"])
								reply=reply+ans
							stepCount=step[4:]
							stepCount=int(stepCount)
							stepCount=stepCount+1
							setIntentSteps(userid,"step"+str(stepCount),"Track payment")


					elif m1:
						benef=m.group(3).strip()
                                                reply="No payments now"
					else:
						reply="Sorry. i cant find a payment in this date range. Thanks for using Hello Citi."
						#setSessionClassification(userid,"nil")
               	                                #setIntentSteps(userid,"step1","nil")
					return reply
				elif(reply=="selectPayment"):
					reply="selecting payments"
					pkl_file = open(userid+'.pkl', 'rb')
				        paymentList = pickle.load(pkl_file)
				        pkl_file.close()
					f=0
					for each in paymentList:
						print each["no"]
						print str(each["no"])
						if(str(each["no"]) in inputText.lower()):
							reply="Got it. Here is the payment you were looking for\n"
							ans="\n Beneficiary Name : "+str(each["beneficiaryName"])
							ans=ans+"\n Account : "+str(each["account"])
							ans=ans+"\n Amount : "+str(each["amount"])
							ans=ans+"\n Date : "+str(each["date"])
							reply=reply+ans
							reply=reply+"\n Is there anything else i can do ?"
							f=1
							setSessionClassification(userid,"nil")
	               	                                setIntentSteps(userid,"step1","nil")

							break
					if(f==0):
						reply= "please enter a valid number \n"
						for each in paymentList:
							ans="\n"+str(each["no"])+"\n Beneficiary Name : "+str(each["beneficiaryName"])
							ans=ans+"\n Account : "+str(each["account"])
							ans=ans+"\n Date : "+str(each["date"])
							reply=reply+ans

					return reply
				else:
					stepCount=step[4:]
					stepCount=int(stepCount)
					stepCount=stepCount+1
					setIntentSteps(userid,"step"+str(stepCount),"Track payment")
					return reply


				



