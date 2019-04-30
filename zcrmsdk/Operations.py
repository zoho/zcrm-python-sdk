'''
Created on Aug 16, 2017

@author: sumanth-3058
'''
class ZCRMModule(object):
    '''
    This class is to deal with Zoho CRM modules
    '''
    def __init__(self, module_apiname):
        '''
        Constructor
        '''
        self.api_name=module_apiname
        self.is_convertable=None
        self.is_creatable=None
        self.is_editable=None
        self.is_deletable=None
        self.web_link=None
        self.singular_label=None
        self.plural_label=None
        self.modified_by=None
        self.modified_time=None
        self.is_viewable=None
        self.is_api_supported=None
        self.is_custom_module=None
        self.is_scoring_supported=None
        self.id=None
        self.module_name=None
        self.business_card_field_limit=None
        self.business_card_fields=list()
        self.profiles=list()
        self.display_field_name=None
        self.display_field_id=None
        self.related_lists=None
        self.layouts=None
        self.fields=None
        self.related_list_properties=None
        self.properties=None
        self.per_page=None
        self.search_layout_fields=None
        self.default_territory_name=None
        self.default_territory_id=None
        self.default_custom_view_id=None
        self.default_custom_view=None
        self.is_global_search_supported=None
        self.sequence_number=None
    
    @staticmethod
    def get_instance(module_apiname):
        return ZCRMModule(module_apiname)
    def get_record(self,entityID):
        try:
            from .Handler import EntityAPIHandler
        except ImportError:
            from Handler import EntityAPIHandler
        record=ZCRMRecord.get_instance(self.api_name, entityID)
        return EntityAPIHandler.get_instance(record).get_record()
    def get_records(self,cvid=None,sort_by=None,sort_order=None,page=0,per_page=200):
        try:
            from .Handler import MassEntityAPIHandler
        except ImportError:
            from Handler import MassEntityAPIHandler
        return MassEntityAPIHandler.get_instance(self).get_records(cvid,sort_by,sort_order,page,per_page)
    def create_records(self,record_ins_list):
        try:
            from .Handler import MassEntityAPIHandler
        except ImportError:
            from Handler import MassEntityAPIHandler
        return MassEntityAPIHandler.get_instance(self).create_records(record_ins_list)
    def upsert_records(self,record_ins_list,duplicate_check_fields=None):
        try:
            from .Handler import MassEntityAPIHandler
        except ImportError:
            from Handler import MassEntityAPIHandler
        return MassEntityAPIHandler.get_instance(self).upsert_records(record_ins_list,duplicate_check_fields)
    def update_records(self,record_ins_list):
        try:
            from .Handler import MassEntityAPIHandler
        except ImportError:
            from Handler import MassEntityAPIHandler
        return MassEntityAPIHandler.get_instance(self).update_records(record_ins_list)
    def mass_update_records(self,entityid_list,field_api_name,value):
        try:
            from .Handler import MassEntityAPIHandler
        except ImportError:
            from Handler import MassEntityAPIHandler
        return MassEntityAPIHandler.get_instance(self).update_mass_records(entityid_list,field_api_name,value)
    def delete_records(self,entityid_list):
        try:
            from .Handler import MassEntityAPIHandler
        except ImportError:
            from Handler import MassEntityAPIHandler
        return MassEntityAPIHandler.get_instance(self).delete_records(entityid_list)
    def get_all_deleted_records(self):
        try:
            from .Handler import MassEntityAPIHandler
        except ImportError:
            from Handler import MassEntityAPIHandler
        return MassEntityAPIHandler.get_instance(self).get_all_deleted_records()
    def get_recyclebin_records(self):
        try:
            from .Handler import MassEntityAPIHandler
        except ImportError:
            from Handler import MassEntityAPIHandler
        return MassEntityAPIHandler.get_instance(self).get_recyclebin_records()
    def get_permanently_deleted_records(self):
        try:
            from .Handler import MassEntityAPIHandler
        except ImportError:
            from Handler import MassEntityAPIHandler
        return MassEntityAPIHandler.get_instance(self).get_permanently_deleted_records()
    def search_records(self,search_word,page=0,per_page=200):
        try:
            from .Handler import MassEntityAPIHandler
        except ImportError:
            from Handler import MassEntityAPIHandler
        return MassEntityAPIHandler.get_instance(self).search_records(search_word,page,per_page,'word')
    def search_records_by_phone(self,phone,page=0,per_page=200):
        try:
            from .Handler import MassEntityAPIHandler
        except ImportError:
            from Handler import MassEntityAPIHandler
        return MassEntityAPIHandler.get_instance(self).search_records(phone,page,per_page,'phone')
    def search_records_by_email(self,email,page=0,per_page=200):
        try:
            from .Handler import MassEntityAPIHandler
        except ImportError:
            from Handler import MassEntityAPIHandler
        return MassEntityAPIHandler.get_instance(self).search_records(email,page,per_page,'email')
    def search_records_by_criteria(self,criteria,page=0,per_page=200):
        try:
            from .Handler import MassEntityAPIHandler
        except ImportError:
            from Handler import MassEntityAPIHandler
        return MassEntityAPIHandler.get_instance(self).search_records(criteria,page,per_page,'criteria')
    def get_all_fields(self):
        try:
            from .Handler import ModuleAPIHandler
        except ImportError:
            from Handler import ModuleAPIHandler
        return ModuleAPIHandler.get_instance(self).get_all_fields()
    def get_field(self,field_id):
        try:
            from .Handler import ModuleAPIHandler
        except ImportError:
            from Handler import ModuleAPIHandler
        return ModuleAPIHandler.get_instance(self).get_field(field_id)
    def get_all_layouts(self):
        try:
            from .Handler import ModuleAPIHandler
        except ImportError:
            from Handler import ModuleAPIHandler
        return ModuleAPIHandler.get_instance(self).get_all_layouts()
    def get_layout(self,layout_id):
        try:
            from .Handler import ModuleAPIHandler
        except ImportError:
            from Handler import ModuleAPIHandler
        return ModuleAPIHandler.get_instance(self).get_layout(layout_id)
    def get_all_customviews(self):
        try:
            from .Handler import ModuleAPIHandler
        except ImportError:
            from Handler import ModuleAPIHandler
        return ModuleAPIHandler.get_instance(self).get_all_customviews()
    def get_customview(self,customview_id):
        try:
            from .Handler import ModuleAPIHandler
        except ImportError:
            from Handler import ModuleAPIHandler
        return ModuleAPIHandler.get_instance(self).get_customview(customview_id)
    def get_all_relatedlists(self):
        try:
            from .Handler import ModuleAPIHandler
        except ImportError:
            from Handler import ModuleAPIHandler
        return ModuleAPIHandler.get_instance(self).get_all_relatedlists()
    def get_relatedlist(self,relatedlist_id):
        try:
            from .Handler import ModuleAPIHandler
        except ImportError:
            from Handler import ModuleAPIHandler
        return ModuleAPIHandler.get_instance(self).get_relatedlist(relatedlist_id)
    def update_module_settings(self):
        try:
            from .Handler import ModuleAPIHandler
        except ImportError:
            from Handler import ModuleAPIHandler
        return ModuleAPIHandler.get_instance(self).update_module_settings()
    def update_customview(self,customview_instance):
        try:
            from .Handler import ModuleAPIHandler
        except ImportError:
            from Handler import ModuleAPIHandler
        return ModuleAPIHandler.get_instance(self).update_customview(customview_instance)
    

