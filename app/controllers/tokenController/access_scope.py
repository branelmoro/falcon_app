# always extend your controller from base_controller
# always give controller class name same as filename
from falcon import HTTP_200
from ..base_controller import CRUDS
from ..base_controller import appException

from ...library import json

# import all required models here
from ...models.oauth2Model import oauth2ScopeModel
from ...models.oauth2Model import oauth2ResourceModel

class accessScope(CRUDS):

	def __init__(self):
		self._search_template = self._getResource('ASS')
		self._search_page_template = self._getResource('ASP')
		self._create_template = self._getResource('AS')
		self._crud_template = self._getResource('ASU')

		self._resources = {
			self._search_template : 'ASS',
			self._search_page_template : 'ASP',
			self._create_template : 'AS',
			self._crud_template : 'ASU'
		}

	def getPath(self):
		return [
			self._create_template,
			self._search_template,
			self._search_page_template,
			self._crud_template
		]

	# def getPath(self):
	# 	return [i for i in self._resources]

	def _post(self, container):
		req = container.req
		resp = container.resp
		'''Handles POST requests'''
		self.__validateHttpPost(req)

		# this is valid request
		appResponce = {}

		resp.status = HTTP_200  # This is the default status

		scope_model = oauth2ScopeModel()

		scope_detail = self._getFilteredRequestData(req, ['code', 'scope_info', 'allowed_get', 'allowed_post', 'allowed_put', 'allowed_delete'])

		appResponce['result'] = scope_model.createScope(scope_detail)

		# insert into redis set

		resp.body = json.encode(appResponce)

	# function to handle all validation
	def __validateHttpPost(self, req):

		self.__commonPreDBValidation(req)

		self.__commonPostDBValidation(req)


	def __commonPostDBValidation(self, req, scope_id=None):

		# data validation
		appResponce = {}

		#db level check
		scope_model = oauth2ScopeModel()

		if scope_id and not scope_model.ifScopeIdExists(scope_id):
			self.raise404()
		elif scope_id and not scope_model.ifScopeEditable(scope_id):
			appResponce['scope_id'] = self._getError('AS_NO_EDIT')
		else:
			if 'code' in req.body and scope_model.ifScopeCodeExists(req.body['code'], scope_id):
				appResponce['code'] = self._getError('AS_CODE_EXISTS')

			resource_model = oauth2ResourceModel()
			if 'allowed_get' in req.body and len(req.body['allowed_get']) > 0 and not resource_model.ifValidResourcesExists(req.body['allowed_get']):
				appResponce['allowed_get'] = self._getError('AS_VALID_RES', data={'method':'get'})
			if 'allowed_post' in req.body and len(req.body['allowed_post']) > 0 and not resource_model.ifValidResourcesExists(req.body['allowed_post']):
				appResponce['allowed_post'] = self._getError('AS_VALID_RES', data={'method':'post'})
			if 'allowed_put' in req.body and len(req.body['allowed_put']) > 0 and not resource_model.ifValidResourcesExists(req.body['allowed_put']):
				appResponce['allowed_put'] = self._getError('AS_VALID_RES', data={'method':'put'})
			if 'allowed_delete' in req.body and len(req.body['allowed_delete']) > 0 and not resource_model.ifValidResourcesExists(req.body['allowed_delete']):
				appResponce['allowed_delete'] = self._getError('AS_VALID_RES', data={'method':'delete'})

			# for update scope case
			if scope_id:
				# check if atleast once resource is given
				lstAllowedScopes = ['allowed_get', 'allowed_post', 'allowed_put', 'allowed_delete']
				receivedScopes = [i for i in lstAllowedScopes if i in req.body]
				receivedNonEmptyScopes = [i for i in receivedScopes if len(req.body[i]) > 0]
				if receivedScopes and not receivedNonEmptyScopes:
					checkDbScopes = [i for i in lstAllowedScopes if i not in req.body]
					if checkDbScopes:
						# run query to check if atleat one resource access exists
						if not scope_model.ifAtleastOneResourceAccessIsGiven(scope_id, checkDbScopes):
							appResponce['allowed_resource'] = self._getError('AS_RESOURCE')
					else:
						appResponce['allowed_resource'] = self._getError('AS_RESOURCE')

		if appResponce:
			raise appException.clientException_400(appResponce)


	def __checkAllowedActionList(self, req, appResponce, allowed_method, is_put):
		if(allowed_method in req.body):
			if(not isinstance(req.body[allowed_method], list)):
				appResponce[allowed_method] = self._getError('AS_VALID_RES', data={'method':allowed_method})
			else:
				nonInt = [i for i in req.body[allowed_method] if not isinstance(i, str)]
				if nonInt:
					appResponce[allowed_method] = self._getError('AS_VALID_RES', data={'method':allowed_method})
		else:
			if not is_put:
				req.body[allowed_method] = []
		return appResponce


	def __commonPreDBValidation(self, req):

		is_put = (req.method == 'PUT')

		appResponce = {}

		if is_put:
			editableFields = ['code', 'scope_info', 'allowed_get', 'allowed_post', 'allowed_put', 'allowed_delete']
			fieldReceived = [i for i in editableFields if i in req.body]
			if not fieldReceived:
				appResponce['scope_id'] = self._getError('NEED_INFO')

		if(
			is_put
			and 'code' in req.body
			and (req.body['code'] == '' or (not isinstance(req.body['code'], str)))
		) or (
			not is_put
			and ('code' not in req.body or req.body['code'] == '' or (not isinstance(req.body['code'], str)))
		):
			appResponce['code'] = self._getError('AS_VALID_CODE')


		if(
			is_put
			and 'scope_info' in req.body
			and (req.body['scope_info'] == '' or (not isinstance(req.body['scope_info'], str)))
		) or (
			not is_put
			and ('scope_info' not in req.body or req.body['scope_info'] == '' or (not isinstance(req.body['scope_info'], str)))
		):
			appResponce['scope_info'] = self._getError('AS_VALID_INFO')


		if(not is_put and 'allowed_get' not in req.body and 'allowed_post' not in req.body and 'allowed_put' not in req.body and 'allowed_delete' not in req.body):
			appResponce['allowed_resource'] = self._getError('AS_RESOURCE')
		else:
			appResponce = self.__checkAllowedActionList(req, appResponce, 'allowed_get', is_put)
			appResponce = self.__checkAllowedActionList(req, appResponce, 'allowed_post', is_put)
			appResponce = self.__checkAllowedActionList(req, appResponce, 'allowed_put', is_put)
			appResponce = self.__checkAllowedActionList(req, appResponce, 'allowed_delete', is_put)

			# for create scope case
			if not is_put:
				lstAllowedScopes = ['allowed_get', 'allowed_post', 'allowed_put', 'allowed_delete']
				receivedScopes = [i for i in lstAllowedScopes if i in req.body and len(req.body[i]) > 0]
				if not receivedScopes:
					appResponce['allowed_resource'] = self._getError('AS_RESOURCE')


		if appResponce:
			raise appException.clientException_400(appResponce)

	def _put(self, container, uid):
		req = container.req
		resp = container.resp
		'''Handles POST requests'''
		self.__validateHttpPut(req, uid)

		# this is valid request
		appResponce = {}


		scope_detail = self._getFilteredRequestData(req, ['code', 'scope_info', 'allowed_get', 'allowed_post', 'allowed_put', 'allowed_delete'])
		scope_detail['id'] = uid

		scope_model = oauth2ScopeModel()
		appResponce['result'] = scope_model.updateScope(scope_detail)

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
		scope_model = oauth2ScopeModel()

		appResponce['result'] = scope_model.deleteScope(uid)

		resp.status = HTTP_200  # This is the default status

		resp.body = json.encode(appResponce)


	def __validateHttpDelete(self, req, uid):

		appResponce = {}
		
		#db level check
		#if skill synonym exists
		scope_model = oauth2ScopeModel()
		if not scope_model.ifScopeIdExists(uid):
			self.raise404()
		elif not scope_model.ifScopeEditable(uid):
			appResponce['code'] = self._getError('AS_NO_EDIT')

		if appResponce:
			raise appException.clientException_400(appResponce)
