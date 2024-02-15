#! /usr/bin/env python


import sys

def emailFile(fileName,toAddr,fromAddr):
    from email.mime.text import MIMEText
    import smtplib    
    fp = open(fileName,'rb')
    msg = MIMEText(fp.read())
    fp.close()
    msg['Subject'] = fileName
    msg['From'] = fromAddr
    msg['To'] = toAddr    
    s = smtplib.SMTP('localhost')
    s.sendmail(me,[you],msg.as_string())
    s.quit()
    return
