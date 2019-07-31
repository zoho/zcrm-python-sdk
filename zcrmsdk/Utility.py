'''
Created on Aug 16, 2017

@author: sumanth-3058
'''
import requests
import json
try:
    from .OAuthClient import ZohoOAuth
    from .OAuthUtility import ZohoOAuthException,ZohoOAuthConstants
    from .CLException import ZCRMException
except ImportError:
    from OAuthClient import ZohoOAuth
    from OAuthUtility import ZohoOAuthException,ZohoOAuthConstants
    from CLException import ZCRMException

class HTTPConnector(object):
    '''
    This module is to make HTTP connections, trigger the requests and receive the response
    '''
    @staticmethod
    def get_instance(url,params,headers,body,method,apiKey,is_bulk_req):
        return HTTPConnector(url,params,headers,body,method,apiKey,is_bulk_req)
    
    def __init__(self, url,params,headers,body,method,apiKey,is_bulk_req):
        '''
        Constructor
        '''
        self.url=url
        self.req_headers=headers
        self.req_method=method
        self.req_params=params
        self.req_body=body
        self.api_key=apiKey
        self.is_bulk_req=is_bulk_req
        self.file=None
        
    def trigger_request(self):
        response=None
        if(self.req_method == APIConstants.REQUEST_METHOD_GET):
            #if(self.req_params!=None and self.req_params.length>0):
            #   self.url=self.url+'?'+self.get_request_params_as_string(self.req_params)
            response=requests.get(self.url, headers=self.req_headers,params=self.req_params,allow_redirects=False)
        elif(self.req_method==APIConstants.REQUEST_METHOD_PUT):
            response=requests.put(self.url, data=json.dumps(self.req_body),params=self.req_params,headers=self.req_headers,allow_redirects=False)
        elif(self.req_method==APIConstants.REQUEST_METHOD_POST):
            if self.file is None:
                response=requests.post(self.url,data=json.dumps(self.req_body), params=self.req_params,headers=self.req_headers,allow_redirects=False)
            else:
                response=requests.post(self.url, files=self.file,headers=self.req_headers,allow_redirects=False,data=self.req_body)
        elif(self.req_method==APIConstants.REQUEST_METHOD_DELETE):
            response=requests.delete(self.url,headers=self.req_headers,params=self.req_params,allow_redirects=False)
        return response
    def get_request_params_as_string(self,params):
        mapAsString=''
        for key in params:
            mapAsString+=key+'='+params[key]
        return mapAsString
    def set_url(self,url):
        self.url=url
    def get_url(self):
        return self.url
    def add_http_header(self,key,value):
        self.req_headers.put(key,value)
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
        self.req_params.put(key,value)
    def get_http_request_params(self):
        return self.req_params
    def set_file(self,file_content):
        self.file=file_content

