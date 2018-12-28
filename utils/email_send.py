# -*- coding:utf-8 -*-
__date__ = '17/2/25 上午3:53'
from random import Random
from users.models import EmailVerfyRecode


import smtplib,requests
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr




def random_str(randomlength=8):
    str=''
    chars='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    length=len(chars)-1
    random=Random()
    for i in range(randomlength):
        str+=chars[random.randint(0,length)]
    return  str


def send_register_email(email, send_type="register"):
    email_record = EmailVerfyRecode()
    if send_type == 'update_email':
        code = random_str(4)
    else:
        code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ""
    email_body = ""

    if send_type == "register":
        email_title = "淘客在线网注册激活链接"
        email_body = "请点击下面的链接激活你的账号: http://taoker.online/active/{0}".format(code)



        send_status = send_mail(email_title, email_body, email)

        if send_status:
            pass
        return {'email':email,'code':code}
    elif send_type == 'forget':
        email_title = "淘客在线网密码重置链接"
        email_body = "请点击下面的链接重置你的密码: http://taoker.online/reset/{0}".format(code)

        send_status = send_mail(email_title, email_body, email)
        if send_status:
            pass
        return {'email':email,'code':code}
    elif send_type == 'update_email':
        email_title = "淘客在线邮箱修改验证码"
        email_body = "你的邮箱验证码为:{0}".format(code)

        send_status = send_mail(email_title, email_body, email)
        if send_status:
            pass
        return {'email':email,'code':code}

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))


def send_mail(email_title,email_body,EMAIL_TO):
    try:

        msg = MIMEText(email_body, 'plain', 'utf-8')
        from_addr = 'taoker-online@qq.com'
        password = 'vrfvuxnnblurdega'
        smtp_server = 'smtp.qq.com'
        to_addr = EMAIL_TO


        msg['From'] = _format_addr(u'淘客在线网：系统管理员 <%s>' % from_addr)
        msg['To'] = _format_addr(u'taoker <%s>' % to_addr)
        msg['Subject'] = Header(email_title, 'utf-8').encode()


        server = smtplib.SMTP_SSL(smtp_server, 465) # SMTP协议默认端口是25
        server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()
        return 1
    except:
        return None


def send_wechat(title,body):
	try:
		url='http://sc.ftqq.com/SCU3164Tc1c397179e2c62c97c843021d6ad06025800f6227d9df.send?text='+title+'&desp='+body
		requests.get(url)
	except:
		return None



