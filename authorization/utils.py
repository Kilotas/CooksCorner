from django.core.mail import EmailMessage

import threading


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self) # вызов конструктора родительского класса thread

    def run(self):
        self.email.send()

class Util:
    @staticmethod # статический метод в данном случае означает что он может быть вызван без создания экземпляра класса Util
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        EmailThread(email).start() # запускаем поток с помощью start