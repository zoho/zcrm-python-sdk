'''
Created on Sep 14, 2017

@author: sumanth-3058
'''

try:
    from .Handler import OrganizationAPIHandler
except ImportError:
    from Handler import OrganizationAPIHandler

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
    