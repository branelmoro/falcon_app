BACKEND_API_URL = "http://127.0.0.1:3032"

CLIENT_APP_CREDENTIALS = [
	"admin_app",
	"shdfvbkflakjfjhslfhalisfjhjsghflajzshdnva"
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
	"appCache" : {
		"host":"127.0.0.1",
		"port":6379,
		"db":4
	},
	"skillDb" : {
		"host":"127.0.0.1",
		"port":6379,
		"db":5
	}
}