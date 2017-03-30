#! /usr/bin/env python3

import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import configparser
from os import path


class MyEmail:
    def __init__(self, user_name, pwd, smtp_ssl_host='smtp.qq.com', port=465):
        self.host = smtplib.SMTP_SSL(smtp_ssl_host, port)
        self.host.login(user_name, pwd)
        self.user_name = user_name

    def __del__(self):
        self.host.close()

    def _send_email(self, user_name, to, msg):
        try:
            self.host.sendmail(user_name, to, msg.as_string())
            print("send email success to %s" % to)
        except smtplib.SMTPException as e:
            print("failed :%s" % e)

    def send_text(self, email_addr, title, context):
        '''
        发送普通文本邮件
        :param email_addr: 邮件地址
        :param title: 邮件标题
        :param context: 内容
        :return: none
        '''
        msg = MIMEText(context)
        msg["Subject"] = title
        msg["From"] = self.user_name
        msg["To"] = email_addr
        self._send_email(self.user_name, email_addr, msg)

    def send_files(self, email_addrs, title, context, file_paths):
        '''
        发送带附件的邮件
        :param email_addrs: 邮件地址
        :param title: 邮件标题
        :param context: 邮件内容
        :param file_paths: 文件路径（list）
        :return: none
        '''
        msg = MIMEMultipart()
        msg["Subject"] = title
        msg["From"] = self.user_name
        msg["To"] = email_addrs

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

        self._send_email(self.user_name, email_addrs, msg)


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("email.ini")
    section_name = 'host'
    user_name = config.get(section_name, 'user_name')
    pwd = config.get(section_name, 'pwd')
    host_name = config.get(section_name, 'host_name')
    port = config.getint(section_name, 'port')

    email = MyEmail(user_name, pwd, host_name, port)

    # 发送普通邮件
    to = config.get(section_name, 'send_to')
    email.send_text(to, '这是一封文本测试邮件', '你好')

    # 发送附件
    file_paths = ['./myemail.py', './mymongodb.py']
    email.send_files(to, '这是一封附件测试邮件', '请看附件', file_paths)

