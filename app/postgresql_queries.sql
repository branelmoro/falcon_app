CREATE DATABASE laborstack
WITH ENCODING = 'UTF8'
TEMPLATE = template0
CONNECTION LIMIT = -1;

-- CREATE EXTENSION postgis;

CREATE TYPE lang AS ENUM ('english','hindi','marathi','gujarati','malayalam','bengali','oriya','tamil','telugu','panjabi','urdu','chinese_simplified','chinese_traditional','arabic','russian','portuguese','japanese','german','korean','french','turkish','italian','polish','ukrainian','persian','romanian','serbian','croatian','thai','dutch','amharic','catalan','danish','greek','spanish','estonian','finnish','armenian','khmer','kannada','malay','nepali','norwegian','slovak','albanian','swedish','tagalog');
CREATE TYPE search_skill_status AS ENUM ('invalid', 'valid', 'pending');
CREATE TYPE search_location_type AS ENUM ('world','country','region','city','area');
CREATE TYPE account_status as ENUM('enabled', 'disabled');
CREATE TYPE primary_contact_type AS ENUM ('mob', 'email');
CREATE TYPE gend AS ENUM ('male','female','unknown');
CREATE TYPE profile_bucket AS ENUM ('a','b','c');--approximately 100 buckets
CREATE TYPE bloodGroup AS ENUM ('A+','A-','B+','B-','AB+','AB-','O+','O-');
CREATE TYPE usertype AS ENUM ('guest','registered_user','admin');

-- oauth2 and admin authentication
CREATE SCHEMA oauth2;
CREATE TABLE oauth2.resource (
 id serial PRIMARY KEY,
 resource_path varchar(300) NOT NULL,
 resource_info varchar(300),
 is_editable boolean DEFAULT true,
 last_edit_time TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now(),
 UNIQUE (resource_path)
);
INSERT INTO oauth2.resource (id, resource_path, resource_info, is_editable) VALUES (1, '/resource/', 'manage resource', false), (2, '/access-scope/', 'manage access-scope', false), (3, '/admin-user/', 'manage admin-user', false), (4, '/client/', 'manage clients', false), (5, '/errors/', 'manage errors', false);
ALTER SEQUENCE oauth2.resource_id_seq RESTART WITH 5;
CREATE TABLE oauth2.scope (
 id serial PRIMARY KEY,
 scope_name varchar(80) NOT NULL UNIQUE,
 scope_info varchar(100),
 allowed_get smallint[],
 allowed_post smallint[],
 allowed_put smallint[],
 allowed_delete smallint[],
 is_editable boolean DEFAULT true,
 last_edit_time TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now()
);
CREATE INDEX oauth2_scope_allowed_get ON oauth2.scope (allowed_get);
CREATE INDEX oauth2_scope_allowed_post ON oauth2.scope (allowed_post);
CREATE INDEX oauth2_scope_allowed_put ON oauth2.scope (allowed_put);
CREATE INDEX oauth2_scope_allowed_delete ON oauth2.scope (allowed_delete);
CREATE INDEX oauth2_scope_is_editable ON oauth2.scope (is_editable);
INSERT INTO oauth2.scope (id, scope_name, scope_info, allowed_get, allowed_post, allowed_put, allowed_delete, is_editable) VALUES (1, 'superuser', '123456', '{1,2,3}', '{1,2,3}', '{1,2,3}', '{1,2,3}', false);
ALTER SEQUENCE oauth2.scope_id_seq RESTART WITH 2;
CREATE TABLE oauth2.admin_user (
 id serial PRIMARY KEY,
 username varchar(80) NOT NULL UNIQUE,
 password varchar(80) NOT NULL,
 scope smallint[],
 is_editable boolean DEFAULT true,
 last_edit_time TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now()
);
CREATE INDEX oauth2_admin_user_password ON oauth2.admin_user (password);
CREATE INDEX oauth2_admin_scope ON oauth2.admin_user (scope);
CREATE INDEX oauth2_admin_user_is_editable ON oauth2.admin_user (is_editable);
INSERT INTO oauth2.admin_user (id, username, password, scope, is_editable) VALUES (1, 'branelm', '123456', '{1}', false);
ALTER SEQUENCE oauth2.admin_user_id_seq RESTART WITH 2;
CREATE TABLE oauth2.client (
 id serial PRIMARY KEY,
 app_id varchar(80) NOT NULL UNIQUE,
 app_secret varchar(80) NOT NULL,
 scope smallint[],
 user_type usertype,
 is_editable boolean DEFAULT true,
 last_edit_time TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now()
);
CREATE INDEX oauth2_client_password ON oauth2.client (app_secret);
CREATE INDEX oauth2_client_scope ON oauth2.client (scope);
CREATE INDEX oauth2_client_usertype ON oauth2.client (user_type);
CREATE INDEX oauth2_client_is_editable ON oauth2.client (is_editable);
INSERT INTO oauth2.client (id, app_id, app_secret, scope, user_type, is_editable) VALUES (1, 'admin_app', 'shdfvbkflakjfjhslfhalisfjhjsghflajzshdnva', '{1,2,3,4,5}','admin', false), (2, 'web_app', 'yturerfa43t565u43qgf35w4e4q3th54sf', '{1,2,3,4,5}','admin', false);
ALTER SEQUENCE oauth2.client_id_seq RESTART WITH 3;


CREATE SCHEMA static_text;
CREATE TABLE static_text.errors (
 id serial PRIMARY KEY,
 info text NOT NULL,
 english text NOT NULL UNIQUE,
 hindi text DEFAULT NULL,
 marathi text DEFAULT NULL,
 gujarati text DEFAULT NULL,
 malayalam text DEFAULT NULL,
 bengali text DEFAULT NULL,
 oriya text DEFAULT NULL,
 tamil text DEFAULT NULL,
 telugu text DEFAULT NULL,
 panjabi text DEFAULT NULL,
 urdu text DEFAULT NULL,
 chinese_simplified text DEFAULT NULL,
 chinese_traditional text DEFAULT NULL,
 arabic text DEFAULT NULL,
 russian text DEFAULT NULL,
 portuguese text DEFAULT NULL,
 japanese text DEFAULT NULL,
 german text DEFAULT NULL,
 korean text DEFAULT NULL,
 french text DEFAULT NULL,
 turkish text DEFAULT NULL,
 italian text DEFAULT NULL,
 polish text DEFAULT NULL,
 ukrainian text DEFAULT NULL,
 persian text DEFAULT NULL,
 romanian text DEFAULT NULL,
 serbian text DEFAULT NULL,
 croatian text DEFAULT NULL,
 thai text DEFAULT NULL,
 dutch text DEFAULT NULL,
 amharic text DEFAULT NULL,
 catalan text DEFAULT NULL,
 danish text DEFAULT NULL,
 greek text DEFAULT NULL,
 spanish text DEFAULT NULL,
 estonian text DEFAULT NULL,
 finnish text DEFAULT NULL,
 armenian text DEFAULT NULL,
 khmer text DEFAULT NULL,
 kannada text DEFAULT NULL,
 malay text DEFAULT NULL,
 nepali text DEFAULT NULL,
 norwegian text DEFAULT NULL,
 slovak text DEFAULT NULL,
 albanian text DEFAULT NULL,
 swedish text DEFAULT NULL,
 tagalog text DEFAULT NULL,
 is_editable boolean DEFAULT true,
 last_edit_time TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now()
);

