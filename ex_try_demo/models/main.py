from odoo import api, fields, models, _
from odoo import http
import requests
import base64
import os
import json
from bs4 import BeautifulSoup
import urllib.request
from .xml_rpc import XMLRPC
from odoo.exceptions import ValidationError
from datetime import datetime, date

class DatabaseSource(models.Model):

	_name = "database.source.demo"
	_description = "Database Source Demo"


	name = fields.Char(string="Tên mô tả",required=True)
	db_zip = fields.Binary(string="Database zip file",required=True)
	is_default = fields.Boolean(string="Default")



class PartnerDemo(models.Model):

	_name = "partner.try.demo"
	_inherit = ['mail.thread','mail.activity.mixin']
	_description = "Partner Try Demo"

	@api.model
	def set_default_tomaho_demo_hostname(self):
		self.env['ir.config_parameter'].sudo().set_param('default_tomaho_demo_hostname','192.168.1.14')

	def _get_default_hostname(self):

		return self.env['ir.config_parameter'].sudo().get_param('default_tomaho_demo_hostname')

	partner_id = fields.Many2one('res.partner',string="Partner")
	
	hostname = fields.Char(string="Host Name",required=True, default=_get_default_hostname)
	
	port = fields.Char(string="Port",required=True)
	
	db_id = fields.Many2one("database.source.demo",string="Database Zip File")

	try_type = fields.Selection(selection=[('restore','Restore'),('create','Create'),('duplicate','Duplicate')],default='create')

	db_name = fields.Char(string="Database Name",required=True)

	passwd = fields.Char(string="Password")

	email = fields.Char(string="Email")

	master_passwd = fields.Char(string="Master Password",required=True)

	phone = fields.Char(string="Phone")

	demo_data = fields.Boolean(string="Demo Data")

	log_ids = fields.One2many('try.demo.log','try_id', readonly=True) 

	user_ids = fields.One2many('user.data','demo_id')
	
	new_db_name = fields.Char(string="Tên bản sao")

	state=fields.Selection(selection=[('draft','Draft'),('create_restore','Database Created'),('create_user','User Created'),('done','Done')],default='draft')

	

	def action_return(self):
		self.env['try.demo.log'].create({
			'try_id': self.id,
			'log': "Trở về trạng thái nháp",
			'date_log' : datetime.now(),
			})
		self.state = 'draft'

	@api.multi
	def create_db(self):

		self.ensure_one()

		url = "http://"+self.hostname+":"+self.port+"/web/database/create"

		datas = {
			'master_pwd': self.master_passwd,
			'name': self.db_name,
			'login': self.email,
			'password': self.passwd,
			'lang': 'en_US',
			'phone': self.phone,
			'demo': self.demo_data,
			'country': "vn"
		}
		#try:
		r = requests.post(url, data=datas)
		if r.status_code == 200:
			
			soup = BeautifulSoup(r.text, 'html.parser')
			# raise Warning(r.text)
			alert_error = soup.find_all(class_="alert alert-danger", limit=1)
			# alert_error = soup.find('div', class_='').find('div')
			result_error = str(alert_error).replace("""[<div class="alert alert-danger">"""," ").replace("""</div>]"""," ")
			if alert_error:
				self.env['try.demo.log'].create({
					'try_id': self.id,
					'log': result_error,
					'date_log' : datetime.now(),
					})
			else:
				self.env['try.demo.log'].create({
					'try_id': self.id,
					'log': "Tạo CSDL thành công!",
					'date_log' : datetime.now(),
					})
				self.write({
					'state': 'create_restore',
				})
		else:
			self.env['try.demo.log'].create({
				'try_id': self.id,
				'log': "Mã lỗi %s: %s" % (r.status_code, r.message),
				'date_log' : datetime.now(),
				})
		


		# except:
		# 	self.env['try.demo.log'].create({
		# 		'try_id': self.id,
		# 		'log': "Can not create database",
		# 		'date_log': datetime.now(),
		# 		})
		# 	raise ValidationError("Can not connect to Host")

		# raise Warning(r.status_code)
		return True

	
	def restore_db(self):


		url = "http://"+self.hostname+":"+self.port+"/web/database/restore"
		file_obj = base64.b64decode(self.db_id.db_zip)
		multipart_form_data = {
			'master_pwd': u'%s' % self.master_passwd,
			'name': u'%s' % self.db_name,
			# 'backup_file': ('new', base64.b64encode(self.db_id.db_zip)),
			'copy': 'true',
		}

		#try:
		r = requests.post(url, data=multipart_form_data, files={"backup_file": ("neww.zip", file_obj)})
		# raise Warning(r.text)
		if r.status_code == 200:
			soup = BeautifulSoup(r.text, 'html.parser')
			# raise Warning(r.text)
			alert_error = soup.find_all(class_="alert alert-danger", limit=1)
			# alert_error = soup.find('div', class_='').find('div')
			result_error = str(alert_error).replace("""[<div class="alert alert-danger">"""," ").replace("""</div>]"""," ")
			if alert_error:
				self.env['try.demo.log'].create({
					'try_id': self.id,
					'log': result_error,
					'date_log' : datetime.now(),
					})
			else:
				self.env['try.demo.log'].create({
					'try_id': self.id,
					'log': "Khôi phục dữ liệu thành công!",
					'date_log' : datetime.now(),
					})
				self.write({
					'state': 'create_restore',
				})
		else:
			self.env['try.demo.log'].create({
				'try_id': self.id,
				'log': "Mã lỗi %s: %s" % (r.status_code, r.message),
				'date_log' : datetime.now(),
				})

	def duplicate_db(self):
		url = "http://"+self.hostname+":"+self.port+"/web/database/duplicate"
		
		datas = {
			'master_pwd': self.master_passwd,
			'name': self.db_name,
			'new_name': self.new_db_name,
			
		}

		r = requests.post(url, data=datas)
		if r.status_code == 200:
			soup = BeautifulSoup(r.text, 'html.parser')
			alert_error = soup.find_all(class_="alert alert-danger", limit=1)
			result_error = str(alert_error).replace("""[<div class="alert alert-danger">"""," ").replace("""</div>]"""," ")
			if alert_error:
				self.env['try.demo.log'].create({
					'try_id': self.id,
					'log': result_error,
					'date_log' : datetime.now(),
					})
			else:
				self.env['try.demo.log'].create({
					'try_id': self.id,
					'log': "Tạo bản sao thành công!",
					'date_log' : datetime.now(),
					})
				self.write({
					'state': 'create_restore',
				})
		else:
			self.env['try.demo.log'].create({
				'try_id': self.id,
				'log': "Mã lỗi %s: %s" % (r.status_code, r.message),
				'date_log' : datetime.now(),
				})



	def do_try_type(self):
		

		if self.try_type == 'create':
			self.create_db()

		elif self.try_type == 'restore':
			self.restore_db()
		else:
			self.duplicate_db()

	# @api.multi
	# def create_users(self):
		
	# 	# self.ensure_one()	

	# 	host_usr = "http://"+self.hostname
		
	# 	# data_usr = self.env['user.data'].search([])

	# 	#try:
	# 	Connection = XMLRPC(host_usr, self.port, self.db_name, self.email, self.passwd)
	# 	Create = Connection.map_model('res.users')
	# 	for line in self.user_ids:
	# 		Create.create({
	# 			'login': line.login,
	# 			'name': line.name,
	# 			'password': line.password,
	# 		})
	# 	self.env['try.demo.log'].create({
	# 		'try_id': self.id,
	# 		'log': "Create user Successfully!",
	# 		'date_log': datetime.now(),
	# 	})
		
	# 	self.state = 'done'
	# 	# except:
	# 	# 	self.env['try.demo.log'].create({
	# 	# 		'try_id': self.id,
	# 	# 		'log': "Can not create user!",
	# 	# 		'date_log': datetime.now(),
	# 	# 	})



	@api.multi
	def send_email(self):
		self.ensure_one()
		record_id = self.env['ir.model.data'].get_object_reference('ex_try_demo','email_template_user_account')[1]
		template = self.env['mail.template'].browse(record_id)
		template.send_mail(self.id)

		self.env['try.demo.log'].create({
				'try_id': self.id,
				'log': "Gửi mail danh sách user - password!",
				'date_log': datetime.now(),
			})
		self.state = 'done'
		return True


class PartnerTryDemoLog(models.Model):

	_name ='try.demo.log'
	_description = 'Partner Try Demo Log'


	try_id = fields.Many2one("partner.try.demo", ondelete='cascade')
	date_log = fields.Datetime(string='Date')
	log = fields.Text(string='Log')

class UserData(models.Model):
	_name = "user.data"
	_description = "User Data"

	demo_id = fields.Many2one('partner.try.demo')
	login = fields.Char(string='User Name')	
	name = fields.Char(string="Name")
	password = fields.Char(string='Password')
	#state = fields.Selection(selection=[('done','Done')])
	@api.multi
	def create_user(self):
		
		

		host_usr = "http://"+self.demo_id.hostname
		
		Connection = XMLRPC(host_usr, self.demo_id.port, self.demo_id.db_name, self.demo_id.email, self.demo_id.passwd)
		User = Connection.map_model('res.users')
		for line in self:
			User.create({
				'login': line.login,
				'name': line.name,
				'password': line.password,
			})
		self.env['try.demo.log'].create({
			'try_id': self.demo_id.id,
			'log': "Tạo tài khoản thành công!",
			'date_log': datetime.now(),
		})
		
		self.demo_id.state = 'create_user'


