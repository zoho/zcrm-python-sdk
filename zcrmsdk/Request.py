'''
Created on Jul 28, 2017

@author: sumanth-3058
'''
try:
    from .Utility import ZCRMConfigUtil, APIConstants,HTTPConnector
    from .CLException import ZCRMException
    from .Response import APIResponse, BulkAPIResponse,FileAPIResponse
except ImportError:
    from Utility import ZCRMConfigUtil, APIConstants,HTTPConnector
    from CLException import ZCRMException
    from Response import APIResponse, BulkAPIResponse,FileAPIResponse
class APIRequest(object):
    '''
    This class is to wrap the API request related stuff like request params,headers,body,..etc
    '''
    def __init__(self, api_handler_ins):
        '''
        Constructor
        '''
        self.construct_api_url()
        self.url+=api_handler_ins.request_url_path
        if(not self.url.startswith("http")):
            self.url="https://"+self.url
        self.request_body=api_handler_ins.request_body
        self.request_headers=api_handler_ins.request_headers
        self.request_params=api_handler_ins.request_params
        self.request_method=api_handler_ins.request_method
        self.request_api_key=api_handler_ins.request_api_key
    
    def construct_api_url(self):
        hit_sand_box=ZCRMConfigUtil.config_prop_dict['sandbox']
        base_url=ZCRMConfigUtil.get_api_base_url().replace('www','sandbox') if hit_sand_box.lower()=='true' else ZCRMConfigUtil.get_api_base_url()
        self.url=base_url+"/crm/"+ZCRMConfigUtil.get_api_version()+"/"
    
    def authenticate_request(self):
        accessToken=ZCRMConfigUtil.get_instance().get_access_token()
        if(self.request_headers==None):
            self.request_headers={APIConstants.AUTHORIZATION:APIConstants.OAUTH_HEADER_PREFIX+accessToken}
        else:
            self.request_headers[APIConstants.AUTHORIZATION]=APIConstants.OAUTH_HEADER_PREFIX+accessToken
        self.request_headers['User-Agent']='ZohoCRM Python SDK'
    def get_api_response(self):
        try:
            self.authenticate_request()
            connector=HTTPConnector.get_instance(self.url, self.request_params, self.request_headers, self.request_body, self.request_method, self.request_api_key, False)
            response=connector.trigger_request()
            return APIResponse(response,response.status_code,self.url,self.request_api_key)
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            import traceback
            CommonUtil.raise_exception(self.url,ex.message,traceback.format_stack())
        
    def get_bulk_api_response(self):
        try:
            self.authenticate_request()
            connector=HTTPConnector.get_instance(self.url, self.request_params, self.request_headers, self.request_body, self.request_method, self.request_api_key, True)
            response=connector.trigger_request()
            return BulkAPIResponse(response,response.status_code,self.url,self.request_api_key)
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            import traceback
            CommonUtil.raise_exception(self.url,ex.message,traceback.format_stack())
        
    def upload_attachment(self,file_path,upload_file=True):
        try:
            self.authenticate_request()
            if upload_file:
                files = {'file': open(file_path,'rb')}
            else:
                files=self.request_body
            connector=HTTPConnector.get_instance(self.url, self.request_params, self.request_headers, self.request_body, self.request_method, self.request_api_key, True)
            connector.set_file(files)
            response=connector.trigger_request()
            return APIResponse(response,response.status_code,self.url,self.request_api_key)
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            import traceback
            CommonUtil.raise_exception(self.url,ex.message,traceback.format_stack())
    def upload_link_as_attachment(self):
        try:
            self.authenticate_request()
            files = {'file': ''}
            connector=HTTPConnector.get_instance(self.url, self.request_params, self.request_headers, self.request_body, self.request_method, self.request_api_key, True)
            connector.set_file(files)
            response=connector.trigger_request()
            return APIResponse(response,response.status_code,self.url,self.request_api_key)
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            import traceback
            CommonUtil.raise_exception(self.url,ex.message,traceback.format_stack())
      
    def download_attachment(self):
        try:
            self.authenticate_request()
            connector=HTTPConnector.get_instance(self.url, self.request_params, self.request_headers, self.request_body, self.request_method, self.request_api_key, True)
            response=connector.trigger_request()
            if response.status_code==APIConstants.RESPONSECODE_OK:
                file_res= FileAPIResponse(response,response.status_code,self.url)
                file_res.status=APIConstants.STATUS_SUCCESS
                content_disp=response.headers['Content-Disposition']
                start_index=content_disp.rindex("'")
                file_res.file_name=content_disp[start_index+1:]
                file_res.response_headers=response.headers
                return file_res
            elif(response.status_code==APIConstants.RESPONSECODE_NO_CONTENT):
                errorMsg=APIConstants.INVALID_DATA+"-"+APIConstants.INVALID_ID_MSG
                exception=ZCRMException(self.url,response.status_code,errorMsg,APIConstants.NO_CONTENT,None,errorMsg)
                raise exception
            else:
                responseJSON=response.json()
                exception=ZCRMException(self.url,response.status_code,responseJSON[APIConstants.MESSAGE],responseJSON[APIConstants.CODE],responseJSON[APIConstants.DETAILS],responseJSON[APIConstants.MESSAGE])
                raise exception
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            import traceback
            CommonUtil.raise_exception(self.url,ex.message,traceback.format_stack())  