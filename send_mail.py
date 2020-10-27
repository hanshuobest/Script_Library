#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename    :send_mail.py
@brief       :往指定的邮箱发送附件
@time        :2020/10/27 18:10:03
@author      :hscoder
@versions    :1.0
@email       :hscoder@163.com
@usage       :
'''


import smtplib
import email.mime.multipart
import email.mime.text
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def send_email(smtp_host, smtp_port, sendAddr, password, recipientAddrs, subject='', content=''):
    '''
    :param smtp_host: 域名
    :param smtp_port: 端口
    :param sendAddr: 发送邮箱
    :param password: 邮箱密码
    :param recipientAddrs: 发送地址
    :param subject: 标题
    :param content: 内容
    :return: 无
    '''
    msg = email.mime.multipart.MIMEMultipart()
    msg['from'] = sendAddr
    msg['to'] = recipientAddrs
    msg['subject'] = subject
    content = content
    txt = email.mime.text.MIMEText(content, 'plain', 'utf-8')
    msg.attach(txt)

    # 添加附件地址
    part = MIMEApplication(
        open(r'test.txt', 'rb').read())
    part.add_header('Content-Disposition', 'attachment',
                    filename="test.txt")  # 发送文件名称
    msg.attach(part)

    try:
        smtpSSLClient = smtplib.SMTP_SSL(
            smtp_host, smtp_port)  # 实例化一个SMTP_SSL对象
        loginRes = smtpSSLClient.login(sendAddr, password)  # 登录smtp服务器
        # loginRes = (235, b'Authentication successful')
        print(f"登录结果：loginRes = {loginRes}")
        if loginRes and loginRes[0] == 235:
            print(f"登录成功，code = {loginRes[0]}")
            smtpSSLClient.sendmail(sendAddr, recipientAddrs, str(msg))
            print(f"mail has been send successfully. message:{str(msg)}")
            smtpSSLClient.quit()
        else:
            print(f"登陆失败，code = {loginRes[0]}")
    except Exception as e:
        print(f"发送失败，Exception: e={e}")


try:
    subject = 'Python 测试邮件'
    content = '这是一封来自 Python 编写的测试邮件。'
    send_email('smtp.163.com', 465, 'hscoder@163.com', 'DPDLIRFSRFZFRZQB', 'hanshuobest@163.com', subject, content)
except Exception as err:
    print(err)