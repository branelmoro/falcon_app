# always extend your controller from base_controller
# always give controller class name same as filename
from falcon import HTTP_200
from ..base_controller import CRUDS
from ..base_controller import appException

from ...library import json

# import all required models here
from ...models.oauth2Model import oauth2ScopeModel
from ...models.oauth2Model import oauth2ClientModel

class client(CRUDS):

	def __init__(self):
		self._search_template = self._getResource('CLS')
		self._search_page_template = self._getResource('CLP')
		self._create_template = self._getResource('CL')
		self._crud_template = self._getResource('CLU')

		self._resources = {
			self._search_template : 'CLS',
			self._search_page_template : 'CLP',
			self._create_template : 'CL',
			self._crud_template : 'CLU'
		}

	def getPath(self):
		return [
			self._create_template,
			self._search_template,
			self._search_page_template,
			self._crud_template
		]

	def _post(self, container):
		req = container.req
		resp = container.resp
		'''Handles POST requests'''
		self.__validateHttpPost(req)

		# this is valid request
		appResponce = {}

		resp.status = HTTP_200  # This is the default status

		client_model = oauth2ClientModel()

		client_detail = self._getFilteredRequestData(req, ['app_id', 'app_secret', 'scope', 'user_type'])

		appResponce['result'] = client_model.createClient(client_detail)

		# insert into redis set

		resp.body = json.encode(appResponce)

	# function to handle all validation
	def __validateHttpPost(self, req):

		self.__commonPreDBValidation(req)

		self.__commonPostDBValidation(req)


	def __commonPostDBValidation(self, req, client_id=None):

		# data validation
		appResponce = {}

		#db level check
		client_model = oauth2ClientModel()

		if client_id and not client_model.ifClientIdExists(client_id):
			self.raise404()
		elif client_id and not client_model.ifClientEditable(client_id):
			appResponce['client_id'] = self._getError('CL_NO_EDIT')
		else:
			if 'app_id' in req.body and client_model.ifAppIdExists(req.body['app_id'], client_id):
				appResponce['app_id'] = self._getError('CL_APPID_EXISTS')

			scope_model = oauth2ScopeModel()
			if 'scope' in req.body and len(req.body['scope']) > 0 and not scope_model.ifValidScopeCodeExists(req.body['scope']):
				appResponce['scope'] = self._getError('VALID_SCOPE_CODE')

		if appResponce:
			raise appException.clientException_400(appResponce)


	def __commonPreDBValidation(self, req):

		is_put = (req.method == 'PUT')

		appResponce = {}

		if is_put:
			editableFields = ['app_id', 'app_secret', 'scope', 'user_type']
			fieldReceived = [i for i in editableFields if i in req.body]
			if not fieldReceived:
				appResponce['app_id'] = self._getError('NEED_INFO')

		if(
			is_put
			and 'app_id' in req.body
			and (req.body['app_id'] == '' or (not isinstance(req.body['app_id'], str)))
		) or (
			not is_put
			and ('app_id' not in req.body or req.body['app_id'] == '' or (not isinstance(req.body['app_id'], str)))
		):
			appResponce['app_id'] = self._getError('CL_VALID_APPID')


		if(
			is_put
			and 'user_type' in req.body
			and (req.body['user_type'] == '' or (not isinstance(req.body['user_type'], str)) or req.body['user_type'] not in self.__allowed_user_types)
		) or (
			not is_put
			and ('user_type' not in req.body or req.body['user_type'] == '' or (not isinstance(req.body['user_type'], str)) or req.body['user_type'] not in self.__allowed_user_types)
		):
			appResponce['user_type'] = self._getError('CL_VALID_UTYPE')


		if(
			is_put
			and 'app_secret' in req.body
			and (req.body['app_secret'] == '' or (not isinstance(req.body['app_secret'], str)))
		) or (
			not is_put
			and ('app_secret' not in req.body or req.body['app_secret'] == '' or (not isinstance(req.body['app_secret'], str)))
		):
			appResponce['app_secret'] = self._getError('CL_SECRET')

		if(
			is_put
			and 'scope' in req.body
			and not isinstance(req.body['scope'], list)
		) or (
			not is_put
			and ('scope' not in req.body or not isinstance(req.body['scope'], list))
		):
			appResponce['scope'] = self._getError('VALID_SCOPE_CODE')
		else:
			if 'scope' in req.body:
				if req.body['scope']:
					nonInt = [i for i in req.body['scope'] if not isinstance(i, str)]
					if nonInt:
						appResponce['scope'] = self._getError('VALID_SCOPE_CODE')
				else:
					appResponce['scope'] = self._getError('ASSIGN_SCOPE')

		if appResponce:
			raise appException.clientException_400(appResponce)

	def _put(self, container, uid):
		req = container.req
		resp = container.resp
		'''Handles POST requests'''
		self.__validateHttpPut(req, uid)

		# this is valid request
		appResponce = {}

		client_detail = self._getFilteredRequestData(req, ['app_id', 'app_secret', 'scope', 'user_type'])
		client_detail['client_id'] = uid

		client_model = oauth2ClientModel()
		appResponce['result'] = client_model.updateClient(client_detail)

		resp.status = HTTP_200  # This is the default status

		resp.body = json.encode(appResponce)


	def __validateHttpPut(self, req, uid):

		self.__commonPreDBValidation(req)

		self.__commonPostDBValidation(req, uid)

	def _delete(self, container, uid):
		req = container.req
		resp = container.resp
		'''Handles POST requests'''
		self.__validateHttpDelete(req, uid)

		# this is valid request
		appResponce = {}
		client_model = oauth2ClientModel()

		appResponce['result'] = client_model.deleteClient(uid)

		resp.status = HTTP_200  # This is the default status

		resp.body = json.encode(appResponce)


	def __validateHttpDelete(self, req, uid):

		appResponce = {}
		
		#db level check
		#if skill synonym exists
		client_model = oauth2ClientModel()

		if not client_model.ifClientIdExists(uid):
			self.raise404()
		elif not client_model.ifClientEditable(uid):
			appResponce['client_id'] = self._getError('CL_NO_EDIT')

		if appResponce:
			raise appException.clientException_400(appResponce)
