'''
Created on Aug 16, 2017

@author: sumanth-3058
'''
try:
    from .OAuthUtility import OAuthLogger
except ImportError:
    from OAuthUtility import OAuthLogger
#import MySQLdb
#import mysql.connector
class ZohoOAuthPersistenceHandler(object):
    '''
    This class deals with persistance of oauth related tokens
    '''
    def save_oauthtokens(self,oAuthTokens):
        try:
            self.delete_oauthtokens(oAuthTokens.userEmail)
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
        
    def get_oauthtokens(self,userEmail):
        try:
            connection=self.getDBConnection()
            cursor=connection.cursor()
            sqlQuery="SELECT useridentifier,accesstoken,refreshtoken,expirytime FROM oauthtokens where useridentifier='"+userEmail+"'"
            cursor.execute(sqlQuery)
            row_count=0
            for(useridentifier,accesstoken,refreshtoken,expirytime) in cursor:
                row_count=row_count+1
                try:
                    from .OAuthClient import ZohoOAuthTokens
                except ImportError:
                    from OAuthClient import ZohoOAuthTokens
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
    def delete_oauthtokens(self,userEmail):
        try:
            connection=self.getDBConnection()
            cursor=connection.cursor()
            #sqlQuery="DELETE FROM oauthtokens where useridentifier='"+userEmail+"'"
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
        try:
            from .OAuthClient import ZohoOAuth
            from .OAuthUtility import ZohoOAuthConstants
        except ImportError:
            from OAuthClient import ZohoOAuth
            from OAuthUtility import ZohoOAuthConstants
        import mysql.connector
        connection=mysql.connector.connect(user=ZohoOAuth.configProperties[ZohoOAuthConstants.DATABASE_USERNAME], password=ZohoOAuth.configProperties[ZohoOAuthConstants.DATABASE_PASSWORD],port=ZohoOAuth.configProperties[ZohoOAuthConstants.DATABASE_PORT],database='zohooauth')
        return connection
        #connection=MySQLdb.connect(host="localhost",user="root",passwd="",db="zohooauth")
        #return connection
class ZohoOAuthPersistenceFileHandler(object):
    '''
    This class deals with persistance of oauth related tokens in File
    '''
    def save_oauthtokens(self,oAuthTokens):
        try:
            self.delete_oauthtokens(oAuthTokens.userEmail)
            try:
                from .OAuthClient import ZohoOAuth
                from .OAuthUtility import ZohoOAuthConstants
            except ImportError:
                from OAuthClient import ZohoOAuth
                from OAuthUtility import ZohoOAuthConstants
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
        
    def get_oauthtokens(self,userEmail):
        try:
            import pickle
            try:
                from .OAuthClient import ZohoOAuth,ZohoOAuthTokens
                from .OAuthUtility import ZohoOAuthConstants
            except ImportError:
                from OAuthClient import ZohoOAuth,ZohoOAuthTokens
                from OAuthUtility import ZohoOAuthConstants
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
            
    def delete_oauthtokens(self,userEmail):
        try:
            import pickle
            try:
                from .OAuthClient import ZohoOAuth
                from .OAuthUtility import ZohoOAuthConstants
            except ImportError:
                from OAuthClient import ZohoOAuth
                from OAuthUtility import ZohoOAuthConstants
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
