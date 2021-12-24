from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def send_mail(sender,recipient,subject,message=None,html=None,atachment=None,password=None,config=None):
        
    recipient_out = ','.join(recipient)
    
    msg = MIMEMultipart('Alternative')
    server = smtplib.SMTP('smtp.office365.com', 587)
    server.ehlo()
    server.starttls()
    server.login(config['Credentials']['email'], config['Credentials']['pass'])

            
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient_out
    text = MIMEText(html,'html')
    msg.attach(text)
    server.sendmail(sender,recipient,msg.as_string())
    server.quit()
    
    return None