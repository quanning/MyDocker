	<h2>#简介</h2>
	<p>	这是一个 arukas 专用的酸酸奶镜像。</p>
	<p>	<span>镜像部署成功后每次启动都会向设定的邮箱发送一封邮件。</span></p>
	
	<h2>#安装部署</h2>
	<p>	<a href="https://app.arukas.io/apps/new">https://app.arukas.io/apps/new</a></p>
	<p>
		<span>--------------------BEGIN----------------------</span>
	</p>
	<p>
		<b>Configuration</b>
	</p>
	<p>
		<b>App Name:</b> 起个名字呗
	</p>
	<p>
		<b>Image:</b> dachuichui/mydocker (使用这个镜像)
	</p>
	<p>
		<b>Service Plan:</b> Free (0 JPY / month) (当然选免费的)
	</p>
	<p>
		<b>Instances:</b> 1 0 JPY / month
	</p>
	<p>
		<b>Endpoint:</b> 留空
	</p>
	<p>
		<b>Custom Domain:</b> 留空
	</p>
	<p>
		<b>Port*: </b> 
	</p>
	<p>
		<span>22 TCP (</span><span>必填 22</span><span>)</span>
	</p>
	<p>
		 14587 TCP ( <span>必填 14587</span><span>)</span>
	</p>
	<p>
		<b>Use ENV:</b> 必选
	</p>
	<p>
		 TOKEN = token
	</p>
	<p>
		 SECRET = secret
	</p>
	<p>
		 SMTP_HOST = smtp.163.com (邮件主机)
	</p>
	<p>
		 SSL_PORT = 465 (邮件ssl端口)
	</p>
	<p>
		 MAIL_USER = example@163.com (用户名)
	</p>
	<p>
		 MAIL_PASSWD = xxxxxx (密码)
	</p>
	<p>
		 MAIL_TO = example@163.com (发到哪)
	</p>
	<p>
		 SSR_PASSWD = xxxxxxx (酸酸奶密码)
	</p>
	<p>
		 SSH_PASSWD = xxxxxxx (ssh密码)
	</p>
	<p>
		Command： 留空
	</p>
	<p>
		--------------------END----------------------
	</p>
	
	<h2>
		#备注
	</h2>
	<p>
		token 和 secret 获取地址: <a href="https://app.arukas.io/settings/api-keys">https://app.arukas.io/settings/api-keys</a>
	</p>
	<p>
		<span>镜像运行成功后在 MAIL_TO 指定的邮箱会收到新邮:</span>
	</p>
	<p>
		标题: [arukas.io] suansuanru updated. 2018-xx-xx xx:xx:xx
	</p>
	<p>
		内容: xxx.xxx.xxx.xxx:xxxx (ssh)
	</p>
	<p>
		ssr://xxxxxxxxxxxxxxxxxx (你懂)
	</p>