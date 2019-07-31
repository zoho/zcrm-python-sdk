'''
Created on Aug 16, 2017

@author: sumanth-3058
'''

class ZohoOAuthConstants(object):
    '''
    OAuth constants
    '''
    IAM_URL="accounts_url";
    SCOPES="scope";
    STATE="state";
    STATE_OBTAINING_GRANT_TOKEN="OBTAIN_GRANT_TOKEN";
    RESPONSE_TYPE="response_type";
    RESPONSE_TYPE_CODE="code";
    CLIENT_ID="client_id";
    CLIENT_SECRET="client_secret";
    REDIRECT_URL="redirect_uri";
    ACCESS_TYPE="access_type";
    ACCESS_TYPE_OFFLINE="offline";
    ACCESS_TYPE_ONLINE="online";
    PROMPT="prompt";
    PROMPT_CONSENT="consent";
    GRANT_TYPE="grant_type";
    GRANT_TYPE_AUTH_CODE="authorization_code";
    TOKEN_PERSISTENCE_PATH="token_persistence_path";
    CUSTOM_PERSISTENCE_HANDLER_PATH = "persistence_handler_path";
    CUSTOM_PERSISTENCE_HANDLER_CLASS = "persistence_handler_class";
    SANDBOX="sandbox";
    DATABASE_PORT="mysql_port";
    DATABASE_PASSWORD="mysql_password";
    DATABASE_USERNAME="mysql_username";
    PERSISTENCE_FILE_NAME="zcrm_oauthtokens.pkl"
    
    GRANT_TYPE_REFRESH="refresh_token";
    CODE="code";
    GRANT_TOKEN="grant_token";
    ACCESS_TOKEN="access_token";
    REFRESH_TOKEN="refresh_token";
    EXPIRES_IN = "expires_in";
    EXPIRIY_TIME = "expiry_time";
    TOKEN = "token";
    DISPATCH_TO = "dispatchTo";
    OAUTH_TOKENS_PARAM = "oauth_tokens";
    
    OAUTH_HEADER_PREFIX="Zoho-oauthtoken ";
    AUTHORIZATION="Authorization";
    REQUEST_METHOD_GET="GET";
    REQUEST_METHOD_POST="POST";
    
    RESPONSECODE_OK=200;

class ZohoOAuthException(Exception):
    '''
    This is the custom exception class for handling Client Library OAuth related exceptions 
    '''
    def __init__(self, err_message):
        self.message=err_message
        Exception.__init__(self,err_message)

    def __str__(self):
        return self.message

class ZohoOAuthHTTPConnector(object):
    '''
    This module is to make HTTP connections, trigger the requests and receive the response
    '''
    @staticmethod
    def get_instance(url,params=None,headers=None,body=None,method=None):
        return ZohoOAuthHTTPConnector(url,params,headers,body,method)
    
    def __init__(self, url,params,headers,body,method):
        '''
        Constructor
        '''
        self.url=url
        self.req_headers=headers
        self.req_method=method
        self.req_params=params
        self.req_body=body
        
    def trigger_request(self):
        response=None
        import requests,json
        if(self.req_method == ZohoOAuthConstants.REQUEST_METHOD_GET):
            response=requests.get(self.url,params=self.req_params, headers=self.req_headers,allow_redirects=False)
        elif(self.req_method==ZohoOAuthConstants.REQUEST_METHOD_POST):
            response=requests.post(self.url,data=json.dumps(self.req_body), params=self.req_params,headers=self.req_headers,allow_redirects=False)
        return response
    def set_url(self,url):
        self.url=url
    def get_url(self):
        return self.url
    def add_http_header(self,key,value):
        self.req_headers[key]=value
    def get_http_headers(self):
        return self.req_headers
    def set_http_request_method(self,method):
        self.req_method=method
    def get_http_request_method(self):
        return self.req_method
    def set_request_body(self,reqBody):
        self.req_body=reqBody
    def get_request_body(self):
        return self.req_body
    def add_http_request_params(self,key,value):
        self.req_params[key]=value
    def get_http_request_params(self):
        return self.req_params
    
class ZohoOAuthParams(object):
    '''
    This class is to OAuth related params(i.e. client_id,client_secret,..)
    '''
    def __init__(self, client_id,client_secret,redirect_uri):
        '''
        Constructor
        '''
        self.clientID=client_id
        self.clientSecret=client_secret
        self.redirectUri=redirect_uri
    @staticmethod
    def get_instance(client_id,client_secret,redirect_uri):
        return ZohoOAuthParams(client_id,client_secret,redirect_uri)
    
import logging
logger=logging.getLogger('Client_Library_OAUTH')
class OAuthLogger(object):
    '''
    This class is to log the exceptions onto console and file
    '''
    @staticmethod
    def add_log(message,level,exception=None):
        logger.setLevel(logging.DEBUG)
        consoleHandler = logging.StreamHandler()
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        try:
            from .Utility import ZCRMConfigUtil,APIConstants
        except ImportError:
            from Utility import ZCRMConfigUtil,APIConstants
        log_path = None
        if(APIConstants.APPLICATION_LOGFILE_PATH in ZCRMConfigUtil.config_prop_dict):
            log_path=ZCRMConfigUtil.config_prop_dict[APIConstants.APPLICATION_LOGFILE_PATH]
        if log_path is not None and log_path.strip()!="":
            import os
            log_path=os.path.join(log_path,'oauth.log')
        
            fileHandler=logging.FileHandler(log_path)
            fileHandler.setLevel(logging.DEBUG)
            fileHandler.setFormatter(formatter)
            logger.addHandler(fileHandler)
        
        consoleHandler.setLevel(logging.DEBUG)
        consoleHandler.setFormatter(formatter)
        # add the handlers to the logger
        logger.addHandler(consoleHandler)
        
        
        if(exception!=None):
            message+='; Exception Message::'+exception.__str__()
        if(level==logging.ERROR):
            logger.error(message)
        elif(level==logging.INFO):
            logger.info(message)
        elif(level==logging.WARNING):
            logger.warning(message)