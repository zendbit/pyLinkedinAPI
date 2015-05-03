# LinkedinAPI
#
# this document is GPLV3
# you can changes or modify and redistribute for free
# author : amru rosyada
# email : amru.rosyada@gmail.com
# twitter : @_mru_
# skype : amru.rosyada
# linkedin api V1
# oauth v2.0
import time
from base64 import b64encode
from urllib.parse import quote, parse_qs
from urllib.request import Request, urlopen
from hmac import new as hmac
from hashlib import sha1
import json

class LinkedinAPI():
    
    # constructor init parameter is client secret and client id
    def __init__(self, client_secret, client_id):
        self.client_secret = client_secret
        self.client_id = client_id
        
        # list of dictionary of twitter rest api url
        # access via dicionary get will return url of rest api
        self.rest_api = {'api_oauth2_authorization':('https://www.linkedin.com/uas/oauth2/authorization', 'GET'),
            'api_oauth2_access_token':('https://www.linkedin.com/uas/oauth2/accessToken', 'POST'),
            'api_people':('https://api.linkedin.com/v1/people/~', 'NA'), # NA mead not associate, will decide later
            'api_companies':('https://api.linkedin.com/v1/companies', 'NA')}

        # scope of application access
        # this scope is depend on your application access
        # remove some access if you only need for specific purpose
        '''self.scope_api = ('r_basicprofile',
            'r_contactinfo',
            'r_emailaddress',
            'r_fullprofile',
            'r_network',
            'rw_company_admin',
            'rw_groups',
            'rw_nus',
            'w_messages',
            'w_share')'''

        # default scope is only r_basicprofile, r_emailaddress and r_fullprofile
        self.scope_api = ('r_basicprofile',
            'r_emailaddress',
            'r_fullprofile')

    # request url authorization
    # parameter is redirect url, should be same with your app setting
    # scope parameter can be tupple or list, if it's not defined will use default setting  self.scope_api
    # ex scope=('r_contactinfo',) or scope=['r_contactinfo']
    def request_authorization_url(self, redirect_url, scope=None):
        # get oauth2 url authorization
        params_qs = {'response_type':'code',
            'client_id':self.client_id,
            'redirect_uri':redirect_url,
            'state':str(time.time()).replace('.', '')}

        # if scope defined add scope to params_qs
        if scope:
            params_qs['scope'] = ' '.join(scope)

        # use default scope, grant all access
        else:
            params_qs['scope'] = ' '.join(self.scope_api)

        url, method = self.rest_api.get('api_oauth2_authorization')

        return '?'.join((url, '&'.join(['%s=%s' % (k, self.percent_quote(params_qs[k])) for k in sorted(params_qs)])))


    # parameter
    # grant type for authorization should be valued with 'authorization_code'
    # code is from authorization step, after uri redirected from authorization url
    # redirect_uri is your redirect uri on app setting, if request authorization redirect_uri should be not empty
    # request_url is rest api url, should be not empty whend make request api
    # access token is required if make api call
    # linkedin using json/xml for request api post/put. json_post_body must be in json format
    def do_request(self, request_url='', grant_type='', code='', redirect_uri='',
        access_token='', request_method='POST', json_post_body=''):

        query_string = ''

        # set headers
        # set default user agent, most service need this to prevent fraud
        headers_payload = {'User-Agent':'HTTP Client'}

        # if method post add content type header to 
        # if authorization step add client secret
        # and client id
        if grant_type == 'authorization_code':
            # setup parameter
            headers_payload['Content-Type'] = 'application/x-www-form-urlencoded'

            params_qs = {}
            params_qs['grant_type'] = grant_type
            params_qs['code'] = code
            params_qs['redirect_uri'] = redirect_uri
            params_qs['client_id'] = self.client_id
            params_qs['client_secret'] = self.client_secret

            # build qs request_url for authentication
            query_string = '&'.join(['%s=%s' % (self.percent_quote(k), self.percent_quote(params_qs[k])) for k in sorted(params_qs)]).encode('ISO-8859-1')


        # if return type is json add to header payload x-li-format: json
        # should in json format
        # for request api
        else:
            headers_payload['x-li'] = 'json'
            headers_payload['x-li-format'] = 'json'
            headers_payload['Content-Type'] = 'application/json'

        # if access token not empty
        # indicate that request an api, should add access_token to header authorization payload
        if access_token != '':
            headers_payload['Authorization'] = 'Bearer ' + self.percent_quote(access_token)

        # if json body request
        # set param_str to json body
        if json_post_body != '' and grant_type != 'authorization_code':
            query_string = json_post_body.encode('ISO-8859-1')

        # request to provider with
        # return result
        try:
            req = Request(request_url, data=query_string, headers=headers_payload, method=request_method)
            res = urlopen(req)

            # default return value
            return res.readall()

        except Exception as e:
            print(e)
            return None

    # parse query string into dictionary
    # parameter is query string key=valuy&key2=value2
    def qs_to_dict(self, qs_string):
        res = parse_qs(qs_string)
        data_out = {}
        for k in res:
            data_out[k] = res[k][0]
        
        return data_out

    # request authentication url
    # requred parameter is oauth_token
    # will return request_auth_url for granting permission
    def request_authenticate_url(self, oauth_token):
        url, method = self.rest_api.get('api_oauth_authorize')
        
        if oauth_token:
            return '?'.join((url, '='.join(('oauth_token', self.percent_quote(oauth_token)))))
            
        # default value is None
        return None
        
    # request access token
    # parameter is code from authorization process
    # redirect uri should be same with your redirect uri on your application setting
    def request_access_token(self, redirect_uri, code):
        url, method = self.rest_api.get('api_oauth2_access_token')
        
        if redirect_uri and code:
            res = self.do_request(request_url=url,
                grant_type='authorization_code',
                code=code,
                redirect_uri=redirect_uri,
                request_method=method)

            if res:
                return json.loads(res.decode('UTF-8'))
                
        # default return none
        return None
        
    # call request api
    # access token for api access
    # params should be refer to linkedin rest api
    # params should be 
    # query_params = {'access_token':'AQU8vqL83uNZYnnHpUuJjBSOfJG08lGmnt9JOxEBH8klL3Omi49nxKa8_0mPHAo0qVUBupKxnrIX2qRL_IdFY5VVEP_lrx__a4evniT-bPylM5Oxq0z_WY1KH3TXd-8gf1RKjKb9t1-NMcH',
    #   'uri':':(id,first-name,skills,educations,languages,twitter-accounts)?format=json',
    #   'method':'GET',
    #   'json_post_body':{}},
    #   'api_type':'api_people'}
    def request_api(self, params):
        # get url request based on api type
        url, method = self.rest_api.get(params.get('api_type'))

        access_token = params.get('access_token')

        # get parameter to be pass
        method = params.get('method')
        json_post_body = json.dumps(params.get('json_post_body'))
        url += params.get('uri')

        res = self.do_request(request_url=url,
            request_method=method,
            access_token=access_token,
            json_post_body=json_post_body)

        if res:
            return res.decode('UTF-8')

        # default return value
        return None

    # percent_quote
    # quote url as percent quote
    def percent_quote(self, text):
        return quote(text, '~')
        