class ZCRMRecord(object):
    '''
    This class is to deal with Zoho CRM entity records
    '''
    def __init__(self,module_apiname,entity_id):
        '''
        Constructor
        '''
        self.module_api_name=module_apiname
        self.entity_id=entity_id
        self.line_items=[]
        self.lookup_label=None
        self.owner=None
        self.created_by=None
        self.modified_by=None
        self.created_time=None
        self.modified_time=None
        self.field_data=dict()
        self.properties = dict()
        self.participants = []
        self.price_details = []
        self.layout=None
        self.tax_list=[]
        self.last_activity_time=None
    @staticmethod
    def get_instance(module_apiname,entity_id=None):
        return ZCRMRecord(module_apiname,entity_id)
    def set_field_value(self,key,value):
        self.field_data[key]=value
    def get_field_value(self,key):
        return self.field_data[key] if key in self.field_data else None
    def add_line_item(self,line_item):
        self.line_items.append(line_item)
    
    def get(self):
        if self.entity_id is None:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            CommonUtil.raise_exception('Record_Get',"id should be set for the record",'ID DOES NOT PROVIDED',"ID")
        try:
            from .Handler import EntityAPIHandler
        except ImportError:
            from Handler import EntityAPIHandler
        return EntityAPIHandler.get_instance(self).get_record()
    def create(self):
        if self.entity_id is not None:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            CommonUtil.raise_exception('Record_Create',"id should not be set for the record",'ID PROVIDED',"ID")
        try:
            from .Handler import EntityAPIHandler
        except ImportError:
            from Handler import EntityAPIHandler
        return EntityAPIHandler.get_instance(self).create_record()
    def update(self):
        if self.entity_id is None:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            CommonUtil.raise_exception('Record_Update',"id should be set for the record",'ID DOES NOT PROVIDED',"ID")
        try:
            from .Handler import EntityAPIHandler
        except ImportError:
            from Handler import EntityAPIHandler
        return EntityAPIHandler.get_instance(self).update_record()
    def delete(self):
        if self.entity_id is None:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            CommonUtil.raise_exception('Record_Delete',"id should be set for the record",'ID DOES NOT PROVIDED',"ID")
        try:
            from .Handler import EntityAPIHandler
        except ImportError:
            from Handler import EntityAPIHandler
        return EntityAPIHandler.get_instance(self).delete_record()
    def convert(self,potential_record=None, assign_to_user=None):
        if self.entity_id is None:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            CommonUtil.raise_exception('Convert_Record',"id should be set for the record",'ID DOES NOT PROVIDED',"ID")
        try:
            from .Handler import EntityAPIHandler
        except ImportError:
            from Handler import EntityAPIHandler
        return EntityAPIHandler.get_instance(self).convert_record(potential_record, assign_to_user)
    
    def upload_attachment(self,file_path):
        if file_path is None:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            CommonUtil.raise_exception('Upload_Attachment',"file path must be given",'FILEPATH NOT PROVIDED',"FILEPATH")
        return ZCRMModuleRelation.get_instance(self, "Attachments").upload_attachment(file_path)
    
    def upload_link_as_attachment(self,link_url):
        if link_url is None:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            CommonUtil.raise_exception('Upload_Link_As_Attachment',"link URL must be given",'URL_LINK NOT PROVIDED',"URL_LINK")
        return ZCRMModuleRelation.get_instance(self, "Attachments").upload_link_as_attachment(link_url)
    
    def download_attachment(self,attachment_id):
        if attachment_id is None:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            CommonUtil.raise_exception('Download_Attachment',"attachment id must be given",'ID DOES NOT PROVIDED',"ID")
        return ZCRMModuleRelation.get_instance(self, "Attachments").download_attachment(attachment_id)
    
    def delete_attachment(self,attachment_id):
        if attachment_id is None:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            CommonUtil.raise_exception('Delete_Attachment',"attachment id must be given",'ID DOES NOT PROVIDED',"ID")
        return ZCRMModuleRelation.get_instance(self, "Attachments").delete_attachment(attachment_id)
    
    def upload_photo(self,file_path):
        if file_path is None:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            CommonUtil.raise_exception('Upload_Photo',"file path must be given",'FILEPATH NOT PROVIDED',"FILEPATH")
        try:
            from .Handler import EntityAPIHandler
        except ImportError:
            from Handler import EntityAPIHandler
        return EntityAPIHandler.get_instance(self).upload_photo(file_path)
    
    def download_photo(self):
        try:
            from .Handler import EntityAPIHandler
        except ImportError:
            from Handler import EntityAPIHandler
        return EntityAPIHandler.get_instance(self).download_photo()
    
    def delete_photo(self):
        try:
            from .Handler import EntityAPIHandler
        except ImportError:
            from Handler import EntityAPIHandler
        return EntityAPIHandler.get_instance(self).delete_photo()
    
    def add_relation(self,junction_record):
        if junction_record is None:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            CommonUtil.raise_exception('add_relation',"junction_record must be given",'JUNCTION RECORD NOT PROVIDED',"JUNCTION RECORD")
        return ZCRMModuleRelation.get_instance(self,junction_record).add_relation()
    
    def remove_relation(self,junction_record):
        if junction_record is None:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            CommonUtil.raise_exception('remove_relation',"junction_record must be given",'JUNCTION RECORD NOT PROVIDED',"JUNCTION RECORD")
        return ZCRMModuleRelation.get_instance(self,junction_record).remove_relation()
    
    def add_note(self,note_ins):
        if note_ins is None:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            CommonUtil.raise_exception('add_note',"note instance must be given",'NOTE INSTANCE NOT PROVIDED',"NOTE INSTANCE")
        return ZCRMModuleRelation.get_instance(self,"Notes").add_note(note_ins)
    
    def update_note(self,note_ins):
        if note_ins is None or note_ins.id is None:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            CommonUtil.raise_exception('update_note',"note instance and note id must be given",'NOTE INSTANCE OR NOTE ID NOT PROVIDED',"NOTE INSTANCE OR ID")
        return ZCRMModuleRelation.get_instance(self,"Notes").update_note(note_ins)
    
    def delete_note(self,note_ins):
        if note_ins is None or note_ins.id is None:
            try:
                from .Utility import CommonUtil
            except ImportError:
                from Utility import CommonUtil
            CommonUtil.raise_exception('delete_note',"note instance and note id must be given",'NOTE INSTANCE OR NOTE ID NOT PROVIDED',"NOTE INSTANCE OR ID")
        return ZCRMModuleRelation.get_instance(self,"Notes").delete_note(note_ins)
    
    def get_notes(self,sort_by=None,sort_order=None,page=1,per_page=20):
        return ZCRMModuleRelation.get_instance(self,"Notes").get_notes(sort_by,sort_order,page,per_page)
    
    def get_attachments(self,page=1,per_page=20):
        return ZCRMModuleRelation.get_instance(self,"Attachments").get_attachments(page,per_page)
    
    def get_relatedlist_records(self,relatedlist_api_name,sort_by=None,sort_order=None,page=1,per_page=20):
        return ZCRMModuleRelation.get_instance(self,relatedlist_api_name).get_records(sort_by,sort_order,page,per_page)
        

