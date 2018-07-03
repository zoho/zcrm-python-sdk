'''
Created on Aug 1, 2017

@author: sumanth-3058
'''
try:
    from .CLException import ZCRMException
    from .Utility import APIConstants
except ImportError:
    from CLException import ZCRMException
    from Utility import APIConstants

class CommonAPIResponse(object):
    def __init__(self,response,status_code,url,apiKey=None):
        '''
        Constructor
        '''
        self.response_json=None
        self.response_headers=None
        self.response=response
        self.status_code=status_code
        self.api_key=apiKey
        self.url=url
        self.data=None
        self.status=None
        self.code=None
        self.message=None
        self.details=None
        self.set_response_json()
        self.process_response()
    def set_response_json(self):
        if(self.status_code!=APIConstants.RESPONSECODE_NO_CONTENT):
            self.response_json=self.response.json()
        self.response_headers=self.response.headers
    def process_response(self):
        if(self.status_code in APIConstants.FAULTY_RESPONSE_CODES):
            self.handle_faulty_responses()
        else:
            self.process_response_data()
    
    def handle_faulty_responses(self):
        return
    def process_response_data(self):
        return
    def get_api_limit_for_current_window(self):
        return self.response_headers[APIConstants.CURR_WINDOW_API_LIMIT]
    def get_remaining_api_count_for_current_window(self):
        return self.response_headers[APIConstants.CURR_WINDOW_REMAINING_API_COUNT]
    def get_expiry_time_of_accesstoken(self):
        return self.response_headers[APIConstants.ACCESS_TOKEN_EXPIRY]
    def get_current_window_reset_time_in_millis(self):
        return self.response_headers[APIConstants.CURR_WINDOW_RESET]
    def get_remaining_api_count_for_the_day(self):
        if APIConstants.API_COUNT_REMAINING_FOR_THE_DAY in self.response_headers:
            return self.response_headers[APIConstants.API_COUNT_REMAINING_FOR_THE_DAY]
        else:
            return None
    def get_api_limit_for_the_day(self):
        if APIConstants.API_LIMIT_FOR_THE_DAY in self.response_headers:
            return self.response_headers[APIConstants.API_LIMIT_FOR_THE_DAY]
        else:
            return None
    
class APIResponse(CommonAPIResponse):
    '''
    classdocs
    '''
    def __init__(self, response,status_code,url,apiKey):
        '''
        Constructor
        '''
        super(APIResponse,self).__init__(response,status_code,url,apiKey)
    def handle_faulty_responses(self):
        if(self.status_code==APIConstants.RESPONSECODE_NO_CONTENT):
            errorMsg=APIConstants.INVALID_DATA+"-"+APIConstants.INVALID_ID_MSG
            exception=ZCRMException(self.url,self.status_code,errorMsg,APIConstants.NO_CONTENT,None,errorMsg)
            raise exception
        else:
            responseJSON=self.response_json
            exception=ZCRMException(self.url,self.status_code,responseJSON[APIConstants.MESSAGE],responseJSON[APIConstants.CODE],responseJSON[APIConstants.DETAILS],responseJSON[APIConstants.MESSAGE])
            raise exception
    def process_response_data(self):
        respJson=self.response_json
        if(self.api_key in respJson):
            respJson=self.response_json[self.api_key]
            if(isinstance(respJson, list)):
                respJson=respJson[0]
        if(APIConstants.STATUS in respJson and (respJson[APIConstants.STATUS]==APIConstants.STATUS_ERROR)):
            exception=ZCRMException(self.url,self.status_code,respJson[APIConstants.MESSAGE],respJson[APIConstants.CODE],respJson[APIConstants.DETAILS],respJson[APIConstants.STATUS])
            raise exception
        elif(APIConstants.STATUS in respJson and (respJson[APIConstants.STATUS]==APIConstants.STATUS_SUCCESS)):
            self.status=respJson[APIConstants.STATUS]
            self.code=respJson[APIConstants.CODE]
            self.message=respJson[APIConstants.MESSAGE]
            self.details=respJson[APIConstants.DETAILS]
        
class BulkAPIResponse(CommonAPIResponse):
    '''
    This class is to store the Bulk APIs responses
    '''
    def __init__(self, response,status_code,url,apiKey):
        '''
        Constructor
        '''
        self.bulk_entity_response=None
        self.info=None
        super(BulkAPIResponse,self).__init__(response,status_code,url,apiKey)
        self.set_info()
        
    def handle_faulty_responses(self):
        if(self.status_code==APIConstants.RESPONSECODE_NO_CONTENT):
            errorMsg=APIConstants.INVALID_DATA+"-"+APIConstants.INVALID_ID_MSG
            exception=ZCRMException(self.url,self.status_code,errorMsg,APIConstants.NO_CONTENT,None,errorMsg)
            raise exception
        else:
            responseJSON=self.response_json
            exception=ZCRMException(self.url,self.status_code,responseJSON['message'],responseJSON['code'],responseJSON['details'],responseJSON['message'])
            raise exception
    def process_response_data(self):
        if(APIConstants.DATA in self.response_json):
            dataList=self.response_json[APIConstants.DATA]
            self.bulk_entity_response=[]
            for eachRecord in dataList:
                if(APIConstants.STATUS in eachRecord):
                    self.bulk_entity_response.append(EntityResponse(eachRecord))
                    
    def set_info(self):
        if APIConstants.INFO in self.response_json:
            self.info=ResponseInfo(self.response_json[APIConstants.INFO])
            
class EntityResponse(object):
    '''
    This class is to store each entity response of the Bulk APIs response
    '''
    def __init__(self,entityResponse):
        '''
        Constructor
        '''
        self.response_json=entityResponse
        self.code=entityResponse[APIConstants.CODE]
        self.message=entityResponse[APIConstants.MESSAGE]
        self.status=entityResponse[APIConstants.STATUS]
        self.details=None
        self.data=None
        self.upsert_action=None
        self.upsert_duplicate_field=None
        if(APIConstants.DETAILS in entityResponse):
            self.details=entityResponse[APIConstants.DETAILS]
        if(APIConstants.ACTION in entityResponse):
            self.upsert_action=entityResponse[APIConstants.ACTION]
        if(APIConstants.DUPLICATE_FIELD in entityResponse):
            self.upsert_duplicate_field=entityResponse[APIConstants.DUPLICATE_FIELD]
    @staticmethod
    def get_instance(self,entityResponse):
        return EntityResponse(entityResponse)
    
class FileAPIResponse(object):
    
    def __init__(self,response,status_code,url):
        self.response=response
        self.status_code=status_code
        self.url=url
        self.file_name=None
        self.response_headers=None
        self.status=None
        self.code=None
        self.message=None
        self.details=None
        
    def get_response_stream(self):
        return self.response
    
class ResponseInfo(object):
    
    def __init__(self,response_info_json):
        self.is_more_records=bool(response_info_json['more_records'])
        self.page=int(response_info_json['page'])
        self.per_page=int(response_info_json['per_page'])
        self.count=int(response_info_json['count'])
    
        