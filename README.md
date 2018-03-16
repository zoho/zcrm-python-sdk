#Python SDK for Zoho CRM
-------------------------
Python SDK for Zoho CRM APIs provides wrapper for Zoho CRM APIs. Hence invoking a Zoho CRM API from your python client application is just a method call.

Python SDK supports both single user as well as multi-user authentication.

Registering a Zoho Client
-------------------------
Since Zoho CRM APIs are authenticated with OAuth2 standards, you should register your client app with Zoho. 
To register your app:

- Visit this page https://accounts.zoho.com/developerconsole.
- Click on “Add Client ID”.
- Enter Client Name, Client Domain and Redirect URI then click “Create”.
- Your Client app would have been created and displayed by now.
- The newly registered app's Client ID and Client Secret can be found by clicking Options → Edit.
(Options is the three dot icon at the right corner).

Setting Up
----------
Python SDK is installable through **pip**. Pip is a tool for dependency management in Python. The SDK expects following things from the client app

Client app must have Python 2.7 and above.
>https://www.python.org/downloads/

Client app must have python requests being installed
>http://docs.python-requests.org/en/master/user/install/

- SDK must be installed through pip.
- The method `ZCRMRestClient.initialize()` must be called on starting up of your application

>MySQL should run in the same machine serving at the default port 3306.  
The database name should be "zohooauth".  
There must be a table "oauthtokens" with the columns "useridentifier"(varchar(100)), "accesstoken"(varchar(100)), "refreshtoken"(varchar(100)), "expirytime"(bigint). 

If ``token_persistence_path`` provided in ``oauth_configuration.properties`` file, then persistence happens in file only. In this case, no need of MySQL

Create a empty file with name **zcrm_oauthtokens.pkl** in the mentioned ``token_persistence_path``

Installation of SDK through pip
-------------------------------
Install Pip(if not installed)
Please refer the document below to install pip

>https://pip.pypa.io/en/stable/installing/

Install SDK
-----------
Run the following command to install the SDK:

>pip install zcrmsdk

By this SDK would have installed and a package named ``zcrmsdk`` would have been created in the installation directory of python (ex. '/Library/Python/2.7/site-packages').

Upgrade the SDK
---------------
Run this command to upgrade the SDK to the latest version.

>pip install --upgrade zcrmsdk

Configurations
--------------
Your OAuth Client details should be given to the SDK as a property file.  
In SDK, we have placed a configuration file (oauth_configuration.properties).   
Please place the respective values in that file. You can find that file under 'zcrmsdk/resources'.  
Please fill the values for the following keys alone.

>client_id=  
client_secret=  
redirect_uri=  
accounts_url=https://accounts.zoho.com  
token_persistence_path=  

client_id, client_secret and redirect_uri are your OAuth client’s configurations that you get after registering your Zoho client.

access_type must be set to offline only because online OAuth client is not supported by the SDK as of now.

``token_persistence_path`` is the path to store the OAuth related tokens in file. If this is set then, no need of `database` for persistence. Persistence happens through `file` only.

Based on your domain(EU,CN) please change the value of `accounts_url`. Default value set as US domain

Include the absolute path in **configuration.properties** for the key ``applicationLogFilePath`` to store the logs. You can find that file under `zcrmsdk/resources`. This file is to log the exceptions during the usage of SDK.

Please fill the value for the following key alone. If log path is not provided then logs won't be stored but you can see them in console

>applicationLogFilePath=

To make API calls to `sandbox account`, please change the value of following key to `true`. By default the value is `false`  

>sandbox=true


If your application needs only single user authentication then you have to set the user Email Id in configurations.properties file like below.

>currentUserEmail=user@email.com


In order to work with multi user authentication, you need to set the user EmailId in current thread as an attribute.

>threading.current_thread().__setattr__('current_user_email','user@email.com')

You can use the above one for single user authentication also but it's recommended to go with setting of email Id in ``configuration.properties`` file.

If you don't set the user email in current thread then SDK expect it from ``configuration.properties`` file. 

If user email is not set in any of these two then SDK will raise exception.

Initialization
--------------
The app would be ready to be initialized after defining the OAuth configuration file.

