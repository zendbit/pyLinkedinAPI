# pyLinkedinAPI (Version 1.0.0)
python wrapper for simplify linkedin rest API 

Dont forget to check REST API Documentation https://developer.linkedin.com/docs

<pre>
# LinkedinAPI
#
# this document is GPLV3
# you can changes or modify and redistribute for free
# author : amru rosyada & windra evie
# email : amru.rosyada@gmail.com
# twitter : @_mru_
# skype : amru.rosyada
# linkedin api V1
# oauth v2.0
</pre>

#Read the Docs
<pre>
request api is simple, linkedin use 2 basis type of uri
1. people basis uri (https://api.linkedin.com/v1/people/~)
2. companies basis uri (https://api.linkedin.com/v1/companies/)


in this API implementation will only support json format even linkedin also support in xml format
it's easier to make standard only using json
so each time API call we must add format=json on each query string


to call api just do this:

l_api = LinkedinAPI('0Pgn', '756')
l_api.request_api(query_params)


what is query_params?
query_params is python dictionary in strict format
use this query_params format when call api

query_params = {'access_token':'', # required
   'uri':'', # required
   'method':'GET', # required it can be GET or POST or PUT, depend on API specification
   'json_post_body':{}, # required if empty should initialize with {} as empty dictionary
   'api_type':''} # required it can be api_people or api_companies depend on what basis to be call


for example I want to get user information
the API said that we need to call with this form https://api.linkedin.com/v1/people/~:(fields of interest)?format=json
example of api is like this https://api.linkedin.com/v1/people/~:(id,first-name,skills,educations,languages,twitter-accounts)?format=json
wee need to skip https://api.linkedin.com/v1/people/~ this one and use only uri after https://api.linkedin.com/v1/people/~
which is :(id,first-name,skills,educations,languages,twitter-accounts)?format=json


so if i call from my pyLinkedinAPI it should be

query_params = {'access_token':'AQU8vqL83uNZYnnHpUuJjBSOfJG08lGmnt9JOxEBH8klL3Omi49nxKa8_0mPHAo0qVUBupKxnrIX2qRL_IdFY5VVEP_lrx__a4evniT-bPylM5Oxq0z_WY1KH3TXd-8gf1RKjKb9t1-NMcH',
    'uri':':(id,first-name,skills,educations,languages,twitter-accounts)?format=json',
    'method':'GET',
    'json_post_body':{},
    'api_type':'api_people'} 

l_api = LinkedinAPI('0Pgn', '756')
l_api.request_api(query_params)


one more example, I want to Check companies basis information about: Check if sharing is enabled for a company
the API documentation said that we must call it with this form https://api.linkedin.com/v1/companies/{id}/is-company-share-enabled?format=json
{id} should remove with real company id, in this case I use dummy as my 287349 company id
it will look like this https://api.linkedin.com/v1/companies/287349/is-company-share-enabled?format=json


if we call it from pyLinkedinAPI it will be like this

query_params = {'access_token':'AQU8vqL83uNZYnnHpUuJjBSOfJG08lGmnt9JOxEBH8klL3Omi49nxKa8_0mPHAo0qVUBupKxnrIX2qRL_IdFY5VVEP_lrx__a4evniT-bPylM5Oxq0z_WY1KH3TXd-8gf1RKjKb9t1-NMcH',
    'uri':'/287349/is-company-share-enabled?format=json',
    'method':'GET',
    'json_post_body':{},
    'api_type':'api_companies'}

l_api = LinkedinAPI('0Pgn', '756')
l_api.request_api(query_params)
</pre>

#Ex: Get URL grant access
<pre>
# create linkedin API object
# LinkedinAPI('YOUR CLIENT SECRET', 'YOUR CLIENT ID')


l_api = LinkedinAPI('0Pgn', '756')



# generate grant authorization grant access to linkedin api
# redirect url parameter is from your linkedin application setting 
# and must be accessible, wee need at lease simulate it in localhost
# request_authorization_url(redirect_url)


authorization_url = l_api.request_authorization_url('http://127.0.0.1:8888/p/authenticate/linkedin')


# in my case authorization_url will give me output:
# https://www.linkedin.com/uas/oauth2/authorization?client_id=756es7gxn3cirr&redirect_uri=http%3A%2F%2F127.0.0.1%3A8888%2Fp%2Fauthenticate%2Flinkedin&response_type=code&scope=r_basicprofile%20r_contactinfo%20r_emailaddress%20r_fullprofile%20r_network%20rw_company_admin%20rw_groups%20rw_nus%20w_messages%20w_share&state=1430617897163575
# then open it in your browser ot grant user privilleges
# it will ask user to grant access to the application, if user accept it should be redirect to your application redirect url
# in my case I emulate it on localhost, you only need care about code variable
# http://127.0.0.1:8888/p/authenticate/linkedin?code=AQTTxW59ACIgwoP7WKRYKtJAzb4cxa3EnwRRfxrLPGAsPGjNP-wbIbVqQl7J&state=1430617897163575
# the code have short life time, as soon as possible use it and get token access using request_access_token(redirect_url, code)
# it life time expired it will give output bad request :D, then we need to start from step authorization to generate new code
# code will be use in next step
</pre>

#Generate request access token
<pre>
# from previous step we got code for generate token access
# http://127.0.0.1:8888/p/authenticate/linkedin?code=AQTTxW59ACIgwoP7WKRYKtJAzb4cxa3EnwRRfxrLPGAsPGjNP-wbIbVqQl7J&state=1430617897163575
# the code have short life time, as soon as possible use it and get token access using request_access_token(redirect_url, code)
# it life time expired it will give output bad request :D, then we need to start from step authorization to generate new code

access_token = l_api.request_access_token('http://127.0.0.1:8888/p/authenticate/linkedin', 'AQTTxW59ACIgwoP7WKRYKtJAzb4cxa3EnwRRfxrLPGAsPGjNP-wbIbVqQl7J')

# in my case access_token will be python dictionary result
# with token information and expires time
# linked in doesnt give us long time access token.
# if it already expired we can do from step authorization. Linkedin care about user data so they doesnt give long time access token
# {'expires_in': 5171070, 'access_token': 'AQU8vqL83uNZYnnHpUuJjBSOfJG08lGmnt9JOxEBH8klL3Omi49nxKa8_0mPHAo0qVUBupKxnrIX2qRL_IdFY5VVEP_lrx__a4evniT-bPylM5Oxq0z_WY1KH3TXd-8gf1RKjKb9t1-NMcH'}
# store that information into database or file to call linkedin rest api
# it will useable until expired.
</pre>

#Other Ex:
<pre>
# I want to Check companies basis information about: Check if sharing is enabled for a company
# the API documentation said that we must call it with this form https://api.linkedin.com/v1/companies/{id}/is-company-share-enabled?format=json
# {id} should remove with real company id, in this case I use dummy as my 287349 company id
# it will look like this https://api.linkedin.com/v1/companies/287349/is-company-share-enabled?format=json
#
# if we call it from pyLinkedinAPI it will be like this
query_params = {'access_token':'AQU8vqL83uNZYnnHpUuJjBSOfJG08lGmnt9JOxEBH8klL3Omi49nxKa8_0mPHAo0qVUBupKxnrIX2qRL_IdFY5VVEP_lrx__a4evniT-bPylM5Oxq0z_WY1KH3TXd-8gf1RKjKb9t1-NMcH',
    'uri':'/287349/is-company-share-enabled?format=json',
    'method':'GET',
    'json_post_body':{},
    'api_type':'api_companies'}

l_api = LinkedinAPI('0Pgn', '756')
l_api.request_api(query_params)

# REST API https://api.linkedin.com/v1/people/~:(fields of interest)?format=json
# REST API call example https://api.linkedin.com/v1/people/~:(id,first-name,skills,educations,languages,twitter-accounts)?format=json
query_params = {'access_token':'AQU8vqL83uNZYnnHpUuJjBSOfJG08lGmnt9JOxEBH8klL3Omi49nxKa8_0mPHAo0qVUBupKxnrIX2qRL_IdFY5VVEP_lrx__a4evniT-bPylM5Oxq0z_WY1KH3TXd-8gf1RKjKb9t1-NMcH',
    'uri':':(id,first-name,skills,educations,languages,twitter-accounts)?format=json',
    'method':'GET',
    'json_post_body':{},
    'api_type':'api_people'}

l_api.request_api(query_params)

# Share update user profile status
# REST API https://api.linkedin.com/v1/people/~/shares?format=json
json_post_body = {'comment':'second test share from pyLinkedinAPI',
    'visibility':{'code':'anyone'}}

query_params = {'access_token':'AQU8vqL83uNZYnnHpUuJjBSOfJG08lGmnt9JOxEBH8klL3Omi49nxKa8_0mPHAo0qVUBupKxnrIX2qRL_IdFY5VVEP_lrx__a4evniT-bPylM5Oxq0z_WY1KH3TXd-8gf1RKjKb9t1-NMcH',
    'uri':'/shares?format=json',
    'method':'POST',
    'json_post_body':json_post_body,
    'api_type':'api_people'}

l_api.request_api(query_params)

# Result
# {
#   "updateKey": "UPDATE-127559940-6000440416531402752",
#   "updateUrl": "https://www.linkedin.com/updates?discuss=&scope=127559940&stype=M&topic=6000440416531402752&type=U&a=70fn"
# }

# example companies
# Check if sharing is enabled for a company
# REST API https://api.linkedin.com/v1/companies/{id}/is-company-share-enabled?format=json
query_params = {'access_token':'AQU8vqL83uNZYnnHpUuJjBSOfJG08lGmnt9JOxEBH8klL3Omi49nxKa8_0mPHAo0qVUBupKxnrIX2qRL_IdFY5VVEP_lrx__a4evniT-bPylM5Oxq0z_WY1KH3TXd-8gf1RKjKb9t1-NMcH',
    'uri':'/287349/is-company-share-enabled?format=json',
    'method':'GET',
    'json_post_body':{},
    'api_type':'api_companies'}

l_api.request_api(query_params)

# Check if the member is a company administrator
# REST API https://api.linkedin.com/v1/companies/{id}/relation-to-viewer/is-company-share-enabled?format=json
query_params = {'access_token':'AQU8vqL83uNZYnnHpUuJjBSOfJG08lGmnt9JOxEBH8klL3Omi49nxKa8_0mPHAo0qVUBupKxnrIX2qRL_IdFY5VVEP_lrx__a4evniT-bPylM5Oxq0z_WY1KH3TXd-8gf1RKjKb9t1-NMcH',
    'uri':'/287349/relation-to-viewer/is-company-share-enabled?format=json',
    'method':'GET',
    'json_post_body':{},
    'api_type':'api_companies'}

l_api.request_api(query_params)

# share from company update status
# https://api.linkedin.com/v1/companies/{id}/shares?format=json
json_post_body = {'visibility':{'code':'anyone'},
    'comment':'There are a lot of great career opportunities here!'}

query_params = {'access_token':'AQU8vqL83uNZYnnHpUuJjBSOfJG08lGmnt9JOxEBH8klL3Omi49nxKa8_0mPHAo0qVUBupKxnrIX2qRL_IdFY5VVEP_lrx__a4evniT-bPylM5Oxq0z_WY1KH3TXd-8gf1RKjKb9t1-NMcH',
    'uri':'/287349/shares?format=json',
    'method':'POST',
    'json_post_body':json_post_body,
    'api_type':'api_companies'}

l_api.request_api(query_params)

# Add a comment on behalf of a company
# REST API https://api.linkedin.com/v1/companies/{id}/updates/key={update-key}/update-comments-as-company/
json_post_body = {'comment':'Posting as a company!'}

query_params = {'access_token':'AQU8vqL83uNZYnnHpUuJjBSOfJG08lGmnt9JOxEBH8klL3Omi49nxKa8_0mPHAo0qVUBupKxnrIX2qRL_IdFY5VVEP_lrx__a4evniT-bPylM5Oxq0z_WY1KH3TXd-8gf1RKjKb9t1-NMcH',
    'uri':'/287349/updates/key=87394862/update-comments-as-company/',
    'method':'PUT',
    'json_post_body':json_post_body,
    'api_type':'api_companies'}

l_api.request_api(query_params)
</pre>
