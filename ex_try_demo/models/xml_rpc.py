# -*- coding: utf-8 -*-

import xmlrpc.client as xmlrpc
from odoo.exceptions import ValidationError

class TimeoutTransport(xmlrpc.Transport):

	def __init__(self, timeout, use_datetime=0):
		self.timeout = timeout
		# xmlrpclib uses old-style classes so we cannot use super()
		xmlrpc.Transport.__init__(self, use_datetime)

	def make_connection(self, host):
		connection = xmlrpc.Transport.make_connection(self, host)
		connection.timeout = self.timeout
		return connection


class TimeoutServerProxy(xmlrpc.ServerProxy):

	def __init__(self, uri, timeout=2, transport=None, encoding=None, verbose=0, allow_none=0, use_datetime=0):
		t = TimeoutTransport(timeout)
		xmlrpc.ServerProxy.__init__(self, uri, t, encoding, verbose, allow_none, use_datetime)


class Model:

	def __init__(self, db, uid, password, models, model):
		self.db = db
		self.uid = uid
		self.password = password
		self.models = models
		self.model = model

	def create(self, vals):
		id = self.models.execute_kw(self.db, self.uid, self.password, self.model, 'create', [vals] if isinstance(vals, dict) else vals)
		return id

	def search(self, query):
		res = self.models.execute_kw(self.db, self.uid, self.password, self.model, 'search', query)
		return res

	def search_count(self, query):
		res = self.models.execute_kw(self.db, self.uid, self.password, self.model, 'search_count', query)
		return res

	def search_read(self, query, fields):
		res = self.models.execute_kw(self.db, self.uid, self.password, self.model, 'search_read', query, {'fields': fields})
		return res

	def update(self, ids, vals):
		self.models.execute_kw(self.db, self.uid, self.password, self.model, 'write', [ids, vals])
		return True

	def unlink(self, ids):
		self.models.execute_kw(self.db, self.uid, self.password, self.model, 'unlink', ids)
		return True

	def execute_def(self, def_name, ids):
		res = self.models.execute_kw(self.db, self.uid, self.password, self.model, def_name, ids or [])
		return res

	def execute_raw_query(self, query):
		res = self.models.execute_kw(self.db, self.uid, self.password, self.model, 'execute_raw_query', [query])
		return res


class XMLRPC:

	def __init__(self, host, port, db, login, password):
		self.db = db
		self.password = password

		url = '%s:%s' % (host,port)
		#try:
		#Verify if the connection is established
		common = TimeoutServerProxy('{}/xmlrpc/2/common'.format(url))

		#Authenticate and get user data (logging in)
		self.uid = common.authenticate(db, login, password, {})

		#Verify if the connectio is correct
		self.models = TimeoutServerProxy('{}/xmlrpc/2/object'.format(url))
		#except:
		#	raise ValidationError("Can not connect to Host")

	def map_model(self, model):
		return Model(self.db, self.uid, self.password, self.models, model)