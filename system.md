# System

# General
* any string starting with a { and ends with a } is a dictionary
* any string starting with a [ and ends with a ] is a list
* When stored in markdown document, list and dictionary strings have had single and double quotes removed for clarity
* json space-issue is patched by replacing pairs of double quotes ('""') with a space (' ')

## Definitions
* claims is a set of JWT Token attributes (aka claims)
* claims is {aud: starter-api_client,  iss: lyttlebit, key:  api_user@lyttlebit.com,  scope: api_user,  sub: client-api,  user: api_user@lyttlebit.com}
* test_data is {id: , type: , owner: }
* owner_data is account_data
* owner_data sample {id: api_user@lyttlebit.com, type: ACCOUNT, username: api_user@lyttlebit.com, displayname: null, password: a1A!aaaa, scope: api_user}
* api_resource is {}
* apiTest is {data: test_data, claims: claims,  owner: owner_data,  api_resource: setting_data}
* ~~token is (aud,iss,sub,user,scope,key)~~
* ~~admin-token is (aud, iss, sub, user, scope:api_admin, key)~~
* ~~guest-token is (aud, iss, sub, user, scope:api_guest, key)~~
* ~~user-token is (aud, iss, sub, user, scope:api_user, key)~~
* form is {id:, type:, owner:, ...}
* triple is (pk,sk,tk)
* primarykey is (pk,sk)
* identity is (id)
* request is 
# data Types
default is TEXT
{}
# Transformation
* model_datum is 
```
{
    id:    {value: abc123,    type:C, size:3-330, validate:R},
    type:  {value: abc123,    type:C, size:3-330, validate:R},
    owner: {value: abc123,    type:C, size:3-330, validate:R},
    password: {value: abc123, type:C, size:3-330, validate:R, encrypted: Y}, 
    point: {value: [1.0,1.0], type:POINT, size:400, validate:R},
    polygon: {value: [[1.0,1.0],[2.0,2.0],[2.0,1.0]], type:POLYGON, size:4000, validate:R}
}
```
* client form is 
```
{ 
    id: abc123, 
    type: SAMPLE, 
    owner: abc123, 
    password: a1A!aaaa, 
    point: [1.0,1.0],
    polygon: [[x,y],[x,y],...]
}
```
* storage form is
```
{pk:SAMPLE#abc123, sk:name#id, tk:value#abc123}
{pk:SAMPLE#abc123, sk:name#type, tk:SAMPLE}
{pk:SAMPLE#abc123, sk:name#owner, tk:value#abc123}
{pk:SAMPLE#abc123, sk:name#password, tk:value#abc123}
{pk:SAMPLE#abc123, sk:name#point, tk:value#(x,y)}
{pk:SAMPLE#abc123, sk:name#point, tk:value#(x,y)}
```

# ISSUES
* convert TYPE to LAYER in form
* When 'password' in model_datum, add password encryption code
* space-issue: spaces in values generate pairs of quotes in Line.getValue() e.g.,  1. model_datum: {id: abc123 (type=C size=3-330 validate=R)}
* When geometry in model_datum, add coordinate to form
* when point in model_datum, add validation code to POST, add mbr code to select

# Processes
## Minor Processes
* Insert record
* Update record
* Get record
* Delete record

## Major Processes
* Authentication (SignIn, SignUp, ForgetPassword) 
* Authorization (Scope)
* Geometry Query (MBR)
* Testing

# Client
* Test Client
 
# Client API

* token claims
* url /<resource>/<owner>/PK/<id>
* url /<resource>/<owner>

| level | method | scope | resource | token | json payload | url |
| ----- | ------ | ----- | -------- | ----- | ------------ | --- |
| client | DELETE | api_user | sample | 336 | payload | /sample/api_user@lyttlebit.com/PK/abc123api_userDELETE0 |
| client | GET    | api_user | sample | 336 | payload | /sample/api_user@lyttlebit.com/PK/abc123api_userGET1 |
| client | POST   | api_user | sample | 336 | {id:abc123api_userPOST3, type:SAMPLE, owner:api_user@lyttlebit.com} | /sample/api_user@lyttlebit.com |
| client | PUT    | api_user | sample | 336 | {id:abc123api_userPUT4 , type:SAMPLE, owner:api_user@lyttlebit.com}  | /sample/api_user@lyttlebit.com/PK/abc123api_userPUT4 |


# Backend



# Client


# Route

| A | B |
| -------- | ------ |
| level    | client | 
| method   | DELETE |
| scope    | api_admin |
| resource | sample |
| token    | xxx |
| payload  | form |
|url       | /sample/api_admin@lyttlebit.com/PK/abc123api_adminDELETE0 | 

