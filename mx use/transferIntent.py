import os
import os.path
import datetime
import pickle
import requests
import citiService
import re
def getClassifiedText(userid):
        print "get classified text"
        filename="sessions/"+userid+".tx"
        if os.path.isfile(filename):
                with open(filename) as f:
                        lines = f.readlines()
			return lines[4].split(',')[1]
        else:
                return "nil"
def getAccountBalanceFlag(userid):
        print "get classified text"
        filename="sessions/"+userid+".tx"
        if os.path.isfile(filename):
                with open(filename) as f:
                        lines = f.readlines()
			return lines[5].split(',')[1]
        else:
                return "nil"


def setAccountBalanceFlag(userid,value):
        print "set session"
        filename="sessions/"+userid+".tx"
        lines=""
        if os.path.isfile(filename):
                with open(filename) as f:
                        lines = f.readlines()
                        lines[5]=userid+","+str(value)+"\n"
                with open(filename,'w')as f:
                        f.writelines(lines)
        else:
                file = open(filename,'w')
                file.write(userid+","+classification+"\n")
                file.close()
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
	filename=userid+"_transfer.sum"
	f=open(filename,"a+")
	output=[]
	lines=f.readlines()
	for line in lines:
		if(line.split(" : ")[0].lower()!=key.lower()):
			output.append(line)
	output.append(key+" : "+value+"\n")
	f.close()
	os.remove(userid+"_transfer.sum")
	f=open(filename,"a+")
	f.writelines(output)		
	f.close()
	print "wrote details................"
def writeToSummary_old(userid,key,value):
	filename=userid+"_transfer.sum"
	f=open(filename,"a+")
	f.write(key+" : "+value+"\n")
	print "wrote details................"

def getFromSummary(userid,key):
	print "userid:",userid
	with open(userid+"_transfer.sum") as f:
		lines=f.readlines()
		for line in lines:
			if(line.split(" : ")[0].lower()==key.lower()):
				return str(line.split(" : ")[1])
		return 0

