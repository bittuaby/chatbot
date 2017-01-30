from suds.client import Client
USER_ACCNT = "jd12345"
PREFORMAT_CODE = "PreformatABC"
WSDL_URL = "https://moxtrapoc.herokuapp.com/soap/listservice?wsdl"
#WSDL_URL = "http://127.0.0.1:5000/soap/listservice?wsdl"
client = Client(WSDL_URL, cache=None)

def getServiceDetails():
	client = Client(WSDL_URL, cache=None)
	print("*" * 40)
	print(" SERVICE DETAILS ".center(40,"*"))
	print(client)

	
#get all USer Details
def getUserDetails():
	client = Client(WSDL_URL, cache=None)
	print("*" * 40)
	print(" LIST ALL ACCOUNT DETAILS ".center(40,"*"))
	result = client.service.getAllUserDetails()

	print(" REQUEST BODY ".center(40,"*"))
	print(client.last_sent().str())

	print(" RAW RESPONSE ".center(40,"*"))
	print(client.last_received().str())

	print("*" * 40)
	print(" PROCESSED RESPONSE ".center(40,"*"))
	users = result.User
	for user in users:
		print  user.userId, user.userFirstName, user.userLastName,  user.lastLoginTime

#getUserDetails
# input parameter - UserId
def getUserSpecificDetails(USER_ACCNT):
	client = Client(WSDL_URL, cache=None)
	print("*" * 40)
	print(" GET AN ACCOUNT DETAILS ".center(40,"*"))
	result = client.service.getUserDetails(USER_ACCNT)

	print(" REQUEST BODY ".center(40,"*"))
	print(client.last_sent().str())

	print(" RAW RESPONSE ".center(40,"*"))
	print(client.last_received().str())

	# print("*" * 40)
	# print(" PROCESSED RESPONSE ".center(40,"*"))
	# print  user.userId, user.userFirstName, user.userLastName,  user.lastLoginTime

	#get all Preformat Details
	# input parameter - UserId
def getUserPreformats(USER_ACCNT):
	print("*" * 40)
	print(" LIST ALL PREFORMAT DETAILS OF A USER".center(40,"*"))
	result = client.service.getAllPreformat(USER_ACCNT)

	print(" REQUEST BODY ".center(40,"*"))
	print(client.last_sent().str())

	print(" RAW RESPONSE ".center(40,"*"))
	print(client.last_received().str())

	# print("*" * 40)
	# print(" PROCESSED RESPONSE ".center(40,"*"))
	preformats = result.Preformat
	resultList=[]
	for preformat in preformats:
	 	print(preformat.preformatCod)
		#resultList.append(str(preformat.preformatCod)+"|"+str(preformat.benePtyNam)+"|"+str(preformat.beneBankNam)+"|"+str(preformat.currency)+"|"+str(preformat.tranAmt))
		dict={"code":str(preformat.preformatCod),"beneficiaryName":str(preformat.benePtyNam),"beneBankName":str(preformat.benePtyNam),"currency":str(preformat.currency),"amount":str(preformat.tranAmt),"account":str(preformat.account)}
		resultList.append(dict)
	print resultList
	return resultList
	#getPreformatDetails
	# input parameter - UserId, PreformatCode
def getPreformatDetails(USER_ACCNT,PREFORMAT_CODE):
	print("*" * 40)
	print(" GET A PREFORMAT DETAILS ".center(40,"*"))
	result = client.service.getPreformat(USER_ACCNT,PREFORMAT_CODE)
	
	print(" REQUEST BODY ".center(40,"*"))
	print(client.last_sent().str())

	print(" RAW RESPONSE ".center(40,"*"))
	print(client.last_received().str())

#print("*" * 40)
#print(" PROCESSED RESPONSE ".center(40,"*"))
#print(preformat.PreformatCode, preformat.BeneficiaryName, preformat.BeneficiaryAccountNumber, preformat.AccountNo, preformat.AccountType, preformat.Currency,preformat.Amount, preformat.BankRoutingCode)

#getUserPreformats("jd12345")

def payByQuickEntry(preformat):
#paybyquick entry
	WSDL_URL = "https://moxtrapoc.herokuapp.com/soap/paymentservice?wsdl"
	#WSDL_URL = "http://127.0.0.1:5000/soap/paymentservice?wsdl"
	client = Client(WSDL_URL, cache=None)

	print("*" * 40)
	print(" PAY BY QUICK ENTRY ".center(40,"*"))
	request = {
		'transRefNo':"1234",
		'valueDate':"21/11/2017",
		'paymentAmount':"100",
		'preformatCode':PREFORMAT_CODE,
		'internalTranUniqueKey':"789"
	}
	result = client.service.payByQuickEntry(request['transRefNo'], request['valueDate'], request['paymentAmount'], request['internalTranUniqueKey'])

	print(" REQUEST BODY ".center(40,"*"))
	print(client.last_sent().str())

	print(" RAW RESPONSE ".center(40,"*"))
	print(client.last_received().str())

def getTransaction(USER_ACCNT):
#get all Transaction Details
	WSDL_URL = "https://moxtrapoc.herokuapp.com/soap/paymentservice?wsdl"
	#WSDL_URL = "http://127.0.0.1:5000/soap/paymentservice?wsdl"
	client = Client(WSDL_URL, cache=None)

	print("*" * 40)
	print(" LIST Transaction DETAILS ".center(40,"*"))

	result = client.service.getTransactionDetails(USER_ACCNT)
	transactions = result.Transaction
	resultList=[]
	for transaction in transactions:
	 	print(transaction.benePtyNam)
		#resultList.append(str(preformat.preformatCod)+"|"+str(preformat.benePtyNam)+"|"+str(preformat.beneBankNam)+"|"+str(preformat.currency)+"|"+str(preformat.tranAmt))
		dict={"referenceNo":str(transaction.transRefNo),"beneficiaryName":str(transaction.benePtyNam),"account":str(transaction.acctNo),"date":str(transaction.valueDate),"amount":str(transaction.paymentAmount),"status":str(transaction.status)}
		resultList.append(dict)
	print resultList
	print(" RAW RESPONSE ".center(40,"*"))
	print(client.last_received().str())
	print(" REQUEST BODY ".center(40,"*"))
	print(client.last_sent().str())
	return resultList

#getTransaction(USER_ACCNT)
