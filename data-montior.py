import smtplib
from email.mime.text import MIMEText
from email.header import Header
import time
from sqlalchemy import create_engine,Column,String,Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import requests
from lxml import etree
from retrying import retry
import utils
logger = utils.init_logger('data-montior_mail')
import traceback

CONSTR='mysql+pymysql://root:root@193.168.15.138:3306/xxxxx?charset=utf8'
engine=create_engine(CONSTR,echo=False)
DBSession=sessionmaker(bind=engine)
session=DBSession()
Base=declarative_base()

class Mybase(Base):
	__tablename__ ='decryption-tools'
	id=Column(Integer,name='Id',primary_key=True)
	name=Column(String(255),nullable=False)
	def __repr__(self):
		return "{}".format(self.name)
def CreatDb():
	Base.metadata.create_all(engine)
#创建
CreatDb()
def send_e(y):
	# 第三方 SMTP 服务
	mail_host="iOA.xxxxx.com.cn"  #设置服务器
	mail_user="aaaaaaaa"    #用户名
	mail_pass="bbbbbbb"   #口令 
	sender = 'aaaaaaaa@xxxxx.com.cn'
	receivers = ['xxxxx@xxxxx.com.cn','yyyyy@xxxxx.com.cn','zzzzzz@xxxxxx.com.cn']  # 接收邮件，可设置为其他邮箱
	message = MIMEText(y, 'html','gb2312')
	message['From'] = Header("xxxxx") #发送人名称
	message['To'] =  Header("yyyyy,zzzzzz") #接收人名称
	subject = 'decryption-tools监控信息'
	message['Subject'] = Header(subject, 'utf-8')
	try:
		smtpObj = smtplib.SMTP() 
		smtpObj.connect(mail_host, 8025 )   
		smtpObj.login(mail_user,mail_pass)
		smtpObj.sendmail(sender, receivers, message.as_string())
		print ("邮件发送成功")
	except smtplib.SMTPException as e:
		logger.error(traceback.print_exc())

@retry
def start():
	url='https://www.nomoreransom.org/en/decryption-tools.html'
	r  = requests.get(url)
	html = etree.HTML(r.text)
	e=0
	_list=[]
	for i in html.xpath('//*[@id="ransomList"]/h4/span/text()'):
		result=i+' Ransom'
		result_=session.query(Mybase).filter_by(name=result).first()
		dic={}
		if result_!=None :
			print ('Found old:',result)
			dic['old']=result
			_list.append(dic)
		else:
			e=1
			dic['new']=result
			print ('** New add **:',result)
			_list.append(dic)
			user=Mybase(name=result)
			session.add(user)
			session.commit()
			session.close()
	html=""
	for r_list in _list:
		for key in r_list:
			if key!='old':
				str_='''<font size="5"><span style="font-family: Simsun; line-height: normal;">增加:<font color="#ff0000"><b>%s</b></font></span></font><br>'''%r_list[key]
				html+=str_
			else:
				str2_='''<font size="5"><span style="font-family: Simsun; line-height: normal;">%s</span><br>'''%r_list[key]
				html+=str2_
	text=('<div>'+html+'</div>')
	with open ('temp.htm','w',encoding="utf-8")as fp:
		fp.write(text)
	return e,text

while  True:
	x, y=start()
	if x==1:
		print ('发邮件')
		send_e(y)
	else:
		print ('没啥新东西')
	time.sleep(3600)