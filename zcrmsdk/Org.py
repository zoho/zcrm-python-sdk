'''
Created on Sep 14, 2017

@author: sumanth-3058
'''

try:
    from .Handler import OrganizationAPIHandler
    from .Handler import VariableAPIHandler
    from .Handler import VariableGroupAPIHandler
except ImportError:
    from Handler import OrganizationAPIHandler
    from Handler import VariableAPIHandler
    from Handler import VariableGroupAPIHandler

class ZCRMOrganization(object):
    '''
    classdocs
    '''

    def __init__(self, org_name,org_id):
        '''
        Constructor
        '''
        self.company_name=org_name
        self.org_id=org_id
        self.alias=None
        self.primary_zuid=None
        self.zgid=None
        self.primary_email=None
        self.website=None
        self.mobile=None
        self.phone=None
        self.employee_count=None
        self.description=None
        self.time_zone=None
        self.iso_code=None
        self.currency_locale=None
        self.currency_symbol=None
        self.street=None
        self.state=None
        self.city=None
        self.country=None
        self.zip_code=None
        self.country_code=None
        self.fax=None
        self.mc_status=None
        self.is_gapps_enabled=None
        self.paid_expiry=None
        self.trial_type=None
        self.trial_expiry=None
        self.is_paid_account=None
        self.paid_type=None
        
    @staticmethod
    def get_instance(org_name=None,org_id=None):
        return ZCRMOrganization(org_name,org_id)
    
    def get_user(self,user_id):
        return OrganizationAPIHandler.get_instance().get_user(user_id)
    def get_current_user(self):
        return OrganizationAPIHandler.get_instance().get_current_user()
    def get_all_users(self,page=1,per_page=200):
        return OrganizationAPIHandler.get_instance().get_all_users(page,per_page)
    def get_all_active_users(self,page=1,per_page=200):
        return OrganizationAPIHandler.get_instance().get_all_active_users(page,per_page)
    def get_all_deactive_users(self,page=1,per_page=200):
        return OrganizationAPIHandler.get_instance().get_all_deactive_users(page,per_page)
    def get_all_confirmed_users(self,page=1,per_page=200):
        return OrganizationAPIHandler.get_instance().get_all_confirmed_users(page,per_page)
    def get_all_not_confirmed_users(self,page=1,per_page=200):
        return OrganizationAPIHandler.get_instance().get_all_not_confirmed_users(page,per_page)
    def get_all_deleted_users(self,page=1,per_page=200):
        return OrganizationAPIHandler.get_instance().get_all_deleted_users(page,per_page)
    def get_all_active_confirmed_users(self,page=1,per_page=200):
        return OrganizationAPIHandler.get_instance().get_all_active_confirmed_users(page,per_page)
    def get_all_admin_users(self,page=1,per_page=200):
        return OrganizationAPIHandler.get_instance().get_all_admin_users(page,per_page)
    def get_all_active_confirmed_admin_users(self,page=1,per_page=200):
        return OrganizationAPIHandler.get_instance().get_all_active_confirmed_admin_users(page,per_page)
    def get_all_profiles(self):
        return OrganizationAPIHandler.get_instance().get_all_profiles()
    def get_profile(self,profile_id):
        return OrganizationAPIHandler.get_instance().get_profile(profile_id)
    def get_all_roles(self):
        return OrganizationAPIHandler.get_instance().get_all_roles()
    def get_role(self,role_id):
        return OrganizationAPIHandler.get_instance().get_role(role_id)
    def create_user(self,user_instance):
        return OrganizationAPIHandler.get_instance().create_user(user_instance)
    def update_user(self,user_instance):
        return OrganizationAPIHandler.get_instance().update_user(user_instance)
    def delete_user(self,user_id):
        return OrganizationAPIHandler.get_instance().delete_user(user_id)
    def get_organization_taxes(self):
        return OrganizationAPIHandler.get_instance().get_organization_taxes()
    def get_organization_tax(self,orgtax_id):
        return OrganizationAPIHandler.get_instance().get_organization_tax(orgtax_id)
    def create_organization_taxes(self,orgtax_instances):
        return OrganizationAPIHandler.get_instance().create_organization_taxes(orgtax_instances)
    def update_organization_taxes(self,orgtax_instances):
        return OrganizationAPIHandler.get_instance().update_organization_taxes(orgtax_instances)
    def delete_organization_taxes(self,orgtax_ids):
        return OrganizationAPIHandler.get_instance().delete_organization_taxes(orgtax_ids)
    def delete_organization_tax(self,orgtax_id):
        return OrganizationAPIHandler.get_instance().delete_organization_tax(orgtax_id)

    def get_variables(self):
        handler_ins = VariableAPIHandler.get_instance()
        return handler_ins.get_variables()

    def create_variables(self, variables):
        handler_ins = VariableAPIHandler.get_instance()
        return handler_ins.create_variables(variables)

    def update_variables(self, variables):
        handler_ins = VariableAPIHandler.get_instance()
        return handler_ins.update_variables(variables)

    def get_variable_groups(self):
        handler_ins = VariableGroupAPIHandler.get_instance()
        return handler_ins.get_variable_groups()