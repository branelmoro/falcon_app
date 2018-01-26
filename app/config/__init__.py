try:
	from .env import env as enviornment
	print("Starting ----- " + enviornment + " enviornment for fetcher")
except ImportError:
	enviornment = "production"
	print("Enviornment not found...Starting ----- " + enviornment + " enviornment for fetcher")

if enviornment == "local":
	from .config_local import *
elif enviornment == "production":
	from .config_production import *