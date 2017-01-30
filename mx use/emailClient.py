import smtplib

gmail_user = 'citimoxtrabot@gmail.com'  
gmail_password = 'moxtra123'

fromAddr = gmail_user  
to = ['bittu.cpp@gmail.com']  
subject = 'OMG Super Important Message'  
body = 'Hey, what\'s up?\n\n- You'

email_text = """\  
From: %s  
To: %s  
Subject: %s

%s
""" % (fromAddr, ", ".join(to), subject, body)

try:  
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(fromAddr, to, email_text)
    server.close()

    print 'Email sent!'
except:  
    print 'Something went wrong...'