Generating self-authorized grant token
For self client apps, the self authorized grant token should be generated from the Zoho Developer Console (https://accounts.zoho.com/developerconsole)

- Visit https://accounts.zoho.com/developerconsole
- Click Options → Self Client of the client for which you wish to authorize.
- Enter one or more (comma separated) valid Zoho CRM scopes that you wish to authorize in the “Scope” field and choose the time of expiry. Provide “aaaserver.profile.READ” scope along with Zoho CRM scopes.
- Copy the grant token for backup
- Generate refresh_token from grant token by using below URL (POST request)
 ``https://accounts.zoho.com/oauth/v2/token?code={grant_token}&redirect_uri={redirect_uri}&client_id={client_id}&client_secret={client_secret}&grant_type=authorization_code``

Copy the refresh_token for backup

Please note that the generated grant token is valid only for the stipulated time you choose while generating it. 

Hence, refresh token should be generated within that time.

Generating access token
-----------------------
Access token can be generated by grant token or refresh token. Following any one of the two methods is sufficient.    

Access Token through grant token:
------------------------------------
The following code snippet should be executed from your main class to get access token. 

Please paste the generated grant token in the string literal mentioned. This is one time process only.

>ZCRMRestClient.initialize()  
oauth_client = ZohoOAuth.get_client_instance()  
grant_token="paste_grant_token_here"  
oauth_tokens = oauth_client.generate_access_token(grant_token) 

Upon successful execution of the above code snippet, the generated access and refresh tokens would have been persisted through our persistence handler class.

Access Token through refresh token:
------------------------------------
The following code snippet should be executed from your main class to get access token. 

Please paste the generated refresh token in the string literal mentioned. This is one time process only.

>ZCRMRestClient.initialize()  
oauth_client = ZohoOAuth.get_client_instance()  
refresh_token="paste_refresh_token_here"  
user_identifier="provide_user_identifier_like_email_here"  
oauth_tokens = oauth_client.generate_access_token_from_refresh_token(refresh_token,user_identifier) 

Upon successful execution of the above code snippet, the generated access and given refresh tokens would have been persisted through our persistence handler class.

Once the OAuth tokens have been persisted, subsequent API calls would use the persisted access and refresh tokens. 

The SDK will take care of refreshing the access token using refresh token, as and when required.

App Startup
------------
The SDK requires the following line of code invoked every time your client app is started.

>ZCRMRestClient.initialize()

Once the SDK has been initialized by the above line, you could use any APIs of the SDK to get proper results.

Using the SDK
-------------
Add the below line in your client app Python files, where you would like to make use of SDK.

>import zcrmsdk

By this, you can access all the functionalities of the Python SDK.

For accessing a module or class use ``zcrmsdk.ClassName``


Class Hierarchy
---------------
All Zoho CRM entities are modelled as modules having classes, methods and instance variables applicable to that particular entity. ZCRMRestClient is the base class of the SDK. ZCRMRestClient has methods to get instances of various other Zoho CRM entities. It is in RestClient module.
The class relations and hierarchy of the SDK follows the entity hierarchy inside Zoho CRM. The class hierarchy of various Zoho CRM entities are given below:


 - ZCRMRestClient
   - ZCRMOrganization
     - ZCRMUser
       - ZCRMUserTheme
         - ZCRMUserCustomizeInfo
       - ZCRMRole
       - ZCRMProfile
         - ZCRMPermission
         - ZCRMProfileSection
           - ZCRMProfileCategory
     - ZCRMModule
       - ZCRMLayout
         - ZCRMSection
           - ZCRMField
           - ZCRMPickListValue
           - ZCRMLookupField
       	 - ZCRMLeadConvertMapping
           - ZCRMLeadConvertMappingField
       - ZCRMCustomView
         - ZCRMCustomViewCategory
         - ZCRMCustomViewCriteria
       - ZCRMRelatedListProperties
         - ZCRMModuleRelatedList
       - ZCRMRecord
       - ZCRMNote
       - ZCRMAttachment
       - ZCRMInventoryLineItem
         - ZCRMTax
       - ZCRMEventParticipant
       - ZCRMPriceBookPricing
       - ZCRMModuleRelation
       - ZCRMJunctionRecord
       - ZCRMTrashRecord

As appearing in the hierarchy, every entity class will have instance variables to fetch its own properties and to fetch data of its immediate child entities through an API call.

For example, a Zoho CRM module (ZCRMModule) object will have instance variables to get a module’s properties like display name, module id, etc. and will also have instance variables to fetch all its child objects(like ZCRMLayout).

Instantiate object
------------------
It is not always effective to follow the complete class hierarchy from the top to fetch the data of an entity at some lower level, since this would involve API calls at each level. 

In order to handle this, every entity class will have a ``get_instance()`` method to get its own dummy object and instance variables to get dummy objects of its child entities.

Please note that the get_instance() method would not have any of its properties filled because it would not fire an API call. This would just return a dummy object that shall be only used to access the non-static methods of the class.

Summing it up
-------------
``ZCRMRestClient.get_module("Contacts")`` would return the actual Contacts module, that has all the properties of the Contacts module filled through an API call

``ZCRMRestClient.get_module_instance("Contacts")`` would return a dummy ZCRMModule object that would refer to the Contacts module, with no properties filled, since this doesn’t make an API call.

Hence, to get records from a module, you need not to start all the way from ZCRMRestClient. Instead, you could get a ZCRMModule instance with ZCRMModule.get_instance() and then invoke its non-static get_records() method from the created instance. 

This would avoid the API call which would have been triggered to populate the ZCRMModule object.

Accessing record properties
----------------------------
Since record properties are dynamic across modules, we have only given the common fields like created_time, created_by, owner etc. as ZCRMRecord’s default properties. 

All other record properties are available as a dictionary in ZCRMRecord object.

To access the individual field values of a record, use the getter and setter methods available. 

The keys of the record properties dictionary are the API names of the module’s fields. 

API names of all fields of all modules are available under ``Setup → Extensions & APIs → APIs → CRM API → API Names``.

To get a field value, use ``record.get_field_value(field_api_name)``. 

To set a field value, use ``record.set_field_value(field_api_name,new_value)``. 

While setting a field value, please make sure of that the set value is of the apt data type of the field to which you are going to set it.

Response Handling
-----------------
``APIResponse`` and ``BulkAPIResponse`` are wrapper objects for Zoho CRM APIs’ responses. All API calling methods would return one of these two objects.

DownloadFile and downloadPhoto returns ``FileAPIResponse`` instead of APIResponse.

A method seeking a single entity would return APIResponse object, whereas a method seeking a list of entities would return BulkAPIResponse object.

Use the instance variable **data** to get the entity data alone from the response wrapper objects. APIResponse.data would return a single Zoho CRM entity object, while BulkAPIResponse.data would return a list of Zoho CRM entity objects.

Other than data, these response wrapper objects have the following properties:

``response_headers`` — remaining API counts for the present day/window and time elapsed for the present window reset.

``info`` — any other information, if provided by the API, in addition to the actual data.

``bulk_entity_response`` (list of ``EntityResponse`` instances) — status of individual entities in a bulk API. For example, in an insert records API may partially fail because of a few records. This array gives the individual records’ creation status.
Exceptions

All unexpected behaviors like faulty API responses, SDK anomalies are handled by the SDK and are raised only as a single exception — ZCRMException. Hence its enough to catch this exception alone in the client app code.


Examples
---------
Sample code to insert a record:
-------------------------------

>try:  
  record_ins_list=list()  
  for i in range(0,2):  
  	record=ZCRMRecord.get_instance('Invoices') #module API Name  
   	record.set_field_value('Subject', 'Invoice'+str(i))  
   	record.set_field_value('Account_Name', 'IIIT')  
   	user=ZCRMUser.get_instance(440872000000175001,'Python Automation User1')  
   	record.set_field_value('Owner',user)  
   	line_item=ZCRMInventoryLineItem.get_instance(ZCRMRecord.get_instance("Products",440872000000224005))  
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
except ZCRMException as ex:  
    print ex.status_code  
    print ex.error_message  
    print ex.error_code  
    print ex.error_details  
    print ex.error_content  

    
Sample code to fetch records:
-----------------------------

>try:  
	module_ins=ZCRMModule.get_instance('Products') #module API Name  
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
except ZCRMException as ex:  
	print ex.status_code  
	print ex.error_message  
	print ex.error_code  
	print ex.error_details  
	print ex.error_content  

For more APIs, please refer [this link](https://www.zoho.com/crm/help/api/v2/#api-reference)