INSERT INTO static_text.errors (id, info, english, is_editable) VALUES (1, 'resource api', 'Resource path already exists in another record in database!', false),
(2, 'resource api', 'Please provide a valid resource id!', false),
(3, 'resource api', 'No resorce information provided for updation.. Please provide some information!', false),
(4, 'resource api', 'Please provide a valid resource path!', false),
(5, 'resource api', 'Please provide some resource information!', false),
(6, 'resource api', 'This resource is not editable!', false),
(7, 'resource api', 'Resource id does not exists in database!', false),
(8, 'access-scope api', 'Invalid scope provided..Please provide a valid scope!', false),
(9, 'access-scope api', 'No scope information provided for updation.. Please provide some information!', false),
(10, 'access-scope api', 'Please provide a valid scope name!', false),
(11, 'access-scope api', 'Please provide valid scope info!', false),
(12, 'access-scope api', 'Please provide atleast one resource access to scope!', false),
(13, 'resource api', 'Scope id does not exists in database!', false),
(14, 'resource api', 'This access scope is not editable!', false),
(15, 'resource api', 'Scope name already exists in another record in database!', false),
(16, 'access-scope api', 'Invalid {method} resources provided..Please provide valid resources!', false),
(17, 'access-scope api', 'Please provide list of valid {method} resources!', false),
(18, 'admin-user api', 'Please provide a valid admin user id!', false),
(19, 'admin-user api', 'No admin-user information provided for updation.. Please provide some information!', false),
(20, 'admin-user api', 'Please provide a valid username for admin user!', false),
(21, 'admin-user api', 'Please provide a password for admin user account!', false),
(22, 'admin-user api, client api', 'Please provide list of valid access scopes!', false),
(23, 'admin-user api, client api', 'Please provide at least one access scope to {endpoint}!', false),
(24, 'admin-user api', 'Admin User id does not exist!', false),
(25, 'admin-user api', 'Admin user is not editable!', false),
(26, 'admin-user api', 'Username already exists in database!', false),
(27, 'admin-user api, client api', 'Invalid scopes provided..Please provide list of valid access scopes!', false),
(28, 'client api', 'Client id does not exist!', false),
(29, 'client api', 'Client is not editable!', false),
(30, 'client api', 'Client App Id already exists in database!', false),
(31, 'client api', 'No client information provided for updation.. Please provide some information!', false),
(32, 'client api', 'Please provide a valid client id!', false),
(33, 'client api', 'Please provide valid app id!', false),
(34, 'client api', 'Please provide valid user type!', false),
(35, 'client api', 'Please provide valid app secret!', false),
(36, 'errors api', 'Please provide a valid error id!', false),
(37, 'errors api', 'No error information provided for updation.. Please provide some information!', false),
(38, 'errors api', 'Please provide error information!', false),
(39, 'errors api', 'Please provide a valid error message in {language}!', false),
(40, 'errors api', 'Error id does not exist!', false),
(41, 'errors api', 'Error is not editable!', false),
(42, 'errors api', 'Error in {language} already exists in database!', false),
(43, 'token api', 'Grant Authorization code not implemented yet!', false),
(44, 'token api', 'Please provide authorization credentials!', false),
(45, 'token api', 'Invalid client app credentials provided for authorization!', false),
(46, 'token api', 'Please provide a grant type!', false),
(47, 'token api', 'Invalid grant type provided..Please provide a valid grant type!', false),
(48, 'token api', 'Please provide username!', false),
(49, 'token api', 'Please provide password!', false),
(50, 'token api', 'Please provide refresh token!', false),
(51, 'token api', 'Authorization code not implemented yet!', false),
(52, 'token api', 'Username and password do not match!', false),
(53, 'token api', 'Please provide access token or refresh token!', false)
;
ALTER SEQUENCE static_text.errors_id_seq RESTART WITH 54;
CREATE TABLE static_text.labels (
 id serial PRIMARY KEY,
 info text NOT NULL,
 english text NOT NULL UNIQUE,
 hindi text DEFAULT NULL,
 marathi text DEFAULT NULL,
 gujarati text DEFAULT NULL,
 malayalam text DEFAULT NULL,
 bengali text DEFAULT NULL,
 oriya text DEFAULT NULL,
 tamil text DEFAULT NULL,
 telugu text DEFAULT NULL,
 panjabi text DEFAULT NULL,
 urdu text DEFAULT NULL,
 chinese_simplified text DEFAULT NULL,
 chinese_traditional text DEFAULT NULL,
 arabic text DEFAULT NULL,
 russian text DEFAULT NULL,
 portuguese text DEFAULT NULL,
 japanese text DEFAULT NULL,
 german text DEFAULT NULL,
 korean text DEFAULT NULL,
 french text DEFAULT NULL,
 turkish text DEFAULT NULL,
 italian text DEFAULT NULL,
 polish text DEFAULT NULL,
 ukrainian text DEFAULT NULL,
 persian text DEFAULT NULL,
 romanian text DEFAULT NULL,
 serbian text DEFAULT NULL,
 croatian text DEFAULT NULL,
 thai text DEFAULT NULL,
 dutch text DEFAULT NULL,
 amharic text DEFAULT NULL,
 catalan text DEFAULT NULL,
 danish text DEFAULT NULL,
 greek text DEFAULT NULL,
 spanish text DEFAULT NULL,
 estonian text DEFAULT NULL,
 finnish text DEFAULT NULL,
 armenian text DEFAULT NULL,
 khmer text DEFAULT NULL,
 kannada text DEFAULT NULL,
 malay text DEFAULT NULL,
 nepali text DEFAULT NULL,
 norwegian text DEFAULT NULL,
 slovak text DEFAULT NULL,
 albanian text DEFAULT NULL,
 swedish text DEFAULT NULL,
 tagalog text DEFAULT NULL,
 is_editable boolean DEFAULT true,
 last_edit_time TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now()
);