class ZCRMInventoryLineItem(object):
    '''
    This class is to deal with Zoho CRM Inventory line items
    '''
    def __init__(self,param):
        if(isinstance(param, ZCRMRecord)):
            self.product=param
            self.id=None
        else:
            self.id=param
            self.product=None
        
        self.list_price=None
        self.quantity=None
        self.description=None
        self.total=None
        self.discount=None
        self.discount_percentage=None
        self.total_after_discount=None
        self.tax_amount=None
        self.net_total=None
        self.delete_flag = False
        self.line_tax = list()
        
    @staticmethod
    def get_instance(param):
        return ZCRMInventoryLineItem(param)
    
class ZCRMTax(object):
    
    def __init__(self,name):
        self.name=name
        self.percentage=None
        self.value=None
        
    @staticmethod
    def get_instance(name):
        return ZCRMTax(name)
    
class ZCRMEventParticipant(object):
    def __init__(self,participant_type,participant_id):
        self.id=participant_type
        self.type=participant_id
        self.email=None
        self.name=None
        self.is_invited=None
        self.status=None 
    @staticmethod
    def get_instance(participant_type,participant_id):
        return ZCRMEventParticipant(participant_type,participant_id)
    
class ZCRMPriceBookPricing(object):
    def __init__(self,price_book_id):
        self.id=price_book_id
        self.to_range=None
        self.from_range=None
        self.discount=None
    @staticmethod
    def get_instance(price_book_id):
        return ZCRMPriceBookPricing(price_book_id)

