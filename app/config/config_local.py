BACKEND_API_URL = "http://127.0.0.1:3032"

CLIENT_APP_CREDENTIALS = [
	"client_id",
	"client_secret"
]

REDIS_DB_CREDENTIALS = {
	"access_tokenDb" : {
		"host":"127.0.0.1",
		"port":6379,
		"db":0
	},
	"refresh_tokenDb" : {
		"host":"127.0.0.1",
		"port":6379,
		"db":1
	},
	"access_scopeDb" : {
		"host":"127.0.0.1",
		"port":6379,
		"db":2
	},
	"sessionDb" : {
		"host":"127.0.0.1",
		"port":6379,
		"db":3
	},
	"skillDb" : {
		"host":"127.0.0.1",
		"port":6379,
		"db":5
	}
}


PGDB1 = {
	"master":{
		"host":"127.0.0.1",
		"username":"branelm",
		"password":"root",
		"database":"laborstack",
		"port":5432
	},
	"slave":[
		{
			"host":"127.0.0.1",
			"username":"branelm",
			"password":"root",
			"database":"laborstack",
			"port":5432
		},
		{
			"host":"127.0.0.1",
			"username":"branelm",
			"password":"root",
			"database":"laborstack",
			"port":5432
		},
		{
			"host":"127.0.0.1",
			"username":"branelm",
			"password":"root",
			"database":"laborstack",
			"port":5432
		},
		{
			"host":"127.0.0.1",
			"username":"branelm",
			"password":"root",
			"database":"laborstack",
			"port":5432
		}
	]
}