CREATE SCHEMA speciality;

CREATE TABLE speciality.skill_parent (
 id smallserial PRIMARY KEY,
 skill_info text NOT NULL,
 english varchar(80) DEFAULT NULL UNIQUE,
 hindi varchar(80) DEFAULT NULL UNIQUE,
 marathi varchar(80) DEFAULT NULL UNIQUE,
 gujarati varchar(80) DEFAULT NULL UNIQUE,
 malayalam varchar(80) DEFAULT NULL UNIQUE,
 bengali varchar(80) DEFAULT NULL UNIQUE,
 oriya varchar(80) DEFAULT NULL UNIQUE,
 tamil varchar(80) DEFAULT NULL UNIQUE,
 telugu varchar(80) DEFAULT NULL UNIQUE,
 panjabi varchar(80) DEFAULT NULL UNIQUE,
 urdu varchar(80) DEFAULT NULL UNIQUE,
 chinese_simplified varchar(80) DEFAULT NULL UNIQUE,
 chinese_traditional varchar(80) DEFAULT NULL UNIQUE,
 arabic varchar(80) DEFAULT NULL UNIQUE,
 russian varchar(80) DEFAULT NULL UNIQUE,
 portuguese varchar(80) DEFAULT NULL UNIQUE,
 japanese varchar(80) DEFAULT NULL UNIQUE,
 german varchar(80) DEFAULT NULL UNIQUE,
 korean varchar(80) DEFAULT NULL UNIQUE,
 french varchar(80) DEFAULT NULL UNIQUE,
 turkish varchar(80) DEFAULT NULL UNIQUE,
 italian varchar(80) DEFAULT NULL UNIQUE,
 polish varchar(80) DEFAULT NULL UNIQUE,
 ukrainian varchar(80) DEFAULT NULL UNIQUE,
 persian varchar(80) DEFAULT NULL UNIQUE,
 romanian varchar(80) DEFAULT NULL UNIQUE,
 serbian varchar(80) DEFAULT NULL UNIQUE,
 croatian varchar(80) DEFAULT NULL UNIQUE,
 thai varchar(80) DEFAULT NULL UNIQUE,
 dutch varchar(80) DEFAULT NULL UNIQUE,
 amharic varchar(80) DEFAULT NULL UNIQUE,
 catalan varchar(80) DEFAULT NULL UNIQUE,
 danish varchar(80) DEFAULT NULL UNIQUE,
 greek varchar(80) DEFAULT NULL UNIQUE,
 spanish varchar(80) DEFAULT NULL UNIQUE,
 estonian varchar(80) DEFAULT NULL UNIQUE,
 finnish varchar(80) DEFAULT NULL UNIQUE,
 armenian varchar(80) DEFAULT NULL UNIQUE,
 khmer varchar(80) DEFAULT NULL UNIQUE,
 kannada varchar(80) DEFAULT NULL UNIQUE,
 malay varchar(80) DEFAULT NULL UNIQUE,
 nepali varchar(80) DEFAULT NULL UNIQUE,
 norwegian varchar(80) DEFAULT NULL UNIQUE,
 slovak varchar(80) DEFAULT NULL UNIQUE,
 albanian varchar(80) DEFAULT NULL UNIQUE,
 swedish varchar(80) DEFAULT NULL UNIQUE,
 tagalog varchar(80) DEFAULT NULL UNIQUE,
 profile_exists boolean DEFAULT false,
 skill_icon_path varchar(80) DEFAULT '/path-to-default/',
 last_edit_time TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now()
);
CREATE INDEX skill_parent_profile_exists ON speciality.skill_parent (profile_exists);


CREATE TABLE speciality.skill_synonym (
 id serial PRIMARY KEY,
 skill_parent_id int DEFAULT NULL references speciality.skill_parent (id),
 skill_name varchar(80) UNIQUE NOT NULL,
 written_language lang[],
 profile_exists boolean DEFAULT false,
 search_count int DEFAULT 0,
 assigned_to int,
 status search_skill_status DEFAULT 'pending',
 skill_icon_path varchar(80) DEFAULT '/path-to-default/',
 last_edit_time TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now()
);
CREATE INDEX skill_synonym_skill_parent_id ON speciality.skill_synonym (skill_parent_id);
CREATE INDEX skill_synonym_profile_exists ON speciality.skill_synonym (profile_exists);
CREATE INDEX skill_synonym_last_edit_time ON speciality.skill_synonym (last_edit_time);
CREATE INDEX skill_synonym_search_count ON speciality.skill_synonym (search_count);
CREATE INDEX skill_synonym_assigned_to ON speciality.skill_synonym (assigned_to);


CREATE TABLE speciality.search_skill (
 id serial PRIMARY KEY,
 search_word varchar(80) NOT NULL UNIQUE,
 assigned_to int,
 status search_skill_status DEFAULT 'pending',
 search_count int DEFAULT 0
);
CREATE INDEX search_skill_assigned_to ON speciality.search_skill (assigned_to);
CREATE INDEX search_skill_status ON speciality.search_skill (status);
CREATE INDEX search_search_count ON speciality.search_skill (search_count);


CREATE TABLE speciality.skill_parent_child_mapping (
 id serial PRIMARY KEY,
 parent_id int references speciality.skill_parent (id),
 child_id int references speciality.skill_parent (id),
 created_by int,
 comment varchar(300),
 last_edit_time TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now()
);
CREATE INDEX skill_parent_child_mapping_parent_id ON speciality.skill_parent_child_mapping (parent_id);
CREATE INDEX skill_parent_child_mapping_child_id ON speciality.skill_parent_child_mapping (child_id);
CREATE INDEX skill_parent_child_mapping_created_by ON speciality.skill_parent_child_mapping (created_by);


CREATE SCHEMA location;

