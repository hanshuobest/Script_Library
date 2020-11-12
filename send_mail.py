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


from os import pardir
import smtplib
import email.mime.multipart
import email.mime.text
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
import argparse


def send_email(smtp_host, smtp_port, sendAddr, password, recipientAddrs, attach_file , subject='', content=''):
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
    
    part = MIMEApplication(
        open(attach_file , 'rb').read()
    )
    part.add_header('Content-Disposition', 'attachment',
                    filename=os.path.basename(attach_file))  # 发送文件名称
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
            #print(f"mail has been send successfully. message:{str(msg)}")
            smtpSSLClient.quit()
            print('send finished!')
        else:
            print(f"登陆失败，code = {loginRes[0]}")
    except Exception as e:
        print(f"发送失败，Exception: e={e}")



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f' , '--file')
    args = parser.parse_args()
    
    try:
        subject = 'Python 发送附件'
        content = '来自智慧的力量'
        attach_file = args.file
        send_email('smtp.163.com', 465, 'hscoder@163.com', 'DPDLIRFSRFZFRZQB', 'hanshuobest@163.com', attach_file, subject, content)
    except Exception as err:
        print(err)


if __name__ == '__main__':
    main()
    