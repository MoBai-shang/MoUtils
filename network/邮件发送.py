# smtplib 用于邮件的发信动作
import os.path
import smtplib
from email.mime.text import MIMEText
from typing import Union
# email 用于构建邮件内容
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
class SSL_SMTP():
    def __init__(self,from_add="2089885010@qq.com",author_code="gftmnlndoobycbgg",to=['mobaigeneral@qq.com'],smtp_server = 'smtp.qq.com'):
        # 发信方的信息：发信邮箱，QQ 邮箱授权码
        self.mail_user=from_add# 用户名
        self.mail_pass=author_code# 口令
        self.receivers=to# 接收邮件，可设置为你的QQ邮箱或者其他邮箱
        self.smtp_server=smtp_server# 第三方 SMTP 服务器
    def __call__(self,context,alias_from=' ',alias_to='',subject=' ',attachs:list=[], _subtype:Union['plain','html']='plain',SSL=False, *args, **kwargs):
        # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
        message=MIMEMultipart()
        message['From'] = Header(alias_from, 'utf-8')
        message['To'] = Header(alias_to, 'utf-8')
        message['Subject'] = Header(subject, 'utf-8')

        text = MIMEText(context, _subtype, 'utf-8')
        message.attach(text)
        for attach in attachs:
            attachment = MIMEApplication(open(attach, 'rb').read())
            attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attach))
            message.attach(attachment)
        try:
            # 开启发信服务，是否加密传输
            smtpObj = smtplib.SMTP_SSL(host=self.smtp_server) if SSL else smtplib.SMTP()
            smtpObj.connect(host=self.smtp_server, port=465) if SSL else smtpObj.connect(self.smtp_server,25) # 25 为 SMTP 端口号
            smtpObj.login(self.mail_user, self.mail_pass)
            smtpObj.sendmail(self.mail_user, self.receivers, message.as_string())
            smtpObj.quit()
            print("邮件发送成功")
        except smtplib.SMTPException:
            print("Error: 无法发送邮件")

send=SSL_SMTP()
send("启禀将军，Voxceleb脚本运行结束啦！",alias_from='kaggle',alias_to='General',subject='kaggle有事要报',attachs=[])