def getConversationResponse(userid,username,step,inputText):
	print "inside get Conversation response  ",step," : ",inputText
        with open("transferConversation.cv") as f:
                lines=f.readlines()
                for line in lines:
			print line.split(",")[0]
			print "checking if ",line.split(",")[0]," equals ",step
			checkFile=str(line.split(",")[0]).strip()
			step=step.strip()
                        if(checkFile==step):
                                reply=line.split(",")[1].strip()
				print step," : ",reply
                                if(reply=="checkBotOrLink"):
                                        if("yes" in inputText.lower() or "ok" in inputText.lower()):
						classifiedText=getClassifiedText(userid)
						preformList=citiService.getUserPreformats("jd12345")
						flag=0
						#checking if preformat is already specified
						print "checking ***** preformat in classified text"
						for word in classifiedText.split(" "):
							for preform in preformList:
								if(word.lower().strip()==str(preform["code"].lower())):
                                                        		writeToSummary(userid,"Preformat Code",str(preform["code"]))
                                                        		writeToSummary(userid,"Beneficiary Name",str(preform["beneficiaryName"]))
                                                        		writeToSummary(userid,"Beneficiary Account Number",str(preform["account"]))
									#finding acno if lready present
									acno=-1
									if ("account" in classifiedText.lower())and(hasNumbers(classifiedText)):
										for word in classifiedText.split(" "):
											if word.isdigit():
												acno=word
												break
										if (acno!=-1):
											print "writing account number"	
											setAccountBalanceFlag(userid,1)
			                                                        	writeToSummary(userid,"Account Number",str(acno))
											flag=2
										else:
		                	                                        	writeToSummary(userid,"Account Number","456789393")
									else:
                                                	        		writeToSummary(userid,"Account Number","456789393")

                                                        		writeToSummary(userid,"Bank Routing Code",str(preform["code"]).lower())
									#finding amount if already present
									amount=-1
									if ("amount" in classifiedText.lower() or "eur" in classifiedText.lower()or "usd" in classifiedText.lower())and(hasNumbers(classifiedText)):
										for word in classifiedText.split(" "):
											if word.isdigit():
												amount=int(word)
												break
										if (amount!=-1):	
			                                                        	writeToSummary(userid,"Amount",str(amount).lower())
										else:
		                	                                        	writeToSummary(userid,"Amount",str(preform["amount"]).lower())
									else:
                                                	        		writeToSummary(userid,"Amount",str(preform["amount"]).lower())
                                                        		writeToSummary(userid,"Currency",str(preform["currency"]).lower())
                                                        		writeToSummary(userid,"Account Type","Savings")
									if(flag==0):
										flag=1
									break
						if (flag==0):	
							print "no preformat in classified text........"
							reply="next"
							stepCount=step[4:]
							stepCount=int(stepCount)
							stepCount=stepCount+1
							setIntentSteps(userid,"step"+str(stepCount),"Transfer intent")
						elif(flag==1):
							print "preformat found.."
							reply="next"
							stepCount=step[4:]
							stepCount=int(stepCount)
							stepCount=stepCount+8
							setIntentSteps(userid,"step"+str(stepCount),"Transfer intent")
						#usecase 1.4
						elif(flag==2):
							print "preformat found.. use case 1.4"
							reply="next"
							stepCount=step[4:]
							stepCount=int(stepCount)
							stepCount=stepCount+15
							setIntentSteps(userid,"step"+str(stepCount),"Transfer intent")


							
					elif("no" in inputText.lower()):
						reply="Great.. Here is the link to the web page"
						reply=reply+"\nhttps://www.citidirectbe.com/893489379"
                                        	setSessionClassification(userid,"nil")
                                        	setIntentSteps(userid,"step1","nil")
						setAccountBalanceFlag(userid,0)
                                        	delname=userid+"_transfer.sum"
						if(os.path.isfile(delname)):
                                        		os.remove(delname)

                                        else:
                                                reply="Do you want to proceed through chat bot (yes/no)"
                                        return reply
				elif(reply=="checkSearchPreformat"):
					classifiedText=getClassifiedText(userid)
					if (" to " in classifiedText.lower() and " for " in classifiedText.lower()):
						print "to and for present"
						reply="Would you like to search this in pre formats (yes/no)?"
                                                stepCount=step[4:]
                                                stepCount=int(stepCount)
                                                stepCount=stepCount+1
                                                setIntentSteps(userid,"step"+str(stepCount),"Transfer intent")

				
						
					else:


						r = re.compile('from(.*?)with preformat code(.*?)')
						m = r.search(classifiedText)
						if m:
							print "hshjj ******* regex matched"
							setAccountBalanceFlag(userid,1)
        	                                	reply="next"
	                	                        stepCount=step[4:]
        	                	                stepCount=int(stepCount)
                	                	        stepCount=stepCount+5
                        	                	setIntentSteps(userid,"step"+str(stepCount),"Transfer intent")

						else:
							print "to and for not present"
        	                                	reply="next"
	                	                        stepCount=step[4:]
        	                	                stepCount=int(stepCount)
                	                	        stepCount=stepCount+2
                        	                	setIntentSteps(userid,"step"+str(stepCount),"Transfer intent")
					return reply	
				elif(reply=="SearchPreformat"):
					print "search in preformats*******************"
					classifiedText=getClassifiedText(userid)
					if("yes" in inputText.lower()):
						beneficiaryName=""
						r = re.compile('to(.*?)for')
						m = r.search(classifiedText)
						if m:
							beneficiaryName=str(m.group(1)).strip()
							print "regex matched ",beneficiaryName
						else:
							print "no regex matched"
						
						preformList=citiService.getUserPreformats("jd12345")
						outputList=[]
						if (beneficiaryName !=""):
							for preform in preformList:
								if str(preform["beneficiaryName"]).lower()==beneficiaryName.lower():
									tup=(str(preform['code']),str(preform['beneBankName']))
									outputList.append(tup)
						if(len(outputList)==0):
							reply="next"
                                                	stepCount=step[4:]
	                                                stepCount=int(stepCount)
        	                                        stepCount=stepCount+2
                	                                setIntentSteps(userid,"step"+str(stepCount),"Transfer intent")
						else:
							reply=""
                                                	stepCount=step[4:]
	                                                stepCount=int(stepCount)
        	                                        stepCount=stepCount+2
                	                                setIntentSteps(userid,"step"+str(stepCount),"Transfer intent")

							for output in outputList:
								reply=reply+str(output)+"\n"
							
					elif('no' in inputText.lower()):
                                                reply="Transaction cancelled. Thanks for using Citi Bank."
                                                setSessionClassification(userid,"nil")
                                                setIntentSteps(userid,"step1","nil")

                                                delname=userid+"_transfer.sum"
						if(os.path.isfile(delname)):
	                                                os.remove(delname)
					else:
						reply="Would you like to search this in preformats (yes/no)?"
					return reply

                                elif(reply=="checkPreFormat"):
					flag=0
					classifiedText=getClassifiedText(userid)
					preformList=citiService.getUserPreformats("jd12345")
                                	r = re.compile('search(.*?)where (.*?) is (.*)')
                                        m = r.search(inputText.lower())
                                	r2 = re.compile('(.*?)payment(.*?)to(.*)last month')
                                        m2 = r2.search(inputText.lower())	
					for preform in preformList:
						if str(preform["code"]).lower()==inputText.lower():
                                                        	writeToSummary(userid,"Preformat Code",str(preform["code"]).lower())
                                                        	writeToSummary(userid,"Beneficiary Name",str(preform["beneficiaryName"]).lower())
                                                        	writeToSummary(userid,"Beneficiary Account Number",str(preform["account"]).lower())
                                                        	writeToSummary(userid,"Bank Routing Code",str(preform["code"]).lower())
								amount=-1
								if ("amount" in classifiedText.lower() or "eur" in classifiedText.lower()or "usd" in classifiedText.lower())and(hasNumbers(classifiedText)):
									for word in classifiedText.split(" "):
										if word.isdigit():
											amount=int(word)
											break
									if (amount!=-1):	
		                                                        	writeToSummary(userid,"Amount",str(amount).lower())
									else:
		                                                        	writeToSummary(userid,"Amount",str(preform["amount"]).lower())
								else:
                                                        		writeToSummary(userid,"Amount",str(preform["amount"]).lower())
                                                        	writeToSummary(userid,"Currency",str(preform["currency"]).lower())
                                                        	writeToSummary(userid,"Account Type","Savings")
								flag=1
								#usecase 2.2
								if("able" in classifiedText.lower() and "search" in classifiedText.lower()):
									reply="Found 1 result according to the given input"
									reply=reply+"\n[ "+ str(preform["code"])+", "+str(preform["beneficiaryName"]+"]") 
									return reply

								break

					if flag==1:
							
						reply="next"
                                                stepCount=step[4:]
                                                stepCount=int(stepCount)
						if(" to " in classifiedText.lower() and " for " in classifiedText.lower()):
							stepCount=stepCount+8
						else:
	                                                stepCount=stepCount+4
                                                setIntentSteps(userid,"step"+str(stepCount),"Transfer intent")
                                                #elif inputText.lower()=="show all" or flag==0:
                                        elif inputText.lower()=="show all" :
						print "no pre format found"
                                                preformatList=[]
						preformList=citiService.getUserPreformats("jd12345")
						for preform in preformList:
							tup=(str(preform["code"]).lower(),str(preform["beneBankName"]).lower())
                                                        preformatList.append(tup)

                                                reply="Please select one of the following options"
                                                for each in preformatList:
                                                	reply=reply+"\n"+str(each)
						print "*************************************",reply
					elif("none" in inputText.lower() or "not" in inputText.lower()):
						print "Inside none.."
						pkl_file = open(userid+'_state.pkl', 'rb')
				        	output = pickle.load(pkl_file) 
					        pkl_file.close()
						print "output is :",output
						output=output.strip()
						if (str(output)=="last month"):
							print "print last month"
							reply="Tell me more about this payment.Amount,acno,transaction no"
						elif(str(output)=="search"):
							reply="I am sorry "+str(username)+" .But you have only 2 preformats with beneficiary name ABC Holdings"
							reply=reply+"\nYou can also search by amount,transaction reference or lyc amount."
                                                stepCount=step[4:]
                                                stepCount=int(stepCount)
                                                stepCount=stepCount+1
                                                setIntentSteps(userid,"step"+str(stepCount),"Transfer intent")
					elif("unable" in inputText.lower()):
						reply="Okay"
                                                setSessionClassification(userid,"nil")
                                                setIntentSteps(userid,"step1","nil")
						setAccountBalanceFlag(userid,0)

					elif m:
						reply="next"
                                                stepCount=step[4:]
                                                stepCount=int(stepCount)
                                                stepCount=stepCount+1
                                                setIntentSteps(userid,"step"+str(stepCount),"Transfer intent")
					elif m2:
						output = open(userid+'_state.pkl', 'wb')
					        pickle.dump("last month", output)
					        output.close()
	                                        preformList=citiService.getUserPreformats("jd12345")
						outputList=[]
						beneficiaryName=(m2.group(3)).strip()
	                                        for preform in preformList:
        	                                	if str(preform["beneficiaryName"]).lower()==beneficiaryName.lower():
                	                                	tup=(str(preform['code']),str(preform['beneBankName']))
                        	                                outputList.append(tup)
		
						if len(outputList)==0:
							print "otput list 0"
							reply="next"
		                                        stepCount=step[4:]
                                	                stepCount=int(stepCount)
                                        	       	stepCount=stepCount+1
                                                	setIntentSteps(userid,"step"+str(stepCount),"Transfer intent")
			                               	reply="searchPayments"
						else:
							reply="Found "+str(len(outputList))+" results as per your details.Please select one of the following options\n"
							reply=reply+"\n"+str(outputList)
					elif flag==0:
	                                	reply="I am unable to find a template with the code you enetered.\nMake sure you are entering the right code\n"
								
                                	return reply
				elif(reply=="secondCheckPreformat"):
					print "inside second preformat check"
                                	r = re.compile('search(.*?)where(.*?)is(.*)')
					print "inputText :",inputText
                                        m = r.search(inputText.lower())
                                        preformList=[]
                                        preformList=citiService.getUserPreformats("jd12345")
					beneficiaryName=""
					#usecase2.3- i had created another last month to make payment to atd
                                	r2 = re.compile('(.*?)to(.*)')
	                                m2 = r2.search(inputText.lower())
                                	r3 = re.compile('(.*?)to(.*?)to(.*)')
	                                m3 = r3.search(inputText.lower())

                                        if m:
						print "matched regex : search where.."
                                        	beneficiaryName=str(m.group(3)).strip()
						output = open(userid+'_state.pkl', 'wb')
					        pickle.dump("search", output)
					        output.close()

						print "beneficiary name:",beneficiaryName
                                                outputList=[]
                                                if (beneficiaryName !=""):
	                                                for preform in preformList:
        	                                        	if str(preform["beneficiaryName"]).lower()==beneficiaryName.lower():
                	                                        	tup=(str(preform['code']),str(preform['beneBankName']))
                        	                                        outputList.append(tup)
		
							if len(outputList)==0:
								print "otput list 0"
								reply="next"
		                                                stepCount=step[4:]
                                	        	        stepCount=int(stepCount)
                                        	        	stepCount=stepCount+1
                                                		setIntentSteps(userid,"step"+str(stepCount),"Transfer intent")
			                                	reply="searchPayments"
							else:
								reply="Found "+str(len(outputList))+" results according to the given input."
								reply=reply+"\n"+str(outputList)
                		                                stepCount=step[4:]
                                		                stepCount=int(stepCount)
								#checking pre formats
                                                		stepCount=stepCount-1
		                                                setIntentSteps(userid,"step"+str(stepCount),"Transfer intent")

						else:
                	                        	reply="SearchPayments"
					#checking 2.1 if amount> entered amount
					#Do u want me to search for all payments to abc holdings above 400 euros
					elif hasNumbers(inputText):
                                        	amount=-1
                                                for word in inputText.split(" "):
                                                	if word.isdigit():
                                                        	amount=int(word)
								break
						if amount !=-1:
							reply="Do you want me to search for all payments to ABC Holdings above "+str(amount)+" euros ?(yes/no)"
							outputList=[]
							for preform in preformList:
                                                		if int(preform["amount"])>=amount and str(preform['beneBankName']).lower()=="abc holdings":
	                                                                outputList.append(preform) 
								output = open(userid+'.pkl', 'wb')
							        pickle.dump(outputList, output)
							        output.close()
		                                                stepCount=step[4:]
                                	        	        stepCount=int(stepCount)
                                        	        	stepCount=stepCount+1
                                                		setIntentSteps(userid,"step"+str(stepCount),"Transfer intent")

