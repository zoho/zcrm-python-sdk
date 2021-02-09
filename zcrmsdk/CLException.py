'''
Created on Aug 16, 2017

@author: sumanth-3058
'''

class ZCRMException(Exception):
    '''
    This is the custom exception class for handling for Client Library exceptions 
    '''
    message = 'Error occurred for {url}. Error Code: {code} Response error_content: {error_content}. Error Details::{error_details}'

    def __init__(self, url, status_code, err_message,exception_code='error',details=None,content=None):
        self.url = url
        self.status_code = status_code
        self.error_content = content
        self.error_message=err_message
        self.error_code=exception_code
        self.error_details=details
        Exception.__init__(self,status_code)

    def __str__(self):
        return self.message.format(url=self.url,code=self.status_code,error_content=self.error_content,error_details=self.error_details)

import logging
logger=logging.getLogger('Client_Library')    
class Logger(object):
    '''
    This class is to log the exceptions onto console
    '''
    @staticmethod
    def add_log(message,level=None,exception=None):
        logger.setLevel(logging.DEBUG)
        console_handler = logging.StreamHandler()
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        try:
            from .Utility import ZCRMConfigUtil
        except ImportError:
            from Utility import ZCRMConfigUtil
        log_path=ZCRMConfigUtil.config_prop_dict['applicationLogFilePath']
        if log_path is not None and log_path.strip()!="":
            import os
            log_path=os.path.join(log_path,'client_library.log')
            file_handler=logging.FileHandler(log_path)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        # add the handlers to the logger
        logger.addHandler(console_handler)
        
        if(exception!=None):
            message+='; Exception Message::'+exception.__str__()
        if(level==logging.ERROR):
            logger.error(message)
        elif(level==logging.INFO or level==logging.DEBUG):
            logger.debug(message)
        elif(level==logging.WARNING):
            logger.warning(message)