CREATE TABLE location.country_grid (
 id smallserial PRIMARY KEY,
 country_code varchar(2) DEFAULT NULL UNIQUE,
 english varchar(80) NOT NULL UNIQUE,
 hindi varchar(80) DEFAULT NULL UNIQUE,
 marathi varchar(80) DEFAULT NULL UNIQUE,
 gujarati varchar(80) DEFAULT NULL UNIQUE,
 malayalam varchar(80) DEFAULT NULL UNIQUE,
 bengali varchar(80) DEFAULT NULL UNIQUE,
 oriya varchar(80) DEFAULT NULL UNIQUE,
 tamil varchar(80) DEFAULT NULL UNIQUE,
 telugu varchar(80) DEFAULT NULL UNIQUE,
 panjabi varchar(80) DEFAULT NULL UNIQUE,
 urdu varchar(80) DEFAULT NULL UNIQUE,
 chinese_simplified varchar(80) DEFAULT NULL UNIQUE,
 chinese_traditional varchar(80) DEFAULT NULL UNIQUE,
 mandarin_chinese varchar(80) DEFAULT NULL UNIQUE,
 arabic varchar(80) DEFAULT NULL UNIQUE,
 russian varchar(80) DEFAULT NULL UNIQUE,
 portuguese varchar(80) DEFAULT NULL UNIQUE,
 japanese varchar(80) DEFAULT NULL UNIQUE,
 german varchar(80) DEFAULT NULL UNIQUE,
 korean varchar(80) DEFAULT NULL UNIQUE,
 french varchar(80) DEFAULT NULL UNIQUE,
 turkish varchar(80) DEFAULT NULL UNIQUE,
 italian varchar(80) DEFAULT NULL UNIQUE,
 polish varchar(80) DEFAULT NULL UNIQUE,
 ukrainian varchar(80) DEFAULT NULL UNIQUE,
 persian varchar(80) DEFAULT NULL UNIQUE,
 romanian varchar(80) DEFAULT NULL UNIQUE,
 serbian varchar(80) DEFAULT NULL UNIQUE,
 croatian varchar(80) DEFAULT NULL UNIQUE,
 thai varchar(80) DEFAULT NULL UNIQUE,
 dutch varchar(80) DEFAULT NULL UNIQUE,
 amharic varchar(80) DEFAULT NULL UNIQUE,
 catalan varchar(80) DEFAULT NULL UNIQUE,
 danish varchar(80) DEFAULT NULL UNIQUE,
 greek varchar(80) DEFAULT NULL UNIQUE,
 spanish varchar(80) DEFAULT NULL UNIQUE,
 estonian varchar(80) DEFAULT NULL UNIQUE,
 finnish varchar(80) DEFAULT NULL UNIQUE,
 armenian varchar(80) DEFAULT NULL UNIQUE,
 khmer varchar(80) DEFAULT NULL UNIQUE,
 kannada varchar(80) DEFAULT NULL UNIQUE,
 malay varchar(80) DEFAULT NULL UNIQUE,
 nepali varchar(80) DEFAULT NULL UNIQUE,
 norwegian varchar(80) DEFAULT NULL UNIQUE,
 slovak varchar(80) DEFAULT NULL UNIQUE,
 albanian varchar(80) DEFAULT NULL UNIQUE,
 swedish varchar(80) DEFAULT NULL UNIQUE,
 tagalog varchar(80) DEFAULT NULL UNIQUE
);

CREATE TABLE location.region_grid (
 id smallserial PRIMARY KEY,
 country_grid_id int NOT NULL references location.country_grid (id),
 region_code varchar(2) DEFAULT NULL,
 english varchar(80) NOT NULL,
 hindi varchar(80) DEFAULT NULL,
 marathi varchar(80) DEFAULT NULL,
 gujarati varchar(80) DEFAULT NULL,
 malayalam varchar(80) DEFAULT NULL,
 bengali varchar(80) DEFAULT NULL,
 oriya varchar(80) DEFAULT NULL,
 tamil varchar(80) DEFAULT NULL,
 telugu varchar(80) DEFAULT NULL,
 panjabi varchar(80) DEFAULT NULL,
 urdu varchar(80) DEFAULT NULL,
 chinese_simplified varchar(80) DEFAULT NULL,
 chinese_traditional varchar(80) DEFAULT NULL,
 mandarin_chinese varchar(80) DEFAULT NULL,
 arabic varchar(80) DEFAULT NULL,
 russian varchar(80) DEFAULT NULL,
 portuguese varchar(80) DEFAULT NULL,
 japanese varchar(80) DEFAULT NULL,
 german varchar(80) DEFAULT NULL,
 korean varchar(80) DEFAULT NULL,
 french varchar(80) DEFAULT NULL,
 turkish varchar(80) DEFAULT NULL,
 italian varchar(80) DEFAULT NULL,
 polish varchar(80) DEFAULT NULL,
 ukrainian varchar(80) DEFAULT NULL,
 persian varchar(80) DEFAULT NULL,
 romanian varchar(80) DEFAULT NULL,
 serbian varchar(80) DEFAULT NULL,
 croatian varchar(80) DEFAULT NULL,
 thai varchar(80) DEFAULT NULL,
 dutch varchar(80) DEFAULT NULL,
 amharic varchar(80) DEFAULT NULL,
 catalan varchar(80) DEFAULT NULL,
 danish varchar(80) DEFAULT NULL,
 greek varchar(80) DEFAULT NULL,
 spanish varchar(80) DEFAULT NULL,
 estonian varchar(80) DEFAULT NULL,
 finnish varchar(80) DEFAULT NULL,
 armenian varchar(80) DEFAULT NULL,
 khmer varchar(80) DEFAULT NULL,
 kannada varchar(80) DEFAULT NULL,
 malay varchar(80) DEFAULT NULL,
 nepali varchar(80) DEFAULT NULL,
 norwegian varchar(80) DEFAULT NULL,
 slovak varchar(80) DEFAULT NULL,
 albanian varchar(80) DEFAULT NULL,
 swedish varchar(80) DEFAULT NULL,
 tagalog varchar(80) DEFAULT NULL,
 UNIQUE (country_grid_id, english),
 UNIQUE (country_grid_id, hindi),
 UNIQUE (country_grid_id, marathi),
 UNIQUE (country_grid_id, gujarati),
 UNIQUE (country_grid_id, malayalam),
 UNIQUE (country_grid_id, bengali),
 UNIQUE (country_grid_id, oriya),
 UNIQUE (country_grid_id, tamil),
 UNIQUE (country_grid_id, telugu),
 UNIQUE (country_grid_id, panjabi),
 UNIQUE (country_grid_id, urdu),
 UNIQUE (country_grid_id, chinese_simplified),
 UNIQUE (country_grid_id, chinese_traditional),
 UNIQUE (country_grid_id, mandarin_chinese),
 UNIQUE (country_grid_id, arabic),
 UNIQUE (country_grid_id, russian),
 UNIQUE (country_grid_id, portuguese),
 UNIQUE (country_grid_id, japanese),
 UNIQUE (country_grid_id, german),
 UNIQUE (country_grid_id, korean),
 UNIQUE (country_grid_id, french),
 UNIQUE (country_grid_id, turkish),
 UNIQUE (country_grid_id, italian),
 UNIQUE (country_grid_id, polish),
 UNIQUE (country_grid_id, ukrainian),
 UNIQUE (country_grid_id, persian),
 UNIQUE (country_grid_id, romanian),
 UNIQUE (country_grid_id, serbian),
 UNIQUE (country_grid_id, croatian),
 UNIQUE (country_grid_id, thai),
 UNIQUE (country_grid_id, dutch),
 UNIQUE (country_grid_id, amharic),
 UNIQUE (country_grid_id, catalan),
 UNIQUE (country_grid_id, danish),
 UNIQUE (country_grid_id, greek),
 UNIQUE (country_grid_id, spanish),
 UNIQUE (country_grid_id, estonian),
 UNIQUE (country_grid_id, finnish),
 UNIQUE (country_grid_id, armenian),
 UNIQUE (country_grid_id, khmer),
 UNIQUE (country_grid_id, kannada),
 UNIQUE (country_grid_id, malay),
 UNIQUE (country_grid_id, nepali),
 UNIQUE (country_grid_id, norwegian),
 UNIQUE (country_grid_id, slovak),
 UNIQUE (country_grid_id, albanian),
 UNIQUE (country_grid_id, swedish),
 UNIQUE (country_grid_id, tagalog)
);
CREATE INDEX region_grid_country_grid_id ON location.region_grid (country_grid_id);

