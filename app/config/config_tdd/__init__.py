print("Setting up TDD enviornment")
from .pgdb import PGDB1
from .redisdb import REDIS_DB_CREDENTIALS

BACKEND_API_URL = "http://127.0.0.1:3032"

CLIENT_APP_CREDENTIALS = [
	"client_id",
	"client_secret"
]
print("Done")