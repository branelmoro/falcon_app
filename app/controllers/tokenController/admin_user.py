# always extend your controller from base_controller
# always give controller class name same as filename
from falcon import HTTP_200
from ..base_controller import CRUDS
from ..base_controller import appException

from ...library import json

# import all required models here
from ...models.oauth2Model import oauth2ScopeModel
from ...models.oauth2Model import oauth2AdminUserModel

class adminUser(CRUDS):

	def __init__(self):
		self._search_template = self._getResource('AUS')
		self._search_page_template = self._getResource('AUP')
		self._create_template = self._getResource('AU')
		self._crud_template = self._getResource('AUU')

		self._resources = {
			self._search_template : 'AUS',
			self._search_page_template : 'AUP',
			self._create_template : 'AU',
			self._crud_template : 'AUU'
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

		admin_user_model = oauth2AdminUserModel()

		admin_user_detail = self._getFilteredRequestData(req, ['username', 'password', 'scope'])

		appResponce['result'] = admin_user_model.createAdminUser(admin_user_detail)

		# insert into redis set

		resp.body = json.encode(appResponce)

	# function to handle all validation
	def __validateHttpPost(self, req):

		self.__commonPreDBValidation(req)

		self.__commonPostDBValidation(req)


	def __commonPostDBValidation(self, req, admin_user_id=None):

		# data validation
		appResponce = {}

		#db level check
		admin_user_model = oauth2AdminUserModel()

		if admin_user_id and not admin_user_model.ifAdminUserIdExists(admin_user_id):
			self.raise404()
		elif admin_user_id and not admin_user_model.ifAdminUserEditable(admin_user_id):
			appResponce['username'] = self._getError(25)
		else:
			if 'username' in req.body and admin_user_model.ifUserNameExists(req.body['username'], admin_user_id):
				appResponce['username'] = self._getError(26)

			scope_model = oauth2ScopeModel()
			if 'scope' in req.body and len(req.body['scope']) > 0 and not scope_model.ifValidScopesExists(req.body['scope']):
				appResponce['scope'] = self._getError(27)

		if appResponce:
			raise appException.clientException_400(appResponce)


	def __commonPreDBValidation(self, req):

		is_put = (req.method == 'PUT')

		appResponce = {}

		if is_put:
			editableFields = ['username', 'password', 'scope']
			fieldReceived = [i for i in editableFields if i in req.body]
			if not fieldReceived:
				appResponce['admin_user_id'] = self._getError(19)

		if(
			is_put
			and 'username' in req.body
			and (req.body['username'] == '' or (not isinstance(req.body['username'], str)))
		) or (
			not is_put
			and ('username' not in req.body or req.body['username'] == '' or (not isinstance(req.body['username'], str)))
		):
			appResponce['username'] = self._getError(20)

		if(
			is_put
			and 'password' in req.body
			and (req.body['password'] == '' or (not isinstance(req.body['password'], str)))
		) or (
			not is_put
			and ('password' not in req.body or req.body['password'] == '' or (not isinstance(req.body['password'], str)))
		):
			appResponce['password'] = self._getError(21)

		if(
			is_put
			and 'scope' in req.body
			and not isinstance(req.body['scope'], list)
		) or (
			not is_put
			and ('scope' not in req.body or not isinstance(req.body['scope'], list))
		):
			appResponce['scope'] = self._getError(22)
		else:
			if 'scope' in req.body:
				if req.body['scope']:
					nonInt = [i for i in req.body['scope'] if not isinstance(i, int)]
					if nonInt:
						appResponce['scope'] = self._getError(22)
				else:
					appResponce['scope'] = self._getError(23, data={'endpoint':'admin user'})

		if appResponce:
			raise appException.clientException_400(appResponce)

	def _put(self, container, uid):
		req = container.req
		resp = container.resp
		'''Handles POST requests'''
		self.__validateHttpPut(req, uid)

		# this is valid request
		appResponce = {}

		admin_user_detail = self._getFilteredRequestData(req, ['username', 'password', 'scope'])
		admin_user_detail['admin_user_id']

		admin_user_model = oauth2AdminUserModel()
		appResponce['result'] = admin_user_model.updateAdminUser(admin_user_detail)

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
		admin_user_model = oauth2AdminUserModel()

		appResponce['result'] = admin_user_model.deleteAdminUser(uid)

		resp.status = HTTP_200  # This is the default status

		resp.body = json.encode(appResponce)


	def __validateHttpDelete(self, req, uid):

		appResponce = {}

		#db level check
		#if skill synonym exists
		admin_user_model = oauth2AdminUserModel()

		if not admin_user_model.ifAdminUserIdExists(uid):
			self.raise404()
		elif not admin_user_model.ifAdminUserEditable(uid):
			appResponce['username'] = self._getError(25)

		if appResponce:
			raise appException.clientException_400(appResponce)