| level | method | scope | resource | token | payload | url |
| ----- | ------ | ----- | -------- | ----- | ------- | --- |
| client | DELETE | api_admin | sample | 340 | Form | /sample/api_admin@lyttlebit.com/PK/abc123api_adminDELETE0 |
| route  | DELETE | Scope | SAMPLE | 337::TOKEN | (SAMPLE#abc123api_adminDELETE0, *)::PRIMARYKEY | Triple |
| client | DELETE | api_guest | sample | 340 | Form | /sample/api_guest@lyttlebit.com/PK/abc123api_guestDELETE0 |
| route  | DELETE | Scope | SAMPLE | 337::TOKEN | (SAMPLE#abc123api_guestDELETE0, *)::PRIMARYKEY | Triple |
| client | DELETE | api_user | sample | 336 | Form | /sample/api_user@lyttlebit.com/PK/abc123api_userDELETE0 |
| route  | DELETE | Scope | SAMPLE | 333::TOKEN | (SAMPLE#abc123api_userDELETE0, *)::PRIMARYKEY | Triple |
| client | GET    | api_admin | sample | 340 | Form | /sample/api_admin@lyttlebit.com/PK/abc123api_adminGET1 |
| route  | GET    | Scope | SAMPLE | 337::TOKEN | (SAMPLE#abc123api_adminGET1, *)::PRIMARYKEY | Triple |
| client | GET    | api_guest | sample | 340 | Form | /sample/api_guest@lyttlebit.com/PK/abc123api_guestGET1 |
| route  | GET    | Scope | SAMPLE | 337::TOKEN | (SAMPLE#abc123api_guestGET1, *)::PRIMARYKEY | Triple |
| client | GET    | api_user | sample | 336 | Form | /sample/api_user@lyttlebit.com/PK/abc123api_userGET1 |
| route  | GET    | Scope | SAMPLE | 333::TOKEN | (SAMPLE#abc123api_userGET1, *)::PRIMARYKEY | Triple |
| client | GET    | api_admin | sample | 340 | Form | /sample/api_admin@lyttlebit.com/PK/abc123api_adminGET2 |
| route  | GET    | Scope | SAMPLE | 337::TOKEN | (SAMPLE#abc123api_adminGET2, *)::PRIMARYKEY | Triple |
| client | GET    | api_guest | sample | 340 | Form | /sample/api_guest@lyttlebit.com/PK/abc123api_guestGET2 |
| route  | GET    | Scope | SAMPLE | 337::TOKEN | (SAMPLE#abc123api_guestGET2, *)::PRIMARYKEY | Triple |
| client | GET    | api_user | sample | 336 | Form | /sample/api_user@lyttlebit.com/PK/abc123api_userGET2 |
| route  | GET    | Scope | SAMPLE | 333::TOKEN | (SAMPLE#abc123api_userGET2, *)::PRIMARYKEY | Triple |
| client | POST   | api_admin | sample | 340 | {id:abc123api_adminPOST3, type:SAMPLE, owner:api_admin@lyttlebit.com} | /sample/api_admin@lyttlebit.com |
| route  | POST   | Scope | SAMPLE | 337::TOKEN | PrimaryKey | (SAMPLE#abc123api_adminPOST3, name#id,value#abc123api_adminPOST3)::TRIPLE |
| route  | POST   | Scope | SAMPLE | 337::TOKEN | PrimaryKey | (SAMPLE#abc123api_adminPOST3, name#type,value#SAMPLE)::TRIPLE |
| route  | POST   | Scope | SAMPLE | 337::TOKEN | PrimaryKey | (SAMPLE#abc123api_adminPOST3, name#owner,value#api_admin@lyttlebit.com)::TRIPLE |
| client | POST   | api_guest | sample | 340 | {id:abc123api_guestPOST3, type:SAMPLE, owner:api_guest@lyttlebit.com} | /sample/api_guest@lyttlebit.com |
| route  | POST   | Scope | SAMPLE | 337::TOKEN | PrimaryKey | (SAMPLE#abc123api_guestPOST3, name#id,value#abc123api_guestPOST3)::TRIPLE |
| route  | POST   | Scope | SAMPLE | 337::TOKEN | PrimaryKey | (SAMPLE#abc123api_guestPOST3, name#type,value#SAMPLE)::TRIPLE |
| route  | POST   | Scope | SAMPLE | 337::TOKEN | PrimaryKey | (SAMPLE#abc123api_guestPOST3, name#owner,value#api_guest@lyttlebit.com)::TRIPLE |
| client | POST   | api_user | sample | 336 | {id:abc123api_userPOST3, type:SAMPLE, owner:api_user@lyttlebit.com} | /sample/api_user@lyttlebit.com |
| route  | POST   | Scope | SAMPLE | 333::TOKEN | PrimaryKey | (SAMPLE#abc123api_userPOST3, name#id,value#abc123api_userPOST3)::TRIPLE |
| route  | POST   | Scope | SAMPLE | 333::TOKEN | PrimaryKey | (SAMPLE#abc123api_userPOST3, name#type,value#SAMPLE)::TRIPLE |
| route  | POST   | Scope | SAMPLE | 333::TOKEN | PrimaryKey | (SAMPLE#abc123api_userPOST3, name#owner,value#api_user@lyttlebit.com)::TRIPLE |
| client | PUT    | api_admin | sample | 340 | {id:abc123api_adminPUT4, type:SAMPLE, owner:api_admin@lyttlebit.com} | /sample/api_admin@lyttlebit.com/PK/abc123api_adminPUT4 |
| route  | PUT    | Scope | SAMPLE | 337::TOKEN| (SAMPLE#abc123api_adminPUT4, name#id)::PRIMARYKEY | (SAMPLE#abc123api_adminPUT4, name#id,value#abc123api_adminPUT4)::TRIPLE |
| route  | PUT    | Scope | SAMPLE | 337::TOKEN| (SAMPLE#abc123api_adminPUT4, name#type)::PRIMARYKEY | (SAMPLE#abc123api_adminPUT4, name#type,value#SAMPLE)::TRIPLE |
| route  | PUT    | Scope | SAMPLE | 337::TOKEN| (SAMPLE#abc123api_adminPUT4, name#owner)::PRIMARYKEY | (SAMPLE#abc123api_adminPUT4, name#owner,value#api_admin@lyttlebit.com)::TRIPLE |
| client | PUT    | api_guest | sample | 340 | {id:abc123api_guestPUT4, type:SAMPLE, owner:api_guest@lyttlebit.com} | /sample/api_guest@lyttlebit.com/PK/abc123api_guestPUT4 |
| route  | PUT    | Scope | SAMPLE | 337::TOKEN| (SAMPLE#abc123api_guestPUT4, name#id)::PRIMARYKEY | (SAMPLE#abc123api_guestPUT4, name#id,value#abc123api_guestPUT4)::TRIPLE |
| route  | PUT    | Scope | SAMPLE | 337::TOKEN| (SAMPLE#abc123api_guestPUT4, name#type)::PRIMARYKEY | (SAMPLE#abc123api_guestPUT4, name#type,value#SAMPLE)::TRIPLE |
| route  | PUT    | Scope | SAMPLE | 337::TOKEN| (SAMPLE#abc123api_guestPUT4, name#owner)::PRIMARYKEY | (SAMPLE#abc123api_guestPUT4, name#owner,value#api_guest@lyttlebit.com)::TRIPLE |
| client | PUT    | api_user | sample | 336 | {id:abc123api_userPUT4, type:SAMPLE, owner:api_user@lyttlebit.com} | /sample/api_user@lyttlebit.com/PK/abc123api_userPUT4 |
| route  | PUT    | Scope | SAMPLE | 333::TOKEN| (SAMPLE#abc123api_userPUT4, name#id)::PRIMARYKEY | (SAMPLE#abc123api_userPUT4, name#id,value#abc123api_userPUT4)::TRIPLE |
| route  | PUT    | Scope | SAMPLE | 333::TOKEN| (SAMPLE#abc123api_userPUT4, name#type)::PRIMARYKEY | (SAMPLE#abc123api_userPUT4, name#type,value#SAMPLE)::TRIPLE |
| route  | PUT    | Scope | SAMPLE | 333::TOKEN| (SAMPLE#abc123api_userPUT4, name#owner)::PRIMARYKEY | (SAMPLE#abc123api_userPUT4, name#owner,value#api_user@lyttlebit.com)::TRIPLE |

# SQL


1. is DELETE 
2. is GET
3. is POST
4. is PUT


## Token

1. aud: <resource-name>_api_client
1. iss: "lyttlebit"
1. key: <user-key>
1. scope: <[api_admin|api_guest|api_user]>
1. sub: "client-api"
1. user: 

## Scope

### api-admin
### api-uest
### api-user

## API

### Delete
### Get
### Post
### Put

## Data

1. id:
1. type: 
1. owner: the record owner id



route.integration.test.js
    |
route_\<resource-name>_<method>_top.js.
    |
function_<resource-name>_<method>    
    |
```    
() is datum
([]) is array 
[[]] is 



DELETE
  [[*]]
    |
  (user-token)(identity)
    |
    + --> [[Client DELETE Route Handler]]
    ^        |
    .      (request) <--- (user-token, identity)   
    .        .
    .        .  
    .        .
    .        .
    .      (request)
    .        |   
    .     [[Server DELETE Route Handler]] 
    .        |     
    .      (user-token, user-token.user, identity) <--- (request)
    .        |
    .     [[Triple Delete Handler]]
    .        |
    + <--- (response)   

GET
  [[*]]
    |
  (user-token)(identity)
    |
    + --> [[Client DELETE Route Handler]]
    ^        |
    .      (request) <--- (user-token, identity)   
    .        .
    .        .  
    .        .
    .        .
    .      (request)
    .        |   
    .     [[Server DELETE Route Handler]] 
    .        |     
    .      (user-token, user-token.user, identity) <--- (request)
    .        |
    .     [[Triple Delete Handler]]
    .        |
    + <--- (response) 

POST
  [[*]]
    |
  (user-token)(form)
    |
    + --> [[Client Post Route Handler]]
    ^        |
    |      (request) <--- (user-token, form)   
    .        .
    .        .  
    .        .
    ^        .
    |      (request)
    |        |   
    |     [[Server POST Route Handler]] 
    |        |     
    |      (user-token, user-token.user, [triple,...])
    |        |
    |     [[Triple Insert Handler]]
    |        |
    + <--- (response)            
   
PUT
  [[*]]
    |
  (user-token)(form)
    |
    + --> [[Client PUT Route Handler]]
    ^        |
    .      (request) <--- (user-token, form, identity)   
    .        .
    .        .  
    .        .
    .        .
    .      (request)
    .        |   
    .     [[Server PUT Route Handler]] 
    .        |     
    .      (user-token, user-token.user, identity, [triple,...]) <--- (request)
    .        |
    .     [[Triple Update Handler]]
    .        |
    + <--- (response)         
           
           
    
      
     [*]   
      |  
      + <--- DELETE
      |
      + <--- GET
      |
      + <--- POST 
      |
      + <--- PUT 
      |    
     [=] 
```

```
         + <-- (response) <------ [response handler] <------------------------------------ +
        /                                                                                  ^
       /                                                                                   | 
[Test Client] --> (request) --> [Request Handler] --> (parameters) --> [Data Handler] -- > +
```

## Globals
1. Claim
1. Owners

## Test Client
1. Define Scope from ['api_admin','api_guest','api_user']
1. Define Method from ['DELETE','GET','POST','PUT']
1. Define Test Data 
1. Define request URL from claims and  ['DELETE','GET','POST','PUT'] 

1. Define Owners from Scope

1. Define form when scope is in ['POST','PUT']
1. Define headers from ['authorization','test']
1. Define test from ['data','claims','owner','api_settings']
1. Define payload from form when scope is ['POST','PUT']

## (request)
1. owners
1. 

## [Request Handler]
### Owners
```json 
{
 "api_admin":{},
 "api_guest":{},
 "api_user":{}
}
{'api_admin': {'id': 'api_admin@lyttlebit.com', 'type': 'ACCOUNT', 'username': 'api_admin@lyttlebit.com', 'displayname': 'DISPLAYNAME_TBD', 'password': 'a1A!aaaa', 'scope': 'api_admin'}, 'api_guest': {'id': 'api_guest@lyttlebit.com', 'type': 'ACCOUNT', 'username': 'api_guest@lyttlebit.com', 'displayname': 'DISPLAYNAME_TBD', 'password': 'a1A!aaaa', 'scope': 'api_guest'}, 'api_user': {'id': 'api_user@lyttlebit.com', 'type': 'ACCOUNT', 'username': 'api_user@lyttlebit.com', 'displayname': 'DISPLAYNAME_TBD', 'password': 'a1A!aaaa', 'scope': 'api_user'}};

```

### Test Form
Test data must contain "id" key and value pair
Test data must contain "type" key and value pair
Test data must contain "owner" key anf value pair 
```json
{ "id":  "abc123 ", "type":  "ACCOUNT ", "owner":  "api_admin@lyttlebit.com" }
```

### Client Form
* Client form must contain a unique identifyer provided by client
```json
{ "id":  "abc123 " }
```

### (Request)
* create url
* make request 
 
# Request Handler
* extract token from request.headers.authorization when provided, otherwise false
* extract test_data from request.headers.test when provided, otherwise false 
* extract form from request.payload when request.method in ['POST','PUT'], otherwise false
* extract id from request.params.id, otherwise false
* extract type from request.path, otherwise false
* stub triple in 
* inject "type" into form from token.key when form not false
* inject "owner" into form from token.key when form not false

### (Parameters)

### Data Handler


## Breakdown Form
The Form
* form must contain an "id" key and value pair
* form will contain a "type" key and value pair, that will be injected during a the POST
* form will contain an "owner" key and value pair, when missing will be injected during the POST from token.key
* the combination of "id" and "type" values must be unique
* the form will also contain other key and value pairs, leftout here for brevity
```json
{ "id":  "abc123 ", "owner":  "api_admin@lyttlebit.com " }
```

## The client requests
Although the data will be stored as triple (defined later), the client acts as if data is stored as form 
```
DELETE /account/{owner}/{id}
GET    /account/{owner}/{id}
POST   /account/{owner} form: {"id":"abc123 ","type":"ACCOUNT ","owner":"api_admin@lyttlebit.com "}
PUT    /account/{owner}/{id} form: {"id":"abc123 ","type":"ACCOUNT ","owner":"api_admin@lyttlebit.com "}
```

## The request handler
* change the form based request (see client requests above) into a triple based request
* extract type from the request.param.type
* extract id from request.param.id
* create a primarykey = ("${type}#${form.id}", "(form.type)"

```
DELETE /account/
```

## Form to Triples
derive the Form's triples from the given form 
```json
{pk:"ACCOUNT#abc123","sk":"name#id","tk":"value#abc123"}
{pk:"ACCOUNT#abc123","sk":"name#type","tk":"value#ACCOUNT"}
{pk:"ACCOUNT#abc123","sk":"name#owner","tk":"value#api_admin@lyttlebit.com"}
{pk:"ACCOUNT#abc123","sk":"name#password","tk":"value#ecryptedstring"}

```


## Derive the primary key for each triple
given the url

```
( "ACCOUNT#abc123 ", "name#id ")
( "ACCOUNT#abc123 ", "name#type ")
( "ACCOUNT#abc123 ", "name#owner ")
```

insert
```
"ACCOUNT#abc123", "name#id",    "abc123"
"ACCOUNT#abc123", "name#type",  "ACCOUNT"
"ACCOUNT#abc123", "name#owner", "api_admin@lyttlebit.com"
```

given the templates
```
method  url                         body
DELETE  /account/owner/PK/id        
GET     /account/owner/PK/id
POST    /account/owner/PK           { "id":  "abc123 ", "type":  "ACCOUNT ", "owner":  "api_admin@lyttlebit.com " }
PUT     /account/owner/PK/id/kind   { "id":  "xyz123 ", "type":  "ACCOUNT ", "owner":  "api_admin@lyttlebit.com " }


```


<function-class-name> = Function<>

| label                | variable             | key                  | size | example              |
| ---                  | ---                  | ---                  | ---  |  ---                 |
| WORKING_FOLDER       | working_folder       | <working-folder>     |    1 | /Users/jameswilfong/..LyttleBit/code/Development/00-Documents/01.TestMaker/temp |
| PROJECT_FILENAME     | project_filename     | <project-filename>   |    1 | starter_api.md       |
| PROJECT_NAME         | project_name         | <project-name>       |    1 | starter_api          |
| CLAIM_ISSUER         | claim_issuer         | <claim-issuer>       |    1 | lyttlebit            |
| CLAIM_AUDIENCE       | claim_audience       | <claim-audience>     |    1 | starter_api_client   |
| CLAIM_SUBJECT        | claim_subject        | <claim-subject>      |    1 | client_api           |
| RESOURCE_NAME        | resource_name        | <resource-name>      |    6 | sample               |
| RESOURCE_TYPE        | resource_type        | <resource-type>      |    6 | SAMPLE               |
| MODEL_PARAMETER      | model_parameter      | <model-parameter>    |    5 | ['top', 'top', 'tm', 'tot', 'topt'] |
| MODEL_DATUM          | model_datum          | <model-datum>        |    1 | {'id': 'abc123 (type=C size=3-330 validate=R)', 'type': 'type_TBD (type=C size=1-50 validate=R)', 'owner': 'owner_TBD (type=C size=3-330 validate=R)'} |
| ROUTE_ACTIVE         | route_active         | <route-active>       |    5 | ['1', '1', '1', '1', '1'] |
| ROUTE_KEY            | route_key            | <route-key>          |    5 | ['sample_delete_kop', 'sample_get_kop', 'sample_get_km', 'sample_post_tot', 'sample_put_topt'] |
| ROUTE_METHOD         | route_method         | <route-method>       |    5 | ['DELETE', 'GET', 'GET', 'POST', 'PUT'] |
| ROUTE_ACTIVE         | route_active         | <route-active>       |    5 | ['1', '1', '1', '1', '1'] |
| ROUTE_SCOPE          | route_scope          | <route-scope>        |    5 | [['api_admin', 'api_guest', 'api_user'], ['api_admin', 'api_guest', 'api_user'], ['api_admin', 'api_guest', 'api_user'], ['api_admin', 'api_guest', 'api_user'], ['api_admin', 'api_guest', 'api_user']] |
| ROUTE_PATH           | route_path           | <route-path>         |    5 | ['/sample/{owner}/PK/{pk}/{sk?}', '/sample/{owner}/PK/{pk}/{sk?}', '/sample/MBR/{north}/{south}/{west}/{east}', '/sample/{owner}', '/sample/{owner}/PK/{pk}/{sk?}'] |
| PARAMETER_BY_KEY     | parameter_by_key     | <parameter-by-key>   |    4 | {'TM': [{'name': 'token_id', 'type': 'TOKEN'}, {'name': 'm_b_r', 'type': 'MBR'}], 'TOP': [{'name': 'token_id', 'type': 'TOKEN'}, {'name': 'owner_id', 'type': 'OWNERID'}, {'name': 'primary_key', 'type': 'PRIMARYKEY'}], 'TOT': [{'name': 'token_id', 'type': 'TOKEN'}, {'name': 'owner_id', 'type': 'OWNERID'}, {'name': 'trip', 'type': 'TRIPLE'}], 'TOPT': [{'name': 'token_id', 'type': 'TOKEN'}, {'name': 'owner_id', 'type': 'OWNERID'}, {'name': 'primary_key', 'type': 'PRIMARYKEY'}, {'name': 'trip', 'type': 'TRIPLE'}]} |


# Model
## DELETE
### token is required
### ownerid is required
### primarykey is required 

# Types
## triple is TRIPLE
## triple '("pk","sk","tk")'


# DELETE
* Standard DELETE 
* Set active to 0 or 1 to turn off or on

# GET

# GET 

# POST

# Singleton POST
    
# Account POST
1. resource_name: account
1. resource_type: ACCOUNT
1. route_key: [account_post_kot]
1. route_method: [POST]
1. route_active: [1]
1. route_path: [/account]
1. route_scope: [[api_guest]]
1. model_parameter_key: [kot]
1. model_datum: {id: abc123 (type=C size=3-330 validate=R), type: ACCOUNT (type=C size=1-50 validate=R), owner: owner_TBD (type=C size=3-330 validate=R), username: abcacom (type=C size=3-330 validate=R), password: a1A!aaaa (type=C size=8-330 validate=R)}

# Account POST
1. resource_name: account
1. resource_type: ACCOUNT
1. route_key: [account_post_tc]
1. route_method: [POST]
1. route_active: [1]
1. route_path: [/account/SIGNIN]
1. route_scope: [[api_guest]]
1. model_parameter_key: [tc]
1. model_datum: {id: abc123 (type=C size=3-330 validate=R), type: ACCOUNT (type=C size=1-50 validate=R), owner: owner_TBD (type=C size=3-330 validate=R), username: abcacom (type=C size=3-330 validate=R), password: a1A!aaaa (type=C size=8-330 validate=R)}

# Account POST
1. resource_name: account
1. resource_type: ACCOUNT
1. route_key: [account_post_tc]
1. route_method: [POST]
1. route_active: [1]
1. route_path: [/account/SIGNIN]
1. route_scope: [[api_guest]]
1. model_parameter_key: [tc]
1. model_datum: {id: abc123 (type=C size=3-330 validate=R), type: ACCOUNT (type=C size=1-50 validate=R), owner: owner_TBD (type=C size=3-330 validate=R), username: abcacom (type=C size=3-330 validate=R), password: a1A!aaaa (type=C size=8-330 validate=R)}


# PUT



# Preprocessed
* WHEN <layer> has password,   
    duplicate <layer>
    add route <layer>/SIGNIN to configuration
    add <layer>(token,owner,cred))
    add <layer>/account
    add <layer>/account/SIGNUP
    add <layer>/account/SIGNIN

* WHEN coordinate, add 

# Processes
* DELETE
* GET
* POST
* PUT
* Spatialization
* Authorization and Authentication 
# Precedence 
TOKEN
OWNERID
TRIPLE
PRIMARYKEY
MBR
# Exclusives
* once a password is added, the layer is a defacto user-account 
```
ACCOUNT Layer
    |
    + Standard IO
    |   + POST /account  account(TOKEN, OWNERID, TRIPLE) <-- (status, message, fail) ------------------ +
    |   |   ^                               + Validate ... |                                            ^
    |   |   |                                           validate token                                  |
    |   |   |                                              + fail (invalid token)  -------------------> +          
    |   |   |                                              + success (valid token)                      ^  
    |   |   |                                              |                                            |
    |   |   |                                           validate coordinate                             |
    |   |   |                                              + fail (invalid coordinate)  --------------> + 
    |   |   |                                              + success (valid coordinate)                 ^
    |   |   |                               + Execute .... |                                            |
    |   |   |                                           when user not found                             | 
    |   |   |                                              + encrypt password                           |
    |   |   |                                              + add layer item, post(OWNERID, TRIPLE)      |
    |   |   |                                                  + fail (bad post) ---------------------> +
    |   |   |                                                  + success (good post)                    ^
    |   |   |                                                                                           |                                                     
    |   |   |                                           when user found                                 |
    |   |   |                                              + authenticate                               |
    |   |   |                                                  + fail (invalid password) -------------> +
    |   |   |                                                  + success (valid password)            
    |   |   |                               + Result .....     |                     
    |   |   |                                              + (status, message, JWT token)
                                            + Return                
                                                                                  
    |   |   + <----------------------------------------------------------------------------------- +                                        
    |   + GET /account/PK/{pk}/{sk?}    account(token, owner, )                 get()
    |   |                                   + validate
    |   |                                       + validate token, always a token so always validate token
    |   |               
    |   + PUT /account/PK/{pk}/{sk}     account(token, owner, primarykey, trip) put()
    |   |                                    + 
    |   + DELETE /account/PK/{pk}/{sk}  account(token, owner, primarykey)       delete()
    + WHEN password
    |   + POST /account/SIGNIN          account(TOKEN, OWNERID, CREDENTIAL)             
    |     
    + WHEN coordinate
    |   + GET /account/MBR/{north}/{south}/{west}/{east} account(token,MBR)
    |

    + SignOut 
```
# Authorization and Authentication
adding "password" to model_datum, 
generate code

## Events
* manually add "password" key to model_datum, eg "password: a1A!aaaa (type=C size=8-330 validate=R)"
* mannually add "coordinate" key to model_datum, eg "coordinate": (x,y) (type= ???? size=???) maybe not 
* manually add api_version, default is <api-version>
* manually add base_version, default is <base-version> 

## Resource Configuration Effects:
~~1. WHEN "TOKEN" IN model_parameter_key THEN add <validate-token> code to template~~

* WHEN "<api-version>" IN api_version THEN manually set api_version in configuration file, eg api_version: 0_0_1
* WHEN "<base-version>" IN api_version THEN manually set version number in configuration file, (eg base_version: 0_0_1)) 

* WHEN "password" IN resource THEN add "username" key to model_datum, eg "username: abcacom (type=C size=3-330 validate=R)"
 
* WHEN "password" IN resource and '<layer>_post_kc' not in route_key THEN add 'POST' to route_method
* WHEN "password" IN resource and '<layer>_post_kc' not in route_key THEN add '1' to route_active
* WHEN "password" IN resource and '<layer>_post_kc' not in route_key THEN add '/<layer>' to route_path
* WHEN "password" IN resource and '<layer>_post_kc' not in route_key THEN add ['api_admim','api_guest','api_user'] to route_scope
* WHEN "password" IN resource and '<layer>_post_kc' not in route_key THEN add 'kc' to route_active 
* WHEN "password" IN resource and '<layer>_post_kc' not in route_key THEN add '<layer>_post_tc' route_key

* WHEN "password" IN resource and '<layer>_put_kc' not in route_key THEN add 'PUT' to route_method
* WHEN "password" IN resource and '<layer>_put_kc' not in route_key THEN add '1' to route_active 
* WHEN "password" IN resource and '<layer>_put_kc' not in route_key THEN add '/<layer>/PK/{pk}/{sk?}' to route_path
* WHEN "password" IN resource and '<layer>_put_kc' not in route_key THEN add ['api_admim','api_guest','api_user'] to route_scope
* WHEN "password" IN resource and '<layer>_put_kc' not in route_key THEN add 'kc' to route_active 
* WHEN "password" IN resource and '<layer>_put_kc' not in route_key THEN add '<layer>_put_kc' route_key
 
## Resource Model API Code Effects:
DELETE - Singleton Pattern
1. WHEN "TOKEN"      IN model_parameter_key THEN add <validate-token-parameter> code to template
1. WHEN "OWNERID"    IN model_parameter_key THEN add <validate-ownerid-parameter> code to template
1. WHEN "PRIMARYKEY" IN model_parameter_key THEN add <validate-primarykey-parameter> code to template
1. WHEN "<base-version>" IN base_version THEN Throw Exception
1. WHEN "<base-version>" NOT IN base_version THEN replace template's '<base-version>' with base_version
1. WHEN "<api-version>" IN api_version THEN Throw Exception
1. WHEN "<api-version>" NOT IN api_version THEN replace template's '<api-version>' with api_version

[Function Parameters]

[Declarations]

[Validations]

[Execute]

GET - Singleton Pattern
1. WHEN "TOKEN"      IN model_parameter_key THEN add <validate-token-parameter> code to template
1. WHEN "OWNERID"    IN model_parameter_key THEN add <validate-ownerid-parameter> code to template
1. WHEN "PRIMARYKEY" IN model_parameter_key THEN add <validate-primarykey-parameter> code to template
1. WHEN "<base-version>" IN base_version THEN Throw Exception
1. WHEN "<base-version>" NOT IN base_version THEN replace template's '<base-version>' with base_version
1. WHEN "<api-version>" IN api_version THEN Throw Exception
1. WHEN "<api-version>" NOT IN api_version THEN replace template's '<api-version>' with api_version

GET - MBR Pattern
1. WHEN "TOKEN"      IN model_parameter_key THEN add <validate-token-parameter> code to template
1. WHEN "OWNERID"    IN model_parameter_key THEN add <validate-ownerid-parameter> code to template
1. WHEN "MBR"        IN model_parameter_key THEN add <validate-mbr-parameter> code to template
1. WHEN "<base-version>" IN base_version THEN Throw Exception
1. WHEN "<base-version>" NOT IN base_version THEN replace template's '<base-version>' with base_version
1. WHEN "<api-version>" IN api_version THEN Throw Exception
1. WHEN "<api-version>" NOT IN api_version THEN replace template's '<api-version>' with api_version

POST - Singleton Pattern
1. WHEN "TOKEN"      IN model_parameter_key THEN add <validate-token-parameter> code to template
1. WHEN "OWNERID"    IN model_parameter_key THEN add <validate-ownerid-parameter> code to template
1. WHEN "TRIPLE" and not("CREDENTIAL") IN model_parameter_key THEN add <validate-triple-parameter> code to template
1. WHEN "<base-version>" IN base_version THEN Throw Exception
1. WHEN "<base-version>" NOT IN base_version THEN replace template's '<base-version>' with base_version
1. WHEN "<api-version>" IN api_version THEN Throw Exception
1. WHEN "<api-version>" NOT IN api_version THEN replace template's '<api-version>' with api_version

POST - Login Pattern
1. WHEN "TOKEN"      IN model_parameter_key THEN add <validate-token-parameter> code to template
* WHEN "CREDENTIAL" and not("TRIPLE")  IN model_parameter_key THEN add <validate-credential-parameter> code to template
1. WHEN "password"   IN model_datum         THEN add Password-Encryption code to template 
1. WHEN "<base-version>" IN base_version THEN Throw Exception
1. WHEN "<base-version>" NOT IN base_version THEN replace template's '<base-version>' with base_version1. WHEN "<api-version>" IN api_version THEN Throw Exception
1. WHEN "<api-version>" NOT IN api_version THEN replace template's '<api-version>' with api_version

PUT - Singleton Pattern
1. WHEN "TOKEN"      IN model_parameter_key THEN add <validate-token-parameter> code to template
1. WHEN "OWNERID"    IN model_parameter_key THEN add <validate-ownerid-parameter> code to template
1. WHEN "PRIMARYKEY" IN model_parameter_key THEN add <validate-primarykey-parameter> code to template
1. WHEN "TRIPLE"     IN model_parameter_key THEN add <validate-triple-parameter> code to template
1. WHEN "password"   IN model_datum         THEN add Password-Encryption code to template 
1. WHEN "<base-version>" IN base_version THEN Throw Exception
1. WHEN "<base-version>" NOT IN base_version THEN replace template's '<base-version>' with base_version
1. WHEN "<api-version>" IN api_version THEN Throw Exception
1. WHEN "<api-version>" NOT IN api_version THEN replace template's '<api-version>' with api_version

## Resource Route Code Effects:
DELETE Processes
* validate Token
* delete 
GET Processes

POST Processes

* WHEN resource-item IS NOT found AND "password" NOT IN resource-item THEN insert resource-item
* WHEN resource-item IS NOT found AND "password" IN     resource-item THEN encrypt resource-item.password and insert
* WHEN resource-item IS     found AND "password" NOT IN resource-item THEN throw DuplicateException
* WHEN resource-item IS     found AND "password" IN     resource-item THEN attempt login

PUT Processes 


 
# Singleton POST
 
1. resource_name: sample
1. resource_type: SAMPLE
1. route_key: [sample_post_tot]
1. route_method: [POST]
1. route_active: [1]
1. route_path: [/sample]
1. route_scope: [[api_admin,api_guest,api_user]]
1. model_parameter_key: [tot]
1. model_datum: {id: abc123 (type=C size=3-330 validate=R), type: ACCOUNT (type=C size=1-50 validate=R), owner: owner_TBD (type=C size=3-330 validate=R)}

   delete /abc/{owner}/PK/{pk}/{sk?}             abc(TOKEN, OWNERID, PRIMARYKEY) delete(PRIMARYKEY)
   
   get    /abc/{owner}/PK/{pk}/{sk?}             abc(TOKEN, OWNERID, PRIMARYKEY) get(PRIMARYKEY)
   get    /abc/MBR/{north}/{south}/{west}/{east} abc(TOKEN, OWNERID, MBR)        get(MBR)
   
   post   /abc/{owner}                           abc(token_id TOKEN, owner_id OWNERID, trip TRIPLE)

eg get abc/PK/
get abc/MBR/
get abc/


# Meanings
LAYER is KIND, KIND is TYPE

# Authorizations
* api_admin authorization
* api_guest authorization
* api_user authorization

# Item
* Item is a JSON object
* item must have an id key
* item must have an owner key
* item must have a type key
* item must have a created key
* item must have an updated key
* item is stored as a set of triples

Item Example

```
{
    "id":"abc",
    "owner":"636b0353-05b8-4f9c-afce-9899f102848c",
    "type":"THING",
    "created":"2023-01-18 13:41:41.266304+00",
    "updated":"2023-01-18 13:41:41.266304+00"
}
```


# Standard Triple 
* TRIPLE is (pk,sk,tk)

# ~~Credential Triple~~
* ~~CREDENTIAL is TRIPLE~~
* ~~CREDENTIAL is (pk,sk,tk)~~
* ~~CREDENTIAL eg '("ACCOUNT#abc","name#password","value#a1A!aaaa")'~~

# Geographic Features
* https://www.rfc-editor.org/rfc/rfc7946
* a feature is encoded as a single TRIPLE
* this reduces the need for polymorphic functions
* types are encoded into sk

# Postgres
* select '(1.0,1.0)'::POINT;
* select '((1.0,1.0),(1.0,2.0),(2.0,2.0),(2.0,1.0))'::PATH;
* select '((1.0,1.0),(1.0,2.0),(2.0,2.0),(2.0,1.0))'::POLYGON;
* select '((1.0,1.0),1.0)'::CIRCLE;

# TRIPLE Point
* point triple is ("ACCOUNT#abc123", "name#point" , 'value#(1.0, 1.0)')
* point triple to POINT conversion is replace('value#(1.0,1.0)')::POINT

* ~~("ACCOUNT#abc123", "name#point" , 'value#{"type":"POINT", "coordinates": [1.0, 1.0]}')~~
* ~~point is ("ACCOUNT#abc123", "name#point" , 'value#{"coordinates": [1.0,1.0]}')~~
* select ((replace(('("ACCOUNT#abc123","name#point","value#{""type"":""POINT"", ""coordinates"": [1.0, 1.0]}")'::TRIPLE).tk,'value#','')::TEXT)::JSONB) ->> 'coordinates';
triple to 

~~getGeometryAsJSONB(TRIPLE)~~
~~select ('("ACCOUNT#abc123","name#point",{"n": "hi"})'::TRIPLE);~~

# TRIPLE PATH aka polyline
* path triple is ("ACCOUNT#abc123", "name#path" , 'value#((1.0,1.0),(1.0,2.0),(2.0,2.0),(2.0,1.0))')
* path triple to PATH conversion is replace('value#((1.0,1.0),(1.0,2.0),(2.0,2.0),(2.0,1.0))')::PATH

# TRIPLE POLYGON
* polygon triple is ("ACCOUNT#abc123", "name#polygon" , 'value#((1.0,1.0),(1.0,2.0),(2.0,2.0),(2.0,1.0))')
* polygon triple to POLYGON conversion is replace('value#((1.0,1.0),(1.0,2.0),(2.0,2.0),(2.0,1.0))')::POLYGON

# TRIPLE BOX 
* (west,north,east,south) -> ((east,north),(west, south)) -->((upper-right),(lower-left))
* box eg ("ACCOUNT#abc123", "name#box", 'value#(-1.0,1.0,1.0,-1.0)')

# TRIPLE MBR 
* mbr 
* mbr is (north, south, west, east)
* mbr eg ("ACCOUNT#abc123", "name#mbr", 'value#(1.0,-1.0,-1.0,1.0)')
* SELECT string_to_array('-1.0,1.0,1.0,-1.0', ',', 'yy'); --> {}
* SELECT string_to_array('xx~^~yy~^~zz', '~^~', 'yy');
* SELECT '-1.0'::DECIMAL;


# Item as set of Triples 
* Item is stored as a set of triples
* triples must roleup into Item  
* id key eg 'THING#abc' 'name#id' 'value#abc'
* owner key eg 'THING#abc' 'name#owner' 'value#636b0353-05b8-4f9c-afce-9899f102848c'
* type key eg 'THING#abc' 'name#type' 'value#THING'
* created key eg 'THING#abc' 'name#created' 'value#2023-01-18 13:41:41.266304+00'
* updated key eg 'THING#abc' 'name#updated' 'value#2023-01-18 13:41:41.266304+00'

# Credential Triple

# Routes


## DELETE
### **Authenticated Personal Singleton Delete**
* user must be authorized
* user must be authenticated
* limit action to user owned items
* limit action to single item
```
* DELETE    abc/{owner}/PK/{pk}/{sk?} 
    + --> abc(TOKEN, OWNERID, PRIMARYKEY) 
        + --> delete(OWNERID, PRIMARYKEY) 
```

## GET

### **Authenticated Personal Singleton Search**
* user must be authorized
* user must be authenticated
* limit action to user owned items
* limit action to zero, one or more items 
* never return password key or value
```
* GET       abc/{owner}/PK/{pk}/{sk?} 
    + --> abc(TOKEN, OWNERID, PRIMARYKEY) 
        + --> get(PRIMARYKEY)
```

### **Authorized Rectangle Bounded Search**
* user must be authorized
* user need NOT be authenticated
* limit action to zero, one or more items 
* limit item(s) to those contained within a Minimum Bounding Rectangle (MBR)
* item has latitude (lat) and longitude (lon) keys
* never return password key or value
```
* GET       abc/MBR/{north}/{south}/{west}/{east} 
    + --> abc(TOKEN, MBR) 
        +--> get(MBR)
```

### **Authenticated Personal Layer Search**
* DEPRECATE
* user must be authorized
* user must be authenticated
* user not required to be authenticated
* never return password key or value
```
get(OWNERID, PRIMARYKEY, KIND)
```

### **Bounded Layer Search**
DEPRECATE
* user not required to be authenticated
* item must have lat and lon keys
* item is contained within Minimum Bounding Rectangle (MBR)
* item must be of specific KIND, aka LAYER
* item must have designated LAYER, aka KIND
* never return password key or value

```
* get(MBR, KIND)
```

## POST
**Authenticated Personal Triple Insert**
* user must be authorized
* user must be authenticated
* user must own item
* no duplicate items????
* item must have **id** key
* item must have **owner** key
* item must have **type** key
* item must have **guid** key, add guid key to item when not found
* item must have **created** key, add created key to item when not found
* item must have **updated** key, add updated key to item when not found 
* owner is ownerid.id
* type must be uppercase
* guid equals a generated GUID
* created equals current datetime
* updated equals created
* triplize item for storage
```
* POST      abc/{owner} 
    + --> abc(TOKEN, OWNERID, TRIPLE) 
          + --> post(OWNERID, TRIPLE)
```

**SignUp**
* user must be authorized
* user not required to be authenticated
* user must own item
* no duplicate items????
* item must have **id** key
* item must have **owner** key
* item must have **type** key
* item must have **guid** key, add guid key to item when not found
* item must have **created** key, add created key to item when not found
* item must have **updated** key, add updated key to item when not found 
* item must have **password** key
* id value must be \<email>
* owner key equals id
* guid equals a generated GUID
* created equals current datetime
* updated equals created
* password must be encrypted before storage
* item must be triplize before storage
* jwt claims aud, iss, key, scope, sub, user
```
* POST      abc/SIGNUP 
    + --> abc(TOKEN, OWNERID, TRIPLE) 
        + --> post(TOKEN, CREDENTIAL)
```

**SignIn**
* user must be authorized
* user not required to be authenticated
* item must have id
* id value must be \<email> or \<GUID>
* item does not need owner key
* item does not need type key
* item must have password key
* item does not need owner key
* item does not need guid key
* item does not need created key
* item does not need updated key
* token is jwt 
* token encoding uses system password
* token is encoded for id
* token is returned 

```
* POST      abc/SIGNIN 
    + --> abc(TOKEN, OWNERID, TRIPLE) 
        +--> post(TOKEN, CREDENTIAL)
```


## PUT
**Personal Singleton Update**
* user required to be authenticated
* user must own item
* Update limited to primary key
* cannot update id key, use get-update-insert-delete process
* cannot update type key, use get-update-insert-delete process
* cannot update created key
* change updated to current date and time
```
* PUT       abc/{owner}/PK/{pk}/{sk?} 
    + --> abc(TOKEN, OWNERID, PRIMARYKEY, TRIPLE) 
        +--> put(OWNERID, PRIMARYKEY, TRIPLE) 
```
t is token TOKEN
T is trip TRIPLE
o is owner_id OWNERID
p is primary_key PRIMARYKEY
m is m_b_r MBR
c is cred CREDENTIAL
{
'c': 'cred CREDENTIAL',
'T': 'token TOKEN',
't': 'trip TRIPLE',
'o': 'owner OWNERID',
'p': 'primary_key PRIMARYKEY'
}

Top  DGPP, DGPP, DG
Tm   DGPP, DG
Tot  DGPP, DGPP, PP
Topt DGPP, DGPP, DGP, P

[
DTop, 
GTop, 
GTm, 
PTot, 
PTopt
]
     , DELETE, GET, POST, PUT
token,  
```

when not (valid token), return {status:403,msg:Forbidden,extra:Invalid-token,user}
when password in trip, encrypt(trip.password)

result post(owner_id, trip) 

when password in trip, return generate_token()
   
return result
```    
    
# DELETE-base
1. generate a standard-delete for each resource (OWNER,PRIMARY)
1. when owner is NULL then invalid, status:400
1. when owner.id is NULL then invalid, status:400
1. when primary_key is NULL then invalid, status:400
1. when primary_key.pk is NULL then invalid, status:400
1. when primary_key.sk is NULL then invalid, status:400
1. when primary_key.sk is *, then delete all where pk = primary_key.pk
1. when primary_key.sk is NOT *, then delete where pk = primary_key.pk and sk=primary_key.sk
1. When ownership not confirmed, return status:404
1. On insert failure, set result-state to status: 500
1. On delete success, include deleted record count in result-state
1.  return result-state

# DELETE-kop        
1. generate a resource-delete for each resource (TOKEN,OWNER,PRIMARY)
1. When invalid token: return status 403
1. On delete, return result

# DELETE-m
* no special handling required

# GET-base
1. generate a standard-get for each resource (OWNER,PRIMARY)
1. when owner is NULL then invalid, status:400
1. when owner.id is NULL then invalid, status:400
1. when primary_key is NULL then invalid, status:400
1. when primary_key.pk is NULL then invalid, status:400
1. when primary_key.sk is NULL then invalid, status:400
1. when primary_key.sk is *, then get where primary_key.pk = pk
1. when primary_key.sk is NOT *, then get where pk = primary_key.pk and sk=primary_key.sk
1. When 'password' in primary_key.sk, then return result:[]
1. When ownership not confirmed, return status:404
1. When primary_key is not FOUND, return status: 200, result:[]
1. When primary_key is FOUND, return status: 200, result:[<triple>,...]

# GET-kop
1. generate a resource-get for each resource (TOKEN,OWNER,PRIMARY)
1. When invalid token: return status 403

# GET-m
1. generate a custom-get for each resource (MBR)
     
        
        
# POST
1. generate a standard-post for each resource (OWNER,TRIPLE)
1. when invalid owner, return status:400
1. when invalid trip, return status:400
1. when invalid trip.pk, return status:400
1. when invalid trip.sk, return status:400
1. when invalid trip.tk, return status:400
1. When password in trip: encrypt password

1. On insert failure, set result-state to status: 500
1. On insert duplicate, set result-state to status: 409, triple: trip
1. On insert success, set result-state to status: 200, insertion: result
* when password in trip, scrub password
1. return result-state

# POST-token-password
1. generate a resource-post for each resource (TOKEN,OWNER,TRIPLE)

1. When invalid token: return status 403
* When lon and lat in 
1. On post success or failure:  set result-state
* When password in trip and 200 or 409 in result-state:
    * validate the password  
    * generate token
    * set result-state to status:200, token: <token>    
* return result-state status:200, token: <token> 

# POST-point
* when [n.n,n.n] convert to (n.n,n.n)

# PUT
* generate a standard-put for each resource (OWNER,PRIMARYKEY,TRIPLE)
1. when invalid owner is NULL, return status:400
1. when invalid owner.id is NULL, return status:400
1. when invalid id is NULL, return status:400
1. when invalid id.pk is NULL, return status:400
1. when invalid id.sk is NULL, return status:400
1. when invalid trip is NULL, return status:400
1. when invalid trip.pk is NULL, return status:400
1. when invalid trip.sk is NULL, return status:400
1. when invalid trip.tk is NULL, return status:400
1. when # not in trip.pk, return status:400 
1. when # not in trip.sk, return status:400
1. when # not in trip.tk, return status:400
1. When password in trip: encrypt password
1. When ownership not confirmed, return status:404
* when "name#id" in trip.sk, status: 403
* when "name#type" in trip.sk, status: 403
1. On update failure not found, result is status: 404 and trip
* On update success, result is status: 200 and trip
* When password in trip and status 200:
    * validate the password  
    * generate token
    * add token to result
    * set result to status:200
* when password in trip, scrub password
* return result

# PUT-password
* generate a resource-put for each resource (TOKEN,OWNER,PRIMARYKEY,TRIPLE)
* When invalid token: return status 403
* When password in trip: encrypt password
* On post success or failure:  set result-state
* When password in trip and 200 or 409 in result-state:
    * validate the password  
    * generate token
    * set result-state to status:200, token: <token>    
* return result-state status:200, token: <token> 




# AUTHENTICATION

## 



'''
# Workout, Text to Json

# use case              t    target  taget                   new     value   value
# targets               v    type    hasName key value       key     type    hasName

# {}                    -       D       N       a1  b           Y       S       N          DN-Y-SN add key-value to target
# {a1: b}               a1      S       N       a1  c           N       S       N          SN-N-SN listify target value, append value to List
# {a1: [b,c]}           a1      L       N       -   -           N       ?       ?          LN-N-??

# {}                    -       D       N       a1  []          Y       L       N           DN-Y-LN add key-value to target
# {a1: []}              a1      L       N       a1  b           N       S       N           LN-N-SN append value to list
# {a1: [b]}             a1      L       N       a1  []          N       L       N           LN-N-LN append value to list
# {a1: [b,[]]}          a1      L       N       a1  {}          N       D       N           LN-N-DN
# {a1: [b,[],{}]}       a1      L       N                       N       ?       ?           LN-N-??

wrong
# {}                    -       D       N       a1  {a:A}       Y       D       N           DN-Y-DN add key-value to target
# {a1: {a:A}}           a1      D       N       a1  {b:B}       N       D       N           DN-N-DN listify target value, append value to List
# {a1: [{a:A,b:B}]}     a1      L       N       -   -           N       ?       ?           LN-N-??
should be
# {}                    -       D       N       a1  {a:A}       Y       D       N           DN-Y-DN add key-value to target
# {a1: {a:A}}           a1      D       N       a1  {b:B}       N       D       N           DN-N-DN add key-value to target
# {a1: [{a:A},{b:B}]}   a1      D       N       a1  {a:A}       N       ?       ?           DN-N-??
# {a1: [{a:A},{b:B},{a:A}]}
#                       a1      D       N       a1  {a:A}       Y       D       N           DN-Y-DN add key-value to target

# {}                    -       D       N       a1  {name:a}    Y       D       Y           DN-Y-DY add key-value to target
# {a1: {name:a}}        a1      D       Y       a1  {name:a}    N       D       Y           DY-N-DY dictify target value, add key-value
# {a1: {a:{name:a}}}    a1      D       N       a1  {name:a}    N       D       Y           DN-N-DY ????
# {a1: {a:{name:a}}}    a1      D       N       a1  {name:b}    N       D       Y           DN-N-DY add key-value to target
# {a1: {a:{name:a},
#       b:{name:b}}}    a1      D       N       -   -           N       ?       ?           DN-N-??

# {}                    -       D       N       a1 [a,b]        Y       L       N           DN-Y-LN add key-value to target
# {a1:[a,b]}            a1      L       N       a1 [c,d]        N       L       N           DL-N-LN rollover
# {a1:[[a,b],[c,d]]}    a1      L       N       a1 [e,f]        N       L       N           DL-N-LN 

S scalar 'a'
{} dict
[] list
{a:A} unnamed dict 
{name: A} named dict
l empty list []
L scalar list [a,b,c] 
m mixed list [a,[],{}]
n list of lists [[],[]]
o list of dict [{a:A},{a:B}]
'''

```
for scope in [api_admin, api_guest, api_user]
    getOwnerData(scope)

```

 
    

# Data
## Owner
### api_admin:
1. id: <scope>@lyttlebit.com
1. type: ACCOUNT
1. username: <scope>@lyttlebit.com
1. displayname: J
1. password: a1A!aaaa
1. scope: <scope>
### api_guest
### api_user

## Claim
### api_admin:
1. aud: starter_api_4_client
1. iss: lyttlebit
1. key: <scope>@lyttlebit.com
1. scope: <scope>
1. sub: client-api
1. user: <scope>@lyttlebit.com
### api_guest
### api_user

## Resource


'''
                         Template
                            |
                            + -> __init__()
                            + -> level(lnStr)
                            + -> getSection()
      set(target, value) -> + 
                            + -> getClassName()    
                            + -> setup()
           add(Template) -> + 
       setDataTemplate() -> + -> getDataTemplate()
                            + -> gett(target, return_type='singleton', key='name')
                            + -> getTemplateStrint()
                            + -> toString()
                            + -> gett()
    
Template -> + -> Template_Resource
            |       + Template_Resource_Account
            + -> Template_Route
            + -> Template_File
            |       + -> TemplateFile_Project
            |       + -> Template_ResourceTest
            |       + -> Template_FileRouteHandler
            +            
    
'''

Template
* Resource
    * ResourceAccount
* Template_ResourceTest    
* Route
    * TestDeleteAccountRouteTemplate
    * TestGetAccountRouteTemplate
    * TestPostAccountRouteTemplate
    * TestPutAccountRouteTemplate
* ModelDatum
    * ModelDatumAccount
    * ModelDatumEmpty 
* Template_File
    * TemplateFile_Function
    * TemplateFile_Project
        * DocumentProjectMdSample
    * TemplateFile_RouteHandler
    * DocumentAppJson
    * DocumentDeploy
    * DocumentDockerCompose
    * DocumentDockerfile
    * DocumentEnv
    * DocumentPackageJson
    * DocumentResourceTestWrapperJs
    
    
    
Document    