CREATE TABLE location.city_grid (
 id serial PRIMARY KEY,
 country_grid_id int NOT NULL references location.country_grid (id),
 region_grid_id int DEFAULT NULL references location.region_grid (id),
 english varchar(80) NOT NULL,
 hindi varchar(80) DEFAULT NULL,
 marathi varchar(80) DEFAULT NULL,
 gujarati varchar(80) DEFAULT NULL,
 malayalam varchar(80) DEFAULT NULL,
 bengali varchar(80) DEFAULT NULL,
 oriya varchar(80) DEFAULT NULL,
 tamil varchar(80) DEFAULT NULL,
 telugu varchar(80) DEFAULT NULL,
 panjabi varchar(80) DEFAULT NULL,
 urdu varchar(80) DEFAULT NULL,
 chinese_simplified varchar(80) DEFAULT NULL,
 chinese_traditional varchar(80) DEFAULT NULL,
 mandarin_chinese varchar(80) DEFAULT NULL,
 arabic varchar(80) DEFAULT NULL,
 russian varchar(80) DEFAULT NULL,
 portuguese varchar(80) DEFAULT NULL,
 japanese varchar(80) DEFAULT NULL,
 german varchar(80) DEFAULT NULL,
 korean varchar(80) DEFAULT NULL,
 french varchar(80) DEFAULT NULL,
 turkish varchar(80) DEFAULT NULL,
 italian varchar(80) DEFAULT NULL,
 polish varchar(80) DEFAULT NULL,
 ukrainian varchar(80) DEFAULT NULL,
 persian varchar(80) DEFAULT NULL,
 romanian varchar(80) DEFAULT NULL,
 serbian varchar(80) DEFAULT NULL,
 croatian varchar(80) DEFAULT NULL,
 thai varchar(80) DEFAULT NULL,
 dutch varchar(80) DEFAULT NULL,
 amharic varchar(80) DEFAULT NULL,
 catalan varchar(80) DEFAULT NULL,
 danish varchar(80) DEFAULT NULL,
 greek varchar(80) DEFAULT NULL,
 spanish varchar(80) DEFAULT NULL,
 estonian varchar(80) DEFAULT NULL,
 finnish varchar(80) DEFAULT NULL,
 armenian varchar(80) DEFAULT NULL,
 khmer varchar(80) DEFAULT NULL,
 kannada varchar(80) DEFAULT NULL,
 malay varchar(80) DEFAULT NULL,
 nepali varchar(80) DEFAULT NULL,
 norwegian varchar(80) DEFAULT NULL,
 slovak varchar(80) DEFAULT NULL,
 albanian varchar(80) DEFAULT NULL,
 swedish varchar(80) DEFAULT NULL,
 tagalog varchar(80) DEFAULT NULL,
 is_verified boolean DEFAULT false,
 parent_city_id int DEFAULT NULL references location.city_grid (id),
 moved_to_keyword_search boolean DEFAULT false,
 UNIQUE (country_grid_id, region_grid_id, english),
 UNIQUE (country_grid_id, region_grid_id, hindi),
 UNIQUE (country_grid_id, region_grid_id, marathi),
 UNIQUE (country_grid_id, region_grid_id, gujarati),
 UNIQUE (country_grid_id, region_grid_id, malayalam),
 UNIQUE (country_grid_id, region_grid_id, bengali),
 UNIQUE (country_grid_id, region_grid_id, oriya),
 UNIQUE (country_grid_id, region_grid_id, tamil),
 UNIQUE (country_grid_id, region_grid_id, telugu),
 UNIQUE (country_grid_id, region_grid_id, panjabi),
 UNIQUE (country_grid_id, region_grid_id, urdu),
 UNIQUE (country_grid_id, region_grid_id, chinese_simplified),
 UNIQUE (country_grid_id, region_grid_id, chinese_traditional),
 UNIQUE (country_grid_id, region_grid_id, mandarin_chinese),
 UNIQUE (country_grid_id, region_grid_id, arabic),
 UNIQUE (country_grid_id, region_grid_id, russian),
 UNIQUE (country_grid_id, region_grid_id, portuguese),
 UNIQUE (country_grid_id, region_grid_id, japanese),
 UNIQUE (country_grid_id, region_grid_id, german),
 UNIQUE (country_grid_id, region_grid_id, korean),
 UNIQUE (country_grid_id, region_grid_id, french),
 UNIQUE (country_grid_id, region_grid_id, turkish),
 UNIQUE (country_grid_id, region_grid_id, italian),
 UNIQUE (country_grid_id, region_grid_id, polish),
 UNIQUE (country_grid_id, region_grid_id, ukrainian),
 UNIQUE (country_grid_id, region_grid_id, persian),
 UNIQUE (country_grid_id, region_grid_id, romanian),
 UNIQUE (country_grid_id, region_grid_id, serbian),
 UNIQUE (country_grid_id, region_grid_id, croatian),
 UNIQUE (country_grid_id, region_grid_id, thai),
 UNIQUE (country_grid_id, region_grid_id, dutch),
 UNIQUE (country_grid_id, region_grid_id, amharic),
 UNIQUE (country_grid_id, region_grid_id, catalan),
 UNIQUE (country_grid_id, region_grid_id, danish),
 UNIQUE (country_grid_id, region_grid_id, greek),
 UNIQUE (country_grid_id, region_grid_id, spanish),
 UNIQUE (country_grid_id, region_grid_id, estonian),
 UNIQUE (country_grid_id, region_grid_id, finnish),
 UNIQUE (country_grid_id, region_grid_id, armenian),
 UNIQUE (country_grid_id, region_grid_id, khmer),
 UNIQUE (country_grid_id, region_grid_id, kannada),
 UNIQUE (country_grid_id, region_grid_id, malay),
 UNIQUE (country_grid_id, region_grid_id, nepali),
 UNIQUE (country_grid_id, region_grid_id, norwegian),
 UNIQUE (country_grid_id, region_grid_id, slovak),
 UNIQUE (country_grid_id, region_grid_id, albanian),
 UNIQUE (country_grid_id, region_grid_id, swedish),
 UNIQUE (country_grid_id, region_grid_id, tagalog)
);
CREATE INDEX city_grid_country_grid_id ON location.city_grid (country_grid_id);
CREATE INDEX city_grid_region_grid_id ON location.city_grid (region_grid_id);
CREATE INDEX city_grid_is_verified ON location.city_grid (is_verified);
CREATE INDEX city_grid_parent_city_id ON location.city_grid (parent_city_id);
CREATE INDEX city_grid_moved_to_keyword_search ON location.city_grid (moved_to_keyword_search);

