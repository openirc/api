from flask_mail import Mail, Message
from jinja2 import Environment, PackageLoader, select_autoescape

mail = Mail()


class NoMailDaemonError(Exception):
    def __init__(self, message):
        self.message = message


class MailEngine:
    def __init__(self):
        self.env = None
        self.mail_daemon = None
        self.mail_url = 'https://openirc.net/'

    def init_app(self, mail_daemon, mail_url):
        self.mail_daemon = mail_daemon

        if mail_url is not None:
            self.mail_url = mail_url

        self.env = Environment(
            loader=PackageLoader('openirc', 'email-templates'),
            autoescape=select_autoescape(['html', 'htm', 'j2', 'xml'])
        )

    def get_new_subscriber(self):
        return self.env.get_template('welcome.html')

    def send_signup_confirmation_token(self, email, token):
        if not self.mail_daemon:
            raise NoMailDaemonError('No Flask-Mailer specified')

        email_template_loader = self.get_new_subscriber()
        email_template = email_template_loader.render(web_url=self.mail_url, token=token)

        msg = Message()
        msg.recipients = [email]
        msg.subject = "OpenIRC E-Mail Confirmation"
        msg.html = email_template

        try:
            self.mail_daemon.send(msg)
        except ConnectionRefusedError as e:
            print('Unable to send confirmation email')
            raise e


mailer = MailEngine()
