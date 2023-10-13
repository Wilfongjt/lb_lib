# Conversions: []
1. eg. 1.1 -> Decimal('1.1') -> 1.1
1. eg. 1 -> int("1") -> 1
1. eg. "1.1" -> str("1.1") -> '1.1'
1. eg. "1" -> str("1") -> '1'
1. eg. True -> bool('True') -> True
1. eg. 3-330 -> typeify('3-330') -> {'max': 330, 'mix': 3}

# Definitions: []
1. __C__ is _Create_ 
1. __R__ is _Read_ scope
1. __U__ is _Update_ scope
1. __D__ is _Delete_ scope
1. __c__ is _character_ type
1. __b__ is _boolean_ type
1. __i__ is _integer_ type
1. __d__ is _decimal_ type

# project:
1. name: example
1. version: '1.1.1'

## claims:
* Javascript Web Tokens (JWT) claims
* claims apply to all resources defined in this project
1. issuer: lyttlebit
1. audience: example-api_client
1. subject: client_api

## roles: []
* API Roles used by system
1. api_admin
1. api_guest
1. api_user

## account:
* User account
### scope:
* scope grants access to any field in the model with the same scope 
1. api_admin: RD
1. api_guest: C
1. api_user: RUD

### model: []
* scope is global to all users
* size is defined as a range eg 3-330 is read as "the minimum size of 3 and maximum size of 330"
* size is relative to the type
1. name: id, type:C, size:3-330, validate:R, scope: R 
1. name: type, type:C, size:3-330, validate:R, scope: R
1. name: owner, type:C, size:3-330, validate:R, scope: R
1. name: username, type:C, size:3-30, validate:R, scope: CRU
1. name: password, type:C, size:8-330, validate:R, scope: CU
1. name: displayname, type:C, size:1-30, validate:R, scope: CRU

### form_sample:
* Useful data for testing
1. id: abc123, 
1. type: ACCOUNT, 
1. owner: abc123,
1. username: abc123#xyx.com
1. password: a1A!aaaa
1. displayname: J

### api_admin
1. id: api_admin@example.com
1. type: ACCOUNT
1. username: api_admin@example.com
1. displayname: J
1. password: a1A!aaaa
1. scope: api_admin
