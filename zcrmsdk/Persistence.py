'''
Created on Aug 16, 2017

@author: sumanth-3058
'''
from .OAuthUtility import OAuthLogger
import mysql.connector


class ZohoOAuthPersistenceHandler(object):
    '''
    This class deals with persistance of oauth related tokens
    '''
    def saveOAuthTokens(self,oAuthTokens):
        try:
            self.deleteOAuthTokens(oAuthTokens.userEmail)
            connection=self.getDBConnection()
            cursor=connection.cursor()
            #sqlQuery="INSERT INTO oauthtokens(useridentifier,accesstoken,refreshtoken,expirytime) VALUES('"+oAuthTokens.userEmail+"','"+oAuthTokens.accessToken+"','"+oAuthTokens.refreshToken+"',"+oAuthTokens.expiryTime+")";
            sqlQuery="INSERT INTO oauthtokens(useridentifier,accesstoken,refreshtoken,expirytime) VALUES(%s,%s,%s,%s)";
            data=(oAuthTokens.userEmail,oAuthTokens.accessToken,oAuthTokens.refreshToken,oAuthTokens.expiryTime)
            cursor.execute(sqlQuery,data)
            connection.commit()
        except Exception as ex:
            import logging
            OAuthLogger.add_log("Exception occured while saving oauthtokens into DB ",logging.ERROR,ex)
            raise ex
        finally:
            cursor.close()
            connection.close()    
        
    def getOAuthTokens(self,userEmail):
        try:
            connection=self.getDBConnection()
            cursor=connection.cursor()
            sqlQuery="SELECT useridentifier,accesstoken,refreshtoken,expirytime FROM oauthtokens where useridentifier='"+userEmail+"'"
            cursor.execute(sqlQuery)
            row_count=0
            for(useridentifier,accesstoken,refreshtoken,expirytime) in cursor:
                row_count=row_count+1
                from .OAuthClient import ZohoOAuthTokens
                return ZohoOAuthTokens(refreshtoken,accesstoken,expirytime,useridentifier)
            if row_count==0:
                raise Exception('No rows found for the given user')
        except Exception as ex:
            import logging
            OAuthLogger.add_log("Exception occured while fetching oauthtokens from DB ",logging.ERROR,ex)
            raise ex
        finally:
            cursor.close()
            connection.close()
    def deleteOAuthTokens(self,userEmail):
        try:
            connection=self.getDBConnection()
            cursor=connection.cursor()
            sqlQuery="DELETE FROM oauthtokens where useridentifier=%s"
            cursor.execute(sqlQuery,(userEmail,))
            connection.commit()
        except Exception as ex:
            import logging
            OAuthLogger.add_log("Exception occured while deleting oauthtokens from DB ",logging.ERROR,ex)
            raise ex
        finally:
            cursor.close()
            connection.close()
            
    def getDBConnection(self):
        connection=mysql.connector.connect(user='root', password='',host='127.0.0.1',database='zohooauth')
        return connection
    
    
class ZohoOAuthPersistenceFileHandler(object):
    '''
    This class deals with persistance of oauth related tokens in File
    '''
    def saveOAuthTokens(self,oAuthTokens):
        try:
            self.deleteOAuthTokens(oAuthTokens.userEmail)
            from .OAuthClient import ZohoOAuth
            from .OAuthUtility import ZohoOAuthConstants
            import os
            os.chdir(ZohoOAuth.configProperties[ZohoOAuthConstants.TOKEN_PERSISTENCE_PATH])
            import pickle
            if os.path.isfile(ZohoOAuthConstants.PERSISTENCE_FILE_NAME):
                with open(ZohoOAuthConstants.PERSISTENCE_FILE_NAME, 'ab') as fp:
                    pickle.dump(oAuthTokens, fp, pickle.HIGHEST_PROTOCOL)
            else:
                with open(ZohoOAuthConstants.PERSISTENCE_FILE_NAME, 'wb') as fp:
                    pickle.dump(oAuthTokens, fp, pickle.HIGHEST_PROTOCOL)
            
        except Exception as ex:
            import logging
            OAuthLogger.add_log("Exception occured while saving oauthtokens into File ",logging.ERROR,ex)
            raise ex
        
    def getOAuthTokens(self,userEmail):
        try:
            import pickle
            from .OAuthClient import ZohoOAuth,ZohoOAuthTokens
            from .OAuthUtility import ZohoOAuthConstants
            import os
            os.chdir(ZohoOAuth.configProperties[ZohoOAuthConstants.TOKEN_PERSISTENCE_PATH])
            responseObj=ZohoOAuthTokens(None,None,None,None)
            if not os.path.isfile(ZohoOAuthConstants.PERSISTENCE_FILE_NAME):
                return responseObj
            with open(ZohoOAuthConstants.PERSISTENCE_FILE_NAME, 'rb') as fp:
                while True:
                    try:
                        oAuthObj=pickle.load(fp)
                        if(userEmail==oAuthObj.userEmail):
                            responseObj=oAuthObj
                            break
                    except EOFError:
                        break
            return responseObj
        except Exception as ex:
            import logging
            OAuthLogger.add_log("Exception occured while fetching oauthtokens from File ",logging.ERROR,ex)
            raise ex
            
    def deleteOAuthTokens(self,userEmail):
        try:
            import pickle
            from .OAuthClient import ZohoOAuth
            from .OAuthUtility import ZohoOAuthConstants
            import os
            os.chdir(ZohoOAuth.configProperties[ZohoOAuthConstants.TOKEN_PERSISTENCE_PATH])
            if not os.path.isfile(ZohoOAuthConstants.PERSISTENCE_FILE_NAME):
                return
            objectsToPreserve=[]
            with open(ZohoOAuthConstants.PERSISTENCE_FILE_NAME, 'rb') as fp:
                while True:
                    try:
                        oAuthObj=pickle.load(fp)
                        if(userEmail!=oAuthObj.userEmail):
                            objectsToPreserve.append(oAuthObj)
                    except EOFError:
                        break
            with open(ZohoOAuthConstants.PERSISTENCE_FILE_NAME, 'wb') as fp:
                for eachObj in objectsToPreserve:
                    pickle.dump(eachObj, fp, pickle.HIGHEST_PROTOCOL)
            
        except Exception as ex:
            import logging
            OAuthLogger.add_log("Exception occured while deleting oauthtokens from File ",logging.ERROR,ex)
            raise ex
