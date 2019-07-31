'''
Created on Aug 16, 2017

@author: sumanth-3058
'''
try:
    from .OAuthUtility import OAuthLogger,ZohoOAuthConstants,ZohoOAuthException,ZohoOAuthHTTPConnector,ZohoOAuthParams
    from .Persistence import ZohoOAuthPersistenceHandler,ZohoOAuthPersistenceFileHandler
except ImportError:
    from OAuthUtility import OAuthLogger,ZohoOAuthConstants,ZohoOAuthException,ZohoOAuthHTTPConnector,ZohoOAuthParams
    from Persistence import ZohoOAuthPersistenceHandler,ZohoOAuthPersistenceFileHandler
import logging
class ZohoOAuth(object):
    '''
    This class is to load oauth configurations and provide OAuth request URIs
    '''
    configProperties={}
    #iamURL='https://accounts.zoho.com'
    
    def __init__(self):
        '''
        Constructor
        '''
    @staticmethod
    def initialize(config_dict = None):
        try:
            ZohoOAuth.set_config_values(config_dict)
            if((ZohoOAuthConstants.TOKEN_PERSISTENCE_PATH not in ZohoOAuth.configProperties or ZohoOAuth.configProperties[ZohoOAuthConstants.TOKEN_PERSISTENCE_PATH] =="") and \
                    (ZohoOAuthConstants.CUSTOM_PERSISTENCE_HANDLER_PATH not in ZohoOAuth.configProperties or ZohoOAuth.configProperties[ZohoOAuthConstants.CUSTOM_PERSISTENCE_HANDLER_PATH] == "")):
                if(ZohoOAuthConstants.DATABASE_PORT not in ZohoOAuth.configProperties or ZohoOAuth.configProperties[ZohoOAuthConstants.DATABASE_PORT]==""):
                    ZohoOAuth.configProperties[ZohoOAuthConstants.DATABASE_PORT]="3306"
                if(ZohoOAuthConstants.DATABASE_USERNAME not in ZohoOAuth.configProperties or ZohoOAuth.configProperties[ZohoOAuthConstants.DATABASE_USERNAME]==""):
                    ZohoOAuth.configProperties[ZohoOAuthConstants.DATABASE_USERNAME]="root"
                if(ZohoOAuthConstants.DATABASE_PASSWORD not in ZohoOAuth.configProperties or ZohoOAuth.configProperties[ZohoOAuthConstants.DATABASE_PASSWORD]==""):
                    ZohoOAuth.configProperties[ZohoOAuthConstants.DATABASE_PASSWORD]=""
            oAuthParams=ZohoOAuthParams.get_instance(ZohoOAuth.configProperties[ZohoOAuthConstants.CLIENT_ID], ZohoOAuth.configProperties[ZohoOAuthConstants.CLIENT_SECRET], ZohoOAuth.configProperties[ZohoOAuthConstants.REDIRECT_URL])
            ZohoOAuthClient.get_instance(oAuthParams)
        except Exception as ex:
            OAuthLogger.add_log('Exception occured while reading oauth configurations',logging.ERROR,ex)
            raise ex
    
    @staticmethod
    def set_config_values(config_dict):
        config_keys = [ZohoOAuthConstants.CLIENT_ID, ZohoOAuthConstants.CLIENT_SECRET, ZohoOAuthConstants.REDIRECT_URL, ZohoOAuthConstants.ACCESS_TYPE
			, ZohoOAuthConstants.IAM_URL, ZohoOAuthConstants.TOKEN_PERSISTENCE_PATH, ZohoOAuthConstants.DATABASE_PORT
			, ZohoOAuthConstants.DATABASE_PASSWORD, ZohoOAuthConstants.DATABASE_USERNAME, ZohoOAuthConstants.CUSTOM_PERSISTENCE_HANDLER_PATH, ZohoOAuthConstants.CUSTOM_PERSISTENCE_HANDLER_CLASS]
        if(ZohoOAuthConstants.ACCESS_TYPE not in config_dict or config_dict[ZohoOAuthConstants.ACCESS_TYPE] is None):
            ZohoOAuth.configProperties[ZohoOAuthConstants.ACCESS_TYPE] = "offline"
        if(ZohoOAuthConstants.IAM_URL not in config_dict or config_dict[ZohoOAuthConstants.IAM_URL] == ""):
            ZohoOAuth.configProperties[ZohoOAuthConstants.IAM_URL] = "https://accounts.zoho.com"
        for key in config_keys:
            if(key in config_dict and config_dict[key] !=""):
                ZohoOAuth.configProperties[key] = config_dict[key].strip()
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
    def get_grant_url():
        return (ZohoOAuth.configProperties[ZohoOAuthConstants.IAM_URL]+"/oauth/v2/auth")
    @staticmethod
    def get_token_url():
        return (ZohoOAuth.configProperties[ZohoOAuthConstants.IAM_URL]+"/oauth/v2/token")
    @staticmethod
    def get_refresh_token_url():
        return (ZohoOAuth.configProperties[ZohoOAuthConstants.IAM_URL]+"/oauth/v2/token")
    @staticmethod
    def get_revoke_token_url():
        return (ZohoOAuth.configProperties[ZohoOAuthConstants.IAM_URL]+"/oauth/v2/token/revoke")
    @staticmethod
    def get_user_info_url():
        return (ZohoOAuth.configProperties[ZohoOAuthConstants.IAM_URL]+"/oauth/user/info")
    @staticmethod
    def get_client_instance():
        oauth_client_ins=ZohoOAuthClient.get_instance()
        if(oauth_client_ins is None):
            raise ZohoOAuthException('ZohoOAuth.initialize() must be called before this')
        return oauth_client_ins
    @staticmethod
    def get_persistence_instance():
        if((ZohoOAuthConstants.TOKEN_PERSISTENCE_PATH not in ZohoOAuth.configProperties or ZohoOAuth.configProperties[ZohoOAuthConstants.TOKEN_PERSISTENCE_PATH]=="") and \
                (ZohoOAuthConstants.CUSTOM_PERSISTENCE_HANDLER_PATH not in ZohoOAuth.configProperties or ZohoOAuth.configProperties[ZohoOAuthConstants.CUSTOM_PERSISTENCE_HANDLER_PATH] == "")):
            return ZohoOAuthPersistenceHandler()
        elif((ZohoOAuthConstants.TOKEN_PERSISTENCE_PATH in ZohoOAuth.configProperties) and ZohoOAuth.configProperties[ZohoOAuthConstants.TOKEN_PERSISTENCE_PATH] != ""):
            return ZohoOAuthPersistenceFileHandler()
        else:
            try:
                from sys import path
                import importlib
                custompersistence_handler = ZohoOAuth.configProperties[ZohoOAuthConstants.CUSTOM_PERSISTENCE_HANDLER_PATH]
                custompersistence_classname = ZohoOAuth.configProperties[ZohoOAuthConstants.CUSTOM_PERSISTENCE_HANDLER_CLASS]
                if custompersistence_classname == "":
                    raise ZohoOAuthException("Token Persistence Class must be given.")
                splitter = "/" if "/" in custompersistence_handler else "\\"
                custompersistence_directory = custompersistence_handler.strip(custompersistence_handler.split(splitter)[-1]).rstrip(splitter)
                path.append(custompersistence_directory)
                custompersistence_modulename = custompersistence_handler.split(splitter)[-1].rstrip(".py")
                try:
                    custompersistence_module = importlib.import_module(custompersistence_modulename)
                    custompersistence_class = getattr(custompersistence_module, custompersistence_modulename)
                    custompersistence_instance = custompersistence_class()
                    return custompersistence_instance
                except Exception as e:
                    raise e
            except Exception as ex:
                OAuthLogger.add_log("Exception occured while fetching instance for Custom DB Persistence", logging.ERROR, ex)
                raise ex