#							if len(outputList)==0:
#								print "otput list 0"
#								reply="next"
#		                                                stepCount=step[4:]
#                                	        	        stepCount=int(stepCount)
#                                        	        	stepCount=stepCount+1
#                                                		setIntentSteps(userid,"step"+str(stepCount),"Transfer intent")
#			                                	reply="searchPayments"
#							else:
#								reply=reply+"\n"+str(outputList)
#                		                                stepCount=step[4:]
#                                		                stepCount=int(stepCount)
								#checking pre formats
#                                                		stepCount=stepCount-1
#		                                                setIntentSteps(userid,"step"+str(stepCount),"Transfer intent")
						else:
                	                        	reply="SearchPayments"


                                                        #find preformats with amt
					
					elif m2 or m3:
						if(m3):
							benef=str(m3.group(3)).strip()
						elif m2:
							benef=str(m2.group(2)).strip()
						if("last month" in inputText.lower()):
							reply="Do you want me to search for all payments made to "+str(benef)+" last month ?"
						else:
							reply="Do you want me to search for all payments made to "+str(benef)+" ?"
                                                stepCount=step[4:]
                            	        	stepCount=int(stepCount)
                                        	stepCount=stepCount+1
                                                setIntentSteps(userid,"step"+str(stepCount),"Transfer intent")



                                        else:
                                		r = re.compile('(.*?)payment to(.*)')
                                        	m = r.search(inputText.lower())
						if m:
							reply="Do you want me to search for all payments made to "+str(m.group(2).strip())+" last month.(yes/no)"
						else:
                                        		reply="SearchPayments"
                                        return reply
				elif (reply=="confirmSearch"):
					print "inside confirm search"
					pkl_file = open(userid+'_state.pkl', 'rb')
			        	patternString = pickle.load(pkl_file) 
				        pkl_file.close()

					if("yes" in inputText.lower() or "ok" in inputText.lower()):
						if (str(patternString)=="last month"):
							pkl_file = open(userid+'.pkl', 'rb')
					        	outputList = pickle.load(pkl_file) 
						        pkl_file.close()
							if(len(outputList)==0):
								reply="Sorry . I am unable to find any .."
	                                	        	setSessionClassification(userid,"nil")
                                        			setIntentSteps(userid,"step1","nil")
							else:
								reply="Is this the payment you were looking for ?"
								reply=reply+"\n"
								for output in outputList:
									ans="Beneficiary Name : "+str(output["beneficiaryName"]+"\n")
									ans=ans+"Beneficiary Account Number : "+str(output["account"]+"\n")
									ans=ans+"Bank Routing code : "+str(output["code"]+"\n")
									ans=ans+"Amount : "+str(output["amount"]+"\n")
								reply=reply+ans
		                                                stepCount=step[4:]
                	               	        	        stepCount=int(stepCount)
                        	               	        	stepCount=stepCount+1
                                	               		setIntentSteps(userid,"step"+str(stepCount),"Transfer intent")
						elif(str(patternString)=="search"):
							reply="No payment was made last month to ABC Holdings last month\n Is there anything else i can do ?"	
	                                                setSessionClassification(userid,"nil")
        	                                        setIntentSteps(userid,"step1","nil")
							setAccountBalanceFlag(userid,0)
					return reply
				elif(reply=="reConfirmSearch"):
						pkl_file = open(userid+'.pkl', 'rb')
				        	outputList = pickle.load(pkl_file) 
					        pkl_file.close()
						preform=outputList[0]
                                                writeToSummary(userid,"Preformat Code",str(preform["code"]).lower())
                                                writeToSummary(userid,"Beneficiary Name",str(preform["beneficiaryName"]).lower())
                                                writeToSummary(userid,"Beneficiary Account Number",str(preform["account"]).lower())
                                                writeToSummary(userid,"Bank Routing Code",str(preform["code"]).lower())
						amount=-1
						if ("amount" in inputText.lower() or "eur" in inputText.lower()or "usd" in inputText.lower())and(hasNumbers(inputText)):
							for word in inputText.split(" "):
								if word.isdigit():
									amount=int(word)
									if (amount!=-1):	
										print "wrote amount "+str(amount)
		                                                        	writeToSummary(userid,"Amount",str(amount).lower())
									else:
										print "wrote defaut amt -1"
		                                                        	writeToSummary(userid,"Amount",str(preform["amount"]).lower())
									break
						else:
                                                	writeToSummary(userid,"Amount",str(preform["amount"]).lower())
							print "wrote default amt"
                                                writeToSummary(userid,"Currency",str(preform["currency"]).lower())
                                                writeToSummary(userid,"Account Type","Savings")

	                                        stepCount=step[4:]
                             	        	stepCount=int(stepCount)
                                       	        stepCount=stepCount+9
                                               	setIntentSteps(userid,"step"+str(stepCount),"Transfer intent")
						reply="next"
						return reply



				elif(reply=="checkDate"):
					if("today" in inputText.lower() or "now" in inputText.lower()):
						date=datetime.datetime.now()
						writeToSummary(userid,"Date",str(date))
                                                reply="next"
                                                stepCount=step[4:]
                                                stepCount=int(stepCount)
                                                stepCount=stepCount+1
                                                setIntentSteps(userid,"step"+str(stepCount),"Transfer intent")
					else:
						writeToSummary(userid,"Date",inputText.lower())
                                                reply="next"
                                                stepCount=step[4:]
                                                stepCount=int(stepCount)
                                                stepCount=stepCount+1
                                                setIntentSteps(userid,"step"+str(stepCount),"Transfer intent")

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
                                                reply="what is the currency"
						stepCount=step[4:]
						stepCount=int(stepCount)
						stepCount=stepCount+1
						setIntentSteps(userid,"step"+str(stepCount),"Transfer intent")

                                        else:
                                                reply="Please specify the amount"
                                        return reply
				elif(reply=="checkCurrency"):
					writeToSummary(userid,"Currency",inputText)
                                        reply="next"
					stepCount=step[4:]
					stepCount=int(stepCount)
					stepCount=stepCount+1
					setIntentSteps(userid,"step"+str(stepCount),"Transfer intent")
					return reply

				elif(reply=="checkAccountBalance"):
					print "inside check account balance"
					flag=getAccountBalanceFlag(userid)
					print "888888888888888acntbalflag",flag
					if (flag.strip()=="1"):
						amount=getFromSummary(userid,"amount")
						print amount
						if (int(amount)<=500):
							print "amount is less than 500 .",str(amount)
	                                        	reply="next"
		                                        stepCount=step[4:]
		                                        stepCount=int(stepCount)
		                                        stepCount=stepCount+2
		                                        setIntentSteps(userid,"step"+str(stepCount),"Transfer intent")
						else:
							reply="Sorry.. You cant make this payment.\nThe payment amount "+str(amount)+"is exceeding the debit account balance which is EUR 500"
							reply=reply+"\n\n Do you want to change the amount for this payment (yes/no)"
		                                        stepCount=step[4:]
		                                        stepCount=int(stepCount)
		                                        stepCount=stepCount+1
		                                        setIntentSteps(userid,"step"+str(stepCount),"Transfer intent")

		
					else:
	                                        reply="next"
	                                        stepCount=step[4:]
	                                        stepCount=int(stepCount)
	                                        stepCount=stepCount+2
	                                        setIntentSteps(userid,"step"+str(stepCount),"Transfer intent")
					return reply

				elif(reply=="checkAmountChange"):
					print "check amount change"
					if("yes" in inputText.lower() and hasNumbers(inputText)):
						inputList=inputText.split(" ")
						f=0
						for word in inputList:
							if(word.isdigit()):
								if(int(word)<=500):
									writeToSummary(userid,"Amount",word)
									f=1
									break
						if f==1:
                		                        reply="next"
                                		        stepCount=step[4:]
		                                        stepCount=int(stepCount)
                		                        stepCount=stepCount+1
                                		        setIntentSteps(userid,"step"+str(stepCount),"Transfer intent")
						else:
							reply="The payment amount is exceeding the debit account balance which is EUR 500"
							
					elif(hasNumbers(inputText)):
						inputList=inputText.split(" ")
						f=0
						for word in inputList:
							if(word.isdigit()):
								if(int(word)<=500):
									writeToSummary(userid,"Amount",word)
									f=1
									break
						if f==1:
                		                        reply="next"
                                		        stepCount=step[4:]
		                                        stepCount=int(stepCount)
                		                        stepCount=stepCount+1
                                		        setIntentSteps(userid,"step"+str(stepCount),"Transfer intent")
						else:
							reply="The payment amount is exceeding the debit account balance which is EUR 500"
					elif("no" in inputText.lower()):
                                        	setSessionClassification(userid,"nil")
                                        	setIntentSteps(userid,"step1","nil")
						setAccountBalanceFlag(userid,0)

                                        	delname=userid+"_transfer.sum"
                                        	os.remove(delname)
						reply="Cancelling Transaction due to insufficient balance"
					else:
						reply="Do you want to change the amount for this payment (yes\no) /"

						
					return reply
				elif(reply=="checkDetails"):
					writeToSummary(userid,"Details",inputText.lower())
					#checking if date already mentioned
					classifiedText=getClassifiedText(userid)
					if("today" in classifiedText.lower() or "now" in classifiedText.lower()):
						date=datetime.datetime.now()
						writeToSummary(userid,"Date",str(date))
                                                reply="next"
                                                stepCount=step[4:]
                                                stepCount=int(stepCount)
                                                stepCount=stepCount+3
                                                setIntentSteps(userid,"step"+str(stepCount),"Transfer intent")
					else:
						reply="next"
                                                stepCount=step[4:]
                                                stepCount=int(stepCount)
                                                stepCount=stepCount+1
                                                setIntentSteps(userid,"step"+str(stepCount),"Transfer intent")
					return reply
				elif(reply=="checkFutureConfirmation"):
					if("yes" in inputText.lower() or "ok" in inputText.lower()):
                                                setSessionClassification(userid,"nil")
                                                setIntentSteps(userid,"step1","nil")
                                                delname=userid+"_transfer.sum"
                                                os.remove(delname)

                                                reply="Got it\n\nYou will be notified every monday when this payment is made"
                                        elif("no" in inputText.lower()):
                                                setSessionClassification(userid,"nil")
                                                setIntentSteps(userid,"step1","nil")
						setAccountBalanceFlag(userid,0)
                                                delname=userid+"_transfer.sum"
                                                os.remove(delname)

                                                reply="Ok"
                                        else:
                                                reply="Do you want to be notified about future payments (yes/no)"

                                        return reply

				elif(reply=="checkFuturePayments"):
					print "inside check future payments...."
					dayList=["sunday","monday","tuesday","wednesday","thursday","friday","saturday"]
					if "every" in inputText.lower() and (any(day in inputText.lower() for day in dayList)):
						reply="next"
	                                        stepCount=step[4:]
        	                                stepCount=int(stepCount)
                	                        stepCount=stepCount+1
                        	                setIntentSteps(userid,"step"+str(stepCount),"Transfer intent")
						return reply
					else:
                                        	setSessionClassification(userid,"nil")
                                        	setIntentSteps(userid,"step1","nil")
						setAccountBalanceFlag(userid,0)

                                        	delname=userid+"_transfer.sum"
                                        	os.remove(delname)
						reply="aiml"
						return reply

				elif(reply=="checkReference"):
					if("no" in inputText.lower()):
						#writeToSummary(userid,"Reference Number",inputText.lower())
        	                                reply="next"
                	                        stepCount=step[4:]
                        	                stepCount=int(stepCount)
                                	        stepCount=stepCount+3
                                        	setIntentSteps(userid,"step"+str(stepCount),"Transfer intent")
					elif("yes" in inputText.lower()):
        	                                reply="What is the payment amount"
                	                        stepCount=step[4:]
                        	                stepCount=int(stepCount)
                                	        stepCount=stepCount+1
                                        	setIntentSteps(userid,"step"+str(stepCount),"Transfer intent")
					else:
						reply="Would you like to change the default value for payment amount currency (yes/no)?"

					return reply
				elif(reply=="showDetailsConfirm"):
					print "inside show details confirm"
					fname=userid+"_transfer.sum"
					
					reply="Here are the payment details.\n\n"
					with open(fname)as f:
						lines=f.readlines()
						#for line in lines:
						#	if(line.split(" : ")[0]=="Amount"):
						#		amount=str(line.split(" : ")[1])
						#	elif(line.split(" : ")[0]=="Date"):
						#		date=str(line.split(" : ")[1])
						#	elif(line.split(" : ")[0]=="Account Name"):
						#		acname=str(line.split(" : ")[1])
					reply=reply+str(lines)+"\n\n"
					reply=reply+"To proceed enter yes or no to cancel the transaction"
                                        stepCount=step[4:]
                                        stepCount=int(stepCount)
                                        stepCount=stepCount+1
                                        setIntentSteps(userid,"step"+str(stepCount),"Transfer intent")
					print "shgdshj*****************hgjg:",reply
					return reply
				elif reply=="checkConfirmation":			
					if("yes" in inputText.lower() or "ok" in inputText.lower()):
                                                reply="Payment Initiated.. Thanks for using HelloCiti.."
                                                stepCount=step[4:]
                                                stepCount=int(stepCount)
                                                stepCount=stepCount+1
                                                setIntentSteps(userid,"step"+str(stepCount),"Transfer intent")
                                        elif("no" in inputText.lower()):
                                                reply="Transaction cancelled. Thanks for using Citi Bank."
                                                setSessionClassification(userid,"nil")
                                                setIntentSteps(userid,"step1","nil")
						setAccountBalanceFlag(userid,0)

                                                delname=userid+"_transfer.sum"
                                                os.remove(delname)
                                        else:
                                                reply="please confirm the payment (yes/no)"

                                        return reply

				else:
					stepCount=step[4:]
					stepCount=int(stepCount)
					classifiedText=getClassifiedText(userid)
					if(stepCount==1 and (" to " in classifiedText.lower()) and (" for " in classifiedText.lower())):
						reply="Would you like to serach this in preformats (yes/no)?"
						stepCount=stepCount+3
					#1.4 will go to check date
					elif(stepCount==1 and checkPreformatCode(userid)==2):
						reply="next"
						stepCount=stepCount+16
					else:
						stepCount=stepCount+1
					setIntentSteps(userid,"step"+str(stepCount),"Transfer intent")
					#if (stepCount==12):
                                        #	setSessionClassification(userid,"nil")
                                        #	setIntentSteps(userid,"step1","nil")
                                        #	delname=userid+"_transfer.sum"
                                        #	os.remove(delname)

					return reply


