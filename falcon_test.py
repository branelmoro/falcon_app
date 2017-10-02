import app as app_wrapper

controllers = app_wrapper.controllers

app = app_wrapper.falcon.API()


arrControllers = []


# print(getattr(arrControllers))

arrControllers.append(controllers.indexController.index)
arrControllers.append(controllers.tokenController.index)
arrControllers.append(controllers.tokenController.resource)
arrControllers.append(controllers.tokenController.accessScope)
arrControllers.append(controllers.tokenController.adminUser)
arrControllers.append(controllers.tokenController.client)
arrControllers.append(controllers.specialityController.saveSearchSkill)
arrControllers.append(controllers.specialityController.searchSkillStatus)

for cntClass in arrControllers:
	obj = cntClass()
	app.add_route(obj.getPath(), obj)



def handle_404(req, resp):
    resp.status = app_wrapper.falcon.HTTP_404
    resp.body = '{"message" : "Url does not exists"}'

app.add_sink(handle_404, '')