class APIConstants(object):
    '''
    This module holds the constants required for the client library
    '''
    ERROR="error"
    REQUEST_METHOD_GET="GET"
    REQUEST_METHOD_POST="POST"
    REQUEST_METHOD_PUT="PUT"
    REQUEST_METHOD_DELETE="DELETE"
    
    OAUTH_HEADER_PREFIX="Zoho-oauthtoken "
    AUTHORIZATION="Authorization"
    
    API_NAME="api_name"
    INVALID_ID_MSG = "The given id seems to be invalid."
    API_MAX_RECORDS_MSG = "Cannot process more than 100 records at a time."
    INVALID_DATA="INVALID_DATA"
    
    CODE_SUCCESS = "SUCCESS"
    
    STATUS_SUCCESS = "success"
    STATUS_ERROR = "error"
    
    LEADS = "Leads"
    ACCOUNTS = "Accounts"
    CONTACTS = "Contacts"
    DEALS = "Deals"
    QUOTES = "Quotes"
    SALESORDERS = "SalesOrders"
    INVOICES = "Invoices"
    PURCHASEORDERS = "PurchaseOrders"
    
    PER_PAGE = "per_page"
    PAGE = "page"
    COUNT = "count"
    MORE_RECORDS = "more_records"
    
    MESSAGE = "message"
    CODE = "code"
    STATUS = "status"
    DETAILS="details"
    
    DATA = "data"
    INFO = "info"
    FIELDS='fields'
    LAYOUTS='layouts'
    CUSTOM_VIEWS='custom_views'
    MODULES='modules'
    RELATED_LISTS='related_lists'
    ORG='org'
    ROLES='roles'
    PROFILES='profiles'
    USERS='users'
    
    RESPONSECODE_OK=200
    RESPONSECODE_CREATED=201
    RESPONSECODE_ACCEPTED=202
    RESPONSECODE_NO_CONTENT=204
    RESPONSECODE_MOVED_PERMANENTLY=301
    RESPONSECODE_MOVED_TEMPORARILY=302
    RESPONSECODE_NOT_MODIFIED=304
    RESPONSECODE_BAD_REQUEST=400
    RESPONSECODE_AUTHORIZATION_ERROR=401
    RESPONSECODE_FORBIDDEN=403
    RESPONSECODE_NOT_FOUND=404
    RESPONSECODE_METHOD_NOT_ALLOWED=405
    RESPONSECODE_REQUEST_ENTITY_TOO_LARGE=413
    RESPONSECODE_UNSUPPORTED_MEDIA_TYPE=415
    RESPONSECODE_TOO_MANY_REQUEST=429
    RESPONSECODE_INTERNAL_SERVER_ERROR=500
    RESPONSECODE_INVALID_INPUT=0
    
    DOWNLOAD_FILE_PATH="../../../../../../resources"
    
    USER_EMAIL_ID="user_email_id"
    CURRENT_USER_EMAIL="currentUserEmail"
    API_BASEURL="apiBaseUrl"
    API_VERSION="apiVersion"
    APPLICATION_LOGFILE_PATH="applicationLogFilePath" 
    ACTION="action"
    DUPLICATE_FIELD="duplicate_field"
    NO_CONTENT="No Content"
    FAULTY_RESPONSE_CODES=[RESPONSECODE_NO_CONTENT,RESPONSECODE_NOT_FOUND,RESPONSECODE_AUTHORIZATION_ERROR,RESPONSECODE_BAD_REQUEST,RESPONSECODE_FORBIDDEN,RESPONSECODE_INTERNAL_SERVER_ERROR,RESPONSECODE_METHOD_NOT_ALLOWED,RESPONSECODE_MOVED_PERMANENTLY,RESPONSECODE_MOVED_TEMPORARILY,RESPONSECODE_REQUEST_ENTITY_TOO_LARGE,RESPONSECODE_TOO_MANY_REQUEST,RESPONSECODE_UNSUPPORTED_MEDIA_TYPE]
    ATTACHMENT_URL="attachmentUrl"
    
    ACCESS_TOKEN_EXPIRY="X-ACCESSTOKEN-RESET";
    CURR_WINDOW_API_LIMIT="X-RATELIMIT-LIMIT";
    CURR_WINDOW_REMAINING_API_COUNT="X-RATELIMIT-REMAINING";
    CURR_WINDOW_RESET="X-RATELIMIT-RESET";
    API_COUNT_REMAINING_FOR_THE_DAY="X-RATELIMIT-DAY-REMAINING";
    API_LIMIT_FOR_THE_DAY="X-RATELIMIT-DAY-LIMIT"
    
