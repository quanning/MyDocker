简介
-----------------------------
这是一个 arukas 专用的酸酸乳镜像。

镜像部署成功后每次启动都会向设定的邮箱发送一封邮件。

## 安装部署
<https://app.arukas.io/apps/new>

```
App Name:		起个名字呗
Image:			dachuichui/mydocker	(使用这个镜像)
Service Plan:		Free (0 JPY / month)	(当然选免费的)
Instances:		1	0 JPY / month
Endpoint 		留空
Custom Domain   	留空
Port*:
			22 TCP     (必填 22)		
			14587 TCP  (必填 14587)	
Use ENV:		必选
			TOKEN       = token
			SECRET      = secret
			SMTP_HOST   = smtp.163.com      (邮件主机)
			SSL_PORT    = 465               (邮件ssl端口)
			MAIL_USER   = example@163.com   (用户名)
			MAIL_PASSWD = xxxxxx            (密码)
			MAIL_TO     = example@163.com   (发到哪)
			ROOT_PASSWD  = xxxxxxxxxx       (root密码)
Command:		留空
```

## 备注
token 和 secret 获取地址: <https://app.arukas.io/settings/api-keys>

镜像运行成功后在 MAIL_TO 指定的邮箱会收到新邮件:
```
标题: [arukas.io] suansuanru updated. 2018-xx-xx xx:xx:xx
内容: xxx.xxx.xxx.xxx:xxxx      (ssh)
      ssr://xxxxxxxxxxxxxxxxxx  (你懂)
```