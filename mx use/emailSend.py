# Import smtplib for the actual sending function
import smtplib

# For guessing MIME type
import mimetypes

# Import the email modules we'll need
import email
import email.mime.application



def sendMail(toAddr,filePath):
	# Create a text/plain message	
	msg = email.mime.Multipart.MIMEMultipart()
	msg['Subject'] = 'Account Proof Document'
	msg['From'] = 'citimoxtrabot@gmail.com'
	msg['To'] = 'bittu.raju@cognizant.com'

	# The main body is just another attachment
	body = email.mime.Text.MIMEText("""Hello, Please find the attached document as your account proof.\n\nRegards,\nCiti Moxtra Bot""")
	msg.attach(body)
	print "attached body"
	# PDF attachment
	filename=filePath
	fp=open(filename,'rb')
	att = email.mime.application.MIMEApplication(fp.read(),_subtype="pdf")
	fp.close()
	att.add_header('Content-Disposition','attachment',filename=filename)
	msg.attach(att)

	# send via Gmail server
	s = smtplib.SMTP('smtp.gmail.com')
	s.starttls()
	s.login('citimoxtrabot@gmail.com','moxtra123')
	s.sendmail('citimoxtrabot@gmail.com',[toAddr], msg.as_string())
	s.quit()
	print "sent mail"


#sendMail('bittu.raju@cognizant.com','acnf.pdf')
