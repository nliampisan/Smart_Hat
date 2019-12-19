import smtplib, ssl

port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = "studymonmon@gmail.com"
receiver_email = "homecom1@gmail.com"
password = "mon@4325"
message = """\
Subject: Emergency Alert

Panic Button from Smart Hat."""

def panic_button_funct():
    print("sending email") 
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

panic_button_funct()