class ZCRMConfigUtil(object):
    '''
    This class is to deal with configuration related things
    '''
    config_prop_dict={}
    @staticmethod
    def get_instance():
        return ZCRMConfigUtil()
    @staticmethod
    def initialize(isToInitializeOAuth,config_dict = None):
        if (config_dict is None):
            raise ZohoOAuthException("Configuration dictionary is mandatory to initialize RestClient")
        mandatory_keys = [ZohoOAuthConstants.CLIENT_ID,ZohoOAuthConstants.CLIENT_SECRET,ZohoOAuthConstants.REDIRECT_URL,APIConstants.CURRENT_USER_EMAIL]
        try:
            from .RestClient import ZCRMRestClient
        except ImportError:
            from RestClient import ZCRMRestClient
        for key in mandatory_keys:
            if(key not in config_dict):
                if(key != APIConstants.CURRENT_USER_EMAIL or ZCRMRestClient.get_instance().get_current_user_email_id() == None):
                    raise ZohoOAuthException(key+ ' is mandatory')
            elif(key in config_dict and (config_dict[key] is None or config_dict[key] == "" )):
                if (key != APIConstants.CURRENT_USER_EMAIL or ZCRMRestClient.get_instance().get_current_user_email_id() == None):
                    raise ZohoOAuthException(key+ ' value is missing')
        ZCRMConfigUtil.set_config_values(config_dict)
        if(isToInitializeOAuth):
            ZohoOAuth.initialize(config_dict)
    @staticmethod
    def get_api_base_url():
        return ZCRMConfigUtil.config_prop_dict["apiBaseUrl"]
    @staticmethod
    def get_api_version():
        return ZCRMConfigUtil.config_prop_dict["apiVersion"]
    @staticmethod
    def set_config_values(config_dict):
        config_keys = [APIConstants.CURRENT_USER_EMAIL,ZohoOAuthConstants.SANDBOX,APIConstants.API_BASEURL,APIConstants.API_VERSION,APIConstants.APPLICATION_LOGFILE_PATH]
        if(ZohoOAuthConstants.SANDBOX not in config_dict or config_dict[ZohoOAuthConstants.SANDBOX]==""):
            ZCRMConfigUtil.config_prop_dict[ZohoOAuthConstants.SANDBOX] = "false"
        if(APIConstants.API_BASEURL not in config_dict or config_dict[APIConstants.API_BASEURL]==""):
            ZCRMConfigUtil.config_prop_dict[APIConstants.API_BASEURL] = "www.zohoapis.com"
        if(APIConstants.API_VERSION not in config_dict or config_dict[APIConstants.API_VERSION]==""):
            ZCRMConfigUtil.config_prop_dict[APIConstants.API_VERSION] = "v2"
        for key in config_keys:
            if(key in config_dict and config_dict[key] !=""):
                ZCRMConfigUtil.config_prop_dict[key] = config_dict[key].strip()
    def get_access_token(self):
        try:
            from .RestClient import ZCRMRestClient
        except ImportError:
            from RestClient import ZCRMRestClient
        userEmail=ZCRMRestClient.get_instance().get_current_user_email_id()
        if(userEmail==None and (ZCRMConfigUtil.config_prop_dict['currentUserEmail']==None or ZCRMConfigUtil.config_prop_dict['currentUserEmail'].strip()=='')):
            raise ZCRMException('fetching current user email',400,'Current user should either be set in ZCRMRestClient or in configuration dictionary',APIConstants.STATUS_ERROR)
        elif(userEmail==None):
            userEmail=ZCRMConfigUtil.config_prop_dict['currentUserEmail']
        clientIns=ZohoOAuth.get_client_instance()
        return clientIns.get_access_token(userEmail)
        
class CommonUtil(object):
    '''
    This class is to provide utility methods
    '''
    @staticmethod
    def get_file_content_as_dictionary(filePointer) :
        dictionary={}
        for line in filePointer:
            line=line.rstrip()
            keyValue=line.split("=")
            if(not keyValue[0].startswith('#')):
                dictionary[keyValue[0].strip()]=keyValue[1].strip()
        filePointer.close()
        return dictionary
    
    @staticmethod
    def raise_exception(url,message,details,content=None):
        zcrm_exception=ZCRMException(url,APIConstants.RESPONSECODE_INVALID_INPUT,message,APIConstants.STATUS_ERROR,details,content)
        import logging
        try:
            from .CLException import Logger
        except ImportError:
            from CLException import Logger
        Logger.add_log(message,logging.ERROR,zcrm_exception)
        raise zcrm_exception
    
    @staticmethod
    def create_api_supported_input_json(input_json,api_key):
        if input_json is None:
            input_json=dict()
        inputJsonArr=list()
        inputJsonArr.append(input_json)
        reqBodyJson=dict()
        reqBodyJson[api_key]=inputJsonArr
        return reqBodyJson