class ZCRMUser(object):
    def __init__(self,user_id,name):
        self.id=user_id
        self.name=name
        self.signature=None
        self.country=None
        self.role=None
        self.customize_info=None
        self.city=None
        self.name_format=None
        self.language=None
        self.locale=None
        self.is_personal_account=None
        self.default_tab_group=None
        self.street=None
        self.alias=None
        self.theme=None
        self.state=None
        self.country_locale=None
        self.fax=None
        self.first_name=None
        self.email=None
        self.zip=None
        self.decimal_separator=None
        self.website=None
        self.time_format=None
        self.profile=None
        self.mobile=None
        self.last_name=None
        self.time_zone=None
        self.zuid=None
        self.is_confirm=None
        self.full_name=None
        self.phone=None
        self.dob=None
        self.date_format=None
        self.status=None
        self.created_by=None;
        self.modified_by=None;
        self.territories=None;
        self.reporting_to=None;
        self.is_online=None;
        self.currency=None;
        self.created_time=None;
        self.modified_time=None;
        self.field_apiname_vs_value=dict();
    @staticmethod
    def get_instance(user_id=None,name=None):
        return ZCRMUser(user_id,name)
    defaultKeys=["Currency","Modified_Time","created_time","territories","reporting_to","Isonline","created_by","Modified_By","country","id","name","role","customize_info","city","signature","name_format","language","locale","personal_account","default_tab_group","alias","street","theme","state","country_locale","fax","first_name","email","zip","decimal_separator","website","time_format","profile","mobile","last_name","time_zone","zuid","confirm","full_name","phone","dob","date_format","status"]
    
