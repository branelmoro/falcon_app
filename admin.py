import types
import admin_panel as app_wrapper

controllers = app_wrapper.controllers

app = app_wrapper.falcon.API()


arrControllers = []


# print(getattr(arrControllers))

# arrControllers.append(controllers.indexController.index)
# arrControllers.append(controllers.tokenController.index)
# arrControllers.append(controllers.tokenController.resource)
# arrControllers.append(controllers.tokenController.accessScope)
# arrControllers.append(controllers.tokenController.adminUser)
# arrControllers.append(controllers.tokenController.client)
# arrControllers.append(controllers.specialityController.saveSearchSkill)
# arrControllers.append(controllers.specialityController.searchSkillStatus)


def __getControllerClasses(controllers):
	controller_modules = [controllers.__dict__.get(a) for a in controllers.__dict__ if a != "base_controller" and a.find("__") != 0 and isinstance(controllers.__dict__.get(a), types.ModuleType)]
	arrControllers = []
	for i in controller_modules:
		abc  =  [i.__dict__.get(a) for a in i.__dict__ if a.find("__") != 0 and isinstance(i.__dict__.get(a), type)]
		arrControllers = arrControllers + abc
	return arrControllers

arrControllers = __getControllerClasses(controllers)

print(arrControllers)


for cntClass in arrControllers:
	obj = cntClass()
	app.add_route(obj.getPath(), obj)



def handle_404(req, resp):
    resp.status = app_wrapper.falcon.HTTP_404
    resp.body = '{"message" : "Url does not exists"}'

app.add_sink(handle_404, '')
