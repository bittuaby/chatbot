import zipfile
import sys
import os
#import comtypes.client
wdFormatPDF = 17

def docx_replace(old_file,new_file,values):
    zin = zipfile.ZipFile (old_file, 'r')
    zout = zipfile.ZipFile (new_file, 'w')
    for item in zin.infolist():
        buffer = zin.read(item.filename)
        if (item.filename == 'word/document.xml'):
            res = buffer.decode("utf-8")
            for val in values:
                res = res.replace(val[0],val[1])
            buffer = res.encode("utf-8")
        
        zout.writestr(item, buffer)
    zout.close()
    zin.close()

def createAccountConfirmationPDF(userid,accno,iban,accName,currency,swiftCode):
    try:
        docx_replace('ACCOUNT CONFIRMATION DOCUMENT.docx',str(userid)+str(accno)+'temp.docx',[('$ACCNO$',accno),('$IBAN$',iban),('$ACCNAME$',accName),('$CURRENCY$',currency),('$SWIFTCODE$',swiftCode)])
        #in_file = os.path.abspath(str(userid)+str(acno)+'temp.docx')
        #out_file = os.path.abspath('output.pdf')
        #word = comtypes.client.CreateObject('Word.Application')
        #doc = word.Documents.Open(in_file)
        #doc.SaveAs(out_file, FileFormat=wdFormatPDF)
        #doc.Close()
        #word.Quit()
	command='soffice --headless --convert-to pdf '+str(userid)+str(accno)+'temp.docx'
	os.system(command)
	os.rename(str(userid)+str(accno)+'temp.pdf','/home/ubuntu/moxtra/AccountProofs/AccountConfirmation_'+str(userid)+'.pdf')
	os.remove(str(userid)+str(accno)+'temp.docx')
	print "pdf generated succesfully"

        return True
    except:
        return False

#createAccountConfirmationPDF("abcd","007","123","Jithu R Jacob","INR","ABC")
