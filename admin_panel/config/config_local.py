BACKEND_API_URL = "http://127.0.0.1:3032"

CLIENT_APP_CREDENTIALS = [
	"admin_app",
	"shdfvbkflakjfjhslfhalisfjhjsghflajzshdnva"
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