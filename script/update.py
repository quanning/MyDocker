#!/usr/bin/env python
import urllib
import urllib2
import cookielib
import re
import json
import gzip
import StringIO
import base64
import string
import sys

from  datetime import datetime
import smtplib  
from email.MIMEText import MIMEText  
from email.Utils import formatdate  
from email.Header import Header  
from email.mime.multipart import MIMEMultipart

default_encoding = 'utf-8'

class ArukaUpdate():
    def __init__(self):

        cfg = self.load_config()        
        data = {}
        token = self.login(cfg['username'], cfg['password'])
        cont = self.get('https://app.arukas.io/api/services/' + cfg['appid'], token, cfg['appid'])
        cont = json.loads(cont)
        data = self.parser(cont, data=data)
        print(self.sendmail(data, cfg))

    def get(self, url, token, appid):
        if url is None:
            return None
        if token is None:
            return None
        header = {
            'Accept': 'application/vnd.api+json',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Authorization': token,
            'Host': 'app.arukas.io',
            'Referer': 'https://app.arukas.io/apps/' + appid,
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
            'X-Requested-With': 'XMLHttpRequest'
        }
        request = urllib2.Request(url, headers=header)
        result = urllib2.urlopen(request).read()
        result = StringIO.StringIO(result)
        gzipper = gzip.GzipFile(fileobj=result)

        return gzipper.read()

    def post(self, url, data, header=None):
        if url is None:
            return None
        data = urllib.urlencode(data).encode('utf-8')
        header = {
            'If-None-Match': 'W/"fd4ef77ca641a702611778a254e0b456"'
        }
        request = urllib2.Request(url, data, headers=header)
        cookies = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
        read = opener.open(request).read()
        cookie = ""
        for ck in cookies:
            cookie += ck.name + "=" + ck.value + ";"
        header.setdefault("Cookie", cookie)
        return read, header

    def login(self, user, password):
        if user is None or password is None:
            return None
        data = {
            "email": "%s" % user,
            "password": "%s" % password
        }
        
        cont, cookie = self.post("https://app.arukas.io/api/sessions", data)
        if cont is None:
            return None
        cont = json.loads(cont)

        return 'Bearer ' + cont['token']

    def parser(self, cont, data=None):
        if cont is None:
            return None
        list = []
        if data:
            list.extend(data['data'])
        for i in range(len(cont['data']['attributes']['port-mappings'][0])):
            dd = dict()
            attributes = cont['data']['attributes']['port-mappings'][0][1]
            ip = re.findall(r'\d{1,3}-\d{1,3}-\d{1,3}-\d{1,3}', attributes['host'])[0].replace('-', '.')
            port = attributes['service-port']
            dd['ip'] = ip
            dd['prot'] = port
            list.append(dd)
        data = {
            'data': list
        }
        return data

    def get_ssr(self, data):
        #SSR://
        server = data['data'][1]['ip']
        server_port = data['data'][1]['prot']
        password = base64.urlsafe_b64encode(('fkxjj@fkxjj').encode(default_encoding)).decode().replace('=','')
        protocol ='auth_chain_a'
        method = 'none'
        obfs = 'http_simple'
        obfsparam = ''
        remarks = 'SuanSuanRu'
        group = 'Arukas.io'

        main_part = "%s:%s:%s:%s:%s:%s" % (server, server_port, protocol, method, obfs, password)

        param_str = "obfsparam=%s&remarks=%s&group=%s" % (base64.urlsafe_b64encode(obfsparam.encode(default_encoding)).decode().replace('=',''),
            base64.urlsafe_b64encode(remarks.encode(default_encoding)).decode().replace('=',''),
            base64.urlsafe_b64encode(group.encode(default_encoding)).decode().replace('=',''))

        sharessr = "%s/?%s" % (main_part, param_str)

        return "ssr://" + base64.urlsafe_b64encode(sharessr.encode(default_encoding)).decode().replace('=','')

    def sendmail(self, data, cfg):
        server_ip = "%s:%s" % (data['data'][0]['ip'], data['data'][0]['prot'])
        #print ("%s vs %s" % (server_ip, cfg['server_ip']))
        if server_ip == cfg['server_ip'] :
            print ("noting...")
            return 200

        cfg['server_ip'] = server_ip
        self.save_config(cfg)

        if sys.getdefaultencoding() != default_encoding:  
            reload(sys)  
            sys.setdefaultencoding(default_encoding)
           
        smtpHost = cfg['smtp_host']
        smtpPort = string.atoi(cfg['smtp_port'])
        sslPort  = string.atoi(cfg['ssl_port'])
        fromMail = cfg['mail_username']
        toMail   = cfg['mail_to']
        username = cfg['mail_username']
        password = cfg['mail_password']

        subject  = '[arukas.io] suansuanru updated. ' + datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        body = "%s:%s\n%s" % (data['data'][0]['ip'],data['data'][0]['prot'], self.get_ssr(data))

        message = MIMEText(body.encode(default_encoding), 'plain', default_encoding)  
        message['Subject'] = Header(subject, default_encoding)  
        message['From'] = fromMail  
        message['To'] = toMail  
        message['Date'] = formatdate()  

        # message = MIMEMultipart()
        # message['From'] = fromMail
        # message['To'] =  toMail
        # message['Subject'] = Header(subject, default_encoding)  
        # message.attach(MIMEText(body.encode(default_encoding),'plain',default_encoding))
        
        # att1 = MIMEText(open('att1.jpg', 'rb').read(), 'base64', 'utf-8')
        # att1["Content-Type"] = 'application/octet-stream'
        # att1["Content-Disposition"] = 'attachment; filename="att1.jpg"'
        # message.attach(att1)

        try:  
            #normal
            #smtp = smtplib.SMTP(smtpHost,smtpPort)  
            #smtp.ehlo()  
            #smtp.login(username,password)  
          
            #tls
            #smtp = smtplib.SMTP(smtpHost,smtpPort)  
            #smtp.set_debuglevel(True)  
            #smtp.ehlo()  
            #smtp.starttls()  
            #smtp.ehlo()  
            #smtp.login(username,password)  
          
            #ssl
            smtp = smtplib.SMTP_SSL(smtpHost,sslPort)  
            smtp.ehlo()  
            smtp.login(username,password)  
          
            smtp.sendmail(fromMail,toMail, message.as_string())  
            smtp.close()
            return 200

        except Exception as e:  
            print e
            return 201

    def load_config(self):
        data = {}
        with open('config.json', 'r') as f:
            data = json.load(f)
        return data

    def save_config(self, data):
        with open('/root/script/config.json', 'r') as f:
            config = json.load(f)
        config = data        
        try:
            with open('/root/script/config.json', 'w') as f:
                json.dump(config, f, indent=4, sort_keys=True)
            return 200
        except Exception as e:  
            print e
            return 201

if __name__ == '__main__':
    ArukaUpdate()