#!/usr/bin/env python
import urllib
import urllib2
import re
import json
import base64
import string
import sys

from  datetime import datetime
import smtplib  
from email.MIMEText import MIMEText  
from email.Utils import formatdate  
from email.Header import Header  
#from email.mime.multipart import MIMEMultipart

default_encoding = 'utf-8'

class ArukaUpdate():
    def __init__(self):
        cfg = self.load_config()

        data = {}
        cont = json.loads(self.get("https://app.arukas.io/api/apps?include=service", cfg))
        data = self.parser(cont, data=data)
        server_ip = "%s:%s" % (data['data'][0]['ip'], data['data'][0]['prot'])

        if cfg['server_ip'] != server_ip :
            print(server_ip)
            print(self.sendmail(data, cfg))

    def get(self, api_url, cfg) :
        request = urllib2.Request(api_url)
        base64string = base64.b64encode('%s:%s' % (cfg['token'], cfg['secret']))
        request.add_header("Authorization", "Basic %s" % base64string)   
        result = urllib2.urlopen(request).read()
        return result

    def parser(self, cont, data=None):
        if cont is None:
            return None
        list = []
        if data:
            list.extend(data['data'])
        for i in range(len(cont['included'][0]['attributes']['port-mappings'][0])):
            dd = dict()
            attributes = cont['included'][0]['attributes']['port-mappings'][0][i]
            ip = re.findall(r'\d{1,3}-\d{1,3}-\d{1,3}-\d{1,3}', attributes['host'])[0].replace('-', '.')
            port = attributes['service-port']
            dd['ip'] = ip
            dd['prot'] = port
            list.append(dd)
        data = {
            'data': list
        }
        return data

    def get_ssr(self, data, cfg):
        #SSR://
        server = data['data'][1]['ip']
        server_port = data['data'][1]['prot']
        password = base64.urlsafe_b64encode((cfg['ssr_password']).encode(default_encoding)).decode().replace('=','')
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
        if sys.getdefaultencoding() != default_encoding:  
            reload(sys)  
            sys.setdefaultencoding(default_encoding)
           
        smtpHost = cfg['smtp_host']
        smtpPort = '25' #string.atoi(cfg['smtp_port'])
        sslPort  = string.atoi(cfg['ssl_port'])
        fromMail = cfg['mail_username']
        toMail   = cfg['mail_to']
        username = cfg['mail_username']
        password = cfg['mail_password']

        subject  = '[arukas.io] suansuanru updated. ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        body = "%s:%s\n%s" % (data['data'][0]['ip'],data['data'][0]['prot'], self.get_ssr(data, cfg))

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
            smtp = smtplib.SMTP_SSL(smtpHost, sslPort)  
            smtp.ehlo()  
            smtp.login(username,password)  
          
            smtp.sendmail(fromMail,toMail, message.as_string())  
            smtp.close()
            
            server_ip = "%s:%s" % (data['data'][0]['ip'], data['data'][0]['prot'])
            cfg['server_ip'] = server_ip

            return self.save_config(cfg)

        except Exception as e:  
            print e
            return 201

    def load_config(self):
        data = {}
        with open('/root/script/config.json', 'r') as f:
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