def checkPreformatCode(userid):
	classifiedText=getClassifiedText(userid)				
	preformList=citiService.getUserPreformats("jd12345")
	flag=0
	#checking if preformat is already specified
	print "checking ***** preformat in classified text :",classifiedText
	for word in classifiedText.split(" "):
		for preform in preformList:
			if(word.lower().strip()==str(preform["code"].lower())):
                        	writeToSummary(userid,"Preformat Code",str(preform["code"]))
                                writeToSummary(userid,"Beneficiary Name",str(preform["beneficiaryName"]))
                                writeToSummary(userid,"Beneficiary Account Number",str(preform["account"]))
				#finding acno if lready present
				acno=-1
				print "checking account"
				if ("account" in classifiedText.lower())and(hasNumbers(classifiedText)):
					for word in classifiedText.split(" "):
						if word.isdigit():
							acno=word
						if (acno!=-1):
							print "writing account number"	
							setAccountBalanceFlag(userid,1)
			                                writeToSummary(userid,"Account Number",str(acno))
							flag=2
						else:
		                	        	writeToSummary(userid,"Account Number","456789393")
				else:
					print "no account number"
                                	writeToSummary(userid,"Account Number","456789393")

                                writeToSummary(userid,"Bank Routing Code",str(preform["code"]).lower())
				#finding amount if already present
				amount=-1
				if ("amount" in classifiedText.lower() or "eur" in classifiedText.lower()or "usd" in classifiedText.lower())and(hasNumbers(classifiedText)):
					for word in classifiedText.split(" "):
						if word.isdigit():
							amount=int(word)
							break
						if (amount!=-1):	
			                        	writeToSummary(userid,"Amount",str(amount).lower())
						else:
		                	               	writeToSummary(userid,"Amount",str(preform["amount"]).lower())
				else:
                                	writeToSummary(userid,"Amount",str(preform["amount"]).lower())
                                writeToSummary(userid,"Currency",str(preform["currency"]).lower())
                                writeToSummary(userid,"Account Type","Savings")
				if(flag==0):
					flag=1
				break
		if(flag>0):
			break

	print "returning "+str(flag)+" from function:::::::::::::::::::::::::::::"					
	return flag