CREATE TABLE location.pincode (
 id serial PRIMARY KEY,
 country_grid_id int NOT NULL references location.country_grid (id),
 region_grid_id int DEFAULT NULL references location.region_grid (id),
 city_grid_id int DEFAULT NULL references location.city_grid (id),
 code varchar(15) NOT NULL,
 UNIQUE (country_grid_id, code)
);
CREATE INDEX pincode_country_grid_id ON location.pincode (country_grid_id);
CREATE INDEX pincode_region_grid_id ON location.pincode (region_grid_id);
CREATE INDEX pincode_city_grid_id ON location.pincode (city_grid_id);
CREATE INDEX pincode_code ON location.pincode (code);

-- long and lat type to be decided later
-- this table used to calculate nearest location from given lat/long
-- table is also used to map ip adresses with location
CREATE TABLE location.search_location (
 id serial PRIMARY KEY,
 country_grid_id int NOT NULL references location.country_grid (id),
 region_grid_id int DEFAULT NULL references location.region_grid (id),
 city_grid_id int DEFAULT NULL references location.city_grid (id),
 pincode_id int DEFAULT NULL references location.pincode (id),
 latitude double precision DEFAULT null check(latitude>=-90 and latitude<=90),
 longitude double precision DEFAULT null check(longitude>=-180 and longitude<=180),
 is_verified boolean DEFAULT false,
 UNIQUE (country_grid_id, region_grid_id, city_grid_id, pincode_id, latitude, longitude)
);
CREATE INDEX search_location_country_grid_id ON location.search_location (country_grid_id);
CREATE INDEX search_location_region_grid_id ON location.search_location (region_grid_id);
CREATE INDEX search_location_city_grid_id ON location.search_location (city_grid_id);
CREATE INDEX search_location_pincode_id ON location.search_location (pincode_id);
CREATE INDEX search_location_is_verified ON location.search_location (is_verified);
CREATE INDEX search_location_latitude ON location.search_location (latitude);
CREATE INDEX search_location_longitude ON location.search_location (longitude);

-- postgis column
ALTER TABLE location.search_location ADD COLUMN loc_geog GEOGRAPHY(POINT,4326);
CREATE INDEX search_location_loc_geog ON location.search_location USING GIST (loc_geog);
SELECT AddGeometryColumn ('location','search_location','loc_geom',4326,'POINT',2);
CREATE INDEX search_location_loc_geom ON location.search_location USING GIST (loc_geom);

-- possible search location word combinations:
-- for same prefered/home contry : area-city, city-region, region
-- for other contries : area(city)-country, city-country, region-country, country, world
CREATE TABLE location.location_keyword (
 id serial PRIMARY KEY,
 keyword varchar(80) NOT NULL,
 country varchar(80) DEFAULT NULL,
 region varchar(80) DEFAULT NULL,
 city varchar(80) DEFAULT NULL,
 country_grid_id int DEFAULT NULL references location.country_grid (id),
 region_grid_id int DEFAULT NULL references location.region_grid (id),
 city_grid_id int DEFAULT NULL references location.city_grid (id),
 parent_city_id int DEFAULT NULL references location.city_grid (id),
 search_location_id int DEFAULT NULL references location.search_location (id),
 location_type search_location_type DEFAULT "country",
 language lang NOT NULL,
 is_alternate_name boolean DEFAULT false,
 CHECK ((location_type = "area" and parent_city_id is not null) or (location_type != "area" and parent_city_id is null)),
 UNIQUE (country_grid_id, region_grid_id, city_grid_id)
);
CREATE INDEX location_keyword_keyword ON location.location_keyword (keyword);
CREATE INDEX location_keyword_country_grid_id ON location.location_keyword (country_grid_id);
CREATE INDEX location_keyword_region_grid_id ON location.location_keyword (region_grid_id);
CREATE INDEX location_keyword_city_grid_id ON location.location_keyword (city_grid_id);
CREATE INDEX location_keyword_parent_city_id ON location.location_keyword (parent_city_id);
CREATE INDEX location_keyword_language ON location.location_keyword (language);
CREATE INDEX location_keyword_search_location_id ON location.location_keyword (search_location_id);
CREATE INDEX location_keyword_location_type ON location.location_keyword (location_type);
CREATE INDEX location_keyword_is_alternate_name ON location.search_location (is_alternate_name);

CREATE SCHEMA ip2location;

-- import locations from maxmind
CREATE TABLE ip2location.import_location_mx (
 id int NOT NULL,
 country varchar(20) NOT NULL,
 region varchar(20) NOT NULL,
 city varchar(50) NOT NULL,
 postalCode varchar(10) NOT NULL,
 latitude double precision DEFAULT null check(latitude>=-90 and latitude<=90),
 longitude double precision DEFAULT null check(longitude>=-180 and longitude<=180),
 metroCode varchar(10) NOT NULL,
 areaCode varchar(10) NOT NULL,
 id serial PRIMARY KEY,
 country_grid_id int DEFAULT NULL references location.country_grid (id),
 region_grid_id int DEFAULT NULL references location.region_grid (id),
 city_grid_id int DEFAULT NULL references location.city_grid (id),
 pincode_id int DEFAULT NULL references location.pincode (id),
 location_id int DEFAULT NULL references location.search_location (id)
);