class ZCRMUserCustomizeInfo(object):
    def __init__(self):
        self.notes_desc=None
        self.is_to_show_right_panel=None
        self.is_bc_view=None
        self.is_to_show_home=None
        self.is_to_show_detail_view=None
        self.unpin_recent_item=None
    @staticmethod
    def get_instance():
        return ZCRMUserCustomizeInfo()
    
class ZCRMUserTheme(object):
    
    def __init__(self):
        self.normal_tab_font_color=None
        self.normal_tab_background=None
        self.selected_tab_font_color=None
        self.selected_tab_background=None
        
    @staticmethod
    def get_instance():
        return ZCRMUserTheme()
    
class ZCRMRole(object):
    def __init__(self,role_id,role_name):
        self.name=role_name
        self.id=role_id
        self.reporting_to=None
        self.label=None
        self.is_admin=None
    
    @staticmethod
    def get_instance(role_id,role_name=None):
        return ZCRMRole(role_id,role_name)
    
        
class ZCRMLayout(object):
    
    def __init__(self,layout_id):
        self.id=layout_id
        self.name=None
        self.created_time=None
        self.modified_time=None
        self.is_visible=None
        self.modified_by=None
        self.accessible_profiles=None
        self.created_by=None
        self.sections=None
        self.status=None
        self.convert_mapping=dict()
        
    @staticmethod
    def get_instance(layout_id):
        return ZCRMLayout(layout_id)
    
class ZCRMAttachment(object):
    def __init__(self,parent_record,attachment_id):
        self.id=attachment_id
        self.parent_record=parent_record
        self.file_name=None
        self.file_type=None
        self.size=None
        self.owner=None
        self.created_by=None
        self.created_time=None
        self.modified_by=None
        self.modified_time=None
        self.parent_module=None
        self.attachment_type=None
        self.parent_name=None
        self.parent_id=None
    @staticmethod
    def get_instance(parent_record,attachment_id=None):
        return ZCRMAttachment(parent_record,attachment_id)

