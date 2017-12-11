awsCredentials = {
	"region_name" : 'us-east-1',
	"aws_access_key_id" : 'AKIAJN72UGDXU5L3LEZQ',
	"aws_secret_access_key" : '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'
}

elasticCredentials = {
	# "host" : 'search-sid-shaadi-search-mx5f7ddd5bgpoljfmuwanj73ua.ap-south-1.es.amazonaws.com',
	# "port" : 80
	"host" : '10.10.0.73',
	"port" : 9200
}


# log_storage values are kinesis or dynamodb or anything else then directly connect to elasticsearch
log_storage = "kinesis"


db_aliases = {
	"db1" : "shaadi_innodb_33_stg",
	"db2" : "shaadi_db2stg",
	"db3" : "shaadi_db3stg",
	"db4" : "shaadi_db4stg",
	"db5" : "shaadi_db5stg"
}


db_max_exclusion_pool_count = {
	"db1" : 150,
	"db2" : 250,
	"db3" : 250,
	"db4" : 100,
	"db5" : 100
}


server_databases_mapping = {
	"1" : {
		"host": "10.10.0.18",
		"port": 3306,
		"user": "root",
		"passwd": "shaadi",
		"databases":[
			"db1",
			"db2",
			"db3",
			"db4",
			"db5"
		]
	}
}