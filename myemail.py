# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
import ConfigParser



class MyEmail:
    def __init__(self, user_name, pwd, smtp_ssl_host='smtp.qq.com', port=465):
        self.host = smtplib.SMTP_SSL(smtp_ssl_host, port)
        self.host.login(user_name, pwd)
        self.user_name = user_name

    def __del__(self):
        self.host.quit()

    def send(self, to, title, context):
        msg = MIMEText(context)
        msg["From"] = self.user_name
        msg["To"] = to
        msg["Subject"] = title

        try:
            self.host.sendmail(self.user_name, to, msg.as_string())
            print("send email success to %s" % to)
        except smtplib.SMTPException, e:
            print "Falied,%s" % e


if __name__ == '__main__':
    config = ConfigParser.ConfigParser()
    config.read("email.ini")
    user_name = config.get('host', 'user_name')
    pwd = config.get('host', 'pwd')
    host_name = config.get('host', 'host_name')
    port = config.getint('host', 'port')

    email = MyEmail(user_name, pwd, host_name, port)
    email.send('448217518@qq.com', 'this is a test email', 'hellow world')

