# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import ConfigParser
from os import path


class MyEmail:
    def __init__(self, user_name, pwd, smtp_ssl_host='smtp.qq.com', port=465):
        self.host = smtplib.SMTP_SSL(smtp_ssl_host, port)
        self.host.login(user_name, pwd)
        self.user_name = user_name

    def __del__(self):
        self.host.quit()

    def _sendemail(self, user_name, to, msg):
        try:
            self.host.sendmail(user_name, to, msg.as_string())
            print("send email success to %s" % to)
        except smtplib.SMTPException, e:
            print "Falied,%s" % e

    def send_text(self, to, title, context):
        msg = MIMEText(context.encode('utf8'))
        msg["Subject"] = title
        msg["From"] = self.user_name
        msg["To"] = to
        self._sendemail(self.user_name, to, msg)

    def send_files(self, to, title, context, file_paths):
        msg = MIMEMultipart()
        msg["Subject"] = title
        msg["From"] = self.user_name
        msg["To"] = to

        # 文字部分(邮件主体)
        text_part = MIMEText(context)
        msg.attach(text_part)

        # 附件部分
        for file_path in file_paths:
            with open(file_path, 'rb') as fp:
                attachment = fp.read()
                part = MIMEApplication(attachment)
                file_name = path.basename(file_path)
                part.add_header('Content-Disposition', 'attachment', filename=file_name)
                msg.attach(part)

        self._sendemail(self.user_name, to, msg)


if __name__ == '__main__':
    config = ConfigParser.ConfigParser()
    config.read("email.ini")
    user_name = config.get('host', 'user_name')
    pwd = config.get('host', 'pwd')
    host_name = config.get('host', 'host_name')
    port = config.getint('host', 'port')

    email = MyEmail(user_name, pwd, host_name, port)

    # 发送普通邮件
    to = '448217518@qq.com'
    email.send_text(to, 'text email test', 'hellow world')

    # 发送附件
    file_paths = ['./myemail.py', './mymongodb.py']
    email.send_files(to, 'attachment email test', '请看附件', file_paths)

