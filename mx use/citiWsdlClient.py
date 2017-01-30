from suds.client import Client
USER_ACCNT = "CITI-123456789"
PREFORMAT_CODE = "Preformat1CITI234"
WSDL_URL = "https://moxtrapoc.herokuapp.com/soap/listservice?wsdl"
client = Client(WSDL_URL, cache=None)

print("*" * 40)
print(" SERVICE DETAILS ".center(40,"*"))
print(client)

#get all USer Details
def listAllUsers():
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
		print user.UserName, user.UserId

#getUserDetails
# input parameter - UserId
def getUserDetails(userid):
	print("*" * 40)
	print(" GET AN ACCOUNT DETAILS ".center(40,"*"))
	result = client.service.getUserDetails(USER_ACCNT)

	print(" REQUEST BODY ".center(40,"*"))
	print(client.last_sent().str())

	print(" RAW RESPONSE ".center(40,"*"))
	print(client.last_received().str())

	print("*" * 40)
	print(" PROCESSED RESPONSE ".center(40,"*"))
	print(result.UserName, result.UserId)

#get all Preformat Details
# input parameter - UserId
def listPreformat(userid):
	print("*" * 40)
	print(" LIST ALL PREFORMAT DETAILS OF A USER".center(40,"*"))
	result = client.service.getAllPreformat(USER_ACCNT)

	print(" REQUEST BODY ".center(40,"*"))
	print(client.last_sent().str())

	print(" RAW RESPONSE ".center(40,"*"))
	print(client.last_received().str())

	print("*" * 40)
	print(" PROCESSED RESPONSE ".center(40,"*"))
	preformats = result.Preformat
	for preformat in preformats:
		print(preformat.PreformatCode, preformat.BeneficiaryName, preformat.BeneficiaryAccountNumber, preformat.AccountNo, preformat.AccountType, preformat.Currency,preformat.Amount, preformat.BankRoutingCode)

#getUserDetails
# input parameter - UserId, PreformatCode
def getPreformatDetails(userid,preformat):
	print("*" * 40)
	print(" GET A PREFORMAT DETAILS ".center(40,"*"))
	result = client.service.getPreformat(USER_ACCNT,PREFORMAT_CODE)

	print(" REQUEST BODY ".center(40,"*"))
	print(client.last_sent().str())

	print(" RAW RESPONSE ".center(40,"*"))
	print(client.last_received().str())

	print("*" * 40)
	print(" PROCESSED RESPONSE ".center(40,"*"))
	print(preformat.PreformatCode, preformat.BeneficiaryName, preformat.BeneficiaryAccountNumber, preformat.AccountNo, preformat.AccountType, preformat.Currency,preformat.Amount, preformat.BankRoutingCode)

