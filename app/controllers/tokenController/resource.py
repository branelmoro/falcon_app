# always extend your controller from base_controller
# always give controller class name same as filename
from falcon import HTTP_200
from ..base_controller import CRUDS
from ..base_controller import appException

from ...library import json

# import all required models here
from ...models.oauth2Model import oauth2ResourceModel

class resource(CRUDS):

	def __init__(self):
		self._search_template = self._getResource('RSS')
		self._search_page_template = self._getResource('RSP')
		self._create_template = self._getResource('RS')
		self._crud_template = self._getResource('RSU')

		self._resources = {
			self._search_template : 'RSS',
			self._search_page_template : 'RSP',
			self._create_template : 'RS',
			self._crud_template : 'RSU'
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

		data = self._getFilteredRequestData(req, ['code', 'resource_path', 'resource_info'])

		oauth2_resource = oauth2ResourceModel()
		appResponce['result'] = oauth2_resource.createNewResource(data)
		resp.status = HTTP_200  # This is the default status
		resp.body = json.encode(appResponce)

	# function to handle all validation
	def __validateHttpPost(self, req):
		# token validation
		self.validateHTTPRequest(req)

		self.__commonValidation(req)

		# data validation
		appResponce = {}

		# database level validation goes here
		oauth2_resource = oauth2ResourceModel()

		if oauth2_resource.ifResourcePathAlreadyExists(req.body['resource_path']):
			appResponce['resource_path'] = self._getError('RS_PATH')

		if oauth2_resource.ifResourceCodeAlreadyExists(req.body['code']):
			appResponce['code'] = 'Resource code already exists in database!'

		if appResponce:
			raise appException.clientException_400(appResponce)

	def __commonValidation(self, req):

		is_put = (req.method == 'PUT')

		appResponce = {}

		if is_put and ('code' not in req.body and 'resource_path' not in req.body and 'resource_info' not in req.body):
			# appResponce['resource_id'] = 'Please provide some information to update'
			appResponce['resource_id'] = self._getError('NEED_INFO')

		if(
			is_put
			and 'resource_path' in req.body
			and (req.body['resource_path'] == '' or (not isinstance(req.body['resource_path'], str)) or req.body['resource_path'].find('/') != 0)
		) or (
			not is_put
			and ('resource_path' not in req.body or req.body['resource_path'] == '' or (not isinstance(req.body['resource_path'], str)) or req.body['resource_path'].find('/') != 0)
		):
			# appResponce['resource_path'] = 'Please provide valid resource path'
			appResponce['resource_path'] = self._getError('RS_VPATH')

		if(
			is_put
			and 'resource_info' in req.body
			and req.body['resource_info'] == ''
		) or (
			not is_put
			and ('resource_info' not in req.body or req.body['resource_info'] == '')
		):
			# appResponce['resource_info'] = 'Please provide some resource information'
			appResponce['resource_info'] = self._getError('RS_INFO')

		if(
			is_put
			and 'code' in req.body
			and req.body['code'] == ''
		) or (
			not is_put
			and ('code' not in req.body or req.body['code'] == '')
		):
			appResponce['code'] = 'Please provide resource code'

		if appResponce:
			raise appException.clientException_400(appResponce)

	def _put(self, container, uid):
		req = container.req
		resp = container.resp
		'''Handles POST requests'''
		self.__validateHttpPut(req, uid)

		# this is valid request
		appResponce = {}

		data = self._getFilteredRequestData(req, ['code', 'resource_path', 'resource_info'])
		data['resource_id'] = uid

		oauth2_resource = oauth2ResourceModel()
		appResponce['result'] = oauth2_resource.updateResource(data)
		resp.status = HTTP_200  # This is the default status
		resp.body = json.encode(appResponce)

	# function to handle all validation
	def __validateHttpPut(self, req, uid):

		self.__commonValidation(req)

		# data validation
		appResponce = {}

		# database level validation goes here
		oauth2_resource = oauth2ResourceModel()

		if not oauth2_resource.ifResourceIdExists(uid):
			self.raise404()
		elif not oauth2_resource.ifResourceEditable(uid):
			# appResponce['resource_id'] = 'This resource is not editable'
			appResponce['resource_id'] = self._getError('RS_NO_EDIT')
		else:
			if 'resource_path' in req.body and oauth2_resource.ifResourcePathAlreadyExists(req.body['resource_path'], uid):
				# appResponce['resource_path'] = 'Resource path already exists in another record'
				appResponce['resource_path'] = self._getError('RS_PATH')
			if 'code' in req.body and oauth2_resource.ifResourceCodeAlreadyExists(req.body['code'], uid):
				appResponce['code'] = 'Resource code already exists in another record'

		if appResponce:
			raise appException.clientException_400(appResponce)

	def _delete(self, container, uid):
		req = container.req
		resp = container.resp
		'''Handles POST requests'''
		self.__validateHttpDelete(req, uid)

		# this is valid request
		appResponce = {}

		oauth2_resource = oauth2ResourceModel()
		appResponce['result'] = oauth2_resource.deleteResource(uid)
		resp.status = HTTP_200  # This is the default status
		resp.body = json.encode(appResponce)

	def __validateHttpDelete(self, req, uid):

		appResponce = {}
		
		# database level validation goes here
		oauth2_resource = oauth2ResourceModel()

		if not oauth2_resource.ifResourceIdExists(uid):
			self.raise404()
		elif not oauth2_resource.ifResourceEditable(uid):
			# appResponce['resource_id'] = 'Resource is not editable'
			appResponce['resource_id'] = self._getError('RS_NO_EDIT')

		if appResponce:
			raise appException.clientException_400(appResponce)