class ZCRMCustomView(object):
    
    def __init__(self,custom_view_id,module_apiname):
        self.id=custom_view_id
        self.module_api_name=module_apiname
        self.display_value=None
        self.is_default=None
        self.name=None
        self.system_name=None
        self.sort_by=None
        self.category=None
        self.fields=list()
        self.favorite=None
        self.sort_order=None
        self.criteria_pattern=None
        self.criteria=None
        self.categories=list()
        self.is_off_line=None
        
    @staticmethod
    def get_instance(custom_view_id,module_apiname=None):
        return ZCRMCustomView(custom_view_id,module_apiname)
    
class ZCRMCustomViewCategory(object):
    
    def __init__(self):
        self.display_value=None
        self.actual_value=None
    @staticmethod
    def get_instance():
        return ZCRMCustomViewCategory()
    
class ZCRMCustomViewCriteria(object):
    
    def __init__(self):
        self.comparator=None
        self.field=None
        self.value=None
        
    @staticmethod
    def get_instance():
        return ZCRMCustomViewCriteria()
    
class ZCRMField(object):
    
    def __init__(self,api_name):
        self.api_name=api_name
        self.is_custom_field=None
        self.lookup_field=None
        self.convert_mapping=None
        self.is_visible=None
        self.field_label=None
        self.length=None
        self.created_source=None
        self.default_value=None
        self.is_mandatory=None
        self.sequence_number=None
        self.is_read_only=None
        self.is_unique_field=None
        self.is_case_sensitive=None
        self.data_type=None
        self.is_formula_field=None
        self.is_currency_field=None
        self.id=None
        self.picklist_values=list()
        self.is_auto_number=None
        self.is_business_card_supported=None
        self.field_layout_permissions=None
        self.decimal_place=None
        self.precision=None
        self.rounding_option=None
        self.formula_return_type=None
        self.formula_expression=None
        self.prefix=None
        self.suffix=None
        self.start_number=None
        self.json_type=None
        
    @staticmethod
    def get_instance(api_name):
        return ZCRMField(api_name)
    
class ZCRMJunctionRecord(object):
    
    def __init__(self,api_name,record_id):
        self.id=record_id
        self.api_name=api_name
        self.related_data=dict()
        
    @staticmethod
    def get_instance(api_name,record_id):
        return ZCRMJunctionRecord(api_name,record_id)
    
    def set_related_data(self,key,value):
        self.related_data[key]=value
        
    def get_related_data(self):
        return self.related_data
        
class ZCRMLeadConvertMapping(object):
    
    def __init__(self,name,converted_id):
        self.id=converted_id
        self.name=name
        self.fields=list()
    @staticmethod
    def get_instance(name,converted_id):
        return ZCRMLeadConvertMapping(name,converted_id)
    
class ZCRMLeadConvertMappingField(object):
    
    def __init__(self,api_name,field_id):
        self.id=field_id
        self.api_name=api_name
        self.field_label=None
        self.is_required=None
        
    @staticmethod
    def get_instance(api_name,field_id):
        return ZCRMLeadConvertMappingField(api_name,field_id)
    
class ZCRMLookupField(object):
    
    def __init__(self,apiName):
        self.api_name=apiName
        self.display_label=None
        self.module=None
        self.id=None
        
    @staticmethod
    def get_instance(api_name):
        return ZCRMLookupField(api_name)
    