CREATE TABLE ip2location.import_ip_location_mx (
 startIpNum bigint NOT NULL,
 endIpNum bigint NOT NULL,
 location_id int DEFAULT NULL references ip2location.import_location_mx (id),
 id serial PRIMARY KEY
);

CREATE TABLE ip2location.ip_location_mapping (
 id serial PRIMARY KEY,
 ipNum bigint NOT NULL,
 latitude double precision NOT NULL check(latitude>=-90 and latitude<=90),
 longitude double precision NOT NULL check(longitude>=-180 and longitude<=180),
 country_grid_id int DEFAULT NULL references location.country_grid (id),
 region_grid_id int DEFAULT NULL references location.region_grid (id),
 city_grid_id int DEFAULT NULL references location.city_grid (id),
 pincode_id int DEFAULT NULL references location.pincode (id),
 location_id int DEFAULT NULL references location.search_location (id),
 is_html5_loc boolean DEFAULT false,
 last_update_time TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now()
);


CREATE SCHEMA account;
CREATE TABLE account.user(
 id serial PRIMARY KEY,
 first_name varchar(80) NOT NULL,
 middle_name varchar(80) DEFAULT NULL,
 last_name varchar(80) NOT NULL,
 gender gend DEFAULT NULL,
 profile_id int DEFAULT NULL,
 password varchar(30) NOT NULL,
 status account_status DEFAULT 'enabled',
 is_locked boolean DEFAULT false,
 locked_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NULL,
 username_ids int[],
 last_login_time TIMESTAMP WITHOUT TIME ZONE DEFAULT NULL,


-- last known location/online detail
 online_status varchar(4) DEFAULT NULL,
 lk_location_online_time TIMESTAMP WITHOUT TIME ZONE DEFAULT NULL,
 lk_location_type varchar(10),
 lk_country_grid_id int DEFAULT NULL references location.country_grid (id),
 lk_region_grid_id int DEFAULT NULL references location.region_grid (id),
 lk_city_grid_id int DEFAULT NULL references location.city_grid (id),
 lk_pincode_id int DEFAULT NULL references location.pincode (id),
 lk_latitude double precision DEFAULT null check(latitude>=-90 and latitude<=90),
 lk_ongitude double precision DEFAULT null check(longitude>=-180 and longitude<=180),


 last_admin_id int DEFAULT NULL,
 admin_update_time TIMESTAMP WITHOUT TIME ZONE DEFAULT NULL
);
-- accout will be created only after verifing at list on of primary contact delails
-- password will be differant for all accounts having same mobile number as primary contact
-- cron will remove locked account holder after 1 year

CREATE TABLE account.security_question(
 id serial PRIMARY KEY,
 user_id int DEFAULT NULL references account.user(id),
 question varchar(200) NOT NULL,
 answer varchar(200) NOT NULL,
 created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now()
);

CREATE TABLE account.default_security_question(
 id serial PRIMARY KEY,
 english varchar(200) DEFAULT NULL UNIQUE,
 hindi varchar(200) DEFAULT NULL UNIQUE,
 marathi varchar(200) DEFAULT NULL UNIQUE,
 gujarati varchar(200) DEFAULT NULL UNIQUE,
 malayalam varchar(200) DEFAULT NULL UNIQUE,
 bengali varchar(200) DEFAULT NULL UNIQUE,
 oriya varchar(200) DEFAULT NULL UNIQUE,
 tamil varchar(200) DEFAULT NULL UNIQUE,
 telugu varchar(200) DEFAULT NULL UNIQUE,
 panjabi varchar(200) DEFAULT NULL UNIQUE,
 urdu varchar(200) DEFAULT NULL UNIQUE,
 chinese_simplified varchar(200) DEFAULT NULL UNIQUE,
 chinese_traditional varchar(200) DEFAULT NULL UNIQUE,
 mandarin_chinese varchar(200) DEFAULT NULL UNIQUE,
 arabic varchar(200) DEFAULT NULL UNIQUE,
 russian varchar(200) DEFAULT NULL UNIQUE,
 portuguese varchar(200) DEFAULT NULL UNIQUE,
 japanese varchar(200) DEFAULT NULL UNIQUE,
 german varchar(200) DEFAULT NULL UNIQUE,
 korean varchar(200) DEFAULT NULL UNIQUE,
 french varchar(200) DEFAULT NULL UNIQUE,
 turkish varchar(200) DEFAULT NULL UNIQUE,
 italian varchar(200) DEFAULT NULL UNIQUE,
 polish varchar(200) DEFAULT NULL UNIQUE,
 ukrainian varchar(200) DEFAULT NULL UNIQUE,
 persian varchar(200) DEFAULT NULL UNIQUE,
 romanian varchar(200) DEFAULT NULL UNIQUE,
 serbian varchar(200) DEFAULT NULL UNIQUE,
 croatian varchar(200) DEFAULT NULL UNIQUE,
 thai varchar(200) DEFAULT NULL UNIQUE,
 dutch varchar(200) DEFAULT NULL UNIQUE,
 amharic varchar(200) DEFAULT NULL UNIQUE,
 catalan varchar(200) DEFAULT NULL UNIQUE,
 danish varchar(200) DEFAULT NULL UNIQUE,
 greek varchar(200) DEFAULT NULL UNIQUE,
 spanish varchar(200) DEFAULT NULL UNIQUE,
 estonian varchar(200) DEFAULT NULL UNIQUE,
 finnish varchar(200) DEFAULT NULL UNIQUE,
 armenian varchar(200) DEFAULT NULL UNIQUE,
 khmer varchar(200) DEFAULT NULL UNIQUE,
 kannada varchar(200) DEFAULT NULL UNIQUE,
 malay varchar(200) DEFAULT NULL UNIQUE,
 nepali varchar(200) DEFAULT NULL UNIQUE,
 norwegian varchar(200) DEFAULT NULL UNIQUE,
 slovak varchar(200) DEFAULT NULL UNIQUE,
 albanian varchar(200) DEFAULT NULL UNIQUE,
 swedish varchar(200) DEFAULT NULL UNIQUE,
 tagalog varchar(200) DEFAULT NULL UNIQUE
);

