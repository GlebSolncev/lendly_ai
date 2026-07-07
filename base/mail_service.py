class MailService:
    def send_support_email(self, name, email, message):
        pass

    def send_reset_password_email(self, email, code):
        pass
        # email_sender = settings.EMAIL_HOST_USER
        # email_password = settings.EMAIL_HOST_PASSWORD
        # email_receiver = email
        #
        # subject = 'Welcome to BuyMyFleet!'
        #
        # em = MIMEMultipart('alternative')
        # em['From'] = email_sender
        # em['To'] = email_receiver
        # em['Subject'] = subject
        #
        # f = open("templates/email/password_verification_mail.html", "r")
        # html = f.read()
        # html = html.replace('{{url}}', f"https://buymyfleet.net/auth/restore-password/?code={code}")
        #
        # part = MIMEText(html, 'html')
        # em.attach(part)
        #
        # context = ssl.create_default_context()
        # with smtplib.SMTP_SSL(settings.EMAIL_HOST, 465, context=context) as server:
        #     server.login(email_sender, email_password)
        #     server.sendmail(email_sender, email_receiver, em.as_string())


mail_service = MailService()