class ZohoOAuthClient(object):
    '''
    This class is to generate oauth related tokens
    '''
    oAuthParams=None
    oAuthClientIns=None

    def __init__(self, oauthParams):
        '''
        Constructor
        '''
        ZohoOAuthClient.oAuthParams=oauthParams
        
    @staticmethod
    def get_instance(param=None):
        if(param!=None and ZohoOAuthClient.oAuthClientIns==None):
            ZohoOAuthClient.oAuthClientIns=ZohoOAuthClient(param)
        return ZohoOAuthClient.oAuthClientIns
            
    def get_access_token(self,userEmail):
        try:
            handler=ZohoOAuth.get_persistence_instance()
            oAuthTokens=handler.get_oauthtokens(userEmail)
            try:
                return oAuthTokens.get_access_token()
            except Exception as e:
                OAuthLogger.add_log("Access token expired hence refreshing",logging.INFO,e)
                oAuthTokens=self.refresh_access_token(oAuthTokens.refreshToken,userEmail)
                return oAuthTokens.accessToken
        except Exception as ex:
            OAuthLogger.add_log("Exception occured while fetching oauthtoken from db",logging.ERROR,ex)
            raise ex
    def generate_access_token_from_refresh_token(self,refreshToken,userEmail):
        self.refresh_access_token(refreshToken, userEmail)
    def refresh_access_token(self,refreshToken,userEmail):
        if(refreshToken==None):
            raise ZohoOAuthException("Refresh token not provided!")
        try:
            connector=self.get_connector(ZohoOAuth.get_refresh_token_url())
            connector.add_http_request_params(ZohoOAuthConstants.GRANT_TYPE,ZohoOAuthConstants.GRANT_TYPE_REFRESH)
            connector.add_http_request_params(ZohoOAuthConstants.REFRESH_TOKEN,refreshToken)
            connector.set_http_request_method(ZohoOAuthConstants.REQUEST_METHOD_POST)
            response=connector.trigger_request()
            responseJSON=response.json()
            if(ZohoOAuthConstants.ACCESS_TOKEN in responseJSON):
                oAuthTokens=self.get_tokens_from_json(responseJSON)
                oAuthTokens.set_user_email(userEmail)
                oAuthTokens.refreshToken=refreshToken
                ZohoOAuth.get_persistence_instance().save_oauthtokens(oAuthTokens)
                return oAuthTokens
            
        except ZohoOAuthException as ex:
            OAuthLogger.add_log("Exception occured while refreshing oauthtoken",logging.ERROR,ex)
            raise ex
            
    def generate_access_token(self,grantToken):
        if(grantToken==None):
            raise ZohoOAuthException("Grant token not provided!")
        try:
            connector=self.get_connector(ZohoOAuth.get_token_url())
            connector.add_http_request_params(ZohoOAuthConstants.GRANT_TYPE,ZohoOAuthConstants.GRANT_TYPE_AUTH_CODE)
            connector.add_http_request_params(ZohoOAuthConstants.CODE,grantToken)
            connector.set_http_request_method(ZohoOAuthConstants.REQUEST_METHOD_POST)
            response=connector.trigger_request()
            responseJSON=response.json()
            if(ZohoOAuthConstants.ACCESS_TOKEN in responseJSON):
                oAuthTokens=self.get_tokens_from_json(responseJSON)
                oAuthTokens.set_user_email(self.get_user_email_from_iam(oAuthTokens.accessToken))
                ZohoOAuth.get_persistence_instance().save_oauthtokens(oAuthTokens)
                return oAuthTokens
            else:
                raise ZohoOAuthException("Exception occured while fetching accesstoken from Grant Token;Response is:"+str(responseJSON))
            
        except ZohoOAuthException as ex:
            OAuthLogger.add_log("Exception occured while generating access token",logging.ERROR,ex)
            raise ex
    
    def get_tokens_from_json(self,responseJson):
        expiresIn = responseJson[ZohoOAuthConstants.EXPIRES_IN]
        expiresIn=expiresIn+(ZohoOAuthTokens.get_current_time_in_millis())
        accessToken=responseJson[ZohoOAuthConstants.ACCESS_TOKEN]
        refreshToken=None
        if(ZohoOAuthConstants.REFRESH_TOKEN in responseJson):
            refreshToken=responseJson[ZohoOAuthConstants.REFRESH_TOKEN]
        oAuthTokens = ZohoOAuthTokens(refreshToken,accessToken,expiresIn)
        return oAuthTokens;
    def get_connector(self,url):
        connector=ZohoOAuthHTTPConnector.get_instance(url,{})
        connector.add_http_request_params(ZohoOAuthConstants.CLIENT_ID, ZohoOAuthClient.oAuthParams.clientID)
        connector.add_http_request_params(ZohoOAuthConstants.CLIENT_SECRET, ZohoOAuthClient.oAuthParams.clientSecret)
        connector.add_http_request_params(ZohoOAuthConstants.REDIRECT_URL, ZohoOAuthClient.oAuthParams.redirectUri)
        return connector
    def get_user_email_from_iam(self,accessToken):
        header={ZohoOAuthConstants.AUTHORIZATION:(ZohoOAuthConstants.OAUTH_HEADER_PREFIX+accessToken)}
        connector=ZohoOAuthHTTPConnector.get_instance(ZohoOAuth.get_user_info_url(),None,header,None,ZohoOAuthConstants.REQUEST_METHOD_GET)
        response=connector.trigger_request()
        return response.json()['Email']

class ZohoOAuthTokens(object):
    '''
    This class is to encapsulate the OAuth tokens
    '''
    def __init__(self, refresh_token,access_token,expiry_time,user_email=None):
        '''
        Constructor
        '''
        self.refreshToken=refresh_token
        self.accessToken=access_token
        self.expiryTime=expiry_time
        self.userEmail=user_email
        
    def get_access_token(self):
        if((self.expiryTime-self.get_current_time_in_millis())>5000):
            return self.accessToken
        else:
            raise ZohoOAuthException("Access token got expired!")
    @staticmethod
    def get_current_time_in_millis():
        import time
        return int(round(time.time() * 1000))
    def set_user_email(self,userEmail):
        self.userEmail=userEmail

from abc import ABC, abstractmethod
class AbstractZohoOAuthPersistence(ABC):
    @abstractmethod
    def get_oauthtokens(self,user_email):
        pass

    @abstractmethod
    def save_oauthtokens(self, oauthtokens):
        pass

    @abstractmethod
    def delete_oauthtokens(self, user_email):
        pass