BACKEND_API_URL = "http://127.0.0.1:3032"

CLIENT_APP_CREDENTIALS = [
	"client_id",
	"client_secret"
]

REDIS_DB_CREDENTIALS = {
	"token_scopeDb" : {
		"host":"127.0.0.1",
		"port":6379,
		"db":0,
		"max_connections":5
	},
	"refresh_tokenDb" : {
		"host":"127.0.0.1",
		"port":6379,
		"db":1,
		"max_connections":5
	},
	"access_scopeDb" : {
		"host":"127.0.0.1",
		"port":6379,
		"db":2,
		"max_connections":5
	},
	"client_sessionDb" : {
		"host":"127.0.0.1",
		"port":6379,
		"db":3,
		"max_connections":5
	},
	"appCache" : {
		"host":"127.0.0.1",
		"port":6379,
		"db":4,
		"max_connections":5
	},
	"skillDb" : {
		"host":"127.0.0.1",
		"port":6379,
		"db":5,
		"max_connections":5
	},
	"token_sessionDb" : {
		"host":"127.0.0.1",
		"port":6379,
		"db":6,
		"max_connections":5
	},
	"user_tokenDb" : {
		"host":"127.0.0.1",
		"port":6379,
		"db":7,
		"max_connections":5
	}
}


PGDB1 = {
	"master":{
		"host":"127.0.0.1",
		"user":"branelm",
		"password":"root",
		"database":"laborstack",
		"port":5432,
		"minconn":0,
		"maxconn":2
	},
	"slave":[
		{
			"host":"127.0.0.1",
			"user":"branelm",
			"password":"root",
			"database":"laborstack",
			"port":5432,
			"minconn":0,
			"maxconn":2
		},
		{
			"host":"127.0.0.1",
			"user":"branelm",
			"password":"root",
			"database":"laborstack",
			"port":5432,
			"minconn":0,
			"maxconn":2
		},
		{
			"host":"127.0.0.1",
			"user":"branelm",
			"password":"root",
			"database":"laborstack",
			"port":5432,
			"minconn":0,
			"maxconn":2
		},
		{
			"host":"127.0.0.1",
			"user":"branelm",
			"password":"root",
			"database":"laborstack",
			"port":5432,
			"minconn":0,
			"maxconn":2
		}
	]
}