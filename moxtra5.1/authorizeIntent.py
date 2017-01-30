import os
import os.path
import requests
from datetime import datetime
import re
import emailSend
import citiService
import pickle
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


def hasNumbers(inputString):
        return any(char.isdigit() for char in inputString)


def writeToSummary(userid,key,value):
	filename=userid+"_transaction.sum"
	f=open(filename,"a+")
	f.write(key+" : "+value+"\n")

#this function reads the conversation file based on steps and perform the corresponding action and return the response
def getConversationResponse(userid,step,inputText):
	print "inside get Conversation response  ",step," : ",inputText
        with open("authorizeConversation.cv") as f:
                lines=f.readlines()
                for line in lines:
			print line.split(",")[0]
			print "checking if ",line.split(",")[0]," equals ",step
			checkFile=str(line.split(",")[0]).strip()
			step=step.strip()
                        if(checkFile==step):
                                reply=line.split(",")[1].strip()
				print step," : ",reply
                                if(reply=="checkDateRange"):
					transactionList=citiService.getTransaction("jd12345")
					if("last week" in inputText.lower()):
						fromDate="01-11-2016"	
						from datetime import datetime as dt
						fromDate = dt.strptime(str(fromDate), "%d-%m-%Y")
						print fromDate
						fromDate=fromDate.strftime('%d/%m/%Y')
						print fromDate
						###to date ###
						toDate="30-11-2016"	
						toDate = dt.strptime(str(toDate), "%d-%m-%Y")
						toDate=toDate.strftime('%d/%m/%Y')
						print toDate
						fromDate = dt.strptime(str(fromDate), "%d/%m/%Y")
						toDate = dt.strptime(str(toDate), "%d/%m/%Y")

						count=0
						transactionList=citiService.getTransaction("jd12345")
						paymentList=[]
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
							reply="Found "+str(len(paymentList))+" transactions from last week where remitter bank wants to modify the payment"
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
								

					elif ("last" in inputText.lower() and "day" in inputText.lower()):
						toDate="27-11-2016"	
						from datetime import datetime as dt
						toDate = dt.strptime(str(toDate), "%d-%m-%Y")
						toDate=toDate.strftime('%d/%m/%Y')
						print toDate
						toDate = dt.strptime(str(toDate), "%d/%m/%Y")
						paymentList=[]
						count=0
						for transaction in transactionList:
							transDate=transaction['date'].split(" ")[0]
							transDate=transDate.strip()
							print "tRANS dTAE :",transDate
							from datetime import datetime as dt
							transDate = dt.strptime(transDate, "%d/%m/%Y")
							if(transDate==toDate):
								transaction["no"]=count+1		
								paymentList.append(transaction)
								count=count+1
						if len(paymentList)==0:
							reply="Sorry. i cant find a payment in this date range. Thanks for using Hello Citi."
							setSessionClassification(userid,"nil")
                	                                setIntentSteps(userid,"step1","nil")
						else:
							reply="Found "+str(len(paymentList))+" transactions from "+str(toDate)+" where remitter bank wants to modify the payment"
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
					else:
						r = re.compile('(.*?)on(.*?)where(.*?)')
						m = r.search(inputText.lower()) 
						if m:
							fromDate=m.group(2).strip()

							dateObj=datetime.strptime(fromDate, '%d-%b-%Y')
							fromDate=dateObj.strftime('%d/%m/%Y') 
							from datetime import datetime as dt
							fromDate = dt.strptime(str(fromDate), "%d/%m/%Y")
							count=0
							transactionList=citiService.getTransaction("jd12345")
							paymentList=[]
							for transaction in transactionList:
								transDate=transaction['date'].split(" ")[0]
								transDate=transDate.strip()
								print "tRANS dTAE :",transDate
								from datetime import datetime as dt
								transDate = dt.strptime(transDate, "%d/%m/%Y")
								if(transDate==fromDate):
									transaction["no"]=count+1		
									paymentList.append(transaction)
									count=count+1
							if len(paymentList)==0:
								reply="Sorry. i cant find a payment in this date range."
							else:
								reply="Found "+str(len(paymentList))+" transactions from "+str(fromDate)+"where remitter bank wants to modify the payment"
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

						else:						
							reply="I am not able to find a transaction for the entered date range"
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
							#serializing the single payment
							output = open(userid+'.pkl', 'wb')
					        	pickle.dump(each, output)
					        	output.close()

							#reply="Got it. Here is the payment you were looking for\n"
							#ans="\n Beneficiary Name : "+str(each["beneficiaryName"])
							#ans=ans+"\n Account : "+str(each["account"])
							#ans=ans+"\n Amount : "+str(each["amount"])
							#ans=ans+"\n Date : "+str(each["date"])
							#ans=ans+"\n\n Status : "+str(each['status'])
							#reply=reply+ans
							#reply=reply+"\n Is there anything else i can do ?"
							f=1
							#setSessionClassification(userid,"nil")
	               	                                #setIntentSteps(userid,"step1","nil")

							break
					if(f==0):
						reply= "please enter a valid number \n"
						for each in paymentList:
							ans="\n"+str(each["no"])+"\n Beneficiary Name : "+str(each["beneficiaryName"])
							ans=ans+"\n Account : "+str(each["account"])
							ans=ans+"\n Date : "+str(each["date"])
							reply=reply+ans
					elif(f==1):
						reply="You can authorize or reject the request to stop payment\n1.Authorize stop\n2.Reject request"
						stepCount=step[4:]
						stepCount=int(stepCount)
						stepCount=stepCount+1
						setIntentSteps(userid,"step"+str(stepCount),"Authorize stop")


					return reply
				elif(reply=="askConfirmation"):
					if("yes" in inputText.lower() or "auth" in inputText.lower() or "1" in inputText.lower()):
						pkl_file = open(userid+'.pkl', 'rb')
					        payment = pickle.load(pkl_file)
					        pkl_file.close()
						payment["requestType"]="auth"
						output = open(userid+'.pkl', 'wb')
			        		pickle.dump(payment, output)
				        	output.close()
						classifiedText=getClassifiedText(userid)
						if("stop" in classifiedText.lower()):
							reply="You have chosen to stop a payment as per the remitter bank request (yes/no)?"
						else:
							reply="You have chosen to authorize stop a payment as per the remitter bank request."
							reply=reply+"\nYou have agreed for citi to debit your account for usd 45698.12 and return funds to the remitter bank."
							reply=reply+"\n\n Confirm(yes/no)"
						stepCount=step[4:]
						stepCount=int(stepCount)
						stepCount=stepCount+1
						setIntentSteps(userid,"step"+str(stepCount),"Authorize stop")

					elif("no" in inputText.lower() or "reject" in inputText.lower() or "2" in inputText.lower()):
						pkl_file = open(userid+'.pkl', 'rb')
					        payment = pickle.load(pkl_file)
					        pkl_file.close()
						payment["requestType"]="reject"
						output = open(userid+'.pkl', 'wb')
			        		pickle.dump(payment, output)
			        		output.close()
						reply="you have chosen to reject the request.would you like to proceed(yes/no)?"
						stepCount=step[4:]
						stepCount=int(stepCount)
						stepCount=stepCount+1
						setIntentSteps(userid,"step"+str(stepCount),"Authorize stop")

					else:
						reply="You can authorize or reject the request to stop payment\n1.Authorize stop\n2.Reject request"
					return reply
				elif(reply=="againConfirmation"):
					if("yes" in inputText.lower()):
						reply="Please provide an optional note"
						stepCount=step[4:]
						stepCount=int(stepCount)
						stepCount=stepCount+1
						setIntentSteps(userid,"step"+str(stepCount),"Authorize stop")
					elif("no" in inputText.lower()):
						reply="Cancelling the transaction"
						setSessionClassification(userid,"nil")
        	     	                        setIntentSteps(userid,"step1","nil")
					else:
						reply="Confirm yes/no"
					return reply


				elif(reply=="optionalNote"):
					pkl_file = open(userid+'.pkl', 'rb')
				        payment = pickle.load(pkl_file)
				        pkl_file.close()
					payment["notes"]=inputText
					reqType=payment["requestType"]
					output = open(userid+'.pkl', 'wb')
			        	pickle.dump(payment, output)
			        	output.close()
					stepCount=step[4:]
					stepCount=int(stepCount)
					stepCount=stepCount+1
					setIntentSteps(userid,"step"+str(stepCount),"Authorize stop")
					print "****************************reqType :",reqType
					if(reqType=="auth"):
						reply="Confirm stopping payment (yes/no)?"
					elif(reqType=="reject"):
						reply="Confirm rejecting request (yes/no)?"
					return reply
				elif(reply=="reConfirmation"):
					pkl_file = open(userid+'.pkl', 'rb')
				        payment = pickle.load(pkl_file)
				        pkl_file.close()
					reqType=payment["requestType"]
					output = open(userid+'.pkl', 'wb')
			        	pickle.dump(payment, output)
			        	output.close()

					if("yes" in inputText.lower()):
						if(reqType=="auth"):
							reply="You have requested authorize stop. Thanks for using hello citi."
						elif(reqType=="reject"):
							reply="Done. Your request has been rejected."
					elif("no" in inputText.lower()):
						reply="Cancelling the transaction"
					setSessionClassification(userid,"nil")
             	                        setIntentSteps(userid,"step1","nil")
					return reply

				else:
					stepCount=step[4:]
					stepCount=int(stepCount)
					stepCount=stepCount+1
					setIntentSteps(userid,"step"+str(stepCount),"Authorize stop")
					return reply


				



