import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import jinja2
from jinja2 import Template


class Message:
    def __init__(self):
        template_loader = jinja2.FileSystemLoader(searchpath="./")
        self.template_env = jinja2.Environment(loader=template_loader)
        self.template = self.template_env.get_template(self.TEMPLATE_FILE)

    def render(self, **kwargs):
        return self.template.render(**kwargs)


class NewOrderMessage(Message):
    TEMPLATE_FILE = "core/templates/neworder.html"


class NewUserMessage(Message):
    TEMPLATE_FILE = "core/templates/newuser.html"


class DeleteUserMessageAdmin(Message):
    TEMPLATE_FILE = "articles/templates/userdeleteadmin.html"


class SendEmail:

    def send_email(self, recipient, token):

        port = 465  # port używany przez protokół ssl
        smtp_serwer = "smtp.gmail.com"
        sender = "kamilobroslak1@gmail.com"
        recipient = str(recipient)  # mail do testów formy maila i czy maile wychodza
        print(recipient)
        password = "disbxlwfqyjhefvd"  # przy wpisaniu hasła do konta google maile wychodzą i nie pojawia się błąd
        subject = "Cześć! Cieszymy się że jesteś z nami :)"

        hash = token.token

        newuser = NewUserMessage()
        content = newuser.render(hash=hash)

        message = MIMEMultipart()
        message["From"] = sender
        message["To"] = recipient
        message["Subject"] = subject

        message.attach(MIMEText(content, "html"))

        text = message.as_string()

        ssl_pol = ssl.create_default_context()

        with smtplib.SMTP_SSL(smtp_serwer, port, context=ssl_pol) as serwer:
            serwer.login(sender, password)
            serwer.sendmail(sender, recipient, text)


class SendOrderEmail:

    def send_email(self, recipient):

        port = 465  # port używany przez protokół ssl
        smtp_serwer = "smtp.gmail.com"
        sender = "kamilobroslak1@gmail.com"
        recipient = str(recipient)  # mail do testów formy maila i czy maile wychodza
        password = "disbxlwfqyjhefvd"  # przy wpisaniu hasła do konta google maile wychodzą i nie pojawia się błąd
        subject = "Właśnie ktoś zlożył zamówienie! :)"

        neworder = NewOrderMessage()
        content = neworder.render()

        message = MIMEMultipart()
        message["From"] = sender
        message["To"] = recipient
        message["Subject"] = subject

        message.attach(MIMEText(content, "html"))

        text = message.as_string()

        ssl_pol = ssl.create_default_context()

        with smtplib.SMTP_SSL(smtp_serwer, port, context=ssl_pol) as serwer:
            serwer.login(sender, password)
            serwer.sendmail(sender, recipient, text)


class EmailToAdminDelete:
    def send_email(self):
        port = 465  # port używany przez protokół ssl
        smtp_serwer = "smtp.gmail.com"
        sender = "kamilobroslak1@gmail.com"
        recipient = "kamil.obroslak@embiq.com"  # mail do testów formy maila i czy maile wychodza
        password = "disbxlwfqyjhefvd"  # przy wpisaniu hasła do konta google maile wychodzą i nie pojawia się błąd
        subject = "Użytkownik usunął konto!"

        user_del = DeleteUserMessageAdmin()
        content = user_del.render()

        message = MIMEMultipart()
        message["From"] = sender
        message["To"] = recipient
        message["Subject"] = subject

        message.attach(MIMEText(content, "html"))

        text = message.as_string()

        ssl_pol = ssl.create_default_context()

        with smtplib.SMTP_SSL(smtp_serwer, port, context=ssl_pol) as serwer:
            serwer.login(sender, password)
            serwer.sendmail(sender, recipient, text)