class ZCRMModuleRelatedList(object):
     
    def __init__(self,api_name):
        self.api_name=api_name
        self.module=None
        self.display_label=None
        self.is_visible=None
        self.name=None
        self.id=None
        self.href=None
        self.type=None 
    
    @staticmethod
    def get_instance(api_name):
        return ZCRMModuleRelatedList(api_name)
    
    def set_relatedlist_properties(self,relatedlist_prop):
        self.id=relatedlist_prop['id']
        self.module=relatedlist_prop['module']
        self.display_label=relatedlist_prop['display_label']
        self.name=relatedlist_prop['name']
        self.type=relatedlist_prop['type']
        self.href=relatedlist_prop['href']
        self.is_visible=bool(relatedlist_prop['visible']) if 'visible' in relatedlist_prop else None
        return self
    
class ZCRMModuleRelation(object):
    
    def __init__(self,parentmodule_apiname_or_parentrecord,related_list_apiname_or_junction_record):
        if isinstance(parentmodule_apiname_or_parentrecord, ZCRMRecord):
            self.parent_record=parentmodule_apiname_or_parentrecord
            self.parent_module_api_name=None
        else:
            self.parent_module_api_name=parentmodule_apiname_or_parentrecord
            self.parent_record=None
        
        if isinstance(related_list_apiname_or_junction_record, ZCRMJunctionRecord):
            self.junction_record=related_list_apiname_or_junction_record
            self.api_name=None
        else:
            self.api_name=related_list_apiname_or_junction_record
            self.junction_record=None
            
        self.label=None
        self.id=None
        self.is_visible=None
        
    @staticmethod
    def get_instance(parentmodule_apiname_or_parentrecord,related_list_apiname_or_junction_record):
        return ZCRMModuleRelation(parentmodule_apiname_or_parentrecord,related_list_apiname_or_junction_record)
    
    def get_records(self,sort_by_field=None,sort_order=None,page=1,per_page=20):
        try:
            from .Handler import RelatedListAPIHandler
        except ImportError:
            from Handler import RelatedListAPIHandler
        return RelatedListAPIHandler.get_instance(self.parent_record,self).get_records(sort_by_field,sort_order,page,per_page)
    def upload_attachment(self,file_path):
        try:
            from .Handler import RelatedListAPIHandler
        except ImportError:
            from Handler import RelatedListAPIHandler
        return RelatedListAPIHandler.get_instance(self.parent_record,self).upload_attachment(file_path)
    def upload_link_as_attachment(self,link_url):
        try:
            from .Handler import RelatedListAPIHandler
        except ImportError:
            from Handler import RelatedListAPIHandler
        return RelatedListAPIHandler.get_instance(self.parent_record,self).upload_link_as_attachment(link_url)
    def download_attachment(self,attachment_id):
        try:
            from .Handler import RelatedListAPIHandler
        except ImportError:
            from Handler import RelatedListAPIHandler
        return RelatedListAPIHandler.get_instance(self.parent_record,self).download_attachment(attachment_id)
    def delete_attachment(self,attachment_id):
        try:
            from .Handler import RelatedListAPIHandler
        except ImportError:
            from Handler import RelatedListAPIHandler
        return RelatedListAPIHandler.get_instance(self.parent_record,self).delete_attachment(attachment_id)
    def add_relation(self):
        try:
            from .Handler import RelatedListAPIHandler
        except ImportError:
            from Handler import RelatedListAPIHandler
        return RelatedListAPIHandler.get_instance(self.parent_record,self.junction_record).add_relation()
    def remove_relation(self):
        try:
            from .Handler import RelatedListAPIHandler
        except ImportError:
            from Handler import RelatedListAPIHandler
        return RelatedListAPIHandler.get_instance(self.parent_record,self.junction_record).remove_relation()
    def add_note(self,zcrm_note_ins):
        try:
            from .Handler import RelatedListAPIHandler
        except ImportError:
            from Handler import RelatedListAPIHandler
        return RelatedListAPIHandler.get_instance(self.parent_record,self).add_note(zcrm_note_ins)
    def update_note(self,zcrm_note_ins):
        try:
            from .Handler import RelatedListAPIHandler
        except ImportError:
            from Handler import RelatedListAPIHandler
        return RelatedListAPIHandler.get_instance(self.parent_record,self).update_note(zcrm_note_ins)
    def delete_note(self,zcrm_note_ins):
        try:
            from .Handler import RelatedListAPIHandler
        except ImportError:
            from Handler import RelatedListAPIHandler
        return RelatedListAPIHandler.get_instance(self.parent_record,self).delete_note(zcrm_note_ins)
    def get_notes(self,sort_by,sort_order,page,per_page):
        try:
            from .Handler import RelatedListAPIHandler
        except ImportError:
            from Handler import RelatedListAPIHandler
        return RelatedListAPIHandler.get_instance(self.parent_record,self).get_notes(sort_by,sort_order,page,per_page)
    def get_attachments(self,page,per_page):
        try:
            from .Handler import RelatedListAPIHandler
        except ImportError:
            from Handler import RelatedListAPIHandler
        return RelatedListAPIHandler.get_instance(self.parent_record,self).get_attachments(page,per_page)
    
