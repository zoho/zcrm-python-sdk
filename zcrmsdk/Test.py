'''
Created on Jul 31, 2017
@author: sumanth-3058
'''
from RestClient import ZCRMRestClient
from Operations import ZCRMModule, ZCRMRecord,\
    ZCRMUser, ZCRMInventoryLineItem, ZCRMTax, ZCRMJunctionRecord, ZCRMNote,\
    ZCRMCustomView, ZCRMRole, ZCRMProfile
from OAuthClient import ZohoOAuth
import threading
from CLException import ZCRMException
from Utility import APIConstants
from Org import ZCRMOrganization
threadLocal=threading.local()
class MyThread(threading.Thread):
    def __init__(self,email):
        super(MyThread,self).__init__()
        self.local=threadLocal
        self.email=email
    def run(self):
        self.local.email=self.email
        print self.local.email

class MyClass(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    def test(self):
        resp=ZCRMModule.get_instance('Invoices').get_record(440872000000208009)
        print resp.data.entity_id
        print resp.data.created_by.name
        print resp.data.modified_by.name
        print resp.data.created_time
        print resp.data.line_items[0].list_price
        print resp.data.line_items[0].product.lookup_label
        print resp.data.line_items[0].product.get_field_value('Product_Code')

    def create_record(self):
        try:
            record=ZCRMRecord.get_instance('Invoices')
            record.set_field_value('Subject', 'Inv4')
            record.set_field_value('Account_Name', 'IIIT')
            user=ZCRMUser.get_instance(1386586000000105001,'Sumanth Ch')
            record.set_field_value('Owner',user)
            line_item=ZCRMInventoryLineItem.get_instance(ZCRMRecord.get_instance("Products",1386586000000803073))
            line_item.discount=10
            line_item.list_price=8
            line_item.description='Product Description'
            line_item.quantity=100
            line_item.tax_amount=2.5
            taxIns=ZCRMTax.get_instance("Vat")
            taxIns.percentage=5
            line_item.line_tax.append(taxIns)
            record.add_line_item(line_item)
            resp=record.create()
            print resp.status_code
            print resp.code
            print resp.details
            print resp.message
            print resp.status
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content

    def update_record(self):
        try:
            record=ZCRMRecord.get_instance('Leads',1386586000001856002)
            record.set_field_value('Last_Name', 'Python')
            record.set_field_value('Mobile', '9999999999')
            record.set_field_value('Phone', '9999999998')
            user=ZCRMUser.get_instance(1386586000000105001,'Sumanth Ch')
            record.set_field_value('Email', 'support@zohocrm.com')
            record.set_field_value('Owner',user)
            resp=record.update()
            print resp.status_code
            print resp.code
            print resp.details
            print resp.message
            print resp.status
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content

    def delete_record(self):
        try:
            record=ZCRMRecord.get_instance('Leads',1386586000001422011)
            resp=record.delete()
            print resp.status_code
            print resp.code
            print resp.details
            print resp.message
            print resp.status
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content

    def get_record(self):
        try:
            #record=ZCRMRecord.get_instance('Leads',440872000000219003)
            record=ZCRMRecord.get_instance('Invoices',1386586000000803061)
            resp=record.get()
            print resp.status_code
            print resp.data.entity_id
            print resp.data.created_by.id
            print resp.data.modified_by.id
            print resp.data.owner.id
            print resp.data.created_by.name
            print resp.data.created_time
            print resp.data.modified_time
            print resp.data.get_field_value('Email')
            print resp.data.get_field_value('Last_Name')
            #print resp.data.field_data
            if resp.data.line_items is not None:
                for line_item in resp.data.line_items:
                    print "::::::LINE ITEM DETAILS::::::"
                    print line_item.id
                    print line_item.product.lookup_label
                    print line_item.product.get_field_value('Product_Code')
                    print line_item.product.entity_id
                    print line_item.list_price
                    print line_item.quantity
                    print line_item.description
                    print line_item.total
                    print line_item.discount
                    print line_item.discount_percentage
                    print line_item.total_after_discount
                    print line_item.tax_amount
                    print line_item.net_total
                    print line_item.delete_flag
                    if line_item.line_tax is not None:
                        for tax in line_item.line_tax:
                            print ":::::: TAX DETAILS ::::::"
                            print tax.name
                            print tax.value
                            print tax.percentage
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content

    def convert_record(self):
        try:
            record=ZCRMRecord.get_instance('Leads',1386586000001422007)
            potential_record=ZCRMRecord.get_instance('Deals')
            potential_record.set_field_value('Deal_Name', 'SAI1')
            potential_record.set_field_value('Closing_Date', '2017-10-10')
            potential_record.set_field_value('Stage', 'Needs Analysis')
            assign_to_user=ZCRMUser.get_instance(1386586000000105001, None)
            resp=record.convert(potential_record, assign_to_user)
            print resp
            print resp[APIConstants.ACCOUNTS]
            print resp[APIConstants.DEALS]
            print resp[APIConstants.CONTACTS]
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content

    def upload_attachment(self):
        try:
            record=ZCRMRecord.get_instance('Leads',1386586000001856002)
            resp=record.upload_attachment('/Users/Downloads/sequel-pro-1.1.dmg')
            print resp.data.id
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content
    def upload_link_as_attachment(self):
        try:
            record=ZCRMRecord.get_instance('Leads',1386586000001856002)
            resp=record.upload_link_as_attachment('www.zoho.com')
            print resp.data.id
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content

    def download_attachment(self):
        try:
            record=ZCRMRecord.get_instance('Leads',1386586000001856002)
            resp=record.download_attachment(1386586000001856008)
            print resp.response_headers
            if resp.status_code==200:
                print resp.file_name
                with open('/Users/Downloads/'+resp.file_name, 'wb') as f:
                    for chunk in resp.response:
                        f.write(chunk)
                f.close()
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content

    def delete_attachment(self):
        try:
            record=ZCRMRecord.get_instance('Leads',1386586000001856002)
            resp=record.delete_attachment(1386586000001858011)
            print resp.status_code
            print resp.code
            print resp.details
            print resp.message
            print resp.status
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content

    def upload_photo(self):
        try:
            record=ZCRMRecord.get_instance('Leads',1386586000001856002)
            resp=record.upload_photo('/Users/Pictures/image.png')
            print resp.status_code
            print resp.code
            print resp.message
            print resp.status
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content

    def download_photo(self):
        try:
            record=ZCRMRecord.get_instance('Leads',1386586000001856002)
            resp=record.download_photo()
            print resp.response_headers
            if resp.status_code==200:
                print resp.file_name
                with open('/Users/Downloads/'+resp.file_name, 'wb') as f:
                    for chunk in resp.response:
                        f.write(chunk)
                f.close()
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content

    def delete_photo(self):
        try:
            record=ZCRMRecord.get_instance('Leads',1386586000001856002)
            resp=record.delete_photo()
            print resp.status_code
            print resp.code
            print resp.details
            print resp.message
            print resp.status
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content

    def add_relation(self):
        try:
            record=ZCRMRecord.get_instance('Leads',1386586000001856002)
            junction_record=ZCRMJunctionRecord.get_instance("Products", 1386586000000803073)
            resp=record.add_relation(junction_record)
            print resp.status_code
            print resp.code
            print resp.details
            print resp.message
            print resp.status
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content

    def remove_relation(self):
        try:
            record=ZCRMRecord.get_instance('Leads',1386586000001856002)
            junction_record=ZCRMJunctionRecord.get_instance("Products", 1386586000000803073)
            resp=record.remove_relation(junction_record)
            print resp.status_code
            print resp.code
            print resp.details
            print resp.message
            print resp.status
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content
    def add_note(self):
        try:
            record=ZCRMRecord.get_instance('Leads',1386586000001856002)
            note_ins=ZCRMNote.get_instance(record, None)
            note_ins.title="title2"
            note_ins.content='content2...'
            resp=record.add_note(note_ins)
            print resp.status_code
            print resp.code
            print resp.data.id
            print resp.message
            print resp.status
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content

    def update_note(self):
        try:
            record=ZCRMRecord.get_instance('Leads',1386586000001856002)
            note_ins=ZCRMNote.get_instance(record, 1386586000001859023)
            note_ins.title="title2 updated"
            note_ins.content='content2 updated...'
            resp=record.update_note(note_ins)
            print resp.status_code
            print resp.code
            print resp.data.modified_by.id
            print resp.data.modified_by.name
            print resp.message
            print resp.status
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content

    def delete_note(self):
        try:
            record=ZCRMRecord.get_instance('Leads',1386586000001856002)
            note_ins=ZCRMNote.get_instance(record, 1386586000001859023)
            resp=record.delete_note(note_ins)
            print resp.status_code
            print resp.code
            print resp.details
            print resp.message
            print resp.status
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content

    def get_notes(self):
        try:
            record=ZCRMRecord.get_instance('Leads',1386586000001856002)
            resp=record.get_notes()
            print resp.status_code
            note_ins_arr=resp.data
            for note_ins in note_ins_arr:
                print note_ins.id
                print note_ins.title
                print note_ins.content
                print note_ins.owner.id
                print note_ins.created_by.id
                print note_ins.modified_by.id
                print note_ins.created_time
                print note_ins.modified_time
                print "\n\n"
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content

    def get_attachments(self):
        try:
            record=ZCRMRecord.get_instance('Leads',1386586000001856002)
            resp=record.get_attachments()
            print resp.status_code
            attachment_ins_arr=resp.data
            for attachment_ins in attachment_ins_arr:
                print attachment_ins.id
                print attachment_ins.file_name
                print attachment_ins.file_type
                print attachment_ins.size
                print attachment_ins.owner.id
                print attachment_ins.created_by.id
                print attachment_ins.modified_by.id
                print attachment_ins.created_time
                print attachment_ins.modified_time
                print attachment_ins.parent_module
                print attachment_ins.attachment_type
                print attachment_ins.parent_name
                print attachment_ins.parent_id
                print attachment_ins.parent_record.entity_id
                print "\n\n"
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content

    def get_related_records(self):
        try:
            record=ZCRMRecord.get_instance('Leads',1386586000001856002)
            resp=record.get_relatedlist_records('Products')
            print resp.status_code
            record_ins_arr=resp.data
            for record_ins in record_ins_arr:
                print record_ins.entity_id
                print record_ins.owner.id
                print record_ins.created_by.id
                print record_ins.modified_by.id
                print record_ins.created_time
                print record_ins.modified_time
                print record_ins.get_field_value('Product_Name')
                print record_ins.get_field_value('Product_Code')
                print record_ins.get_field_value('Vendor_Name')
                print record_ins.get_field_value('Commission_Rate')
                print record_ins.get_field_value('Qty_in_Demand')
                print record_ins.get_field_value('Tax')
                print record_ins.get_field_value('Unit_Price')
                print record_ins.get_field_value('Reorder_Level')
                print record_ins.get_field_value('Usage_Unit')
                print record_ins.get_field_value('Qty_Ordered')
                print record_ins.get_field_value('Qty_in_Stock')
                print record_ins.get_field_value('Sales_Start_Date')
                print record_ins.get_field_value('Sales_End_Date')
                print record_ins.get_field_value('Taxable')
                print record_ins.get_field_value('Support_Expiry_Date')
                print record_ins.get_field_value('Manufacturer')
                print record_ins.get_field_value('Description')
                print record_ins.field_data
                print "\n\n"
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content
    def get_records(self):
        try:
            module_ins=ZCRMModule.get_instance('Products')
            resp=module_ins.get_records()
            print resp.status_code
            record_ins_arr=resp.data
            for record_ins in record_ins_arr:
                print record_ins.entity_id
                print record_ins.owner.id
                print record_ins.created_by.id
                print record_ins.modified_by.id
                print record_ins.created_time
                print record_ins.modified_time
                product_data=record_ins.field_data
                for key in product_data:
                    print key+":"+str(product_data[key])
                print "\n\n"
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content

    def create_records(self):
        try:
            record_ins_list=list()
            for i in range(0,2):
                record=ZCRMRecord.get_instance('Invoices')
                record.set_field_value('Subject', 'Invoice'+str(i))
                record.set_field_value('Account_Name', 'IIIT')
                user=ZCRMUser.get_instance(1386586000000105001,'Sumanth Ch')
                record.set_field_value('Owner',user)
                line_item=ZCRMInventoryLineItem.get_instance(ZCRMRecord.get_instance("Products",1386586000000803073))
                line_item.discount=10
                line_item.list_price=8
                line_item.description='Product Description'
                line_item.quantity=100
                line_item.tax_amount=2.5
                taxIns=ZCRMTax.get_instance("Vat")
                taxIns.percentage=5
                line_item.line_tax.append(taxIns)
                record.add_line_item(line_item)
                record_ins_list.append(record)
            resp=ZCRMModule.get_instance('Invoices').create_records(record_ins_list)
            print resp.status_code
            entity_responses=resp.bulk_entity_response
            for entity_response in entity_responses:
                print entity_response.details
                print entity_response.status
                print entity_response.message
                print entity_response.code
                print entity_response.data.entity_id
                print entity_response.data.created_by.id
                print entity_response.data.created_time
                print entity_response.data.modified_by.id
                print "\n\n"
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content
    def update_records(self):
        try:
            module_ins=ZCRMModule.get_instance('Invoices')
            entityid_list=[1386586000001858001,1386586000001521031,1386586000001282039]
            bulk_resp=module_ins.update_records(entityid_list, 'Status', 'Created')
            print bulk_resp.status_code
            entity_responses=bulk_resp.bulk_entity_response
            for entity_response in entity_responses:
                print entity_response.details
                print entity_response.status
                print entity_response.message
                print entity_response.code
                print entity_response.data.entity_id
                print entity_response.data.created_by.id
                print entity_response.data.created_time
                print entity_response.data.modified_by.id
                print "\n\n"
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content

    def upsert_records(self):
        try:
            record_ins_list=list()
            for i in range(0,2):
                record=ZCRMRecord.get_instance('Invoices')
                record.set_field_value('Subject', 'Invoice'+str(i))
                record.set_field_value('Account_Name', 'IIIT')
                user=ZCRMUser.get_instance(1386586000000105001,'Sumanth Ch')
                record.set_field_value('Owner',user)
                line_item=ZCRMInventoryLineItem.get_instance(ZCRMRecord.get_instance("Products",1386586000000803073))
                line_item.discount=10
                line_item.list_price=8
                line_item.description='Product Description'
                line_item.quantity=100
                line_item.tax_amount=2.5
                taxIns=ZCRMTax.get_instance("Vat")
                taxIns.percentage=5
                line_item.line_tax.append(taxIns)
                record.add_line_item(line_item)
                record_ins_list.append(record)
            record=ZCRMRecord.get_instance('Invoices',1386586000001282039)
            record.set_field_value('Subject', 'Invoice1.1')
            line_item=ZCRMInventoryLineItem.get_instance(ZCRMRecord.get_instance("Products",1386586000000803073))
            line_item.discount=10
            line_item.list_price=8
            line_item.description='Product Description'
            line_item.quantity=100
            line_item.tax_amount=2.5
            taxIns=ZCRMTax.get_instance("Vat")
            taxIns.percentage=5
            line_item.line_tax.append(taxIns)
            record.add_line_item(line_item)
            record_ins_list.append(record)
            duplicate_check_fields=list();
            duplicate_check_fields.append("field1");
            resp=ZCRMModule.get_instance('Invoices').upsert_records(record_ins_list,duplicate_check_fields)
            print resp.status_code
            entity_responses=resp.bulk_entity_response
            for entity_response in entity_responses:
                print entity_response.details
                print entity_response.status
                print entity_response.message
                print entity_response.code
                print entity_response.data.entity_id
                print entity_response.data.created_by.id
                print entity_response.data.created_time
                print entity_response.data.modified_by.id
                print "\n\n"
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content

    def delete_records(self):
        try:
            entityid_list=[1386586000001856020,1386586000001856019]
            resp=ZCRMModule.get_instance('Invoices').delete_records(entityid_list)
            print resp.status_code
            entity_responses=resp.bulk_entity_response
            for entity_response in entity_responses:
                print entity_response.details
                print entity_response.status
                print entity_response.message
                print entity_response.code
                print entity_response.data.entity_id
                print "\n\n"
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content

    def get_deleted_records(self,delete_type):
        try:
            module_ins=ZCRMModule.get_instance('Invoices')
            if delete_type=='permanent':
                resp=module_ins.get_permanently_deleted_records()
            elif delete_type=='recycle':
                resp=module_ins.get_recyclebin_records()
            else:
                resp=module_ins.get_all_deleted_records()
            print resp.status_code
            trash_record_ins_arr=resp.data

            resp_info=resp.info
            print resp_info.count
            print resp_info.page
            print resp_info.per_page
            print resp_info.is_more_records
            for record_ins in trash_record_ins_arr:
                print record_ins.id
                print record_ins.type
                print record_ins.display_name
                if record_ins.created_by is not None:
                    print record_ins.created_by.id
                if record_ins.deleted_by is not None:
                    print record_ins.deleted_by.id
                print record_ins.deleted_time
                print "\n\n"
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content

    def search_records(self):
        try:
            module_ins=ZCRMModule.get_instance('Products')
            resp=module_ins.search_records('Java')
            print resp.status_code
            resp_info=resp.info
            print resp_info.count
            print resp_info.page
            print resp_info.per_page
            print resp_info.is_more_records
            record_ins_arr=resp.data
            for record_ins in record_ins_arr:
                print record_ins.entity_id
                print record_ins.owner.id
                print record_ins.created_by.id
                print record_ins.modified_by.id
                print record_ins.created_time
                print record_ins.modified_time
                print record_ins.get_field_value('Product_Name')
                print record_ins.get_field_value('Product_Code')
                print record_ins.get_field_value('Vendor_Name')
                print record_ins.get_field_value('Commission_Rate')
                print record_ins.get_field_value('Qty_in_Demand')
                print record_ins.get_field_value('Tax')
                print record_ins.get_field_value('Unit_Price')
                print record_ins.get_field_value('Reorder_Level')
                print record_ins.get_field_value('Usage_Unit')
                print record_ins.get_field_value('Qty_Ordered')
                print record_ins.get_field_value('Qty_in_Stock')
                print record_ins.get_field_value('Sales_Start_Date')
                print record_ins.get_field_value('Sales_End_Date')
                print record_ins.get_field_value('Taxable')
                print record_ins.get_field_value('Support_Expiry_Date')
                print record_ins.get_field_value('Manufacturer')
                print record_ins.get_field_value('Description')
                print record_ins.field_data
                print "\n\n"
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content

    def get_fields(self):
        try:
            module_ins=ZCRMModule.get_instance('Accounts')
            resp=module_ins.get_all_fields()
            print resp.status_code
            field_ins_arr=resp.data
            for field_ins in field_ins_arr:
                print field_ins.api_name
                print field_ins.id
                print field_ins.is_custom_field
                print field_ins.lookup_field
                print field_ins.convert_mapping
                print field_ins.is_visible
                print field_ins.field_label
                print field_ins.length
                print field_ins.created_source
                print field_ins.default_value
                print field_ins.is_mandatory
                print field_ins.sequence_number
                print field_ins.is_read_only
                print field_ins.is_unique_field
                print field_ins.is_case_sensitive
                print field_ins.data_type
                print field_ins.is_formula_field
                print field_ins.is_currency_field
                print field_ins.picklist_values
                print field_ins.is_auto_number
                print field_ins.is_business_card_supported
                print field_ins.field_layout_permissions
                print field_ins.decimal_place
                print field_ins.precision
                print field_ins.rounding_option
                print field_ins.formula_return_type
                print field_ins.formula_expression
                print field_ins.prefix
                print field_ins.suffix
                print field_ins.start_number
                print field_ins.json_type
                print "\n\n"
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content

    def get_field(self):
        try:
            module_ins=ZCRMModule.get_instance('Accounts')
            api_resp=module_ins.get_field(1386586000000002423)
            print api_resp.status_code
            field_ins=api_resp.data
            print field_ins.api_name
            print field_ins.id
            print field_ins.is_custom_field
            print field_ins.lookup_field
            print field_ins.convert_mapping
            print field_ins.is_visible
            print field_ins.field_label
            print field_ins.length
            print field_ins.created_source
            print field_ins.default_value
            print field_ins.is_mandatory
            print field_ins.sequence_number
            print field_ins.is_read_only
            print field_ins.is_unique_field
            print field_ins.is_case_sensitive
            print field_ins.data_type
            print field_ins.is_formula_field
            print field_ins.is_currency_field
            print field_ins.picklist_values
            print field_ins.is_auto_number
            print field_ins.is_business_card_supported
            print field_ins.field_layout_permissions
            print field_ins.decimal_place
            print field_ins.precision
            print field_ins.rounding_option
            print field_ins.formula_return_type
            print field_ins.formula_expression
            print field_ins.prefix
            print field_ins.suffix
            print field_ins.start_number
            print field_ins.json_type
            print "\n\n"
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content

    def get_all_layouts(self):
        try:
            module_ins=ZCRMModule.get_instance('Accounts')
            resp=module_ins.get_all_layouts()
            print resp.status_code
            layout_ins_arr=resp.data
            for layout_ins in layout_ins_arr:
                print "\n\n:::LAYOUT DETAILS:::"
                print layout_ins.name
                print layout_ins.id
                print layout_ins.created_time
                print layout_ins.modified_time
                print layout_ins.convert_mapping
                print layout_ins.is_visible
                print layout_ins.modified_by.id
                profiles=layout_ins.accessible_profiles
                if profiles is not None:
                    for profile in profiles:
                        print "\n\n"
                        print profile.id
                        print profile.name
                        print profile.is_default
                print layout_ins.created_by
                sections= layout_ins.sections
                if sections is not None:
                    print "\n:::SECTION DETAILS:::"
                    for secton in sections:
                        print secton.name
                        print secton.display_name
                        print secton.column_count
                        print secton.sequence_number
                        fields=secton.fields
                        if fields is not None:
                            print "\n:::FIELD DETAILS:::"
                            for field_ins in fields:
                                print field_ins.api_name
                                print field_ins.id
                                print field_ins.is_custom_field
                                print field_ins.lookup_field
                                print field_ins.convert_mapping
                                print field_ins.is_visible
                                print field_ins.field_label
                                print field_ins.length
                                print field_ins.created_source
                                print field_ins.default_value
                                print field_ins.is_mandatory
                                print field_ins.sequence_number
                                print field_ins.is_read_only
                                print field_ins.is_unique_field
                                print field_ins.is_case_sensitive
                                print field_ins.data_type
                                print field_ins.is_formula_field
                                print field_ins.is_currency_field
                                print field_ins.picklist_values
                                print field_ins.is_auto_number
                                print field_ins.is_business_card_supported
                                print field_ins.field_layout_permissions
                                print field_ins.decimal_place
                                print field_ins.precision
                                print field_ins.rounding_option
                                print field_ins.formula_return_type
                                print field_ins.formula_expression
                                print field_ins.prefix
                                print field_ins.suffix
                                print field_ins.start_number
                                print field_ins.json_type
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content

    def get_layout(self):
        try:
            module_ins=ZCRMModule.get_instance('Accounts')
            resp=module_ins.get_layout(1386586000000343007)
            print resp.status_code
            layout_ins_arr=[resp.data]
            for layout_ins in layout_ins_arr:
                print "\n\n:::LAYOUT DETAILS:::"
                print layout_ins.name
                print layout_ins.id
                print layout_ins.created_time
                print layout_ins.modified_time
                print layout_ins.convert_mapping
                print layout_ins.is_visible
                print layout_ins.modified_by.id
                profiles=layout_ins.accessible_profiles
                if profiles is not None:
                    for profile in profiles:
                        print "\n\n"
                        print profile.id
                        print profile.name
                        print profile.is_default
                print layout_ins.created_by
                sections= layout_ins.sections
                if sections is not None:
                    print "\n:::SECTION DETAILS:::"
                    for secton in sections:
                        print secton.name
                        print secton.display_name
                        print secton.column_count
                        print secton.sequence_number
                        fields=secton.fields
                        if fields is not None:
                            print "\n:::FIELD DETAILS:::"
                            for field_ins in fields:
                                print field_ins.api_name
                                print field_ins.id
                                print field_ins.is_custom_field
                                print field_ins.lookup_field
                                print field_ins.convert_mapping
                                print field_ins.is_visible
                                print field_ins.field_label
                                print field_ins.length
                                print field_ins.created_source
                                print field_ins.default_value
                                print field_ins.is_mandatory
                                print field_ins.sequence_number
                                print field_ins.is_read_only
                                print field_ins.is_unique_field
                                print field_ins.is_case_sensitive
                                print field_ins.data_type
                                print field_ins.is_formula_field
                                print field_ins.is_currency_field
                                picklist_values=field_ins.picklist_values
                                if picklist_values is not None:
                                    for picklist_value_ins in picklist_values:
                                        print picklist_value_ins.display_value
                                        print picklist_value_ins.actual_value
                                        print picklist_value_ins.sequence_number
                                        print picklist_value_ins.maps
                                print field_ins.is_auto_number
                                print field_ins.is_business_card_supported
                                print field_ins.field_layout_permissions
                                print field_ins.decimal_place
                                print field_ins.precision
                                print field_ins.rounding_option
                                print field_ins.formula_return_type
                                print field_ins.formula_expression
                                print field_ins.prefix
                                print field_ins.suffix
                                print field_ins.start_number
                                print field_ins.json_type
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content

    def get_all_customviews(self):
        try:
            module_ins=ZCRMModule.get_instance('Accounts')
            resp=module_ins.get_all_customviews()
            print resp.status_code
            cv_ins_arr=resp.data
            for customview_ins in cv_ins_arr:
                print "\n\n:::CUSTOM VIEW DETAILS:::"
                print customview_ins.id
                print customview_ins.module_api_name
                print customview_ins.display_value
                print customview_ins.is_default
                print customview_ins.name
                print customview_ins.system_name
                print customview_ins.sort_by
                print customview_ins.category
                fields=customview_ins.fields
                print "\n:::FIELDS:::"
                for field in fields:
                    print field
                print customview_ins.favorite
                print customview_ins.sort_order
                cv_criteria= customview_ins.criteria
                if cv_criteria is not None:
                    print "\n\n :::CRITERIA::::"
                    for criteria_ins in cv_criteria:
                        print criteria_ins.field
                        print criteria_ins.comparator
                        print criteria_ins.value
                    print customview_ins.criteria_pattern
                categories=customview_ins.categories
                print "\n\n :::CATEGORIES::::"
                if categories is not None:
                    for category in categories:
                        print category.actual_value
                        print category.display_value
                print customview_ins.is_off_line
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content

    def get_customview(self):
        try:
            module_ins=ZCRMModule.get_instance('Accounts')
            resp=module_ins.get_customview(1386586000000075535)
            print resp.status_code
            cv_ins_arr=[resp.data]
            for customview_ins in cv_ins_arr:
                print "\n\n:::CUSTOM VIEW DETAILS:::"
                print customview_ins.id
                print customview_ins.module_api_name
                print customview_ins.display_value
                print customview_ins.is_default
                print customview_ins.name
                print customview_ins.system_name
                print customview_ins.sort_by
                print customview_ins.category
                fields=customview_ins.fields
                print "\n:::FIELDS:::"
                for field in fields:
                    print field
                print customview_ins.favorite
                print customview_ins.sort_order
                cv_criteria= customview_ins.criteria
                if cv_criteria is not None:
                    print "\n\n :::CRITERIA::::"
                    for criteria_ins in cv_criteria:
                        print criteria_ins.field
                        print criteria_ins.comparator
                        print criteria_ins.value
                    print customview_ins.criteria_pattern
                categories=customview_ins.categories
                print "\n\n :::CATEGORIES::::"
                if categories is not None:
                    for category in categories:
                        print category.actual_value
                        print category.display_value
                print customview_ins.is_off_line
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content

    def update_module_settings(self):
        try:
            module_instance=ZCRMModule.get_instance('Accounts')
            module_instance.per_page=30
            module_instance.business_card_fields=['Employees','Annual_Revenue','Phone','Account_Type','Fax']
            module_instance.default_custom_view=ZCRMCustomView.get_instance(1386586000000075535, 'All Accounts')
            module_instance.default_territory_id=1386586000001172312
            resp=module_instance.update_module_settings()
            print resp.status_code
            print resp.message
            print resp.code
            print resp.status
            print resp.details
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content

    def update_customview(self):
        try:
            module_ins=ZCRMModule.get_instance('Accounts')
            cv_ins=ZCRMCustomView.get_instance(1386586000000075535, 'Accounts')
            cv_ins.sort_by='Phone'
            cv_ins.sort_order='asc'
            resp=module_ins.update_customview(cv_ins)
            print resp.status_code
            print resp.message
            print resp.code
            print resp.status
            print resp.details
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content

    def get_all_relatedlists(self):
        try:
            module_ins=ZCRMModule.get_instance('Accounts')
            resp=module_ins.get_all_relatedlists()
            print resp.status_code
            relatedlist_instances=resp.data
            for relatedlist_instance in relatedlist_instances:
                print "\n\n:::MODULE RELATEDLIST DETAILS:::"
                print relatedlist_instance.api_name
                print relatedlist_instance.module
                print relatedlist_instance.display_label
                print relatedlist_instance.is_visible
                print relatedlist_instance.name
                print relatedlist_instance.id
                print relatedlist_instance.href
                print relatedlist_instance.type
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content

    def get_relatedlist(self):
        try:
            module_ins=ZCRMModule.get_instance('Accounts')
            resp=module_ins.get_relatedlist(1386586000000003781)
            print resp.status_code
            relatedlist_instances=[resp.data]
            for relatedlist_instance in relatedlist_instances:
                print "\n\n:::MODULE RELATEDLIST DETAILS:::"
                print relatedlist_instance.api_name
                print relatedlist_instance.module
                print relatedlist_instance.display_label
                print relatedlist_instance.is_visible
                print relatedlist_instance.name
                print relatedlist_instance.id
                print relatedlist_instance.href
                print relatedlist_instance.type
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content

    def get_org_details(self):
        try:
            resp=ZCRMRestClient.get_instance().get_organization_details()
            print resp.status_code
            org_ins=resp.data
            print org_ins.company_name
            print org_ins.org_id
            print org_ins.alias
            print org_ins.primary_zuid
            print org_ins.zgid
            print org_ins.primary_email
            print org_ins.website
            print org_ins.mobile
            print org_ins.phone
            print org_ins.employee_count
            print org_ins.description
            print org_ins.time_zone
            print org_ins.iso_code
            print org_ins.currency_locale
            print org_ins.currency_symbol
            print org_ins.street
            print org_ins.state
            print org_ins.city
            print org_ins.country
            print org_ins.zip_code
            print org_ins.country_code
            print org_ins.fax
            print org_ins.mc_status
            print org_ins.is_gapps_enabled
            print org_ins.paid_expiry
            print org_ins.trial_type
            print org_ins.trial_expiry
            print org_ins.is_paid_account
            print org_ins.paid_type
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content

    def get_all_users(self,page=1,per_page=200):
        return self.get_users('all',page,per_page)
    def get_all_deactive_users(self,page=1,per_page=200):
        return self.get_users('DeactiveUsers',page,per_page)
    def get_all_active_users(self,page=1,per_page=200):
        return self.get_users('ActiveUsers',page,per_page)
    def get_all_confirmed_users(self,page=1,per_page=200):
        return self.get_users('ConfirmedUsers',page,per_page)
    def get_all_not_confirmed_users(self,page=1,per_page=200):
        return self.get_users('NotConfirmedUsers',page,per_page)
    def get_all_deleted_users(self,page=1,per_page=200):
        return self.get_users('DeletedUsers',page,per_page)
    def get_all_active_confirmed_users(self,page=1,per_page=200):
        return self.get_users('ActiveConfirmedUsers',page,per_page)
    def get_all_admin_users(self,page=1,per_page=200):
        return self.get_users('AdminUsers',page,per_page)
    def get_all_active_confirmed_admin_users(self,page=1,per_page=200):
        return self.get_users('ActiveConfirmedAdmins',page,per_page)
    def get_current_user(self):
        return self.get_users('CurrentUser')

    def get_users(self,user_type,page,per_page):
        try:
            if user_type=='all':
                resp=ZCRMOrganization.get_instance().get_all_users(page,per_page)
            elif user_type=='DeactiveUsers':
                resp=ZCRMOrganization.get_instance().get_all_deactive_users(page,per_page)
            elif user_type=='ActiveUsers':
                resp=ZCRMOrganization.get_instance().get_all_active_users(page,per_page)
            elif user_type=='ConfirmedUsers':
                resp=ZCRMOrganization.get_instance().get_all_confirmed_users(page,per_page)
            elif user_type=='NotConfirmedUsers':
                resp=ZCRMOrganization.get_instance().get_all_not_confirmed_users(page,per_page)
            elif user_type=='DeletedUsers':
                resp=ZCRMOrganization.get_instance().get_all_deleted_users(page,per_page)
            elif user_type=='ActiveConfirmedUsers':
                resp=ZCRMOrganization.get_instance().get_all_active_confirmed_users(page,per_page)
            elif user_type=='AdminUsers':
                resp=ZCRMOrganization.get_instance().get_all_admin_users(page,per_page)
            elif user_type=='ActiveConfirmedAdmins':
                resp=ZCRMOrganization.get_instance().get_all_active_confirmed_admin_users(page,per_page)
            elif user_type=='CurrentUser':
                resp=ZCRMOrganization.get_instance().get_current_user()
            print resp.status_code
            if resp.status_code!=200:
                return
            users=resp.data
            for user in users:
                print "\n\n"
                print user.id
                print user.name
                print user.signature
                print user.country
                crm_role=user.role
                if crm_role is not None:
                    print crm_role.name
                    print crm_role.id
                customize_info= user.customize_info
                if customize_info is not None:
                    print customize_info.notes_desc
                    print customize_info.is_to_show_right_panel
                    print customize_info.is_bc_view
                    print customize_info.is_to_show_home
                    print customize_info.is_to_show_detail_view
                    print customize_info.unpin_recent_item
                print user.city
                print user.name_format
                print user.language
                print user.locale
                print user.is_personal_account
                print user.default_tab_group
                print user.street
                print user.alias
                user_theme=user.theme
                if user_theme is not None:
                    print user_theme.normal_tab_font_color
                    print user_theme.normal_tab_background
                    print user_theme.selected_tab_font_color
                    print user_theme.selected_tab_background
                print user.state
                print user.country_locale
                print user.fax
                print user.first_name
                print user.email
                print user.zip
                print user.decimal_separator
                print user.website
                print user.time_format
                crm_profile= user.profile
                if crm_profile is not None:
                    print crm_profile.id
                    print crm_profile.name
                print user.mobile
                print user.last_name
                print user.time_zone
                print user.zuid
                print user.is_confirm
                print user.full_name
                print user.phone
                print user.dob
                print user.date_format
                print user.status
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content
    def get_user(self):
        try:
            resp=ZCRMOrganization.get_instance().get_user(1386586000000105001)
            print resp.status_code
            if resp.status_code!=200:
                return
            users=[resp.data]
            for user in users:
                print user.id
                print user.name
                print user.signature
                print user.country
                crm_role=user.role
                if crm_role is not None:
                    print crm_role.name
                    print crm_role.id
                customize_info= user.customize_info
                if customize_info is not None:
                    print customize_info.notes_desc
                    print customize_info.is_to_show_right_panel
                    print customize_info.is_bc_view
                    print customize_info.is_to_show_home
                    print customize_info.is_to_show_detail_view
                    print customize_info.unpin_recent_item
                print user.city
                print user.name_format
                print user.language
                print user.locale
                print user.is_personal_account
                print user.default_tab_group
                print user.street
                print user.alias
                user_theme=user.theme
                if user_theme is not None:
                    print user_theme.normal_tab_font_color
                    print user_theme.normal_tab_background
                    print user_theme.selected_tab_font_color
                    print user_theme.selected_tab_background
                print user.state
                print user.country_locale
                print user.fax
                print user.first_name
                print user.email
                print user.zip
                print user.decimal_separator
                print user.website
                print user.time_format
                crm_profile= user.profile
                if crm_profile is not None:
                    print crm_profile.id
                    print crm_profile.name
                print user.mobile
                print user.last_name
                print user.time_zone
                print user.zuid
                print user.is_confirm
                print user.full_name
                print user.phone
                print user.dob
                print user.date_format
                print user.status
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content

    def create_user(self):
        try:
            user_ins=ZCRMUser.get_instance()
            user_ins.last_name="Python Automation user2"
            user_ins.email='sumanth+pythonautomationusr2@zohocorp.com'
            user_ins.role=ZCRMRole.get_instance(1386586000000026005, 'CEO')
            user_ins.profile=ZCRMProfile.get_instance(1386586000000026011, 'Administrator')
            resp=ZCRMOrganization.get_instance().create_user(user_ins)
            print resp.status_code
            print resp.message
            print resp.code
            print resp.status
            print resp.details
            print resp.data
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content

    def update_user(self):
        try:
            user_ins=ZCRMUser.get_instance(1386586000001409001,'Python Automation user2')
            user_ins.first_name="Poornima"

            resp=ZCRMOrganization.get_instance().update_user(user_ins)
            print resp.status_code
            print resp.message
            print resp.code
            print resp.status
            print resp.details
            print resp.data
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content
    def delete_user(self):
        try:
            resp=ZCRMOrganization.get_instance().delete_user(1386586000001066023)
            print resp.status_code
            print resp.message
            print resp.code
            print resp.status
            print resp.details
            print resp.data
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content

    def get_profiles(self):
        try:
            resp=ZCRMOrganization.get_instance().get_all_profiles()
            profiles=resp.data
            print resp.status_code
            for profile in profiles:
                print "\n\n"
                print profile.name
                print profile.id
                print profile.is_default
                print profile.created_time
                print profile.modified_time
                print profile.modified_by
                print profile.description
                print profile.created_by
                print profile.category
                print profile.permissions
                sections= profile.sections
                if sections is not None:
                    for section in sections:
                        print section.name
                        print section.categories
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content

    def get_profile(self):
        try:
            resp=ZCRMOrganization.get_instance().get_profile(1386586000000026014)
            profiles=[resp.data]
            print resp.status_code
            for profile in profiles:
                print profile.name
                print profile.id
                print profile.is_default
                print profile.created_time
                print profile.modified_time
                print profile.modified_by
                print profile.description
                print profile.created_by
                print profile.category
                permissions= profile.permissions
                if permissions is not None:
                    print ":::PERMISSIONS:::"
                    for permission in permissions:
                        print permission.name
                        print permission.id
                        print permission.display_label
                        print permission.module
                        print permission.is_enabled
                sections= profile.sections
                if sections is not None:
                    for section in sections:
                        print section.name
                        categories=section.categories
                        if categories is not None:
                            print "::::CATEGORIES:::"
                            for category in categories:
                                print category.name
                                print category.display_label
                                print category.permission_ids
                                print category.module
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content

    def get_roles(self):
        try:
            resp=ZCRMOrganization.get_instance().get_all_roles()
            roles=resp.data
            print resp.status_code
            for role in roles:
                print "\n\n"
                print role.name
                print role.id
                print role.display_label
                print role.is_admin
                if role.reporting_to is not None:
                    print role.reporting_to.id
                    print role.reporting_to.name
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content

    def get_role(self):
        try:
            resp=ZCRMOrganization.get_instance().get_role(1386586000000026008)
            roles=[resp.data]
            print resp.status_code
            for role in roles:
                print role.name
                print role.id
                print role.display_label
                print role.is_admin
                if role.reporting_to is not None:
                    print role.reporting_to.id
                    print role.reporting_to.name
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content

    def get_modules(self):
        try:
            resp=ZCRMRestClient.get_instance().get_all_modules()
            modules=resp.data
            print resp.status_code
            for module in modules:
                print "\n\n::MODULE::"
                print module.api_name
                print module.is_convertable
                print module.is_creatable
                print module.is_editable
                print module.is_deletable
                print module.web_link
                print module.singular_label
                print module.plural_label
                print module.modified_by
                print module.modified_time
                print module.is_viewable
                print module.is_api_supported
                print module.is_custom_module
                print module.is_scoring_supported
                print module.id
                print module.module_name
                print module.business_card_field_limit
                print module.business_card_fields
                profiles= module.profiles
                if profiles is not None:
                    for profile in profiles:
                        print profile.name
                        print profile.id
                print module.display_field_name
                print module.display_field_id
                if module.related_lists is not None:
                    for relatedlist in module.related_lists:
                        print relatedlist.display_label
                        print relatedlist.is_visible
                        print relatedlist.api_name
                        print relatedlist.module
                        print relatedlist.name
                        print relatedlist.id
                        print relatedlist.href
                        print relatedlist.type
                if  module.layouts is not None:
                    for layout in module.layouts:
                        self.print_layout(layout)
                if  module.fields is not None:
                    for field_ins in module.fields:
                        self.print_filed(field_ins)
                if module.related_list_properties is not None:
                    print module.related_list_properties.sort_by
                    print module.related_list_properties.sort_order
                    print module.related_list_properties.fields
                print module.properties
                print module.per_page
                print module.search_layout_fields
                print module.default_territory_name
                print module.default_territory_id
                print module.default_custom_view_id
                print module.default_custom_view
                print module.is_global_search_supported
                print module.sequence_number
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content

    def print_layout(self,layout_ins):
        print  "\n\n:::LAYOUT DETAILS:::"
        print  layout_ins.name
        print  layout_ins.id
        print  layout_ins.created_time
        print  layout_ins.modified_time
        print  layout_ins.convert_mapping
        print  layout_ins.is_visible
        print  layout_ins.modified_by.id
        profiles=layout_ins.accessible_profiles
        if profiles is not None:
            for profile in profiles:
                print  "\n\n"
                print  profile.id
                print  profile.name
                print  profile.is_default
        print  layout_ins.created_by
        sections= layout_ins.sections
        if sections is not None:
            print  "\n:::SECTION DETAILS:::"
            for secton in sections:
                print  secton.name
                print  secton.display_name
                print  secton.column_count
                print  secton.sequence_number
                fields=secton.fields
                if fields is not None:
                    print  "\n:::FIELD DETAILS:::"
                    for field_ins in fields:
                        self.print_field(field_ins)

    def print_field(self,field_ins):
        try:
            print field_ins.api_name
            print field_ins.id
            print field_ins.is_custom_field
            print field_ins.lookup_field
            print field_ins.convert_mapping
            print field_ins.is_visible
            print field_ins.field_label
            print field_ins.length
            print field_ins.created_source
            print field_ins.default_value
            print field_ins.is_mandatory
            print field_ins.sequence_number
            print field_ins.is_read_only
            print field_ins.is_unique_field
            print field_ins.is_case_sensitive
            print field_ins.data_type
            print field_ins.is_formula_field
            print field_ins.is_currency_field
            picklist_values=field_ins.picklist_values
            if picklist_values is not None:
                for picklist_value_ins in picklist_values:
                    print  picklist_value_ins.display_value
                    print  picklist_value_ins.actual_value
                    print  picklist_value_ins.sequence_number
                    print  picklist_value_ins.maps
            print field_ins.is_auto_number
            print field_ins.is_business_card_supported
            print field_ins.field_layout_permissions
            print field_ins.decimal_place
            print field_ins.precision
            print field_ins.rounding_option
            print field_ins.formula_return_type
            print field_ins.formula_expression
            print field_ins.prefix
            print field_ins.suffix
            print field_ins.start_number
            print field_ins.json_type
        except Exception as e:
            print e
    def get_module(self):
        try:
            resp=ZCRMRestClient.get_instance().get_module('Accounts')
            modules=[resp.data]
            print resp.status_code
            for module in modules:
                print module.api_name
                print module.is_convertable
                print module.is_creatable
                print module.is_editable
                print module.is_deletable
                print module.web_link
                print module.singular_label
                print module.plural_label
                print module.modified_by
                print module.modified_time
                print module.is_viewable
                print module.is_api_supported
                print module.is_custom_module
                print module.is_scoring_supported
                print module.id
                print module.module_name
                print module.business_card_field_limit
                print module.business_card_fields
                profiles= module.profiles
                if profiles is not None:
                    for profile in profiles:
                        print profile.name
                        print profile.id
                print module.display_field_name
                print module.display_field_id
                if module.related_lists is not None:
                    for relatedlist in module.related_lists:
                        print relatedlist.display_label
                        print relatedlist.is_visible
                        print relatedlist.api_name
                        print relatedlist.module
                        print relatedlist.name
                        print relatedlist.id
                        print relatedlist.href
                        print relatedlist.type
                if  module.layouts is not None:
                    for layout in module.layouts:
                        self.print_layout(layout)
                if  module.fields is not None:
                    for field_ins in module.fields:
                        self.print_field(field_ins)
                if module.related_list_properties is not None:
                    print module.related_list_properties.sort_by
                    print module.related_list_properties.sort_order
                    print module.related_list_properties.fields
                print module.properties
                print module.per_page
                print module.search_layout_fields
                print module.default_territory_name
                print module.default_territory_id
                print module.default_custom_view_id
                print module.default_custom_view
                print module.is_global_search_supported
                print module.sequence_number
        except ZCRMException as ex:
            print ex.status_code
            print ex.error_message
            print ex.error_code
            print ex.error_details
            print ex.error_content


obj=MyClass()
#threading.current_thread().setName('support@zohocrm.com')
#threading.current_thread().__setattr__('current_user_email','support@zohocrm.com')
ZCRMRestClient.initialize()

#obj.test()

#obj.create_record()

#obj.update_record()

#obj.delete_record()

#obj.get_record()

#obj.convert_record()

#obj.upload_attachment()

#obj.upload_link_as_attachment()

#obj.download_attachment()

#obj.delete_attachment()

#obj.upload_photo()

#obj.download_photo()

#obj.delete_photo()

#obj.add_relation()

#obj.remove_relation()

#obj.add_note()

#obj.update_note()

#obj.delete_note()

#obj.get_notes()

#obj.get_attachments()

#obj.get_related_records()

#obj.get_records()

#obj.create_records()

#obj.update_records()

#obj.upsert_records()

#obj.delete_records()

#obj.get_deleted_records('permanent')

#obj.get_deleted_records('recycle')

#obj.get_deleted_records('all')

#obj.search_records()

#obj.get_fields()

#obj.get_field()

#obj.get_all_layouts()

#obj.get_layout()

#obj.get_all_customviews()

#obj.get_customview()

#obj.update_customview()

#obj.update_module_settings()

#obj.get_all_relatedlists()

#obj.get_relatedlist()

#obj.get_org_details()

#obj.get_all_users()

#obj.get_user()

#obj.get_all_active_confirmed_admin_users()

#obj.get_all_active_confirmed_users()

#obj.get_all_active_users()

#obj.get_all_admin_users()

#obj.get_all_confirmed_users()

#obj.get_all_deactive_users()

#obj.get_all_deleted_users()

#obj.get_all_not_confirmed_users()

#obj.get_current_user()

#obj.create_user()

#obj.update_user()

#obj.delete_user()

#obj.get_profiles()

#obj.get_profile()

#obj.get_roles()

#obj.get_role()

#obj.get_modules()

obj.get_module()