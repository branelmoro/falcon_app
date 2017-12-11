awsCredentials = {
	"region_name" : 'us-east-1',
	"aws_access_key_id" : 'AKIAIWKFQJBWQ3FTNPWA',
	"aws_secret_access_key" : '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'
}

elasticCredentials = {
	"host" : 'elastic-search-binlog.shaadi.com',
	"port" : 80
}


# log_storage values are kinesis or dynamodb or anything else then directly connect to elasticsearch
log_storage = "kinesis"


db_aliases = {
	"db1" : "shaadi_innodb_33",
	"db2" : "shaadi_db2",
	"db3" : "shaadi_db3",
	"db4" : "shaadi_db4",
	"db5" : "shaadi_db5"
}


db_max_exclusion_pool_count = {
	"db1" : 150,
	"db2" : 250,
	"db3" : 250,
	"db4" : 100,
	"db5" : 100
}


server_databases_mapping = {
	"01" : {
		"host": "localhost",
		"port": 3306,
		"user": "user_binlog",
		"passwd": "u$3r@b!n",
		"databases":[
			"db1"
		]
	},
	"02" : {
		"host": "localhost",
		"port": 3306,
		"user": "user_binlog",
		"passwd": "u$3r@b!n",
		"databases":[
			"db2"
		]
	},
	"03" : {
		"host": "localhost",
		"port": 3306,
		"user": "branel",
		"passwd": "B6@n3l",
		"databases":[
			"db3"
		]
	}
}