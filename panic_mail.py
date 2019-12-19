import smtplib
conn = smtplib.SMTP('imap.gmail.com',587)
conn.ehlo()
conn.starttls()
conn.login('studymonmon@gmail.com', 'mon@4325')

conn.sendmail('studymonmon@gmail.com','homecom1@gmail.com','Subject: Emergency Alert \n\n Reply Reply Reply')
conn.quit()