-- CREATE SCHEMA primary_contact;
CREATE TABLE primary_contact(
 id serial PRIMARY KEY,
 user_id int DEFAULT NULL references account.user(id),
 profile_id int DEFAULT NULL references account.user(id),
 contact_type primary_contact_type DEFAULT 'mob',
 country_code varchar(10) DEFAULT NULL,
 detail varchar(30) NOT NULL,
 verification_code varchar(10) NOT NULL,
 vcode_sent_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NULL,
 is_verified boolean DEFAULT false,
 last_verified_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NULL,
 is_locked boolean DEFAULT false,
 locked_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NULL,
 CONSTRAINT user_profile check(user_id is not null or profile_id is not null)
);


CREATE SCHEMA profile;
CREATE TABLE profile.profile_parent (
 id serial PRIMARY KEY,
 gender gend DEFAULT NULL,
 blood_group bloodGroup DEFAULT NULL,
 dob date DEFAULT NULL,

 account_id int DEFAULT NULL references account.user (id),
 primary_contact_ids int[],

 bucket profile_bucket NOT NULL,

 is_locked boolean DEFAULT false,
 locked_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NULL,

 created_by int DEFAULT NULL references account.user (id),
 created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now(),

 last_admin_id int DEFAULT NULL,
 admin_update_time TIMESTAMP WITHOUT TIME ZONE DEFAULT NULL,

 last_edit_time TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now()

-- permanant address detail
 p_address1 varchar(100) NOT NULL,
 p_address2 varchar(100) NOT NULL,
 p_country_grid_id int DEFAULT NULL references location.country_grid (id),
 p_region_grid_id int DEFAULT NULL references location.region_grid (id),
 p_city_grid_id int DEFAULT NULL references location.city_grid (id),
 p_pincode_id int DEFAULT NULL references location.pincode (id),

-- current address detail
 same_as_p_address boolean DEFAULT false,
 c_address1 varchar(100) DEFAULT NULL,
 c_address2 varchar(100) DEFAULT NULL,
 c_country_grid_id int DEFAULT NULL references location.country_grid (id),
 c_region_grid_id int DEFAULT NULL references location.region_grid (id),
 c_city_grid_id int DEFAULT NULL references location.city_grid (id),
 c_pincode_id int DEFAULT NULL references location.pincode (id),

-- last known location/online detail
 online_status varchar(4) DEFAULT NULL,
 lk_location_online_time TIMESTAMP WITHOUT TIME ZONE DEFAULT NULL,
 lk_location_type varchar(10),
 lk_country_grid_id int DEFAULT NULL references location.country_grid (id),
 lk_region_grid_id int DEFAULT NULL references location.region_grid (id),
 lk_city_grid_id int DEFAULT NULL references location.city_grid (id),
 lk_pincode_id int DEFAULT NULL references location.pincode (id),
 lk_latitude double precision DEFAULT null check(latitude>=-90 and latitude<=90),
 lk_ongitude double precision DEFAULT null check(longitude>=-180 and longitude<=180),

 skill_synonyms_chosen int[],
 parent_skills int[],

 profile_language lang NOT NULL,
 first_name varchar(80) NOT NULL,
 middle_name varchar(80) NOT NULL,
 last_name varchar(80) NOT NULL,
);
-- postgis column
ALTER TABLE profile.profile_parent ADD COLUMN loc_geog GEOGRAPHY(POINT,4326);
CREATE INDEX profile_parent_loc_geog ON profile.profile_parent USING GIST (loc_geog);
SELECT AddGeometryColumn ('profile','profile_parent','loc_geom',4326,'POINT',2);
CREATE INDEX profile_parent_loc_geom ON profile.profile_parent USING GIST (loc_geom);
-- newly created profile will not be visible in search untill all mobile numbers are verified
-- cron will remove profile having non verified mobile_number after 1 month
-- cron will remove locked profile not having account holder after 1 month
-- cron will remove locked profile having account holder after 1 year

-- table contains emails to be sent for locked profiles and handovered profiles
CREATE TABLE profile.locked_profile_email (
 id serial PRIMARY KEY,
 account_id int NOT NULL references account.user (id),
 locked_profile_id int NOT NULL references profile.profile_parent (id),
 email varchar(30) NOT NULL,
 message text NOT NULL,
 is_sent boolean DEFAULT false,
 last_edit_time TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now()
);

-- table contains SMS to be sent for locked profiles and handovered profiles
CREATE TABLE profile.locked_profile_sms (
 id serial PRIMARY KEY,
 account_id int NOT NULL references account.user (id),
 locked_profile_id int NOT NULL references profile.profile_parent (id),
 sms varchar(30) NOT NULL,
 message text NOT NULL,
 is_sent boolean DEFAULT false,
 last_edit_time TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now()
);

-- other profile tables are to be added later
-- qlalification,
-- professional_experience,
-- known_languages,
-- user_profiles_known_locations,
-- profile_documents
-- document_html_and_image_conversion_tables
-- assignmets_completed


CREATE SCHEMA jobs;
CREATE TABLE jobs.assignment (
 id serial PRIMARY KEY,
 posted_by int NOT NULL references account.user (id),

 title varchar(100) NOT NULL,
 message text NOT NULL,

 primary_contact_ids int[],

 skill_synonyms_chosen int[],
 parent_skills int[],

 country_grid_id int DEFAULT NULL references location.country_grid (id),
 region_grid_id int DEFAULT NULL references location.region_grid (id),
 city_grid_id int DEFAULT NULL references location.city_grid (id),
 pincode_id int DEFAULT NULL references location.pincode (id),

 location_online_time TIMESTAMP WITHOUT TIME ZONE DEFAULT NULL,
 latitude double precision DEFAULT null check(latitude>=-90 and latitude<=90),
 longitude double precision DEFAULT null check(longitude>=-180 and longitude<=180),

 last_edit_time TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now()
);
-- postgis column
ALTER TABLE jobs.assignment ADD COLUMN loc_geog GEOGRAPHY(POINT,4326);
CREATE INDEX assignment_loc_geog ON jobs.assignment USING GIST (loc_geog);
SELECT AddGeometryColumn ('jobs','assignment','loc_geom',4326,'POINT',2);
CREATE INDEX assignment_loc_geom ON jobs.assignment USING GIST (loc_geom);
-- cron will disable assignments after 1 month
-- disabled assignments will be deleted after 2 month

-- other jobs tables are to be added later


-- CREATE SCHEMA chat;