class ZCRMNote(object):
    
    def __init__(self,parent_record,note_id):
        self.id=note_id
        self.parent_record=parent_record
        self.title=None
        self.content=None
        self.owner=None
        self.created_by=None
        self.created_time=None
        self.modified_by=None
        self.modified_time=None
        self.attachments=None
        self.size=None
        self.is_voice_note=None
        self.parent_module=None
        self.parent_name=None
        self.parent_id=None
        
    @staticmethod
    def get_instance(parent_record,note_id=None):
        return ZCRMNote(parent_record,note_id)
    
class ZCRMPermission(object):
    
    def __init__(self,permission_name,permission_id):
        self.id=permission_id;
        self.name=permission_name;
        self.display_label=None;
        self.module=None;
        self.is_enabled=None;
        
    @staticmethod
    def get_instance(permission_name,permission_id):
        return ZCRMPermission(permission_name,permission_id)
    
class ZCRMPickListValue(object):
    
    def __init__(self):
        self.display_value=None
        self.sequence_number=None
        self.actual_value=None
        self.maps=None
    @staticmethod
    def get_instance():
        return ZCRMPickListValue()
    
class ZCRMProfile(object):
    
    def __init__(self,profile_id,profile_name):
        self.name=profile_name
        self.id=profile_id
        self.is_default=None
        self.created_time=None
        self.modified_time=None
        self.modified_by=None
        self.description=None
        self.created_by=None
        self.category=None
        self.permissions=list()
        self.sections=list()
    
    @staticmethod
    def get_instance(profile_id,profile_name=None):
        return ZCRMProfile(profile_id,profile_name)
    
class ZCRMProfileCategory(object):
    
    def __init__(self,profile_category_name):
        self.name=profile_category_name
        self.module=None
        self.display_label=None
        self.permission_ids=list()
        
    @staticmethod
    def get_instance(profile_category_name):
        return ZCRMProfileCategory(profile_category_name)
    
class ZCRMProfileSection(object):
    
    def __init__(self,section_name):
        self.name=section_name
        self.categories=list()
        
    @staticmethod
    def get_instance(section_name):
        return ZCRMProfileSection(section_name)
    
class ZCRMRelatedListProperties(object):
    
    def __init__(self):
        self.sort_by=None
        self.sort_order=None
        self.fields=None
        
    @staticmethod
    def get_instance():
        return ZCRMRelatedListProperties()
    
class ZCRMSection(object):
    
    def __init__(self,section_name):
        self.name=section_name
        self.display_name=None
        self.column_count=None
        self.sequence_number=None
        self.fields=None
        
    @staticmethod
    def get_instance(section_name):
        return ZCRMSection(section_name)
    

class ZCRMTrashRecord(object):
    
    def __init__(self,entity_type,entity_id):
        self.id = entity_id
        self.type=entity_type
        self.display_name=None
        self.deleted_time=None
        self.created_by=None
        self.deleted_by=None
        
    @staticmethod
    def get_instance(entity_type,entity_id=None):
        return ZCRMTrashRecord(entity_type,entity_id)