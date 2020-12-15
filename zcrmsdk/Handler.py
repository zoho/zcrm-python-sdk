'''
Created on Aug 16, 2017

@author: sumanth-3058
'''
import traceback
try:
    from .CLException import ZCRMException
    from .Utility import APIConstants
    from .Request import APIRequest
except ImportError:
    from CLException import ZCRMException
    from Utility import APIConstants
    from Request import APIRequest
from array import array
from decimal import Decimal

class APIHandler(object):
    '''
    This class is to wrap all the details required to make an api call(i.e. REQUEST_METHOD,REQUEST_URL,REQUEST_BODY,...etc)
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.request_url_path=None
        self.request_body=None
        self.request_headers=None
        self.request_params=None
        self.request_method=None
        self.request_api_key=None
    def add_param(self,key,value):
        if self.request_params is None:
            self.request_params=dict()
        self.request_params[key]=value
    def add_header(self,key,value):
        if self.request_headers is None:
            self.request_headers=dict()
        self.request_headers[key]=value

class EntityAPIHandler(APIHandler):
    '''
    This class is to deal with all the entity single records
    '''
    def __init__(self,zcrmRecord):
        self.zcrmrecord=zcrmRecord
        
    @staticmethod
    def get_instance(zcrm_record):
        return EntityAPIHandler(zcrm_record)
    
    def get_record(self):
        try:
            handler_ins=APIHandler()
            handler_ins.request_url_path=self.zcrmrecord.module_api_name+"/"+str(self.zcrmrecord.entity_id)
            handler_ins.request_method=APIConstants.REQUEST_METHOD_GET
            handler_ins.request_api_key=APIConstants.DATA
            apiResponse=APIRequest(handler_ins).get_api_response()
            self.set_record_properties(apiResponse.response_json[APIConstants.DATA][0])
            apiResponse.data=self.zcrmrecord
            return apiResponse
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())
    def create_record(self, trigger, process, lar_id):
        try:
            handler_ins=APIHandler()
            handler_ins.request_url_path=self.zcrmrecord.module_api_name
            handler_ins.request_method=APIConstants.REQUEST_METHOD_POST
            handler_ins.request_api_key=APIConstants.DATA
            input_json=self.get_zcrmrecord_as_json()
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            request_json = CommonUtil.create_api_supported_input_json(input_json, APIConstants.DATA)
            if trigger is not None:
                request_json[APIConstants.TRIGGER] = trigger
            if process is not None:
                request_json[APIConstants.PROCESS] = process
            if lar_id is not None:
                request_json[APIConstants.LAR_ID] = lar_id
            handler_ins.request_body = request_json
            apiResponse=APIRequest(handler_ins).get_api_response()
            reponseDetails=apiResponse.response_json[APIConstants.DATA][0]['details']
            self.zcrmrecord.entity_id=reponseDetails['id']
            self.zcrmrecord.created_time=reponseDetails['Created_Time']
            createdBy=reponseDetails['Created_By']
            try:
                from .Operations import ZCRMUser
            except ImportError:
                from Operations import ZCRMUser
            self.zcrmrecord.created_by=ZCRMUser.get_instance(createdBy['id'],createdBy['name'])
            apiResponse.data=self.zcrmrecord
            return apiResponse
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())
        
    def update_record(self, trigger, process):
        try:
            handler_ins=APIHandler()
            handler_ins.request_url_path=self.zcrmrecord.module_api_name+"/"+str(self.zcrmrecord.entity_id)
            handler_ins.request_method=APIConstants.REQUEST_METHOD_PUT
            handler_ins.request_api_key=APIConstants.DATA
            input_json=self.get_zcrmrecord_as_json()
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            request_json = CommonUtil.create_api_supported_input_json(input_json, APIConstants.DATA)
            if trigger is not None:
                request_json[APIConstants.TRIGGER] = trigger
            if process is not None:
                request_json[APIConstants.PROCESS] = process
            handler_ins.request_body = request_json
            api_response=APIRequest(handler_ins).get_api_response()
            reponseDetails=api_response.response_json[APIConstants.DATA][0]['details']
            self.zcrmrecord.entity_id=reponseDetails['id']
            self.zcrmrecord.created_time=reponseDetails['Created_Time']
            self.zcrmrecord.modified_time=reponseDetails['Modified_Time']
            createdBy=reponseDetails['Created_By']
            try:
                from .Operations import ZCRMUser
            except ImportError:
                from Operations import ZCRMUser
            self.zcrmrecord.created_by=ZCRMUser.get_instance(createdBy['id'],createdBy['name'])
            modifiedBy=reponseDetails['Modified_By']
            self.zcrmrecord.modified_by=ZCRMUser.get_instance(modifiedBy['id'],modifiedBy['name'])
            api_response.data=self.zcrmrecord
            return api_response
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())
        
    def delete_record(self):
        try:
            handler_ins=APIHandler()
            handler_ins.request_url_path=self.zcrmrecord.module_api_name+"/"+str(self.zcrmrecord.entity_id)
            handler_ins.request_method=APIConstants.REQUEST_METHOD_DELETE
            handler_ins.request_api_key=APIConstants.DATA
            api_response=APIRequest(handler_ins).get_api_response()
            return api_response
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())
    
    def convert_record(self,potential_record,assign_to_user):
        try:
            handler_ins=APIHandler()
            handler_ins.request_url_path=self.zcrmrecord.module_api_name+"/"+str(self.zcrmrecord.entity_id)+"/actions/convert"
            handler_ins.request_method=APIConstants.REQUEST_METHOD_POST
            handler_ins.request_api_key=APIConstants.DATA
            input_json=dict()
            if assign_to_user is not None:
                input_json['assign_to']=assign_to_user.id
            if potential_record is not None:
                input_json['Deals']=self.get_instance(potential_record).get_zcrmrecord_as_json()
            if(assign_to_user is not None or potential_record is not None):
                inputJsonArr=list()
                inputJsonArr.append(input_json)
                reqBodyJson=dict()
                reqBodyJson[APIConstants.DATA]=inputJsonArr
                handler_ins.request_body=reqBodyJson
            api_response=APIRequest(handler_ins).get_api_response()
            converted_dict=dict()
            convertedIdsJson=api_response.response_json[APIConstants.DATA][0]
            if APIConstants.CONTACTS in convertedIdsJson and convertedIdsJson[APIConstants.CONTACTS] is not None:
                converted_dict[APIConstants.CONTACTS]=convertedIdsJson[APIConstants.CONTACTS]
            if APIConstants.ACCOUNTS in convertedIdsJson and convertedIdsJson[APIConstants.ACCOUNTS] is not None:
                converted_dict[APIConstants.ACCOUNTS]=convertedIdsJson[APIConstants.ACCOUNTS]
            if APIConstants.DEALS in convertedIdsJson and convertedIdsJson[APIConstants.DEALS] is not None:
                converted_dict[APIConstants.DEALS]=convertedIdsJson[APIConstants.DEALS]
            
            return converted_dict
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())
        
    def upload_photo(self,file_path):
        try:
            handler_ins=APIHandler()
            handler_ins.request_url_path=self.zcrmrecord.module_api_name+"/"+str(self.zcrmrecord.entity_id)+"/photo"
            handler_ins.request_method=APIConstants.REQUEST_METHOD_POST
            handler_ins.request_api_key=APIConstants.DATA
            return APIRequest(handler_ins).upload_attachment(file_path)
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())
            
    def download_photo(self):
        try:
            handler_ins=APIHandler()
            handler_ins.request_url_path=self.zcrmrecord.module_api_name+"/"+str(self.zcrmrecord.entity_id)+"/photo"
            handler_ins.request_method=APIConstants.REQUEST_METHOD_GET
            handler_ins.request_api_key=APIConstants.DATA
            return APIRequest(handler_ins).download_attachment()
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())
    
    def delete_photo(self):
        try:
            handler_ins=APIHandler()
            handler_ins.request_url_path=self.zcrmrecord.module_api_name+"/"+str(self.zcrmrecord.entity_id)+"/photo"
            handler_ins.request_method=APIConstants.REQUEST_METHOD_DELETE
            handler_ins.request_api_key=APIConstants.DATA
            return APIRequest(handler_ins).get_api_response()
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())
            
    def get_zcrmrecord_as_json(self):
        try:
            from .Operations import ZCRMUser,ZCRMRecord
        except ImportError:
            from Operations import ZCRMUser,ZCRMRecord
        record_json=dict()
        apiNameVsValues=self.zcrmrecord.field_data
        if self.zcrmrecord.owner is not None :
            record_json["Owner"]=str(self.zcrmrecord.owner.id)
        if self.zcrmrecord.layout is not None:
            record_json["Layout"]=str(self.zcrmrecord.layout.id)
        for key in apiNameVsValues:
            value=apiNameVsValues[key]
            if isinstance(value, ZCRMRecord):
                value=str(value.entity_id)
            elif isinstance(value, ZCRMUser):
                value=str(value.id)
            record_json[key]=value
        
        if len(self.zcrmrecord.line_items)>0:
            record_json["Product_Details"]=self.get_line_item_json(self.zcrmrecord.line_items)
        if len(self.zcrmrecord.participants)>0:
            record_json["Participants"]=self.get_participants_as_jsonarray()
        if len(self.zcrmrecord.price_details)>0:
            record_json["Pricing_Details"]=self.get_price_details_as_jsonarray()
        if len(self.zcrmrecord.tax_list)>0:
            record_json["Tax"]=self.get_tax_list_as_jsonarray()
        if len(self.zcrmrecord.tag_list) > 0:
            record_json["Tag"] = self.get_tag_list_as_jsonarray()
        return record_json

    def get_tag_list_as_jsonarray(self):
        tagListJsonArr = list()
        tagList = self.zcrmrecord.tag_list
        for tagIns in tagList:
            tagListJsonArr.append(self.get_zcrmtag_detail_as_json(tagIns))
        return tagListJsonArr

    def get_zcrmtag_detail_as_json(self, tagIns):
        tagJSON = dict()
        if tagIns.id != None:
            tagJSON["id"] = tagIns.id
        tagJSON["name"] = tagIns.name
        return tagJSON

    def get_tax_list_as_jsonarray(self):
        taxListJsonArr=list()
        taxList=self.zcrmrecord.tax_list
        for taxIns in taxList:
            taxListJsonArr.append(taxIns.name)
        return taxListJsonArr
        
    def get_price_details_as_jsonarray(self):
        priceDetailsArr = list()
        priceDetailsList = self.zcrmrecord.price_details
        for priceBookPricingIns in priceDetailsList:
            priceDetailsArr.append(self.get_zcrmprice_detail_as_json(priceBookPricingIns))
        return priceDetailsArr
    
    def get_zcrmprice_detail_as_json(self,priceBookPricingIns):
        priceDetailJSON = dict()
        if priceBookPricingIns.id != None:
            priceDetailJSON["id"]=priceBookPricingIns.id
        priceDetailJSON["discount"]=priceBookPricingIns.discount
        priceDetailJSON["to_range"]=priceBookPricingIns.to_range
        priceDetailJSON["from_range"]=priceBookPricingIns.from_range
        return priceDetailJSON
    
    def get_participants_as_jsonarray(self):
        participantsArr = list()
        participantsList = self.zcrmrecord.participants
        for participantIns in participantsList:
            participantsArr.append(self.get_zcrmparticipant_as_json(participantIns))
        return participantsArr
        
    def get_zcrmparticipant_as_json(self,participantIns):
        participantJSON = dict()
        participantJSON["participant"]= str(participantIns.id)
        participantJSON["type"]=str(participantIns.type)
        participantJSON["name"]=str(participantIns.name)
        participantJSON["Email"]=str(participantIns.email)
        participantJSON["invited"]=bool(participantIns.is_invited)
        participantJSON["status"]=str(participantIns.status)
        return participantJSON;
        
    def get_line_item_json(self,lineItemsArray):
        lineItemsAsJSONArray=list()
        for lineItem in lineItemsArray:
            lineItemData=dict()
            if lineItem.quantity is None:
                raise ZCRMException(self.request_url_path,APIConstants.RESPONSECODE_BAD_REQUEST,"Mandatory Field 'quantity' is missing.",None)
            if lineItem.id is not None:
                lineItemData["id"]=str(lineItem.id)
            if lineItem.product is not None:
                lineItemData["product"]=str(lineItem.product.entity_id)
            if lineItem.description is not None:
                lineItemData["product_description"]=lineItem.description
            if lineItem.list_price is not None:
                lineItemData["list_price"]=lineItem.list_price
            lineItemData["quantity"]=lineItem.quantity
            if lineItem.discount_percentage == None:
                lineItemData["Discount"]=lineItem.discount
            else:
                lineItemData["Discount"]=lineItem.discount_percentage+"%"
            lineTaxes=lineItem.line_tax
            lineTaxArray=list()
            for lineTaxInstance in lineTaxes:
                tax=dict()
                tax['name']=lineTaxInstance.name
                tax['value']=lineTaxInstance.value
                tax['percentage']=lineTaxInstance.percentage
                lineTaxArray.append(tax)
            lineItemData['line_tax']=lineTaxArray
            lineItemsAsJSONArray.append(lineItemData)
        return lineItemsAsJSONArray
    
    def set_record_properties(self,responseDict):
        try:
            from .Operations import ZCRMUser,ZCRMLayout,ZCRMRecord,ZCRMTax,ZCRMTag
        except ImportError:
            from Operations import ZCRMUser,ZCRMLayout,ZCRMRecord,ZCRMTax,ZCRMTag
        for key in responseDict:
            value=responseDict[key]
            if(value is None):
                continue
            if(key=="id"):
                self.zcrmrecord.entity_id=value
            elif("Product_Details"==key and self.zcrmrecord.module_api_name in APIConstants.INVENTORY_MODULES):
                self.set_inventory_line_items(value)
            elif("Participants"==key and self.zcrmrecord.module_api_name == "Events"):
                self.set_participants(value)
            elif ("Pricing_Details"==key and self.zcrmrecord.module_api_name == "Price_Books"):
                self.set_price_details(value)
            elif("Created_By"==key):
                createdBy = ZCRMUser.get_instance(value["id"], value["name"])
                self.zcrmrecord.created_by=createdBy
            elif("Modified_By"==key):
                modifiedBy = ZCRMUser.get_instance(value["id"], value["name"])
                self.zcrmrecord.modified_by=modifiedBy
            elif("Created_Time"==key):
                self.zcrmrecord.created_time=str(value)
            elif("Modified_Time"==key):
                self.zcrmrecord.modified_time=str(value)
            elif("Last_Activity_Time"==key):
                self.zcrmrecord.last_activity_time=str(value)
            elif("Owner"==key):
                owner =ZCRMUser.get_instance(value["id"], value["name"])
                self.zcrmrecord.owner=owner
            elif("Layout"==key):
                layout = None
                if(value is not None):
                    layout = ZCRMLayout.get_instance(value["id"])
                    layout.name=value["name"]
                self.zcrmrecord.layout=layout
            elif("Handler"==key and value is not None):
                handler = ZCRMUser.get_instance(value["id"], value["name"])
                self.zcrmrecord.field_data[key]= handler
            elif ("Tax"==key and isinstance(value, array)):
                for taxName in value:
                    taxIns=ZCRMTax.get_instance(taxName)
                    self.zcrmrecord.tax_list.append(taxIns)
            elif ("Tag" == key and isinstance(value, array)):
                for tag in value:
                    tag_ins = ZCRMTag.get_instance(tag['name'], tag['id'])
                    self.zcrmrecord.tag_list.append(tag_ins)
            elif ("tags" == key ):
                for tag in value:
                    tag_ins = ZCRMTag.get_instance(None, tag)
                    self.zcrmrecord.tag_list.append(tag_ins)
            elif ("$line_tax" == key):
                for lineTax in value:
                    taxInstance = ZCRMTax.get_instance(lineTax["name"])
                    taxInstance.percentage = lineTax['percentage']
                    taxInstance.value = float(lineTax['value'])
                    self.zcrmrecord.tax_list.append(taxInstance)
            elif(key.startswith('$')):
                self.zcrmrecord.properties[key.replace('$','')]= value
            elif(isinstance(value,array)):
                if("id" in value):
                    lookupRecord = ZCRMRecord.get_instance(key, value["id"])
                    lookupRecord.lookup_label=value if ("name" in value) else None
                    self.zcrmrecord.field_data[key]=lookupRecord
                else:
                    self.zcrmrecord.field_data[key]= value
            else:
                self.zcrmrecord.field_data[key]=responseDict[key]
    
    def set_price_details(self,priceDetails):
        for priceDetail in priceDetails:
            self.zcrmrecord.price_details.append(self.get_zcrm_pricebook_pricing(priceDetail))
    def get_zcrm_pricebook_pricing(self,priceDetails):
        try:
            from .Operations import ZCRMPriceBookPricing
        except ImportError:
            from Operations import ZCRMPriceBookPricing
        priceDetailIns = ZCRMPriceBookPricing.get_instance(priceDetails["id"])
        priceDetailIns.discount=Decimal(priceDetails["discount"])
        priceDetailIns.to_range=Decimal(priceDetails["to_range"])
        priceDetailIns.from_range=Decimal(priceDetails["from_range"])
        return priceDetailIns;       
    def set_participants(self,participants):
        for participant in participants:
            self.zcrmrecord.participants.append(self.get_zcrmparticipant(participant))
    def get_zcrmparticipant(self,participantDetails):
        try:
            from .Operations import ZCRMEventParticipant
        except ImportError:
            from Operations import ZCRMEventParticipant

        email = None
        id = None

        if "Email" in participantDetails:
            email = participantDetails['Email']
            id = participantDetails['participant']
        else:
            email = participantDetails['participant']

        participant = ZCRMEventParticipant.get_instance(participantDetails['type'], id)
        participant.name=participantDetails["name"]
        participant.email = email
        participant.is_invited=bool(participantDetails["invited"])
        participant.status=participantDetails["status"]
        
        return participant
    
    def set_inventory_line_items(self,lineItems):
        for lineItem in lineItems:
            self.zcrmrecord.line_items.append(self.get_zcrminventory_line_item(lineItem))
    
    def get_zcrminventory_line_item(self,lineItemDetails):
        try:
            from .Operations import ZCRMInventoryLineItem,ZCRMRecord,ZCRMTax
        except ImportError:
            from Operations import ZCRMInventoryLineItem,ZCRMRecord,ZCRMTax
        productDetails = lineItemDetails["product"]
        lineItemInstance = ZCRMInventoryLineItem.get_instance(lineItemDetails["id"])
        product = ZCRMRecord.get_instance("Products", productDetails["id"])
        product.lookup_label=productDetails["name"]
        if 'Product_Code' in productDetails:
            product.field_data['Product_Code']=productDetails['Product_Code']
        lineItemInstance.product=product
        lineItemInstance.description=lineItemDetails["product_description"]
        lineItemInstance.quantity=int(lineItemDetails["quantity"])
        lineItemInstance.list_price=float(lineItemDetails["list_price"])
        lineItemInstance.total=float(lineItemDetails["total"])
        lineItemInstance.discount=float(lineItemDetails["Discount"])
        lineItemInstance.total_after_discount=float(lineItemDetails["total_after_discount"])
        lineItemInstance.tax_amount=float(lineItemDetails["Tax"])
        lineTaxes = lineItemDetails["line_tax"]
        for lineTax in lineTaxes:
            taxInstance=ZCRMTax.get_instance(lineTax["name"])
            taxInstance.percentage=lineTax['percentage']
            taxInstance.value=float(lineTax['value'])
            lineItemInstance.line_tax.append(taxInstance)
        lineItemInstance.net_total=float(lineItemDetails["net_total"])
        
        return lineItemInstance

    def get_blueprint_data(self):
        try:
            handler_ins = APIHandler()
            handler_ins.request_url_path = self.zcrmrecord.module_api_name + '/' + str(self.zcrmrecord.entity_id) + \
                                           '/actions/blueprint'
            handler_ins.request_method = APIConstants.REQUEST_METHOD_GET
            handler_ins.request_api_key = APIConstants.BLUEPRINT
            return APIRequest(handler_ins).get_api_response()
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            CommonUtil.raise_exception(handler_ins.request_url_path, ex.__str__(), traceback.format_stack())

    def update_blueprint_data(self):
        try:
            handler_ins = APIHandler()
            handler_ins.request_url_path = self.zcrmrecord.module_api_name + "/" + str(self.zcrmrecord.entity_id) + \
                                           '/actions/blueprint'
            handler_ins.request_method = APIConstants.REQUEST_METHOD_PUT
            handler_ins.request_api_key = APIConstants.BLUEPRINT
            input_json = self.get_zcrmrecord_blueprint_as_json()
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            body = CommonUtil.create_api_supported_blueprint_json(input_json, APIConstants.BLUEPRINT, self.zcrmrecord.blueprint_transition_id)
            handler_ins.request_body = body
            return APIRequest(handler_ins).get_api_response()
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            CommonUtil.raise_exception(handler_ins.request_url_path, ex.__str__(), traceback.format_stack())

    def get_zcrmrecord_blueprint_as_json(self):
        try:
            from .Operations import ZCRMRecord, ZCRMUser, ZCRMInventoryLineItem, ZCRMPriceBookPricing
        except ImportError:
            from Operations import ZCRMRecord, ZCRMUser, ZCRMInventoryLineItem, ZCRMPriceBookPricing
        record_json = dict()
        apiNameVsValues = self.zcrmrecord.blueprint_values
        for apiName in apiNameVsValues:
            value = apiNameVsValues[apiName]
            if (isinstance(value, dict)):
                temp_dict = dict()
                for key in value.keys():
                    each_value = value[key]
                    if isinstance(each_value, ZCRMRecord):
                        each_value = str(each_value.entity_id)
                    elif isinstance(each_value, ZCRMUser):
                        each_value = str(each_value.id)
                    elif isinstance(each_value, list):
                        if isinstance(each_value.__getitem__(0), ZCRMInventoryLineItem):
                            each_value = self.get_line_item_json(each_value)
                        elif isinstance(each_value.__getitem__(0), ZCRMPriceBookPricing):
                            pricebook_list = list()
                            for every_pricebook_pricing in each_value:
                                pricebook_list.append(self.get_zcrmprice_detail_as_json(every_pricebook_pricing))
                    temp_dict[key] = each_value
                record_json[apiName] = temp_dict
            else:
                if isinstance(value, ZCRMRecord):
                    value = str(value.entity_id)
                elif isinstance(value, ZCRMUser):
                    value = str(value.id)
                record_json[apiName] = value
        if len(self.zcrmrecord.blueprint_checklist) > 0:
            record_json["CheckLists"] = self.zcrmrecord.blueprint_checklist
        return record_json

class RelatedListAPIHandler(APIHandler):
    
    def __init__(self,parent_record,related_list_or_junction_record):
        self.parent_record=parent_record
        try:
            from .Operations import ZCRMModuleRelation
        except ImportError:
            from Operations import ZCRMModuleRelation
        if isinstance(related_list_or_junction_record, ZCRMModuleRelation):
            self.related_lists=related_list_or_junction_record
            self.junction_record=None
        else:
            self.junction_record=related_list_or_junction_record
            self.related_lists=None
    
    @staticmethod
    def get_instance(parent_record,related_list_or_junction_record):
        return RelatedListAPIHandler(parent_record,related_list_or_junction_record)
    
    def get_records(self,sort_by_field,sort_order,page,per_page):
        try:
            handler_ins=APIHandler()
            handler_ins.request_url_path=self.parent_record.module_api_name+"/"+str(self.parent_record.entity_id)+"/"+self.related_lists.api_name
            handler_ins.request_method=APIConstants.REQUEST_METHOD_GET
            handler_ins.request_api_key=APIConstants.DATA
            if sort_by_field is not None:
                handler_ins.add_param('sort_by', sort_by_field)
            if sort_order is not None:
                handler_ins.add_param('sort_order', sort_order)
            handler_ins.add_param('page', page)
            handler_ins.add_param('per_page', per_page)
            bulk_api_response=APIRequest(handler_ins).get_bulk_api_response()
            records_json=bulk_api_response.response_json[APIConstants.DATA]
            records_ins_list=list()
            try:
                from .Operations import ZCRMRecord
            except ImportError:
                from Operations import ZCRMRecord
            for record_json in records_json:
                record_ins=ZCRMRecord.get_instance(self.related_lists.api_name, record_json['id'])
                EntityAPIHandler.get_instance(record_ins).set_record_properties(record_json)
                records_ins_list.append(record_ins)
            bulk_api_response.data=records_ins_list
            return bulk_api_response
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())
        
    def add_relation(self):
        try:
            handler_ins=APIHandler()
            handler_ins.request_url_path=self.parent_record.module_api_name+"/"+str(self.parent_record.entity_id)+"/"+self.junction_record.api_name+"/"+str(self.junction_record.id)
            handler_ins.request_method=APIConstants.REQUEST_METHOD_PUT
            handler_ins.request_api_key=APIConstants.DATA
            junction_record_data=self.junction_record.get_related_data()
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            handler_ins.request_body=CommonUtil.create_api_supported_input_json(junction_record_data, APIConstants.DATA)
            return APIRequest(handler_ins).get_api_response()
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())
        
    def remove_relation(self):
        try:
            handler_ins=APIHandler()
            handler_ins.request_url_path=self.parent_record.module_api_name+"/"+str(self.parent_record.entity_id)+"/"+self.junction_record.api_name+"/"+str(self.junction_record.id)
            handler_ins.request_method=APIConstants.REQUEST_METHOD_DELETE
            handler_ins.request_api_key=APIConstants.DATA
            return APIRequest(handler_ins).get_api_response()
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())
        
    def add_note(self,zcrm_note_ins):
        try:
            handler_ins=APIHandler()
            handler_ins.request_url_path=self.parent_record.module_api_name+"/"+str(self.parent_record.entity_id)+"/"+self.related_lists.api_name
            handler_ins.request_method=APIConstants.REQUEST_METHOD_POST
            handler_ins.request_api_key=APIConstants.DATA
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            handler_ins.request_body=CommonUtil.create_api_supported_input_json(self.get_zcrmnote_as_json(zcrm_note_ins), APIConstants.DATA)
            api_response= APIRequest(handler_ins).get_api_response()
            details=api_response.response_json[APIConstants.DATA][0][APIConstants.DETAILS]
            zcrm_note_ins=self.get_zcrm_note(details, zcrm_note_ins)
            api_response.data=zcrm_note_ins
            return api_response
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())
        
    def update_note(self,zcrm_note_ins):
        try:
            handler_ins=APIHandler()
            handler_ins.request_url_path=self.parent_record.module_api_name+"/"+str(self.parent_record.entity_id)+"/"+self.related_lists.api_name+"/"+str(zcrm_note_ins.id)
            handler_ins.request_method=APIConstants.REQUEST_METHOD_PUT
            handler_ins.request_api_key=APIConstants.DATA
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            handler_ins.request_body=CommonUtil.create_api_supported_input_json(self.get_zcrmnote_as_json(zcrm_note_ins), APIConstants.DATA)
            api_response= APIRequest(handler_ins).get_api_response()
            details=api_response.response_json[APIConstants.DATA][0][APIConstants.DETAILS]
            zcrm_note_ins=self.get_zcrm_note(details, zcrm_note_ins)
            api_response.data=zcrm_note_ins
            return api_response
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())
        
    def delete_note(self,zcrm_note_ins):
        try:
            handler_ins=APIHandler()
            handler_ins.request_url_path=self.parent_record.module_api_name+"/"+str(self.parent_record.entity_id)+"/"+self.related_lists.api_name+"/"+str(zcrm_note_ins.id)
            handler_ins.request_method=APIConstants.REQUEST_METHOD_DELETE
            handler_ins.request_api_key=APIConstants.DATA
            return APIRequest(handler_ins).get_api_response()
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())
    def get_notes(self,sort_by,sort_order,page,per_page):
        try:
            handler_ins=APIHandler()
            handler_ins.request_url_path=self.parent_record.module_api_name+"/"+str(self.parent_record.entity_id)+"/"+self.related_lists.api_name
            handler_ins.request_method=APIConstants.REQUEST_METHOD_GET
            handler_ins.request_api_key=APIConstants.DATA
            handler_ins.add_param('page', page)
            handler_ins.add_param('per_page', per_page)
            if sort_by is not None:
                handler_ins.add_param('sort_by',sort_by)
            if sort_order is not None:
                handler_ins.add_param('sort_order',sort_order)
            bulk_api_res= APIRequest(handler_ins).get_bulk_api_response()
            notes_json_arr=bulk_api_res.response_json[APIConstants.DATA]
            note_ins_arr=list()
            for note_json in notes_json_arr:
                note_ins_arr.append(self.get_zcrm_note(note_json, None))
            bulk_api_res.data=note_ins_arr
            return bulk_api_res
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())
    
    def get_attachments(self,page,per_page):
        try:
            handler_ins=APIHandler()
            handler_ins.request_url_path=self.parent_record.module_api_name+"/"+str(self.parent_record.entity_id)+"/"+self.related_lists.api_name
            handler_ins.request_method=APIConstants.REQUEST_METHOD_GET
            handler_ins.request_api_key=APIConstants.DATA
            handler_ins.add_param('page', page)
            handler_ins.add_param('per_page', per_page)
            bulk_api_res= APIRequest(handler_ins).get_bulk_api_response()
            attachments_json_arr=bulk_api_res.response_json[APIConstants.DATA]
            attachment_ins_arr=list()
            for attachment_json in attachments_json_arr:
                attachment_ins_arr.append(self.get_zcrm_attachment(attachment_json))
            bulk_api_res.data=attachment_ins_arr
            return bulk_api_res
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())
        
    def get_zcrmnote_as_json(self,zcrm_note_ins):
        note_json=dict()
        if zcrm_note_ins.title is not None:
            note_json['Note_Title']=zcrm_note_ins.title
        note_json['Note_Content']=zcrm_note_ins.content
        return note_json
    
    def get_zcrm_note(self,note_details,zcrm_note_ins):
        if zcrm_note_ins is None:
            try:
                from .Operations import ZCRMNote
            except ImportError:
                from Operations import ZCRMNote
            zcrm_note_ins=ZCRMNote.get_instance(self.parent_record, note_details['id'])
        if 'id' in note_details:
            zcrm_note_ins.id=note_details['id']
        if 'Note_Title' in note_details:
            zcrm_note_ins.title=note_details['Note_Title']
        if 'Note_Content' in note_details:
            zcrm_note_ins.content=note_details['Note_Content']
        try:
            from .Operations import ZCRMUser
        except ImportError:
            from Operations import ZCRMUser
        if 'Owner' in note_details:
            zcrm_note_ins.owner=ZCRMUser.get_instance(note_details['Owner']['id'], note_details['Owner']['name'])
        zcrm_note_ins.created_by=ZCRMUser.get_instance(note_details['Created_By']['id'], note_details['Created_By']['name'])
        zcrm_note_ins.modified_by=ZCRMUser.get_instance(note_details['Modified_By']['id'], note_details['Modified_By']['name'])
        if 'Created_Time' in note_details:
            zcrm_note_ins.created_time=note_details['Created_Time']
        if 'Modified_Time' in note_details:
            zcrm_note_ins.modified_time=note_details['Modified_Time']
        if '$voice_note' in note_details:
            zcrm_note_ins.is_voice_note=note_details['$voice_note']
        if '$se_module' in note_details:
            zcrm_note_ins.parent_module=note_details['$se_module']
        if 'Parent_Id' in note_details:
            zcrm_note_ins.parent_name=note_details['Parent_Id']['name']
            zcrm_note_ins.parent_id=note_details['Parent_Id']['id']
        if '$size' in note_details:
            zcrm_note_ins.size=note_details['$size']
        if '$attachments' in note_details and note_details['$attachments'] is not None:
            attachment_arr=note_details['$attachments']
            attachment_ins_arr=list()
            for attachment_details in attachment_arr:
                attachment_ins_arr.append(self.get_zcrm_attachment(attachment_details))
            zcrm_note_ins.attachments=attachment_ins_arr
        return zcrm_note_ins
    
    def get_zcrm_attachment(self,attachment_details):
        try:
            from .Operations import ZCRMAttachment,ZCRMUser
        except ImportError:
            from Operations import ZCRMAttachment,ZCRMUser
        attachment_ins=ZCRMAttachment.get_instance(self.parent_record, attachment_details['id'])
        file_name=attachment_details["File_Name"]
        attachment_ins.file_name=file_name
        if '.' in file_name:
            attachment_ins.file_type=file_name[file_name.index('.')+1:]
        attachment_ins.size=attachment_details['Size']
        attachment_ins.owner = ZCRMUser.get_instance(attachment_details["Owner"]["id"], attachment_details["Owner"]["name"])
        attachment_ins.created_by = ZCRMUser.get_instance(attachment_details["Created_By"]["id"], attachment_details["Created_By"]["name"])
        attachment_ins.modified_by = ZCRMUser.get_instance(attachment_details["Modified_By"]["id"], attachment_details["Modified_By"]["name"])
        attachment_ins.created_time=attachment_details["Created_Time"]
        attachment_ins.modified_time=attachment_details["Modified_Time"]
        attachment_ins.parent_module=attachment_details['$se_module']
        attachment_ins.attachment_type=attachment_details['$type']
        attachment_ins.parent_id=attachment_details['Parent_Id']['id']
        attachment_ins.parent_name=attachment_details['Parent_Id']['name']
        return attachment_ins
        
    def upload_attachment(self,file_path):
        try:
            handler_ins=APIHandler()
            handler_ins.request_url_path=self.parent_record.module_api_name+"/"+str(self.parent_record.entity_id)+"/"+self.related_lists.api_name
            handler_ins.request_method=APIConstants.REQUEST_METHOD_POST
            handler_ins.request_api_key=APIConstants.DATA
            api_response_ins= APIRequest(handler_ins).upload_attachment(file_path)
            details=api_response_ins.response_json[APIConstants.DATA][0]['details']
            try:
                from .Operations import ZCRMAttachment
            except ImportError:
                from Operations import ZCRMAttachment
            attachment_ins=ZCRMAttachment.get_instance(self.parent_record, details['id'])
            api_response_ins.data=attachment_ins
            return api_response_ins
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())
    def upload_link_as_attachment(self,link_url):
        try:
            handler_ins=APIHandler()
            handler_ins.request_url_path=self.parent_record.module_api_name+"/"+str(self.parent_record.entity_id)+"/"+self.related_lists.api_name
            handler_ins.request_method=APIConstants.REQUEST_METHOD_POST
            handler_ins.request_api_key=APIConstants.DATA
            reqBody=dict()
            reqBody[APIConstants.ATTACHMENT_URL]=link_url
            handler_ins.request_body=reqBody
            #handler_ins.add_param(APIConstants.ATTACHMENT_URL, link_url)
            api_response_ins= APIRequest(handler_ins).upload_link_as_attachment()
            details=api_response_ins.response_json[APIConstants.DATA][0]['details']
            try:
                from .Operations import ZCRMAttachment
            except ImportError:
                from Operations import ZCRMAttachment
            attachment_ins=ZCRMAttachment.get_instance(self.parent_record, details['id'])
            api_response_ins.data=attachment_ins
            return api_response_ins
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())
        
    def download_attachment(self,attachment_id):
        try:
            handler_ins=APIHandler()
            handler_ins.request_url_path=self.parent_record.module_api_name+"/"+str(self.parent_record.entity_id)+"/"+self.related_lists.api_name+"/"+str(attachment_id)
            handler_ins.request_method=APIConstants.REQUEST_METHOD_GET
            return APIRequest(handler_ins).download_attachment()
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())
        
    def delete_attachment(self,attachment_id):
        try:
            handler_ins=APIHandler()
            handler_ins.request_url_path=self.parent_record.module_api_name+"/"+str(self.parent_record.entity_id)+"/"+self.related_lists.api_name+"/"+str(attachment_id)
            handler_ins.request_method=APIConstants.REQUEST_METHOD_DELETE
            handler_ins.request_api_key=APIConstants.DATA
            return APIRequest(handler_ins).get_api_response()
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())
        
class MassEntityAPIHandler(APIHandler):
        
    def __init__(self,module_instance):
        self.module_instance=module_instance
            
    @staticmethod
    def get_instance(module_instance):
        return MassEntityAPIHandler(module_instance)

    def get_records(self,cvid,sort_by,sort_order,page,per_page,custom_headers, custom_parameters):
        try:
            handler_ins=APIHandler()
            handler_ins.request_url_path=self.module_instance.api_name
            handler_ins.request_method=APIConstants.REQUEST_METHOD_GET
            handler_ins.request_api_key=APIConstants.DATA
            if cvid is not None:
                handler_ins.add_param("cvid", cvid)
            if sort_by is not None:
                handler_ins.add_param("sort_by", sort_by)
            if sort_order is not None:
                handler_ins.add_param("sort_order", sort_order)
            if custom_headers is not None:
                for header_name, value in custom_headers.items():
                    handler_ins.add_header(header_name, value)
            if custom_parameters is not None:
                for parameter_name, value in custom_parameters.items():
                    handler_ins.add_param(parameter_name, value)
            handler_ins.add_param("page", page)
            handler_ins.add_param("per_page", per_page)
            bulk_api_response=APIRequest(handler_ins).get_bulk_api_response()
            data_arr=bulk_api_response.response_json[APIConstants.DATA]
            record_ins_list=list()
            try:
                from .Operations import ZCRMRecord
            except ImportError:
                from Operations import ZCRMRecord
            for record_data in data_arr:
                zcrm_record=ZCRMRecord.get_instance(self.module_instance.api_name, record_data['id'])
                EntityAPIHandler.get_instance(zcrm_record).set_record_properties(record_data)
                record_ins_list.append(zcrm_record)
            bulk_api_response.data=record_ins_list
            return bulk_api_response
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())

    def create_records(self,record_ins_list, trigger, process, lar_id):
        try:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            if len(record_ins_list)>100:
                CommonUtil.raise_exception('Records_Create',"records count must be less than or equals to 100",'MORE RECORDS PROVIDED',"MORE RECORDS")
            handler_ins=APIHandler()
            handler_ins.request_url_path=self.module_instance.api_name
            handler_ins.request_method=APIConstants.REQUEST_METHOD_POST
            handler_ins.request_api_key=APIConstants.DATA
            data_array=list()
            for record_ins in record_ins_list:
                if record_ins.entity_id is None:
                    data_array.append(EntityAPIHandler.get_instance(record_ins).get_zcrmrecord_as_json())
                else:
                    CommonUtil.raise_exception('Records_Create',"record id must be None",'RECORD ID PROVIDED',"RECORD ID")
            request_json = dict()
            request_json[APIConstants.DATA] = data_array
            if trigger is not None:
                request_json[APIConstants.TRIGGER] = trigger
            if process is not None:
                request_json[APIConstants.PROCESS] = process
            if lar_id is not None:
                request_json[APIConstants.LAR_ID] = lar_id
            handler_ins.request_body = request_json
            
            bulk_api_response=APIRequest(handler_ins).get_bulk_api_response()
            
            created_records=list()
            entity_responses=bulk_api_response.bulk_entity_response
            length=len(entity_responses)
            for i in range(0,length):
                entity_response_ins=entity_responses[i]
                if entity_response_ins.status==APIConstants.STATUS_SUCCESS:
                    record_create_details=entity_response_ins.details
                    new_record=record_ins_list[i]
                    EntityAPIHandler.get_instance(new_record).set_record_properties(record_create_details)
                    created_records.append(new_record)
                    entity_response_ins.data=new_record
            bulk_api_response.data=created_records
            return bulk_api_response
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())
        
    def upsert_records(self,record_ins_list,duplicate_check_fields, trigger, process, lar_id):
        try:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            if len(record_ins_list)>100:
                CommonUtil.raise_exception('Records_Upsert',"records count must be less than or equals to 100",'MORE RECORDS PROVIDED',"MORE RECORDS")
            handler_ins=APIHandler()
            handler_ins.request_url_path=self.module_instance.api_name+"/upsert"
            handler_ins.request_method=APIConstants.REQUEST_METHOD_POST
            handler_ins.request_api_key=APIConstants.DATA
            data_array=list()
            for record_ins in record_ins_list:
                record_json=EntityAPIHandler.get_instance(record_ins).get_zcrmrecord_as_json()
                if record_ins.entity_id is not None:
                    record_json['id']=str(record_ins.entity_id)
                data_array.append(record_json)
            request_json=dict()
            request_json[APIConstants.DATA] = data_array
            if trigger is not None:
                request_json[APIConstants.TRIGGER] = trigger
            if process is not None:
                request_json[APIConstants.PROCESS] = process
            if lar_id is not None:
                request_json[APIConstants.LAR_ID] = lar_id
            if duplicate_check_fields is not None:
                request_json[APIConstants.DUPLICATE_CHECK_FIELDS] = duplicate_check_fields

            handler_ins.request_body=request_json
            
            bulk_api_response=APIRequest(handler_ins).get_bulk_api_response()
            
            created_records=list()
            entity_responses=bulk_api_response.bulk_entity_response
            length=len(entity_responses)
            for i in range(0,length):
                entity_response_ins=entity_responses[i]
                if entity_response_ins.status==APIConstants.STATUS_SUCCESS:
                    record_create_details=entity_response_ins.details
                    new_record=record_ins_list[i]
                    EntityAPIHandler.get_instance(new_record).set_record_properties(record_create_details)
                    created_records.append(new_record)
                    entity_response_ins.data=new_record
            bulk_api_response.data=created_records
            return bulk_api_response
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())
    
    def update_records(self,record_ins_list, trigger, process):
        try:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            if len(record_ins_list)>100:
                CommonUtil.raise_exception('Records_Update',"records count must be less than or equals to 100",'MORE RECORDS PROVIDED',"MORE RECORDS")
            handler_ins=APIHandler()
            handler_ins.request_url_path=self.module_instance.api_name
            handler_ins.request_method=APIConstants.REQUEST_METHOD_PUT
            handler_ins.request_api_key=APIConstants.DATA
            data_array=list()
            for record_ins in record_ins_list:
                record_json=EntityAPIHandler.get_instance(record_ins).get_zcrmrecord_as_json()
                if record_ins.entity_id is not None:
                    record_json['id']=str(record_ins.entity_id)
                data_array.append(record_json)
            request_json=dict()
            request_json[APIConstants.DATA]=data_array
            if trigger is not None:
                request_json[APIConstants.TRIGGER] = trigger
            if process is not None:
                request_json[APIConstants.PROCESS] = process
            handler_ins.request_body=request_json
            
            bulk_api_response=APIRequest(handler_ins).get_bulk_api_response()
            
            created_records=list()
            entity_responses=bulk_api_response.bulk_entity_response
            length=len(entity_responses)
            for i in range(0,length):
                entity_response_ins=entity_responses[i]
                if entity_response_ins.status==APIConstants.STATUS_SUCCESS:
                    record_create_details=entity_response_ins.details
                    new_record=record_ins_list[i]
                    EntityAPIHandler.get_instance(new_record).set_record_properties(record_create_details)
                    created_records.append(new_record)
                    entity_response_ins.data=new_record
            bulk_api_response.data=created_records
            return bulk_api_response
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())

    def update_mass_records(self,entityid_list,field_api_name,value):
        try:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            if len(entityid_list)>100:
                CommonUtil.raise_exception('Records_Mass_Update',"entity id count must be less than or equals to 100",'MORE RECORDS PROVIDED',"MORE RECORDS")
            handler_ins=APIHandler()
            handler_ins.request_url_path=self.module_instance.api_name
            handler_ins.request_method=APIConstants.REQUEST_METHOD_PUT
            handler_ins.request_api_key=APIConstants.DATA
            handler_ins.request_body=self.construct_json_for_massupdate(entityid_list,field_api_name,value)
            
            bulk_api_response=APIRequest(handler_ins).get_bulk_api_response()
            
            updated_records=list()
            entity_responses=bulk_api_response.bulk_entity_response
            length=len(entity_responses)
            try:
                from .Operations import ZCRMRecord
            except ImportError:
                from Operations import ZCRMRecord
            for i in range(0,length):
                entity_response_ins=entity_responses[i]
                if entity_response_ins.status==APIConstants.STATUS_SUCCESS:
                    record_update_details=entity_response_ins.details
                    updated_record=ZCRMRecord.get_instance(self.module_instance.api_name, record_update_details['id'])
                    EntityAPIHandler.get_instance(updated_record).set_record_properties(record_update_details)
                    updated_records.append(updated_record)
                    entity_response_ins.data=updated_record
            bulk_api_response.data=updated_records
            return bulk_api_response
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())
    
    def delete_records(self,entityid_list):
        try:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            if len(entityid_list)>100:
                CommonUtil.raise_exception('Records_delete',"entity id count must be less than or equals to 100",'MORE RECORDS PROVIDED',"MORE RECORDS")
            handler_ins=APIHandler()
            handler_ins.request_url_path=self.module_instance.api_name
            handler_ins.request_method=APIConstants.REQUEST_METHOD_DELETE
            handler_ins.request_api_key=APIConstants.DATA
            ids_as_string=','.join(str(entity_id) for entity_id in entityid_list)
            handler_ins.add_param('ids', ids_as_string)
            
            bulk_api_response=APIRequest(handler_ins).get_bulk_api_response()
            
            entity_responses=bulk_api_response.bulk_entity_response
            try:
                from .Operations import ZCRMRecord
            except ImportError:
                from Operations import ZCRMRecord
            length=len(entity_responses)
            for i in range(0,length):
                entity_response_ins=entity_responses[i]
                record_delete_details=entity_response_ins.details
                deleted_record=ZCRMRecord.get_instance(self.module_instance.api_name, record_delete_details['id'])
                entity_response_ins.data=deleted_record
            return bulk_api_response
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())
        
    def get_all_deleted_records(self, page, per_page, custom_headers):
        return self.get_deleted_records('all', page, per_page, custom_headers)
    def get_recyclebin_records(self, page, per_page, custom_headers):
        return self.get_deleted_records('recycle', page, per_page, custom_headers)
    def get_permanently_deleted_records(self, page, per_page, custom_headers):
        return self.get_deleted_records('permanent', page, per_page, custom_headers)
    def get_deleted_records(self,trashed_type, page, per_page, custom_headers):
        try:
            handler_ins=APIHandler()
            handler_ins.request_url_path=self.module_instance.api_name+"/deleted"
            handler_ins.request_method=APIConstants.REQUEST_METHOD_GET
            handler_ins.request_api_key=APIConstants.DATA
            if trashed_type is not None:
                handler_ins.add_param("type", trashed_type)
            if custom_headers is not None:
                for header, value in custom_headers.items():
                    handler_ins.add_header(header, value)
            handler_ins.add_param("page", page)
            handler_ins.add_param("per_page", per_page)
            bulk_api_response=APIRequest(handler_ins).get_bulk_api_response()
            data_arr=bulk_api_response.response_json[APIConstants.DATA]
            record_ins_list=list()
            try:
                from .Operations import ZCRMTrashRecord
            except ImportError:
                from Operations import ZCRMTrashRecord
            for record_data in data_arr:
                trash_record=ZCRMTrashRecord.get_instance(record_data['type'], record_data['id'])
                self.set_trash_record_properties(trash_record, record_data)
                record_ins_list.append(trash_record)
            bulk_api_response.data=record_ins_list
            return bulk_api_response
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())
        
    def search_records(self,search_word,page,per_page,type):
        try:
            handler_ins=APIHandler()
            handler_ins.request_url_path=self.module_instance.api_name+"/search"
            handler_ins.request_method=APIConstants.REQUEST_METHOD_GET
            handler_ins.request_api_key=APIConstants.DATA
            handler_ins.add_param(type, search_word)
            handler_ins.add_param("page", page)
            handler_ins.add_param("per_page", per_page)
            bulk_api_response=APIRequest(handler_ins).get_bulk_api_response()
            data_arr=bulk_api_response.response_json[APIConstants.DATA]
            record_ins_list=list()
            try:
                from .Operations import ZCRMRecord
            except ImportError:
                from Operations import ZCRMRecord
            for record_data in data_arr:
                zcrm_record=ZCRMRecord.get_instance(self.module_instance.api_name, record_data['id'])
                EntityAPIHandler.get_instance(zcrm_record).set_record_properties(record_data)
                record_ins_list.append(zcrm_record)
            bulk_api_response.data=record_ins_list
            return bulk_api_response
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())
            
    def set_trash_record_properties(self,trash_record_ins,trash_record_prop):
        try:
            from .Operations import ZCRMUser
        except ImportError:
            from Operations import ZCRMUser
        if 'display_name' in trash_record_prop:
            trash_record_ins.display_name=trash_record_prop['display_name']
        if 'created_by' in trash_record_prop and trash_record_prop['created_by'] is not None:
            trash_record_ins.created_by=ZCRMUser.get_instance(trash_record_prop['created_by']['id'],trash_record_prop['created_by']['name'])
        if 'deleted_by' in trash_record_prop and trash_record_prop['deleted_by'] is not None:
            trash_record_ins.deleted_by=ZCRMUser.get_instance(trash_record_prop['deleted_by']['id'],trash_record_prop['deleted_by']['name'])
        trash_record_ins.deleted_time=trash_record_prop['deleted_time']
            
        
    def construct_json_for_massupdate(self,entityid_list,field_api_name,field_value):
        input_json_arr=list()
        for entity_id in entityid_list:
            each_json=dict()
            each_json['id']=str(entity_id)
            each_json[field_api_name]=field_value
            input_json_arr.append(each_json)
        data_json=dict()
        data_json[APIConstants.DATA]=input_json_arr
        return data_json

class ModuleAPIHandler(APIHandler):
    
    def __init__(self,module_instance):
        self.module_instance=module_instance
        
    @staticmethod
    def get_instance(module_ins):
        return ModuleAPIHandler(module_ins)
    
    def get_field(self,field_id):
        try:
            if field_id is None:
                try:
                    from .Utility import CommonUtil
                except ImportError:
                    from Utility import CommonUtil
                CommonUtil.raise_exception('Field_GET',"field id must be given",'FIELD ID IS NOT PROVIDED',"FIELD ID")
            handler_ins=APIHandler()
            handler_ins.request_url_path="settings/fields/"+str(field_id)
            handler_ins.request_method=APIConstants.REQUEST_METHOD_GET
            handler_ins.request_api_key=APIConstants.FIELDS
            handler_ins.add_param('module', self.module_instance.api_name)
            apiResponse=APIRequest(handler_ins).get_api_response()
            apiResponse.data=self.get_zcrmfield(apiResponse.response_json[APIConstants.FIELDS][0])
            return apiResponse
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())
        
    def get_all_fields(self):
        try:
            handler_ins=APIHandler()
            handler_ins.request_url_path="settings/fields"
            handler_ins.request_method=APIConstants.REQUEST_METHOD_GET
            handler_ins.request_api_key=APIConstants.FIELDS
            handler_ins.add_param('module', self.module_instance.api_name)
            bulk_api_response=APIRequest(handler_ins).get_bulk_api_response()
            fields=bulk_api_response.response_json[APIConstants.FIELDS]
            field_instance_arr=list()
            for field in fields:
                field_instance_arr.append(self.get_zcrmfield(field))
            bulk_api_response.data=field_instance_arr
            return bulk_api_response
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())
        
    def get_all_layouts(self):
        try:
            handler_ins=APIHandler()
            handler_ins.request_url_path="settings/layouts"
            handler_ins.request_method=APIConstants.REQUEST_METHOD_GET
            handler_ins.request_api_key=APIConstants.LAYOUTS
            handler_ins.add_param('module', self.module_instance.api_name)
            bulk_api_response=APIRequest(handler_ins).get_bulk_api_response()
            layouts=bulk_api_response.response_json[APIConstants.LAYOUTS]
            layout_instance_arr=list()
            for layout in layouts:
                layout_instance_arr.append(self.get_zcrmlayout(layout))
            bulk_api_response.data=layout_instance_arr
            return bulk_api_response
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())
        
    def get_layout(self,layout_id):
        try:
            if layout_id is None:
                try:
                    from .Utility import CommonUtil
                except ImportError:
                    from Utility import CommonUtil
                CommonUtil.raise_exception('Layout_GET',"layout id must be given",'LAYOUT ID IS NOT PROVIDED',"LAYOUT ID")
            handler_ins=APIHandler()
            handler_ins.request_url_path="settings/layouts/"+str(layout_id)
            handler_ins.request_method=APIConstants.REQUEST_METHOD_GET
            handler_ins.request_api_key=APIConstants.LAYOUTS
            handler_ins.add_param('module', self.module_instance.api_name)
            api_response=APIRequest(handler_ins).get_api_response()
            api_response.data=self.get_zcrmlayout(api_response.response_json[APIConstants.LAYOUTS][0])
            return api_response
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())
        
    def get_all_customviews(self):
        try:
            handler_ins=APIHandler()
            handler_ins.request_url_path="settings/custom_views"
            handler_ins.request_method=APIConstants.REQUEST_METHOD_GET
            handler_ins.request_api_key=APIConstants.CUSTOM_VIEWS
            handler_ins.add_param('module', self.module_instance.api_name)
            bulk_api_response=APIRequest(handler_ins).get_bulk_api_response()
            response_json=bulk_api_response.response_json
            categories=response_json['info']['translation'] if 'translation' in response_json['info'] else None
            customviews=response_json[APIConstants.CUSTOM_VIEWS]
            customview_instances=list()
            for customview in customviews:
                customview_instances.append(self.get_zcrm_customview(customview, categories))
            bulk_api_response.data=customview_instances
            return bulk_api_response
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())
        
    def get_customview(self,customview_id):
        try:
            if customview_id is None:
                try:
                    from .Utility import CommonUtil
                except ImportError:
                    from Utility import CommonUtil
                CommonUtil.raise_exception('Customview_GET',"custom view id must be given",'CUSTOM VIEW ID IS NOT PROVIDED',"CUSTOM VIEW ID")
            handler_ins=APIHandler()
            handler_ins.request_url_path="settings/custom_views/"+str(customview_id)
            handler_ins.request_method=APIConstants.REQUEST_METHOD_GET
            handler_ins.request_api_key=APIConstants.CUSTOM_VIEWS
            handler_ins.add_param('module', self.module_instance.api_name)
            api_response=APIRequest(handler_ins).get_api_response()
            response_json=api_response.response_json
            categories=response_json['info']['translation'] if 'translation' in response_json['info'] else None
            api_response.data=self.get_zcrm_customview(response_json[APIConstants.CUSTOM_VIEWS][0], categories)
            return api_response
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())
        
    def update_module_settings(self):
        try:
            handler_ins=APIHandler()
            handler_ins.request_url_path="settings/modules/"+self.module_instance.api_name
            handler_ins.request_method=APIConstants.REQUEST_METHOD_PUT
            handler_ins.request_api_key=APIConstants.MODULES
            handler_ins.request_body=self.construct_json_for_module_update(self.module_instance)
            return APIRequest(handler_ins).get_api_response()
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())
    def update_customview(self,customview_instance):
        try:
            handler_ins=APIHandler()
            handler_ins.request_url_path="settings/custom_views/"+str(customview_instance.id)
            handler_ins.request_method=APIConstants.REQUEST_METHOD_PUT
            handler_ins.add_param('module', self.module_instance.api_name)
            handler_ins.request_body=self.construct_json_for_cv_update(customview_instance)
            return APIRequest(handler_ins).get_api_response()
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())
    def get_all_relatedlists(self):
        try:
            handler_ins=APIHandler()
            handler_ins.request_url_path="settings/related_lists"
            handler_ins.request_method=APIConstants.REQUEST_METHOD_GET
            handler_ins.add_param('module', self.module_instance.api_name)
            bulk_api_response=APIRequest(handler_ins).get_bulk_api_response()
            response_json=bulk_api_response.response_json
            related_lists=response_json[APIConstants.RELATED_LISTS]
            relatedlist_instances=list()
            for related_list in related_lists:
                try:
                    from .Operations import ZCRMModuleRelatedList
                except ImportError:
                    from Operations import ZCRMModuleRelatedList
                relatedlist_ins=ZCRMModuleRelatedList.get_instance(related_list['api_name'])
                relatedlist_instances.append(relatedlist_ins.set_relatedlist_properties(related_list))
            bulk_api_response.data=relatedlist_instances
            return bulk_api_response
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())
    
    def get_relatedlist(self,relatedlist_id):
        try:
            handler_ins=APIHandler()
            handler_ins.request_url_path="settings/related_lists/"+str(relatedlist_id)
            handler_ins.request_method=APIConstants.REQUEST_METHOD_GET
            handler_ins.add_param('module', self.module_instance.api_name)
            api_response=APIRequest(handler_ins).get_api_response()
            response_json=api_response.response_json
            related_list=response_json[APIConstants.RELATED_LISTS][0]
            try:
                from .Operations import ZCRMModuleRelatedList
            except ImportError:
                from Operations import ZCRMModuleRelatedList
            relatedlist_ins=ZCRMModuleRelatedList.get_instance(related_list['api_name'])
            api_response.data=relatedlist_ins.set_relatedlist_properties(related_list)
            return api_response
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())
        
    def construct_json_for_cv_update(self,customview_instance):
        cv_settings=dict()
        if customview_instance.sort_by is not None:
            cv_settings['sort_by']=customview_instance.sort_by
        if customview_instance.sort_order is not None:
            cv_settings['sort_order']=customview_instance.sort_order
        input_json=dict()
        input_json[APIConstants.CUSTOM_VIEWS]=[cv_settings]
        return input_json
      
    def construct_json_for_module_update(self,module_instance):
        module_settings=dict()
        if module_instance.per_page is not None:
            module_settings['per_page']=module_instance.per_page
        if module_instance.business_card_fields is not None:
            module_settings['business_card_fields']=module_instance.business_card_fields
        if module_instance.default_custom_view is not None:
            custom_view_dict=dict()
            custom_view_dict['id']=module_instance.default_custom_view.id
            module_settings['default_custom_view']=custom_view_dict
        if module_instance.default_territory_id is not None:
            territory_dict=dict()
            territory_dict['id']=module_instance.default_territory_id
            module_settings['territory']=territory_dict
        if module_instance.related_list_properties is not None:
            prop_arr=dict()
            prop_arr['sort_by']=module_instance.related_list_properties.sort_by
            prop_arr['sort_order']=module_instance.related_list_properties.sort_order
            prop_arr['fields']=module_instance.related_list_properties.fields
            module_settings['related_list_properties']=prop_arr
        input_json=dict()
        input_json[APIConstants.MODULES]=[module_settings]
        return input_json
    def get_zcrm_customview(self,customview_details,categories):
        try:
            from .Operations import ZCRMCustomView,ZCRMCustomViewCriteria
        except ImportError:
            from Operations import ZCRMCustomView,ZCRMCustomViewCriteria
        customview_instance = ZCRMCustomView.get_instance(customview_details['id'],self.module_instance.api_name)
        customview_instance.display_value=customview_details['display_value']
        customview_instance.is_default=bool(customview_details['default'])
        customview_instance.name=customview_details['name']
        customview_instance.system_name=customview_details['system_name']
        customview_instance.sort_by=customview_details['sort_by'] if 'sort_by' in customview_details else None
        customview_instance.category=customview_details['category'] if 'category' in customview_details else None
        customview_instance.fields=customview_details['fields'] if 'fields' in customview_details else None
        customview_instance.favorite=customview_details['favorite'] if 'favorite' in customview_details else None
        customview_instance.sort_order=customview_details['sort_order'] if 'sort_order' in customview_details else None
        if 'criteria' in  customview_details and customview_details['criteria'] is not None:
            criteria_list=customview_details['criteria']
            if isinstance(criteria_list, list):
                criteria_pattern=""
                length=len(criteria_list)
                criteria_instances=list()
                criteria_index=1
                for i in range(0,length):
                    criteria=criteria_list[i]
                    if criteria=='or' or criteria=='and':
                        criteria_pattern=criteria_pattern+criteria+" "
                    else:
                        criteria_instance=ZCRMCustomViewCriteria.get_instance()
                        criteria_instance.field=criteria['field'] if 'field' in criteria else None
                        criteria_instance.value=criteria['value'] if 'value' in criteria else None
                        criteria_instance.comparator=criteria['comparator'] if 'comparator' in criteria else None
                        criteria_pattern=criteria_pattern+str(criteria_index)+" "
                        criteria_index=criteria_index+1
                        criteria_instances.append(criteria_instance)
                customview_instance.criteria=criteria_instances
                customview_instance.criteria_pattern=criteria_pattern
            else:
                criteria_instance=ZCRMCustomViewCriteria.get_instance()
                criteria_instance.field=criteria_list['field'] if 'field' in criteria_list else None
                criteria_instance.value=criteria_list['value'] if 'value' in criteria_list else None
                criteria_instance.comparator=criteria_list['comparator'] if 'comparator' in criteria_list else None
                customview_instance.criteria=[criteria_instance]
        if categories is not None:
            try:
                from .Operations import ZCRMCustomViewCategory
            except ImportError:
                from Operations import ZCRMCustomViewCategory
            category_instances=list()
            for category in categories:
                cv_category_instance=ZCRMCustomViewCategory.get_instance()
                cv_category_instance.display_value=categories[category]
                cv_category_instance.actual_value=category
                category_instances.append(cv_category_instance)
            customview_instance.categories=category_instances
        if 'offline' in customview_details:
            customview_instance.is_off_line=customview_details['offline']
        
        return customview_instance
    
    def get_zcrmlayout(self,layout_details):
        try:
            from .Operations import ZCRMLayout,ZCRMUser,ZCRMProfile
        except ImportError:
            from Operations import ZCRMLayout,ZCRMUser,ZCRMProfile
        layout_instance=ZCRMLayout.get_instance(layout_details['id'])
        layout_instance.created_time=layout_details['created_time']
        layout_instance.modified_time=layout_details['modified_time']
        layout_instance.name=layout_details['name']
        layout_instance.is_visible=bool(layout_details['visible'])
        if layout_details['created_by'] is not None:
            layout_instance.created_by=ZCRMUser.get_instance(layout_details['created_by']['id'],layout_details['created_by']['name'])
        if layout_details['modified_by'] is not None:
            layout_instance.modified_by=ZCRMUser.get_instance(layout_details['modified_by']['id'],layout_details['modified_by']['name'])
        
        accessible_profile_arr=layout_details['profiles']
        accessible_profile_instances=list()
        for profile in accessible_profile_arr:
            profile_ins=ZCRMProfile.get_instance(profile['id'],profile['name'])
            profile_ins.is_default=bool(profile['default'])
            accessible_profile_instances.append(profile_ins)
        layout_instance.accessible_profiles=accessible_profile_instances
        layout_instance.sections=self.get_all_sections_of_layout(layout_details['sections'])
        layout_instance.status=layout_details['status']
        if 'convert_mapping' in layout_details:
            try:
                from .Operations import ZCRMLeadConvertMapping,ZCRMLeadConvertMappingField
            except ImportError:
                from Operations import ZCRMLeadConvertMapping,ZCRMLeadConvertMappingField
            convert_modules=['Contacts','Deals','Accounts']
            for convert_module in convert_modules:
                if convert_module in layout_details['convert_mapping']:
                    convert_map=layout_details['convert_mapping'][convert_module]
                    convert_map_ins=ZCRMLeadConvertMapping.get_instance(convert_map['name'],convert_map['id'])
                    if 'fields' in convert_map:
                        field_data=convert_map['fields']
                        for each_field_data in field_data:
                            convert_mapping_field_ins=ZCRMLeadConvertMappingField.get_instance(each_field_data['api_name'],each_field_data['id'])
                            convert_mapping_field_ins.field_label=each_field_data['field_label']
                            convert_mapping_field_ins.is_required=bool(each_field_data['required'])
                            convert_map_ins.fields.append(convert_mapping_field_ins)
                    layout_instance.convert_mapping[convert_module]=convert_map_ins
        return layout_instance
    
    def get_all_sections_of_layout(self,all_section_details):
        section_instances=list()
        try:
            from .Operations import ZCRMSection
        except ImportError:
            from Operations import ZCRMSection
        for section in all_section_details:
            section_ins=ZCRMSection.get_instance(section['name'])
            section_ins.display_label=section['display_label']
            section_ins.column_count=int(section['column_count'])
            section_ins.sequence_number=int(section['sequence_number'])
            section_ins.fields=self.get_section_fields(section['fields'])
            section_instances.append(section_ins)
        return section_instances
        
    def get_section_fields(self,fields):
        section_fields=list()
        for field in fields:
            section_fields.append(self.get_zcrmfield(field))
        return section_fields

    def get_zcrmfield(self,field_details):
        try:
            from .Operations import ZCRMField,ZCRMLayout,ZCRMCustomViewCriteria
        except ImportError:
            from Operations import ZCRMField,ZCRMLayout,ZCRMCustomViewCriteria
        field_instance=ZCRMField.get_instance(field_details['api_name'])
        field_instance.sequence_number=int(field_details['sequence_number']) if 'sequence_number' in field_details else None
        field_instance.id=field_details['id']
        field_instance.is_mandatory=bool(field_details['required']) if 'required' in field_details else None
        field_instance.default_value=field_details['default_value'] if 'default_value' in field_details else None
        field_instance.is_custom_field=bool(field_details['custom_field']) if 'custom_field' in field_details else None
        field_instance.is_visible=bool(field_details['visible']) if 'visible' in field_details else None
        field_instance.field_label=field_details['field_label'] if 'field_label' in field_details else None
        field_instance.length=int(field_details['length']) if 'length' in field_details else None
        field_instance.created_source=field_details['created_source'] if 'created_source' in field_details else None
        field_instance.is_read_only=bool(field_details['read_only']) if 'read_only' in field_details else None
        field_instance.is_business_card_supported=bool(field_details['businesscard_supported']) if 'businesscard_supported' in field_details else None
        field_instance.data_type=field_details['data_type'] if 'data_type' in field_details else None
        field_instance.convert_mapping=field_details['convert_mapping'] if 'convert_mapping' in field_details else None
        
        if 'view_type' in field_details:
            viewtype_dict=field_details['view_type']
            field_layout_permissions=list()
            if viewtype_dict['view']:
                field_layout_permissions.append('VIEW')
            if viewtype_dict['quick_create']:
                field_layout_permissions.append('QUICK_CREATE')
            if viewtype_dict['create']:
                field_layout_permissions.append('CREATE')
            if viewtype_dict['edit']:
                field_layout_permissions.append('EDIT')
            field_instance.field_layout_permissions=field_layout_permissions
        if 'pick_list_values' in field_details:
            picklist_arr=field_details['pick_list_values']
            if len(picklist_arr)>0:
                picklist_instance_arr=list()
                for picklist in picklist_arr:
                    picklist_instance_arr.append(self.get_picklist_value_instance(picklist))
                field_instance.picklist_values=picklist_instance_arr
            
        if 'lookup' in field_details and len(field_details['lookup'])>0:
            field_instance.lookup_field=self.get_lookup_field_instance(field_details['lookup'])
        
        if 'unique' in field_details and len(field_details['unique'])>0:
            field_instance.is_unique_field=True
            field_instance.is_case_sensitive=bool(field_details['unique']['casesensitive'])
            
        if 'decimal_place' in field_details and field_details['decimal_place'] is not None:
            field_instance.decimal_place=field_details['decimal_place']
        
        if 'json_type' in field_details and field_details['json_type'] is not None:
            field_instance.json_type=field_details['json_type']
            
        if 'formula' in field_details and len(field_details['formula'])>0:
            field_instance.is_formula_field=True
            field_instance.formula_return_type=field_details['formula']['return_type']
            field_instance.formula_expression=field_details['formula']['expression'] if 'expression' in field_details['formula'] else None
        
        if 'currency' in field_details and len(field_details['currency'])>0:
            field_instance.is_currency_field=True
            field_instance.precision=int(field_details['currency']['precision']) if 'precision' in field_details['currency'] else None
            field_instance.rounding_option=field_details['currency']['rounding_option'] if 'rounding_option' in field_details['currency'] else None
        
        if 'auto_number' in field_details and len(field_details['auto_number'])>0:
            field_instance.is_auto_number=True
            field_instance.prefix=field_details['auto_number']['prefix'] if 'prefix' in field_details['auto_number'] else None
            field_instance.suffix=field_details['auto_number']['suffix'] if 'suffix' in field_details['auto_number'] else None
            field_instance.start_number=field_details['auto_number']['start_number'] if 'start_number' in field_details['auto_number'] else None

        field_instance.display_label = field_details['display_label'] if 'display_label' in field_details else None
        field_instance.field_label = field_details['field_label'] if 'field_label' in field_details else None
        field_instance.tooltip = field_details['tooltip'] if 'tooltip' in field_details else None
        if 'association_details' in field_details and field_details['association_details'] is not None:
            associationdict = dict(field_details['association_details'])
            for keys in associationdict.keys():
                related_or_lookup_field = dict(associationdict[keys])
                if related_or_lookup_field is not None:
                    field_dict = dict()
                    for field_key in related_or_lookup_field.keys():
                        field_dict[field_key] = related_or_lookup_field[field_key]
                    field_instance.association_details[keys] = field_dict
        field_instance.is_webhook = bool(field_details['webhook']) if 'webhook' in field_details else None
        if 'crypt' in field_details and field_details['crypt'] is not None:
            try:
                from .Operations import ZCRMTransitionCrypt
            except Exception:
                from Operations import ZCRMTransitionCrypt
            crypt_dict = field_details['crypt']
            crypt_instance = ZCRMTransitionCrypt.get_instance()
            crypt_instance.mode = crypt_dict['mode'] if 'mode' in crypt_dict else None
            crypt_instance.column = crypt_dict['column'] if 'column' in crypt_dict else None
            crypt_instance.table = crypt_dict['table'] if 'table' in crypt_dict else None
            crypt_instance.status = crypt_dict['status'] if 'status' in crypt_dict else None
            field_instance.crypt = crypt_instance
        field_instance.created_source = field_details['created_source'] if 'created_source' in field_details else None
        field_instance.column_name = field_details['column_name'] if 'column_name' in field_details else None
        field_instance.type = field_details['_type'] if '_type' in field_details else None
        field_instance.is_history_tracking = bool(field_details['history_tracking']) if 'history_tracking' in field_details else None
        field_instance.is_system_mandatory = bool(field_details['system_mandatory']) if 'system_mandatory' in field_details else None

        if 'related_details' in field_details and len(field_details['related_details']) > 0:
            field_instance.related_details = self.get_lookup_field_instance(field_details['related_details'])
        field_instance.transition_sequence = field_details['transition_sequence'] if 'transition_sequence' in field_details else None
        if 'layouts' in field_details and field_details['layouts'] is not None:
            layout_dict = field_details['layouts']
            layout_instance = ZCRMLayout.get_instance(layout_dict['id'])
            layout_instance.name = layout_dict['name']
            field_instance.layouts = layout_instance
        if 'criteria' in field_details and field_details['criteria'] is not None:
            criteria_instance = ZCRMCustomViewCriteria.get_instance()
            criteria_instance.comparator = field_details['criteria']['comparator']
            criteria_instance.value = field_details['criteria']['value']
            field_instance.criteria = criteria_instance

        return field_instance
    def get_picklist_value_instance(self,picklist):
        try:
            from .Operations import ZCRMPickListValue
        except ImportError:
            from Operations import ZCRMPickListValue
        picklist_ins=ZCRMPickListValue.get_instance()
        picklist_ins.display_value=picklist['display_value']
        picklist_ins.actual_value=picklist['actual_value']
        if 'sequence_number' in picklist and picklist['sequence_number'] is not None:
            picklist_ins.sequence_number=picklist['sequence_number']
        if 'maps' in picklist:
            picklist_ins.maps=picklist['maps']
            
        return picklist_ins
    
    def get_lookup_field_instance(self,lookup_field_details):
        try:
            from .Operations import ZCRMLookupField,ZCRMBlueprintRelatedModule
        except ImportError:
            from Operations import ZCRMLookupField,ZCRMBlueprintRelatedModule
        lookup_field_instance=ZCRMLookupField.get_instance(lookup_field_details['api_name'])
        lookup_field_instance.display_label=lookup_field_details['display_label'] if 'display_label' in lookup_field_details else None
        lookup_field_instance.id=lookup_field_details['id']
        lookup_field_instance.module=lookup_field_details['module']
        if (isinstance(lookup_field_details['module'], dict)):
            moduledict = lookup_field_details['module']
            relatedmodule_instance = ZCRMBlueprintRelatedModule.get_instance(moduledict['id'])
            relatedmodule_instance.display_label = moduledict['display_label'] if 'display_label' in moduledict else None
            relatedmodule_instance.module_name = moduledict['module_name'] if 'display_label' in moduledict else None
            lookup_field_instance.module = relatedmodule_instance
        else:
            lookup_field_instance.module = lookup_field_details['module']
        lookup_field_instance.type = lookup_field_details['_type'] if '_type' in lookup_field_details else None
        lookup_field_instance.field_label = lookup_field_details['field_label'] if 'field_label' in lookup_field_details else None
        return lookup_field_instance

    def get_zcrmlayouts(self,layouts):
        layout_instances=list()
        for each_layout_details in layouts:
            layout_instances.append(self.get_zcrmlayout(each_layout_details))
        return layout_instances
    
    def get_zcrmfields(self,fields):
        field_instances=list()
        for field in fields:
            field_instances.append(self.get_zcrmfield(field))
        return field_instances
    
class MetaDataAPIHandler(APIHandler):
    
    @staticmethod
    def get_instance():
        return MetaDataAPIHandler()
    
    def get_all_modules(self):
        try:
            handler_ins=APIHandler()
            handler_ins.request_url_path="settings/modules"
            handler_ins.request_method=APIConstants.REQUEST_METHOD_GET
            handler_ins.request_api_key=APIConstants.MODULES
            bulk_api_response=APIRequest(handler_ins).get_bulk_api_response()
            modules_json=bulk_api_response.response_json[APIConstants.MODULES]
            module_ins_list=list()
            for module_json in modules_json:
                module_ins_list.append(self.get_zcrmmodule(module_json))
            bulk_api_response.data=module_ins_list
            return bulk_api_response
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())
            
    def get_module(self,module_api_name):
        try:
            handler_ins=APIHandler()
            handler_ins.request_url_path="settings/modules/"+module_api_name
            handler_ins.request_method=APIConstants.REQUEST_METHOD_GET
            handler_ins.request_api_key=APIConstants.MODULES
            api_response=APIRequest(handler_ins).get_api_response()
            module_json=api_response.response_json[APIConstants.MODULES][0]
            api_response.data=self.get_zcrmmodule(module_json)
            return api_response
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())
        
        
    def get_zcrmmodule(self,module_details):
        try:
            from .Operations import ZCRMModule
        except ImportError:
            from Operations import ZCRMModule
        crmmodule_instance=ZCRMModule.get_instance(module_details[APIConstants.API_NAME])
        crmmodule_instance.is_viewable=bool(module_details['viewable'])
        crmmodule_instance.is_creatable=bool(module_details['creatable'])
        crmmodule_instance.is_convertable=bool(module_details['convertable'])
        crmmodule_instance.is_editable=bool(module_details['editable'])
        crmmodule_instance.is_deletable=bool(module_details['deletable'])
        crmmodule_instance.web_link=module_details['web_link'] if 'web_link' in module_details else None
        crmmodule_instance.singular_label=module_details['singular_label']
        crmmodule_instance.plural_label=module_details['plural_label']
        crmmodule_instance.id=module_details['id']
        crmmodule_instance.modified_time=module_details['modified_time']
        crmmodule_instance.is_api_supported=bool(module_details['api_supported'])
        crmmodule_instance.is_scoring_supported=bool(module_details['scoring_supported'])
        crmmodule_instance.module_name=module_details['module_name']
        crmmodule_instance.business_card_field_limit=int(module_details['business_card_field_limit']) if 'business_card_field_limit' in module_details else None
        crmmodule_instance.sequence_number=module_details['sequence_number'] if 'sequence_number' in module_details else None
        crmmodule_instance.is_global_search_supported=bool(module_details['global_search_supported']) if 'global_search_supported' in module_details else None
        try:
            from .Operations import ZCRMUser,ZCRMProfile,ZCRMModuleRelatedList
        except ImportError:
            from Operations import ZCRMUser,ZCRMProfile,ZCRMModuleRelatedList
        if module_details['modified_by'] is not None:
            crmmodule_instance.modified_by=ZCRMUser.get_instance(module_details['modified_by']["id"],module_details['modified_by']["name"])
        
        crmmodule_instance.is_custom_module='custom'==module_details['generated_type'] if 'generated_type' in module_details else None
        
        if 'business_card_fields' in module_details:
            crmmodule_instance.business_card_fields=module_details['business_card_fields']
        
        profiles=module_details['profiles']
        for profile in profiles:
            crmmodule_instance.profiles.append(ZCRMProfile.get_instance(profile['id'],profile['name']))
        
        if 'display_field' in module_details and module_details['display_field'] is not None:
            crmmodule_instance.display_field_name=module_details['display_field']
            #crmmodule_instance.display_field_id=module_details['display_field']['id']) if 'id' in module_details['display_field'] else None
        
        if 'related_lists' in module_details and module_details['related_lists'] is not None:
            relatedlists=module_details['related_lists']
            relatedlist_instances=list()
            for relatedlist in relatedlists:
                module_relatedlist_ins=ZCRMModuleRelatedList.get_instance(relatedlist['api_name'])
                relatedlist_instances.append(module_relatedlist_ins.set_relatedlist_properties(relatedlist))
            crmmodule_instance.related_lists=relatedlist_instances
        
        if 'layouts' in module_details and module_details['layouts'] is not None:
            crmmodule_instance.layouts=ModuleAPIHandler.get_instance(ZCRMModule.get_instance(module_details[APIConstants.API_NAME])).get_zcrmlayouts(module_details['layouts'])
        
        if 'fields' in module_details and module_details['fields'] is not None:
            crmmodule_instance.fields=ModuleAPIHandler.get_instance(ZCRMModule.get_instance(module_details[APIConstants.API_NAME])).get_zcrmfields(module_details['fields'])
        
        if 'related_list_properties' in module_details and module_details['related_list_properties'] is not None:
            crmmodule_instance.related_list_properties=self.get_relatedlist_property_instance(module_details['related_list_properties'])
        
        if '$properties' in module_details and module_details['$properties'] is not None:
            crmmodule_instance.properties=module_details['$properties']
            
        if 'per_page' in module_details and module_details['per_page'] is not None:
            crmmodule_instance.per_page=int(module_details['per_page'])
        
        if 'search_layout_fields' in module_details and module_details['search_layout_fields'] is not None:
            crmmodule_instance.search_layout_fields=module_details['search_layout_fields']
        
        if 'custom_view' in module_details and module_details['custom_view'] is not None:
            crmmodule_instance.default_custom_view=ModuleAPIHandler.get_instance(ZCRMModule.get_instance(module_details[APIConstants.API_NAME])).get_zcrm_customview(module_details['custom_view'],None)
            crmmodule_instance.default_custom_view_id=module_details['custom_view']['id']
        
        if 'territory' in module_details and module_details['territory'] is not None:
            crmmodule_instance.default_territory_id=module_details['territory']['id']
            crmmodule_instance.default_territory_name=module_details['territory']['name']
            
        return crmmodule_instance
            
    def get_relatedlist_property_instance(self,relatedlist_property):
        try:
            from .Operations import ZCRMRelatedListProperties
        except ImportError:
            from Operations import ZCRMRelatedListProperties
        reltedlist_property_instance=ZCRMRelatedListProperties.get_instance()
        reltedlist_property_instance.sort_by=relatedlist_property['sort_by'] if 'sort_by' in relatedlist_property else None
        reltedlist_property_instance.sort_order=relatedlist_property['sort_order'] if 'sort_order' in relatedlist_property else None
        reltedlist_property_instance.fields=relatedlist_property['fields'] if 'fields' in relatedlist_property else None
        return reltedlist_property_instance
    
class OrganizationAPIHandler(APIHandler):
    
    @staticmethod
    def get_instance():
        return OrganizationAPIHandler()
    
    def get_organization_details(self):
        try:
            handler_ins=APIHandler()
            handler_ins.request_url_path="org"
            handler_ins.request_method=APIConstants.REQUEST_METHOD_GET
            handler_ins.request_api_key=APIConstants.ORG
            api_response=APIRequest(handler_ins).get_api_response()
            org_json=api_response.response_json[APIConstants.ORG][0]
            api_response.data=self.get_zcrm_organization(org_json)
            return api_response
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())
            
    def get_all_roles(self):
        try:
            handler_ins=APIHandler()
            handler_ins.request_url_path="settings/roles"
            handler_ins.request_method=APIConstants.REQUEST_METHOD_GET
            handler_ins.request_api_key=APIConstants.ROLES
            bulk_api_response=APIRequest(handler_ins).get_bulk_api_response()
            roles=bulk_api_response.response_json[APIConstants.ROLES]
            role_instances=list()
            for role in roles:
                role_instances.append(self.get_zcrm_role(role))
            bulk_api_response.data=role_instances
            return bulk_api_response
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())
    
    def get_role(self,role_id):
        try:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            if role_id is None:
                CommonUtil.raise_exception('Role_GET',"role id must be given",'ROLE ID IS NOT PROVIDED',"ROLE ID")
            handler_ins=APIHandler()
            handler_ins.request_url_path="settings/roles/"+str(role_id)
            handler_ins.request_method=APIConstants.REQUEST_METHOD_GET
            handler_ins.request_api_key=APIConstants.ROLES
            api_response=APIRequest(handler_ins).get_api_response()
            role=api_response.response_json[APIConstants.ROLES][0]
            api_response.data=self.get_zcrm_role(role)
            return api_response
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())
    def get_all_profiles(self):
        try:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            handler_ins=APIHandler()
            handler_ins.request_url_path="settings/profiles"
            handler_ins.request_method=APIConstants.REQUEST_METHOD_GET
            handler_ins.request_api_key=APIConstants.PROFILES
            bulk_api_response=APIRequest(handler_ins).get_api_response()
            profiles=bulk_api_response.response_json[handler_ins.request_api_key]
            profile_instances=list()
            for profile in profiles:
                profile_instances.append(self.get_zcrm_profile(profile))
            bulk_api_response.data=profile_instances
            return bulk_api_response
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())
    def get_profile(self,profile_id):
        try:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            if profile_id is None:
                CommonUtil.raise_exception('Profile_GET',"profile id must be given",'PROFILE ID IS NOT PROVIDED',"PROFILE ID")
            handler_ins=APIHandler()
            handler_ins.request_url_path="settings/profiles/"+str(profile_id)
            handler_ins.request_method=APIConstants.REQUEST_METHOD_GET
            handler_ins.request_api_key=APIConstants.PROFILES
            api_response=APIRequest(handler_ins).get_api_response()
            profile=api_response.response_json[handler_ins.request_api_key][0]
            api_response.data=self.get_zcrm_profile(profile)
            return api_response
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())
    def create_user(self,user_instance):
        try:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            if user_instance is None:
                CommonUtil.raise_exception('User_POST',"user instance must be given",'USER INSTANCE IS NOT PROVIDED',"USER INSTANCE ID")
            handler_ins=APIHandler()
            handler_ins.request_url_path="users"
            handler_ins.request_method=APIConstants.REQUEST_METHOD_POST
            handler_ins.request_api_key=APIConstants.USERS
            handler_ins.request_body=self.construct_json_from_user_instance(user_instance)
            return APIRequest(handler_ins).get_api_response()
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())
            
    def update_user(self,user_instance):
        try:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            if user_instance is None or user_instance.id is None:
                CommonUtil.raise_exception('User_PUT',"user instance and id must be given",'USER INSTANCE OR ID IS NOT PROVIDED',"USER INSTANCE ID")
            handler_ins=APIHandler()
            handler_ins.request_url_path="users/"+str(user_instance.id)
            handler_ins.request_method=APIConstants.REQUEST_METHOD_PUT
            handler_ins.request_api_key=APIConstants.USERS
            handler_ins.request_body=self.construct_json_from_user_instance(user_instance)
            return APIRequest(handler_ins).get_api_response()
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())
            
    def delete_user(self,user_id):
        try:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            if user_id is None :
                CommonUtil.raise_exception('User_DELETE',"user id must be given",'USER ID IS NOT PROVIDED',"USER ID")
            handler_ins=APIHandler()
            handler_ins.request_url_path="users/"+str(user_id)
            handler_ins.request_method=APIConstants.REQUEST_METHOD_DELETE
            handler_ins.request_api_key=APIConstants.USERS
            return APIRequest(handler_ins).get_api_response()
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())
            
    def get_user(self,user_id):
        try:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            if user_id is None:
                CommonUtil.raise_exception('User_GET',"user id must be given",'USER ID IS NOT PROVIDED',"USER ID")
            handler_ins=APIHandler()
            handler_ins.request_url_path="users/"+str(user_id)
            handler_ins.request_method=APIConstants.REQUEST_METHOD_GET
            handler_ins.request_api_key=APIConstants.USERS
            api_response= APIRequest(handler_ins).get_api_response()
            api_response.data=self.get_zcrm_user(api_response.response_json[APIConstants.USERS][0])
            return api_response
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())
    
    def get_all_users(self,page,per_page):
        return self.get_users(None,page,per_page)
    def get_all_deactive_users(self,page,per_page):
        return self.get_users('DeactiveUsers',page,per_page)
    def get_all_active_users(self,page,per_page):
        return self.get_users('ActiveUsers',page,per_page)
    def get_all_confirmed_users(self,page,per_page):
        return self.get_users('ConfirmedUsers',page,per_page)
    def get_all_not_confirmed_users(self,page,per_page):
        return self.get_users('NotConfirmedUsers',page,per_page)
    def get_all_deleted_users(self,page,per_page):
        return self.get_users('DeletedUsers',page,per_page)
    def get_all_active_confirmed_users(self,page,per_page):
        return self.get_users('ActiveConfirmedUsers',page,per_page)
    def get_all_admin_users(self,page,per_page):
        return self.get_users('AdminUsers',page,per_page)
    def get_all_active_confirmed_admin_users(self,page,per_page):
        return self.get_users('ActiveConfirmedAdmins',page,per_page)
    def get_current_user(self):
        return self.get_users('CurrentUser',1,200)
    def get_users(self,user_type,page,per_page):
        try:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            handler_ins=APIHandler()
            if user_type is not None:
                handler_ins.add_param('type', user_type)
            handler_ins.request_url_path="users"
            handler_ins.add_param('page', page)
            handler_ins.add_param('per_page', per_page)
            handler_ins.request_method=APIConstants.REQUEST_METHOD_GET
            handler_ins.request_api_key=APIConstants.USERS
            bulk_api_response= APIRequest(handler_ins).get_bulk_api_response()
            users_json=bulk_api_response.response_json[APIConstants.USERS]
            user_instances=list()
            for user_details in users_json:
                user_instances.append(self.get_zcrm_user(user_details))
            bulk_api_response.data=user_instances
            return bulk_api_response
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            CommonUtil.raise_exception(handler_ins.request_url_path,ex.__str__(),traceback.format_stack())

    def get_organization_taxes(self):
        try:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            handler_ins = APIHandler()
            handler_ins.request_url_path = 'org/taxes'
            handler_ins.request_method = APIConstants.REQUEST_METHOD_GET
            handler_ins.request_api_key = APIConstants.TAXES
            bulk_api_response = APIRequest(handler_ins).get_bulk_api_response()
            org_tax_json = bulk_api_response.response_json[APIConstants.TAXES]
            org_tax_instances = list()
            for org_tax_details in org_tax_json:
                org_tax_instances.append(self.get_zcrm_org_tax(org_tax_details))
            bulk_api_response.data = org_tax_instances
            return bulk_api_response

        except ZCRMException as ex:
            raise ex

        except Exception as ex:
            CommonUtil.raise_exception(handler_ins.request_url_path, ex.__str__(), traceback.format_stack())

    def get_organization_tax(self, org_tax_id):
        try:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            handler_ins = APIHandler()
            handler_ins.request_url_path = 'org/taxes/' + org_tax_id
            handler_ins.request_method = APIConstants.REQUEST_METHOD_GET
            handler_ins.request_api_key = APIConstants.TAXES
            api_response = APIRequest(handler_ins).get_api_response()
            api_response.data = self.get_zcrm_org_tax(api_response.response_json[APIConstants.TAXES][0])
            return api_response
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            CommonUtil.raise_exception(handler_ins.request_url_path, ex.__str__(), traceback.format_stack())

    def create_organization_taxes(self, orgtax_instances):
        try:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            if len(orgtax_instances) > 100:
                CommonUtil.raise_exception('OrgTax_Create', "orgtax instances count must be less than or equals to 100",
                                           'MORE ORGTAX PROVIDED', "MORE ORGTAX")
            handler_ins = APIHandler()
            handler_ins.request_url_path = 'org/taxes'
            handler_ins.request_method = APIConstants.REQUEST_METHOD_POST
            handler_ins.request_api_key = APIConstants.TAXES
            org_tax_array = list()
            for orgtax_instance in orgtax_instances:
                if orgtax_instance.id is None:
                    org_tax_array.append(self.get_zcrmorgtax_as_json(orgtax_instance))
                else:
                    CommonUtil.raise_exception('OrgTax_Create', "orgtax id must be None", 'ORGTAX ID PROVIDED',
                                               "ORGTAX ID")
            request_json = dict()
            request_json[APIConstants.TAXES] = org_tax_array
            handler_ins.request_body = request_json
            bulk_api_response = APIRequest(handler_ins).get_bulk_api_response()
            return bulk_api_response
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            CommonUtil.raise_exception(handler_ins.request_url_path, ex.__str__(), traceback.format_stack())

    def update_organization_taxes(self, orgtax_instances):
        try:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            if len(orgtax_instances) > 100:
                CommonUtil.raise_exception('OrgTax_Update', "orgtax instances count must be less than or equals to 100",
                                           'MORE ORGTAX PROVIDED', "MORE ORGTAX")
            handler_ins = APIHandler()
            handler_ins.request_url_path = 'org/taxes'
            handler_ins.request_method = APIConstants.REQUEST_METHOD_PUT
            handler_ins.request_api_key = APIConstants.TAXES
            org_tax_array = list()
            for orgtax_instance in orgtax_instances:
                if orgtax_instance.id is None:
                    CommonUtil.raise_exception('OrgTax_Update', "orgtax id must not be be None", 'ORGTAX ID NOT PROVIDED',
                                               "ORGTAX ID")
                else:
                    org_tax_array.append(self.get_zcrmorgtax_as_json(orgtax_instance))

            request_json = dict()
            request_json[APIConstants.TAXES] = org_tax_array
            handler_ins.request_body = request_json
            bulk_api_response = APIRequest(handler_ins).get_bulk_api_response()
            return bulk_api_response
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            CommonUtil.raise_exception(handler_ins.request_url_path, ex.__str__(), traceback.format_stack())

    def delete_organization_taxes(self, orgtax_ids):
        try:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            if len(orgtax_ids) > 100:
                CommonUtil.raise_exception('OrgTax_delete',
                                           "orgtax ids count must be less than or equals to 100",
                                           'MORE ORGTAX IDS PROVIDED', "MORE ORGTAX")
            handler_ins = APIHandler()
            handler_ins.request_url_path = 'org/taxes'
            handler_ins.request_method = APIConstants.REQUEST_METHOD_DELETE
            handler_ins.request_api_key = APIConstants.TAXES
            ids_as_string = ','.join(str(orgtax_id) for orgtax_id in orgtax_ids)
            handler_ins.add_param('ids', ids_as_string)

            bulk_api_response = APIRequest(handler_ins).get_bulk_api_response()

            return bulk_api_response
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            CommonUtil.raise_exception(handler_ins.request_url_path, ex.__str__(), traceback.format_stack())

    def delete_organization_tax(self, orgtax_id):
        try:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil

            handler_ins = APIHandler()
            handler_ins.request_url_path = 'org/taxes/' + orgtax_id
            handler_ins.request_method = APIConstants.REQUEST_METHOD_DELETE
            handler_ins.request_api_key = APIConstants.TAXES
            api_response = APIRequest(handler_ins).get_api_response()
            return api_response
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            CommonUtil.raise_exception(handler_ins.request_url_path, ex.__str__(), traceback.format_stack())

    def get_zcrmorgtax_as_json(self,orgtax_instance):
        orgtax_as_json=dict()

        if orgtax_instance.id is not None:
            orgtax_as_json['id']=str(orgtax_instance.id)
        if orgtax_instance.name is not None:
            orgtax_as_json['name'] = str(orgtax_instance.name)
        if orgtax_instance.display_label is not None:
            orgtax_as_json['display_label'] = str(orgtax_instance.display_label)
        if orgtax_instance.value is not None:
            orgtax_as_json['value'] = str(orgtax_instance.value)
        if orgtax_instance.sequence_number is not None:
            orgtax_as_json['sequence_number'] = str(orgtax_instance.sequence_number)

        return orgtax_as_json

    def get_zcrm_org_tax(self, orgtax_details):
        try:
            from .Operations import ZCRMOrgTax
        except ImportError:
            from Operations import ZCRMOrgTax

        org_tax_instance = ZCRMOrgTax.get_instance(orgtax_details['id'],orgtax_details['name'])
        org_tax_instance.display_label = orgtax_details['name']
        org_tax_instance.value = orgtax_details['value']
        return org_tax_instance

    def construct_json_from_user_instance(self,user_instance):
        user_info_json=dict()
        if user_instance.role is not None:
            user_info_json['role']=str(user_instance.role.id)
        if user_instance.profile is not None:
            user_info_json['profile']=str(user_instance.profile.id)
        if user_instance.country is not None:
            user_info_json['country']=user_instance.country
        if user_instance.name is not None:
            user_info_json['name']=user_instance.name
        if user_instance.city is not None:
            user_info_json['city']=user_instance.city
        if user_instance.signature is not None:
            user_info_json['signature']=user_instance.signature
        if user_instance.name_format is not None:
            user_info_json['name_format']=user_instance.name_format
        if user_instance.language is not None:
            user_info_json['language']=user_instance.language
        if user_instance.locale is not None:
            user_info_json['locale']=user_instance.locale
        if user_instance.is_personal_account is not None:
            user_info_json['personal_account']=bool(user_instance.is_personal_account)
        if user_instance.default_tab_group is not None:
            user_info_json['default_tab_group']=user_instance.default_tab_group
        if user_instance.street is not None:
            user_info_json['street']=user_instance.street
        if user_instance.alias is not None:
            user_info_json['alias']=user_instance.alias
        if user_instance.state is not None:
            user_info_json['state']=user_instance.state
        if user_instance.country_locale is not None:
            user_info_json['country_locale']=user_instance.country_locale
        if user_instance.fax is not None:
            user_info_json['fax']=user_instance.fax
        if user_instance.first_name is not None:
            user_info_json['first_name']=user_instance.first_name
        if user_instance.email is not None:
            user_info_json['email']=user_instance.email
        if user_instance.zip is not None:
            user_info_json['zip']=user_instance.zip
        if user_instance.decimal_separator is not None:
            user_info_json['decimal_separator']=user_instance.decimal_separator
        if user_instance.website is not None:
            user_info_json['website']=user_instance.website
        if user_instance.time_format is not None:
            user_info_json['time_format']=user_instance.time_format
        if user_instance.mobile is not None:
            user_info_json['mobile']=user_instance.mobile
        if user_instance.last_name is not None:
            user_info_json['last_name']=user_instance.last_name
        if user_instance.time_zone is not None:
            user_info_json['time_zone']=user_instance.time_zone
        if user_instance.phone is not None:
            user_info_json['phone']=user_instance.phone
        if user_instance.dob is not None:
            user_info_json['dob']=user_instance.dob
        if user_instance.date_format is not None:
            user_info_json['date_format']=user_instance.date_format
        if user_instance.status is not None:
            user_info_json['status']=user_instance.status
        customFieldsData=user_instance.field_apiname_vs_value
        for key in customFieldsData:
            user_info_json[key]=customFieldsData[key]
        try:
            from .Utility import CommonUtil
        except ImportError:
            from Utility import CommonUtil
        return CommonUtil.create_api_supported_input_json(user_info_json,APIConstants.USERS)
    def get_zcrm_role(self,role_details):
        try:
            from .Operations import ZCRMRole,ZCRMUser
        except ImportError:
            from Operations import ZCRMRole,ZCRMUser
        role_instance=ZCRMRole.get_instance(role_details['id'],role_details['name'])
        role_instance.display_label=role_details['display_label']
        role_instance.is_admin=bool(role_details['admin_user'])
        if 'reporting_to' in role_details and role_details['reporting_to'] is not None:
            role_instance.reporting_to = ZCRMRole.get_instance(role_details['reporting_to']['id'],role_details['reporting_to']['name'])
        if 'forecast_manager' in role_details and role_details['forecast_manager'] is not None:
            role_instance.forecast_manager = ZCRMUser.get_instance(role_details['forecast_manager']['id'], role_details['forecast_manager']['name'])
        if 'share_with_peers' in role_details:
            role_instance.share_with_peers = role_details['share_with_peers']
        return role_instance
    def get_zcrm_profile(self,profile_details):
        try:
            from .Operations import ZCRMProfile,ZCRMUser,ZCRMPermission,ZCRMProfileSection,ZCRMProfileCategory 
        except ImportError:
            from Operations import ZCRMProfile,ZCRMUser,ZCRMPermission,ZCRMProfileSection,ZCRMProfileCategory
        profile_instance=ZCRMProfile.get_instance(profile_details['id'], profile_details['name'])
        profile_instance.created_time=profile_details['created_time']
        profile_instance.modified_time=profile_details['modified_time']
        profile_instance.description=profile_details['description']
        profile_instance.category=profile_details['category']
        if profile_details['modified_by'] is not None:
            profile_instance.modified_by=ZCRMUser.get_instance(profile_details['modified_by']['id'], profile_details['modified_by']['name'])
        if profile_details['created_by'] is not None:
            profile_instance.created_by=ZCRMUser.get_instance(profile_details['created_by']['id'], profile_details['created_by']['name'])
        if 'permissions_details' in profile_details:
            permissions=profile_details['permissions_details']
            for permission in permissions:
                permission_ins=ZCRMPermission.get_instance(permission['name'],permission['id'])
                permission_ins.display_label=permission['display_label']
                permission_ins.module=permission['module']
                permission_ins.is_enabled=bool(permission['enabled'])
                profile_instance.permissions.append(permission_ins)
        if 'sections' in profile_details:
            sections=profile_details['sections']
            for section in sections:
                profile_section_instance=ZCRMProfileSection.get_instance(section['name'])
                if 'categories' in section:
                    categories=section['categories']
                    for category in categories:
                        category_ins=ZCRMProfileCategory.get_instance(category['name'])
                        category_ins.display_label=category['display_label']
                        category_ins.permission_ids=category['permissions_details']
                        category_ins.module=category['module'] if 'module' in category else None
                        profile_section_instance.categories.append(category_ins)
                profile_instance.sections.append(profile_section_instance)
        return profile_instance
    def get_zcrm_organization(self,org_details):
        try:
            from .Org import ZCRMOrganization
        except ImportError:
            from Org import ZCRMOrganization
        org_instance=ZCRMOrganization.get_instance(org_details['company_name'],org_details['id'])
        org_instance.alias=org_details['alias']
        org_instance.city=org_details['city']
        org_instance.country=org_details['country']
        org_instance.country_code=org_details['country_code']
        org_instance.currency_locale=org_details['currency_locale']
        org_instance.currency_symbol=org_details['currency_symbol']
        org_instance.description=org_details['description']
        org_instance.employee_count=org_details['employee_count']
        org_instance.fax=org_details['fax']
        org_instance.is_gapps_enabled=bool(org_details['gapps_enabled'])
        org_instance.iso_code=org_details['iso_code']
        org_instance.mc_status=org_details['mc_status']
        org_instance.mobile=org_details['mobile']
        
        org_instance.phone=org_details['phone']
        org_instance.primary_email=org_details['primary_email']
        org_instance.primary_zuid=org_details['primary_zuid']
        org_instance.state=org_details['state']
        org_instance.street=org_details['street']
        org_instance.time_zone=org_details['time_zone']
        org_instance.website=org_details['website']
        org_instance.zgid=org_details['zgid']
        org_instance.zip_code=org_details['zip']
        
        if org_details['license_details'] is not None:
            license_details=org_details['license_details']
            org_instance.is_paid_account=bool(license_details['paid'])
            org_instance.paid_type=license_details['paid_type']
            org_instance.paid_expiry=license_details['paid_expiry']
            org_instance.trial_type=license_details['trial_type']
            org_instance.trial_expiry=license_details['trial_expiry']
        return org_instance
    def get_zcrm_user(self,user_details):
        try:
            from .Operations import ZCRMUser,ZCRMRole,ZCRMProfile
        except ImportError:
            from Operations import ZCRMUser,ZCRMRole,ZCRMProfile
        user_instance=ZCRMUser.get_instance(user_details['id'],user_details['name'] if 'name' in user_details else None)
        user_instance.country=user_details['country'] if 'country' in user_details else None
        if 'role' in user_details:
            user_instance.role=ZCRMRole.get_instance(user_details['role']['id'],user_details['role']['name'])
        if 'customize_info' in user_details:
            user_instance.customize_info=self.get_zcrm_user_customizeinfo(user_details['customize_info'])
        user_instance.city=user_details['city'] if 'city' in user_details else None
        user_instance.signature=user_details['signature'] if 'signature' in user_details else None
        user_instance.name_format=user_details['name_format'] if 'name_format' in user_details else None
        user_instance.language=user_details['language'] if 'language' in user_details else None
        user_instance.locale=user_details['locale'] if 'locale' in user_details else None
        user_instance.is_personal_account=bool(user_details['personal_account']) if 'personal_account' in user_details else None
        user_instance.default_tab_group=user_details['default_tab_group'] if 'default_tab_group' in user_details else None
        user_instance.alias=user_details['alias'] if 'alias' in user_details else None
        user_instance.street=user_details['street'] if 'street' in user_details else None
        user_instance.city=user_details['city'] if 'city' in user_details else None
        if 'theme' in user_details:
            user_instance.theme=self.get_zcrm_user_theme(user_details['theme'])
        user_instance.state=user_details['state'] if 'state' in user_details else None
        user_instance.country_locale=user_details['country_locale'] if 'country_locale' in user_details else None
        user_instance.fax=user_details['fax'] if 'fax' in user_details else None
        user_instance.first_name=user_details['first_name'] if 'first_name' in user_details else None
        user_instance.email=user_details['email'] if 'email' in user_details else None
        user_instance.zip=user_details['zip'] if 'zip' in user_details else None
        user_instance.decimal_separator=user_details['decimal_separator'] if 'decimal_separator' in user_details else None
        user_instance.website=user_details['website'] if 'website' in user_details else None
        user_instance.time_format=user_details['time_format'] if 'time_format' in user_details else None
        if 'profile' in user_details:
            user_instance.profile=ZCRMProfile.get_instance(user_details['profile']['id'],user_details['profile']['name'])
        user_instance.mobile=user_details['mobile'] if 'mobile' in user_details else None
        user_instance.last_name=user_details['last_name'] if 'last_name' in user_details else None
        user_instance.time_zone=user_details['time_zone'] if 'time_zone' in user_details else None
        user_instance.zuid=user_details['zuid'] if 'zuid' in user_details else None
        user_instance.is_confirm=bool(user_details['confirm']) if 'confirm' in user_details else None
        user_instance.full_name=user_details['full_name'] if 'full_name' in user_details else None
        user_instance.phone=user_details['phone'] if 'phone' in user_details else None
        user_instance.dob=user_details['dob'] if 'dob' in user_details else None
        user_instance.date_format=user_details['date_format'] if 'date_format' in user_details else None
        user_instance.status=user_details['status'] if 'status' in user_details else None
        if 'territories' in user_details:
            user_instance.territories=user_details['territories']
        if 'reporting_to' in user_details:
            user_instance.reporting_to=user_details['reporting_to']
        if 'Currency' in user_details:
            user_instance.currency=user_details['Currency']
        user_instance.created_by=user_details['created_by'] if 'created_by' in user_details else None
        user_instance.modified_by=user_details['Modified_By'] if 'Modified_By' in user_details else None
        if 'Isonline' in user_details:
            user_instance.is_online=user_details['Isonline']
        user_instance.created_time=user_details['created_time'] if 'created_time' in user_details else None
        user_instance.modified_time=user_details['Modified_Time'] if 'Modified_Time' in user_details else None
        try:
            for userkey in user_details:
                if userkey not in ZCRMUser.defaultKeys:
                    user_instance.field_apiname_vs_value[userkey]=user_details[userkey]
        except Exception as e:
            pass
        return user_instance
    def get_zcrm_user_customizeinfo(self,customize_info):
        try:
            from .Operations import ZCRMUserCustomizeInfo
        except ImportError:
            from Operations import ZCRMUserCustomizeInfo
        customize_info_instance=ZCRMUserCustomizeInfo.get_instance()
        customize_info_instance.notes_desc=customize_info['notes_desc']
        customize_info_instance.is_to_show_right_panel=bool(customize_info['show_right_panel']) if 'show_right_panel' in customize_info else None
        customize_info_instance.is_bc_view=customize_info['bc_view']
        customize_info_instance.is_to_show_home=bool(customize_info['show_home']) if 'show_home' in customize_info else None
        customize_info_instance.is_to_show_detail_view=bool(customize_info['show_detail_view']) if 'show_detail_view' in customize_info else None
        customize_info_instance.unpin_recent_item=customize_info['unpin_recent_item']
        return customize_info_instance
    
    def get_zcrm_user_theme(self,user_theme_info):
        try:
            from .Operations import ZCRMUserTheme
        except ImportError:
            from Operations import ZCRMUserTheme
        user_theme_instance=ZCRMUserTheme.get_instance()
        user_theme_instance.normal_tab_font_color=user_theme_info['normal_tab']['font_color']
        user_theme_instance.normal_tab_background=user_theme_info['normal_tab']['background']
        user_theme_instance.selected_tab_font_color=user_theme_info['selected_tab']['font_color']
        user_theme_instance.selected_tab_background=user_theme_info['selected_tab']['background']
        return user_theme_instance

class TagAPIHandler(APIHandler):
    def __init__(self, module_instance):
        self.module_instance = module_instance

    @staticmethod
    def get_instance(module_ins=None):
        return TagAPIHandler(module_ins)

    def get_tags(self):
        try:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil

            handler_ins = APIHandler()
            handler_ins.request_url_path = "settings/tags"
            handler_ins.request_method = APIConstants.REQUEST_METHOD_GET
            handler_ins.request_api_key = APIConstants.TAG
            handler_ins.add_param('module', self.module_instance.api_name)
            bulk_api_response = APIRequest(handler_ins).get_bulk_api_response()
            tags_json = bulk_api_response.response_json[APIConstants.TAG]
            tag_list = []
            for tag_details in tags_json:
                tag_list.append(self.get_zcrmtag(tag_details))
            bulk_api_response.data = tag_list
            return bulk_api_response
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            CommonUtil.raise_exception(handler_ins.request_url_path, ex.__str__(), traceback.format_stack())

    def get_tag_count(self, tag_id):
        try:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil

            handler_ins = APIHandler()
            handler_ins.request_url_path = 'settings/tags/' + tag_id + '/actions/records_count'
            handler_ins.request_method = APIConstants.REQUEST_METHOD_GET
            handler_ins.add_param('module',self.module_instance.api_name)
            api_response = APIRequest(handler_ins).get_api_response()
            tags_json = api_response.response_json
            api_response.data = self.get_zcrmtag(tags_json)
            return api_response
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            CommonUtil.raise_exception(handler_ins.request_url_path, ex.__str__(), traceback.format_stack())

    def create_tags(self,tag_instances):
        try:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            if len(tag_instances) > 50:
                CommonUtil.raise_exception('Tags_Create', "Tag instances count must be less than or equals to 50",
                                           'MORE TAGS PROVIDED', "MORE TAGs")
            if len(tag_instances) < 1:
                CommonUtil.raise_exception('Tags_Update', "Tag instances count must be atleast 1",
                                           'NO TAGS PROVIDED', "NO TAGs")
            handler_ins = APIHandler()
            handler_ins.request_url_path = 'settings/tags'
            handler_ins.add_param('module', self.module_instance.api_name)
            handler_ins.request_method = APIConstants.REQUEST_METHOD_POST
            handler_ins.request_api_key = APIConstants.TAG
            tag_array= list()
            for tag_instance in tag_instances:
                if tag_instance.id is None:
                    tag_array.append(self.get_zcrmtag_as_json(tag_instance))
                else:
                    CommonUtil.raise_exception('Tags_Create', "TAG id must be None", 'TAG ID PROVIDED',
                                               "TAG ID")
            request_json = dict()
            request_json[APIConstants.TAG] = tag_array
            handler_ins.request_body = request_json
            bulk_api_response = APIRequest(handler_ins).get_bulk_api_response()
            entity_responses = bulk_api_response.bulk_entity_response
            length = len(entity_responses)
            created_tags=list()

            for i in range(0, length):
                entity_response_ins = entity_responses[i]
                if entity_response_ins.status == APIConstants.STATUS_SUCCESS:
                    tag_create_details = entity_response_ins.details
                    new_tag = self.get_zcrmtag(tag_create_details)
                    new_tag.name = tag_instances[i].name
                    created_tags.append(new_tag)
                    entity_response_ins.data = new_tag
            bulk_api_response.data = created_tags
            return bulk_api_response
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            CommonUtil.raise_exception(handler_ins.request_url_path, ex.__str__(), traceback.format_stack())
    def update_tags(self,tag_instances):
        try:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            if len(tag_instances) > 50:
                CommonUtil.raise_exception('Tags_Update', "Tag instances count must be less than or equals to 50",
                                           'MORE TAGS PROVIDED', "MORE TAGs")
            if len(tag_instances) < 1:
                CommonUtil.raise_exception('Tags_Update', "Tag instances count must be atleast 1",
                                           'NO TAGS PROVIDED', "NO TAGs")
            handler_ins = APIHandler()
            handler_ins.request_url_path = 'settings/tags'
            handler_ins.add_param('module', self.module_instance.api_name)
            handler_ins.request_method = APIConstants.REQUEST_METHOD_PUT
            handler_ins.request_api_key = APIConstants.TAG
            tag_array= list()
            for tag_instance in tag_instances:
                if tag_instance.id is None:
                    CommonUtil.raise_exception('Tags_Update', "TAG id must be None", 'TAG ID PROVIDED',
                                               "TAG ID")
                else:
                    tag_array.append(self.get_zcrmtag_as_json(tag_instance))
            request_json = dict()
            request_json[APIConstants.TAG] = tag_array
            handler_ins.request_body = request_json
            bulk_api_response = APIRequest(handler_ins).get_bulk_api_response()
            entity_responses = bulk_api_response.bulk_entity_response
            length = len(entity_responses)
            updated_tags=list()
            for i in range(0, length):
                entity_response_ins = entity_responses[i]
                if entity_response_ins.status == APIConstants.STATUS_SUCCESS:
                    tag_create_details = entity_response_ins.details
                    new_tag = self.get_zcrmtag(tag_create_details)
                    new_tag.name = tag_instances[i].name
                    updated_tags.append(new_tag)
                    entity_response_ins.data = new_tag
            bulk_api_response.data = updated_tags
            return bulk_api_response
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            CommonUtil.raise_exception(handler_ins.request_url_path, ex.__str__(), traceback.format_stack())

    def add_tags_to_multiple_records(self, tag_list, record_list):
        try:
            try:
                from .Utility import CommonUtil
                from .Operations import ZCRMRecord, ZCRMTag
            except ImportError:
                from Utility import CommonUtil
                from Operations import ZCRMRecord, ZCRMTag
            if len(tag_list) > 50:
                CommonUtil.raise_exception('add_tags_to_multiple_records', "Tag names count must be less than or equals to 50",
                                           'MORE TAGS PROVIDED', "MORE TAGs")
            if len(tag_list) < 1:
                CommonUtil.raise_exception('add_tags_to_multiple_records', "Tag names count must be atleast 1",
                                           'NO TAGS PROVIDED', "NO TAGs")
            if len(record_list) > 100:
                CommonUtil.raise_exception('add_tags_to_multiple_records', "record id count must be less than or equals to 100",
                                           'MORE RECORDS PROVIDED', "MORE RECORDS")
            if len(record_list) < 1:
                CommonUtil.raise_exception('add_tags_to_multiple_records', "record id count must be atleast 1",
                                           'NO RECORDS PROVIDED', "NO RECORDS")
            handler_ins = APIHandler()
            handler_ins.request_url_path = self.module_instance.api_name + '/actions/add_tags'
            handler_ins.request_method = APIConstants.REQUEST_METHOD_POST
            handler_ins.request_api_key = APIConstants.DATA
            record_ids_as_string = ','.join(str(record_id) for record_id in record_list)
            tag_names_as_string = ','.join(str(tag_name) for tag_name in tag_list)
            handler_ins.add_param('ids', record_ids_as_string)
            handler_ins.add_param('tag_names', tag_names_as_string)
            bulk_api_response = APIRequest(handler_ins).get_bulk_api_response()
            entity_responses = bulk_api_response.bulk_entity_response
            length = len(entity_responses)
            records=list()
            for i in range(0, length):
                entity_response_ins = entity_responses[i]
                if entity_response_ins.status == APIConstants.STATUS_SUCCESS:
                    tag_added_details = entity_response_ins.details
                    record = ZCRMRecord.get_instance(self.module_instance.api_name, tag_added_details['id'])
                    for tag in tag_added_details['tags']:
                        record.tag_list.append(ZCRMTag.get_instance(None, tag))
                    records.append(record)
                    entity_response_ins.data = record
            bulk_api_response.data = records
            return bulk_api_response
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            CommonUtil.raise_exception(handler_ins.request_url_path, ex.__str__(), traceback.format_stack())

    def remove_tags_from_multiple_records(self, tag_list, record_list):
        try:
            try:
                from .Utility import CommonUtil
                from .Operations import ZCRMRecord, ZCRMTag
            except ImportError:
                from Utility import CommonUtil
                from Operations import ZCRMRecord, ZCRMTag
            if len(tag_list) > 50:
                CommonUtil.raise_exception('remove_tags_to_multiple_records', "Tag names count must be less than or equals to 50",
                                           'MORE TAGS PROVIDED', "MORE TAGs")
            if len(tag_list) < 1:
                CommonUtil.raise_exception('remove_tags_to_multiple_records', "Tag names count must be atleast 1",
                                           'NO TAGS PROVIDED', "NO TAGs")
            if len(record_list) > 100:
                CommonUtil.raise_exception('remove_tags_to_multiple_records', "record id count must be less than or equals to 100",
                                           'MORE RECORDS PROVIDED', "MORE RECORDS")
            if len(record_list) < 1:
                CommonUtil.raise_exception('remove_tags_to_multiple_records', "record id count must be atleast 1",
                                           'NO RECORDS PROVIDED', "NO RECORDS")
            handler_ins = APIHandler()
            handler_ins.request_url_path = self.module_instance.api_name + '/actions/remove_tags'
            handler_ins.request_method = APIConstants.REQUEST_METHOD_POST
            handler_ins.request_api_key = APIConstants.DATA
            record_ids_as_string = ','.join(str(record_id) for record_id in record_list)
            tag_names_as_string = ','.join(str(tag_name) for tag_name in tag_list)
            handler_ins.add_param('ids', record_ids_as_string)
            handler_ins.add_param('tag_names', tag_names_as_string)
            bulk_api_response = APIRequest(handler_ins).get_bulk_api_response()
            entity_responses = bulk_api_response.bulk_entity_response
            length = len(entity_responses)
            records=list()
            for i in range(0, length):
                entity_response_ins = entity_responses[i]
                if entity_response_ins.status == APIConstants.STATUS_SUCCESS:
                    tag_added_details = entity_response_ins.details
                    record = ZCRMRecord.get_instance(self.module_instance.api_name,tag_added_details['id'])
                    for tag in tag_added_details['tags']:
                        record.tag_list.append(ZCRMTag.get_instance(None, tag))
                    records.append(record)
                    entity_response_ins.data = record
            bulk_api_response.data = records
            return bulk_api_response
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            CommonUtil.raise_exception(handler_ins.request_url_path, ex.__str__(), traceback.format_stack())

    def add_tags(self, record, tag_list):
        try:
            try:
                from .Utility import CommonUtil
                from .Operations import ZCRMTag
            except ImportError:
                from Utility import CommonUtil
                from Operations import ZCRMTag
            if len(tag_list) > 10:
                CommonUtil.raise_exception('add_tags', "Tag names count must be less than or equals to 10",
                                           'MORE TAGS PROVIDED', "MORE TAGs")
            if len(tag_list) < 1:
                CommonUtil.raise_exception('add_tags', "Tag names count must be atleast 1",
                                           'NO TAGS PROVIDED', "NO TAGs")
            if record is None or record.entity_id is None :
                CommonUtil.raise_exception('add_tags', "no record given",
                                           'NO RECORD PROVIDED', "NO RECORD")
            handler_ins = APIHandler()
            handler_ins.request_url_path = record.module_api_name + '/'+record.entity_id+ '/actions/add_tags'
            handler_ins.request_method = APIConstants.REQUEST_METHOD_POST
            handler_ins.request_api_key = APIConstants.DATA
            tag_names_as_string = ','.join(str(tag_name) for tag_name in tag_list)
            handler_ins.add_param('tag_names', tag_names_as_string)
            api_response = APIRequest(handler_ins).get_api_response()
            response_details = api_response.response_json[APIConstants.DATA][0]['details']
            EntityAPIHandler.get_instance(record).set_record_properties(response_details)
            api_response.data = record
            return api_response
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            CommonUtil.raise_exception(handler_ins.request_url_path, ex.__str__(), traceback.format_stack())

    def remove_tags(self, record, tag_list):
        try:
            try:
                from .Utility import CommonUtil
                from .Operations import ZCRMTag
            except ImportError:
                from Utility import CommonUtil
                from Operations import ZCRMTag
            if len(tag_list) > 10:
                CommonUtil.raise_exception('remove_tags', "Tag names count must be less than or equals to 10",
                                           'MORE TAGS PROVIDED', "MORE TAGs")
            if len(tag_list) < 1:
                CommonUtil.raise_exception('remove_tags', "Tag names count must be atleast 1",
                                           'NO TAGS PROVIDED', "NO TAGs")
            if record is None or record.entity_id is None :
                CommonUtil.raise_exception('remove_tags', "no record given",
                                           'NO RECORD PROVIDED', "NO RECORD")
            handler_ins = APIHandler()
            handler_ins.request_url_path = record.module_api_name + '/'+record.entity_id + '/actions/remove_tags'
            handler_ins.request_method = APIConstants.REQUEST_METHOD_POST
            handler_ins.request_api_key = APIConstants.DATA
            tag_names_as_string = ','.join(str(tag_name) for tag_name in tag_list)
            handler_ins.add_param('tag_names', tag_names_as_string)
            api_response = APIRequest(handler_ins).get_api_response()
            response_details = api_response.response_json[APIConstants.DATA][0]['details']
            EntityAPIHandler.get_instance(record).set_record_properties(response_details)
            api_response.data = record
            return api_response
        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            CommonUtil.raise_exception(handler_ins.request_url_path, ex.__str__(), traceback.format_stack())

    def delete(self, tag_id):
        try:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil

            if tag_id is None :
                CommonUtil.raise_exception('delete', "no tag id given",'NO TAG ID PROVIDED', "NO TAG ID")
            handler_ins = APIHandler()
            handler_ins.request_url_path = 'settings/tags/' + tag_id
            handler_ins.request_method = APIConstants.REQUEST_METHOD_DELETE
            handler_ins.request_api_key = APIConstants.TAG
            api_response = APIRequest(handler_ins).get_api_response()
            return api_response

        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            CommonUtil.raise_exception(handler_ins.request_url_path, ex.__str__(), traceback.format_stack())

    def merge(self, tag_id, merge_tag_id):
        try:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil

            if tag_id is None :
                CommonUtil.raise_exception('merge', "no tag id given",'NO TAG ID PROVIDED', "NO TAG ID")
            if merge_tag_id is None:
                CommonUtil.raise_exception('merge', "no merge tag id given", 'NO MERGE TAG ID PROVIDED'
                                           , "NO MERGE TAG ID")
            handler_ins = APIHandler()
            handler_ins.request_url_path = 'settings/tags/' + merge_tag_id + '/actions/merge'
            handler_ins.request_method = APIConstants.REQUEST_METHOD_POST
            handler_ins.request_api_key = APIConstants.TAG
            tag_json = dict()
            tag_json["conflict_id"] = tag_id
            handler_ins.request_body = CommonUtil.create_api_supported_input_json(tag_json, APIConstants.TAG)
            api_response = APIRequest(handler_ins).get_api_response()
            response_details = api_response.response_json[APIConstants.TAG][0]['details']
            api_response.data = self.get_zcrmtag(response_details)
            return api_response

        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            CommonUtil.raise_exception(handler_ins.request_url_path, ex.__str__(), traceback.format_stack())

    def update(self, tag):
        try:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil

            if tag is None :
                CommonUtil.raise_exception('update', "no tag provided",'NO TAG  PROVIDED', "NO TAG ")

            handler_ins = APIHandler()
            handler_ins.request_url_path = 'settings/tags/' + tag.id
            handler_ins.request_method = APIConstants.REQUEST_METHOD_PUT
            handler_ins.add_param('module', tag.module_apiname)
            handler_ins.request_api_key = APIConstants.TAG
            tag_json=dict()
            tag_json["name"] = tag.name
            handler_ins.request_body = CommonUtil.create_api_supported_input_json(tag_json, APIConstants.TAG)
            api_response = APIRequest(handler_ins).get_api_response()
            response_details = api_response.response_json[APIConstants.TAG][0]['details']
            tag = self.get_zcrmtag(response_details)
            api_response.data = tag
            return api_response

        except ZCRMException as ex:
            raise ex
        except Exception as ex:
            CommonUtil.raise_exception(handler_ins.request_url_path, ex.__str__(), traceback.format_stack())


    def get_zcrmtag(self, tag_details):
        try:
            from .Operations import ZCRMTag, ZCRMUser
        except ImportError:
            from Operations import ZCRMTag, ZCRMUser
        tag_instance = ZCRMTag.get_instance(tag_details['id'] if 'id' in tag_details else None,
                                            tag_details['name'] if 'name' in tag_details else None)

        if 'created_by' in tag_details and tag_details['created_by'] is not None:
            tag_instance.created_by = ZCRMUser.get_instance(tag_details['created_by']['id']
                                                            , tag_details['created_by']['name'])
        if 'modified_by' in tag_details and tag_details['modified_by'] is not None:
            tag_instance.modified_by = ZCRMUser.get_instance(tag_details['modified_by']['id']
                                                            , tag_details['modified_by']['name'])
        tag_instance.created_time = tag_details['created_time'] if 'created_time' in tag_details else None
        tag_instance.modified_time = tag_details['modified_time'] if 'modified_time' in tag_details else None
        tag_instance.count = tag_details['count'] if 'count' in tag_details else None

        return tag_instance

    def get_zcrmtag_as_json(self, tag_ins):
        tag_json = dict()
        if tag_ins.name is not None:
            tag_json['name'] = tag_ins.name
        if tag_ins.id is not None:
            tag_json['id'] = str(tag_ins.id)
        return tag_json


class VariableAPIHandler(APIHandler):
    def __init__(self):
        self.variable = None

    @staticmethod
    def get_instance():
        return VariableAPIHandler()

    def get_variables(self):
        try:
            from .Operations import ZCRMVariable
            from .Operations import ZCRMVariableGroup
        except Exception:
            from Operations import ZCRMVariable
            from Operations import ZCRMVariableGroup
        try:
            handler_ins = APIHandler()
            handler_ins.request_url_path = "settings/variables"
            handler_ins.request_method = APIConstants.REQUEST_METHOD_GET
            handler_ins.add_header("Content-Type", "application/json")
            handler_ins.request_api_key = "variables"
            response = APIRequest(handler_ins).get_bulk_api_response()
            response_json = response.response_json
            data = response_json["variables"]
            data_list = list()
            for json_data in data:
                variables_ins = ZCRMVariable.get_instance()
                self.get_variables_res_as_obj(json_data, variables_ins)
                data_list.append(variables_ins)

            response.data = data_list
            return response

        except ZCRMException as ex:
            print(ex.status_code)

    def get_variables_res_as_obj(self, json_data, entity_instance):
        try:
            from .Operations import ZCRMVariable
            from .Operations import ZCRMVariableGroup
        except Exception:
            from Operations import ZCRMVariable
            from Operations import ZCRMVariableGroup
        for key, value in json_data.items():

            if "id" == key:
                entity_instance.id = value

            elif "name" == key:
                entity_instance.name = value

            elif "api_name" == key:
                entity_instance.api_name = value

            elif "type" == key:
                entity_instance.type = value

            elif "value" == key:
                entity_instance.value = value

            elif "variable_group" == key:
                ZCRMVariableGroup_ins = ZCRMVariableGroup.get_instance()
                ZCRMVariableGroup_ins.id = value['id']
                ZCRMVariableGroup_ins.api_name = value['api_name']
                entity_instance.variable_group = ZCRMVariableGroup_ins

            elif "description" == key:
                entity_instance.description = value

    def get_variable(self, group):
        try:
            from .Operations import ZCRMVariable
            from .Operations import ZCRMVariableGroup
        except Exception:
            from Operations import ZCRMVariable
            from Operations import ZCRMVariableGroup
        try:
            handler_ins = APIHandler()
            handler_ins.request_url_path = "settings/variables/" + self.variable.id
            handler_ins.request_method = APIConstants.REQUEST_METHOD_GET
            handler_ins.add_header("Content-Type", "application/json")
            if group is not None:
                handler_ins.add_param("group", group)
            handler_ins.request_api_key = "variables"
            response = APIRequest(handler_ins).get_api_response()
            response_json = response.response_json
            data = response_json["variables"]
            json_data = data[0]
            variables_ins = ZCRMVariable.get_instance()
            self.get_variable_res_as_obj(json_data, variables_ins)
            response.data = variables_ins
            return response

        except ZCRMException as ex:
            print(ex.status_code)

    def get_variable_res_as_obj(self, json_data, entity_instance):
        try:
            from .Operations import ZCRMVariable
            from .Operations import ZCRMVariableGroup
        except Exception:
            from Operations import ZCRMVariable
            from Operations import ZCRMVariableGroup
        for key, value in json_data.items():
            if "id" == key:
                entity_instance.id = value

            elif "name" == key:
                entity_instance.name = value

            elif "api_name" == key:
                entity_instance.api_name = value

            elif "type" == key:
                entity_instance.type = value

            elif "value" == key:
                entity_instance.value = value

            elif "variable_group" == key:
                ZCRMVariableGroup_ins = ZCRMVariableGroup.get_instance()
                ZCRMVariableGroup_ins.id = value['id']
                ZCRMVariableGroup_ins.api_name = value['api_name']
                entity_instance.variable_group = ZCRMVariableGroup_ins

            elif "description" == key:
                entity_instance.description = value

    def create_variables(self, variables):
        try:
            from .Operations import ZCRMVariable
            from .Operations import ZCRMVariableGroup
        except Exception:
            from Operations import ZCRMVariable
            from Operations import ZCRMVariableGroup
        try:
            handler_ins = APIHandler()
            handler_ins.request_url_path = "settings/variables"
            handler_ins.request_method = APIConstants.REQUEST_METHOD_POST
            handler_ins.add_header("Content-Type", "application/json")
            handler_ins.request_api_key = "variables"
            request_body = dict()
            data_list = list()
            for each_variable in variables:
                data_object = self.convert_object_to_json(each_variable)
                data_list.append(data_object)

            request_body['variables'] = data_list
            handler_ins.request_body = request_body
            response = APIRequest(handler_ins).get_bulk_api_response()
            return response

        except ZCRMException as ex:
            print(ex.status_code)

    def convert_object_to_json(self, entity_instance):
        try:
            from .Operations import ZCRMVariable
            from .Operations import ZCRMVariableGroup
        except Exception:
            from Operations import ZCRMVariable
            from Operations import ZCRMVariableGroup
        variables_json = dict()
        if bool(entity_instance.id):
            variables_json['id'] = entity_instance.id

        if bool(entity_instance.name):
            variables_json['name'] = entity_instance.name

        if bool(entity_instance.api_name):
            variables_json['api_name'] = entity_instance.api_name

        if bool(entity_instance.type):
            variables_json['type'] = entity_instance.type

        if bool(entity_instance.value):
            variables_json['value'] = entity_instance.value

        if bool(entity_instance.variable_group):
            variable_group_json = dict()
            variable_group = entity_instance.variable_group
            if bool(variable_group.id):
                variable_group_json['id'] = variable_group.id

            if bool(variable_group.api_name):
                variable_group_json['api_name'] = variable_group.api_name

            variables_json['variable_group'] = variable_group_json

        if bool(entity_instance.description):
            variables_json['description'] = entity_instance.description

        return variables_json

    def update_variables(self, variables):
        try:
            from .Operations import ZCRMVariable
            from .Operations import ZCRMVariableGroup
        except Exception:
            from Operations import ZCRMVariable
            from Operations import ZCRMVariableGroup
        try:
            handler_ins = APIHandler()
            handler_ins.request_url_path = "settings/variables"
            handler_ins.request_method = APIConstants.REQUEST_METHOD_PUT
            handler_ins.add_header("Content-Type", "application/json")
            handler_ins.request_api_key = "variables"
            request_body = dict()
            data_list = list()
            for each_variable in variables:
                data_object = self.convert_object_to_json(each_variable)
                data_list.append(data_object)

            request_body['variables'] = data_list
            handler_ins.request_body = request_body
            response = APIRequest(handler_ins).get_bulk_api_response()
            return response

        except ZCRMException as ex:
            print(ex.status_code)

    def update_variable(self):
        try:
            from .Operations import ZCRMVariable
            from .Operations import ZCRMVariableGroup
        except Exception:
            from Operations import ZCRMVariable
            from Operations import ZCRMVariableGroup
        try:
            handler_ins = APIHandler()
            handler_ins.request_url_path = "settings/variables/" + self.variable.id
            handler_ins.request_method = APIConstants.REQUEST_METHOD_PUT
            handler_ins.add_header("Content-Type", "application/json")
            handler_ins.request_api_key = "variables"
            request_body = dict()
            data_list = list()
            data_object = self.convert_object_to_json(self.variable)
            data_list.append(data_object)
            request_body['variables'] = data_list
            handler_ins.request_body = request_body
            response = APIRequest(handler_ins).get_api_response()
            return response

        except ZCRMException as ex:
            print(ex.status_code)

    def delete_variable(self):
        try:
            from .Operations import ZCRMVariable
            from .Operations import ZCRMVariableGroup
        except Exception:
            from Operations import ZCRMVariable
            from Operations import ZCRMVariableGroup
        try:
            handler_ins = APIHandler()
            handler_ins.request_url_path = "settings/variables/" + self.variable.id
            handler_ins.request_method = APIConstants.REQUEST_METHOD_DELETE
            handler_ins.add_header("Content-Type", "application/json")
            handler_ins.request_api_key = "variables"
            request_body = dict()
            data_list = list()
            data_object = self.convert_object_to_json(self.variable)
            data_list.append(data_object)
            request_body['variables'] = data_list
            handler_ins.request_body = request_body
            response = APIRequest(handler_ins).get_api_response()
            return response

        except ZCRMException as ex:
            print(ex.status_code)


class VariableGroupAPIHandler(APIHandler):
    def __init__(self):
        self.variable_group = None

    @staticmethod
    def get_instance():
        return VariableGroupAPIHandler()

    def get_variable_groups(self):
        try:
            from .Operations import ZCRMVariableGroup
        except Exception:
            from Operations import ZCRMVariableGroup
        try:
            handler_ins = APIHandler()
            handler_ins.request_url_path = "settings/variable_groups"
            handler_ins.request_method = APIConstants.REQUEST_METHOD_GET
            handler_ins.add_header("Content-Type", "application/json")
            handler_ins.request_api_key = "variable_groups"
            response = APIRequest(handler_ins).get_bulk_api_response()
            response_json = response.response_json
            data = response_json["variable_groups"]
            data_list = list()
            for json_data in data:
                variable_groups_ins = ZCRMVariableGroup.get_instance()
                self.get_variable_groups_res_as_obj(json_data, variable_groups_ins)
                data_list.append(variable_groups_ins)

            response.data = data_list
            return response

        except ZCRMException as ex:
            print(ex.status_code)

    def get_variable_groups_res_as_obj(self, json_data, entity_instance):
        try:
            from .Operations import ZCRMVariableGroup
        except Exception:
            from Operations import ZCRMVariableGroup
        for key, value in json_data.items():
            if "id" == key:
                entity_instance.id = value

            elif "name" == key:
                entity_instance.name = value

            elif "api_name" == key:
                entity_instance.api_name = value

            elif "display_label" == key:
                entity_instance.display_label = value

            elif "description" == key:
                entity_instance.description = value

    def get_variable_group(self):
        try:
            from .Operations import ZCRMVariableGroup
        except Exception:
            from Operations import ZCRMVariableGroup
        try:
            handler_ins = APIHandler()
            handler_ins.request_url_path = "settings/variable_groups/" + self.variable_group.id
            handler_ins.request_method = APIConstants.REQUEST_METHOD_GET
            handler_ins.add_header("Content-Type", "application/json")
            handler_ins.request_api_key = "variable_groups"
            response = APIRequest(handler_ins).get_api_response()
            response_json = response.response_json
            data = response_json["variable_groups"]
            json_data = data[0]
            variable_groups_ins = ZCRMVariableGroup.get_instance()
            self.get_variable_group_res_as_obj(json_data, variable_groups_ins)
            response.data = variable_groups_ins
            return response

        except ZCRMException as ex:
            print(ex.status_code)

    def get_variable_group_res_as_obj(self, json_data, entity_instance):
        try:
            from .Operations import ZCRMVariableGroup
        except Exception:
            from Operations import ZCRMVariableGroup
        for key, value in json_data.items():
            if "id" == key:
                entity_instance.id = value

            elif "name" == key:
                entity_instance.name = value

            elif "api_name" == key:
                entity_instance.api_name = value

            elif "display_label" == key:
                entity_instance.display_label = value

            elif "description" == key:
                entity_instance.description = value


class BlueprintAPIHandler(object):

    def __init__(self,zcrmrecord,entity_type,entity_id):
        self.zcrmrecord = zcrmrecord
        self.entity_type = entity_type
        self.entity_id = entity_id

    @staticmethod
    def get_instance(zcrmrecord,entity_type,entity_id):
        return BlueprintAPIHandler(zcrmrecord,entity_type,entity_id)

    def update(self):
        try:
            apiresponse = EntityAPIHandler.get_instance(self.zcrmrecord).update_blueprint_data()
            apiresponse.data = self.zcrmrecord
            return apiresponse
        except ZCRMException as ex:
            raise ex

    def get(self):
        try:
            apiresponse = EntityAPIHandler.get_instance(self.zcrmrecord).get_blueprint_data()
            return apiresponse
        except ZCRMException as ex:
            raise ex