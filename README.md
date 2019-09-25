#Python SDK for Zoho CRM
-------------------------
Python SDK acts as a wrapper for Zoho CRM APIs. Hence, invoking a Zoho CRM API from your python client application is just a method call.

Python SDK supports both single user as well as multi-user authentication.

Registering a Zoho Client
-------------------------
Since Zoho CRM APIs are authenticated with OAuth2 standards, you should register your client app with Zoho. 
To register your app:

- Visit the page "https://accounts.zoho.com/developerconsole".
- Click “Add Client ID”.
- Enter Client Name, Client Domain, and Redirect URI. Click “Create”.
- Your Client app is created and displayed.
- Click Options → Edit to know the registered app's Client ID and Client Secret.
(Options is the three dot icon at the right corner).

Setting Up
----------
Python SDK is installable only through **pip**. Pip is a tool for dependency management in Python. The SDK expects following things from the client app.

Client app must have Python 2.7 and above.
>https://www.python.org/downloads/

Client app must have python requests installed
>http://docs.python-requests.org/en/master/user/install/

- The method "ZCRMRestClient.initialize(configuration_dictionary)" must be called on starting up of your application


>MySQL should run in the same machine, either serving at the default port 3306 or a custom port which needs to be configured in ``mysql_port`` in configuration_dictionary.  
The database name should be "zohooauth".  
There must be a table "oauthtokens" with the columns "useridentifier"(varchar(100)), "accesstoken"(varchar(100)), "refreshtoken"(varchar(100)), "expirytime"(bigint). 

If ``token_persistence_path`` is provided in ``configuration_dictionary`` file, then persistence happens in file only. In this case, MySQL is not required.

Create an empty file with name **zcrm_oauthtokens.pkl** in the mentioned ``token_persistence_path``

If Custom DB implementation is used to persist tokens, then "persistence_handler_class" and "persistence_handler_path" keys must be added in ``configuration_dictionary``

Installation of SDK through pip
-------------------------------
Install Pip(if not installed).
Please refer to the document below to install pip.

>https://pip.pypa.io/en/stable/installing/

Install SDK
-----------
Run the following command to install the SDK:

>pip install zcrmsdk

This command installs the SDK and creates a package named ``zcrmsdk`` in the installation directory of python (ex. '/Library/Python/2.7/site-packages').

Upgrade the SDK
---------------
Run this command to upgrade the SDK to the latest version.

>pip install --upgrade zcrmsdk

Configuration
--------------
Below is a sample configuration dictionary containing all keys, which needs to be passed to ZCRMRestClient.initialize() on starting up your application.
>configuration_dictionary = { <br>
'apiBaseUrl':'https://www.zohoapis.com',<br>
'apiVersion':'v2',<br>
'currentUserEmail':'email@gmail.com' <br>
'sandbox':'False'<br>
'applicationLogFilePath':'',<br>
'client_id':'1000.3xxxxxxxxxxxxxxxxxxxxxxxxX0YW',<br>
'client_secret':'29xxxxxxxxxxxxxxxxxxxxxxxxxxxxx7e32',<br>
'redirect_uri':'https://www.abc.com',<br>
'accounts_url':'https://accounts.zoho.com',<br>
'token_persistence_path':'/Users/Zoho/Desktop/PythonSDK/FilePersistence',<br>
'access_type':'online',<br>
//Use the below keys for MySQL DB persistence<br>
'mysql_username':'',<br>
'mysql_password':'',<br>
'mysql_port':'3306',<br>
//Use the below keys for custom DB persistence<br>
'persistence_handler_class' : 'Custom',<br>
'persistence_handler_path': '/Users/Zoho/Desktop/PythonSDK/CustomPersistance.py'<br>
}

Based on the preferred persistence, add all mandatory keys in the configuration dictionary.
client_id, client_secret and redirect_uri are your OAuth client’s configurations that you get upon registering your Zoho client.

access_type must be set to offline, as online OAuth client is not supported by the SDK as of now.

``token_persistence_path`` is the path to store the OAuth related tokens in file. If this is set, then there is no need of `database` for persistence. Persistence happens through `file` only.

Based on your domain(EU, CN), change the value of `accounts_url`. Default value is `https://accounts.zoho.com`.

Include the absolute path in **configuration_dictionary** for the key ``applicationLogFilePath`` to store the logs. This file is to log the exceptions during the usage of the SDK.

To make API calls to `sandbox account`, set sandbox value in the configuration_dictionary. By default, the value is `false`.

>'sandbox':'true'

If your application needs only single user authentication then you have to set the user Email ID in the configuration_dictionary as below.

>'currentUserEmail':'user@email.com'


To work with multi-user authentication, set the user Email ID in current thread as an attribute.

>threading.current_thread().__setattr__('current_user_email','user@email.com')

You can use the above method for single user authentication too, but it is recommended to set the email ID in the ``configuration_dictionary``

If you do not set the user email in current thread, then the SDK expects it from the ``configuration_dictionary``.

The SDK raises an exception if user_email is not set in any of the above mentioned methods.

Initialization
--------------
The app will be ready to be initialized after defining the OAuth configuration file.

Generating self-authorized grant token
For self client apps, the self-authorized grant token should be generated from the Zoho Developer Console (https://accounts.zoho.com/developerconsole)

- Visit https://accounts.zoho.com/developerconsole
- Click Options → Self Client of the client that you want to authorize.
- Enter one or more (comma-separated) valid Zoho CRM scopes that you wish to authorize in the “Scope” field and choose the time of expiry. Provide “aaaserver.profile.READ” scope along with other Zoho CRM scopes.
- Copy the grant token for backup.
- Generate refresh_token from grant token by using the below URL (POST request).
 ``https://accounts.zoho.com/oauth/v2/token?code={grant_token}&redirect_uri={redirect_uri}&client_id={client_id}&client_secret={client_secret}&grant_type=authorization_code``
Copy the refresh_token for backup.

Note that the generated grant token is valid only for the stipulated time you choose while generating it. 

Hence, a refresh token should be generated within that time.

Generating access token
-----------------------
Access token can be generated from grant token or refresh token. Following any one of the below two methods is sufficient.    

Access Token through grant token:
------------------------------------
Execute the following code snippet from your main class to get an access token. 

Paste the generated grant token in the string literal mentioned. This is one-time process only.

>ZCRMRestClient.initialize(configuration_dictionary) <br>
oauth_client = ZohoOAuth.get_client_instance()  <br>
grant_token="paste_grant_token_here" <br>
oauth_tokens = oauth_client.generate_access_token(grant_token) <br>

Upon successful execution of the above code snippet, the generated access and refresh tokens will be persisted through our persistence handler class, based on the preferred persistence.

Access Token through refresh token:
------------------------------------
Executed the below code snippet from your main class to get an access token. 

Paste the generated refresh token in the string literal mentioned. This is one time process only.

>ZCRMRestClient.initialize(configuration_dictionary) <br>
oauth_client = ZohoOAuth.get_client_instance()<br>
refresh_token="paste_refresh_token_here"  <br>
user_identifier="provide_user_identifier_like_email_here"  <br>
oauth_tokens = oauth_client.generate_access_token_from_refresh_token(refresh_token,user_identifier) <br>

Upon successful execution of the above code, the generated access and given refresh tokens will be persisted through our persistence handler class, based on the preferred persistence.

Once the OAuth tokens have been persisted, subsequent API calls will use these tokens. 

The SDK will take care of refreshing the access token using the refresh token, as and when required.

App Startup
------------
Invoke the below statement every time your client app is started.

>ZCRMRestClient.initialize(configuration_dictionary)

Once the SDK has been initialized by the above line, you can use any APIs of the SDK to get the desired results.

Using the SDK
-------------
Add the below line in your client app Python files, where you would like to use the SDK.

>import zcrmsdk

By this, you can access all the functionalities of Python SDK.

For accessing a module or class use ``zcrmsdk.ClassName``


Class Hierarchy
---------------
All Zoho CRM entities are modelled as modules having classes, methods, and instance variables applicable to that particular entity. ZCRMRestClient is the base class of the SDK. ZCRMRestClient has methods to get instances of various other Zoho CRM entities. It is in RestClient module.
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
``ZCRMRestClient.get_module("Contacts")`` would return the actual Contacts module, that has all the properties of the Contacts module filled through an API call.

``ZCRMRestClient.get_module_instance("Contacts")`` would return a dummy ZCRMModule object that would refer to the Contacts module, with no properties filled, since this does not make an API call.

Hence, to get records from a module, you need not to start all the way from ZCRMRestClient. Instead, you could get a ZCRMModule instance with ZCRMModule.get_instance() and then invoke its non-static get_records() method from the created instance. 

This would avoid the API call which would have been triggered to populate the ZCRMModule object.

Accessing record properties
----------------------------
Since record properties are dynamic across modules, we have only given the common fields like created_time, created_by, owner etc as ZCRMRecord’s default properties. 

All other record properties are available as a dictionary in ZCRMRecord object.

To access the individual field values of a record, use the getter and setter methods available. 

The keys of the record properties dictionary are the API names of the module’s fields. 

API names of all fields of all modules are available under ``Setup → Developer Space → APIs → API Names``.

To get a field value, use ``record.get_field_value(field_api_name)``. 

To set a field value, use ``record.set_field_value(field_api_name,new_value)``. 

While setting a field value, ensure that the set value is of the apt data type of the field to which you are going to set it.

Response Handling
-----------------
``APIResponse`` and ``BulkAPIResponse`` are wrapper objects for Zoho CRM APIs’ responses. All API calling methods will return one of these two objects.

DownloadFile and downloadPhoto returns ``FileAPIResponse`` instead of APIResponse.

A method seeking a single entity would return APIResponse object, whereas a method seeking a list of entities would return BulkAPIResponse object.

Use the instance variable **data** to get the entity data alone from the response wrapper objects. APIResponse.data would return a single Zoho CRM entity object, while BulkAPIResponse.data would return a list of Zoho CRM entity objects.

Other than data, these response wrappers have the following properties:

``response_headers`` — remaining API count for the present day/window and time elapsed for the present window reset.

``info`` — any other information, if provided by the API, besides the actual data.

``bulk_entity_response`` (list of ``EntityResponse`` instances) — status of individual entities in a bulk API. For example, an insert records API may partially fail because of a few records. This array gives the individual records’ creation status.

Exceptions
All unexpected behaviors like faulty API responses, SDK anomalies are handled by the SDK and are raised only as a single exception — ZCRMException. Hence it's enough to catch this exception alone in the client app code.


Examples
---------
Sample code to insert a record:
-------------------------------

>try:  <br>
&nbsp;&nbsp;&nbsp;&nbsp;record_ins_list=list()  <br>
&nbsp;&nbsp;&nbsp;&nbsp;for i in range(0,2):<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;record=ZCRMRecord.get_instance('Invoices') #module API Name  <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;record.set_field_value('Subject', 'Invoice'+str(i))  <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;record.set_field_value('Account_Name', 'IIIT')  <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;user=ZCRMUser.get_instance(440872000000175001,'Python Automation User1')<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;record.set_field_value('Owner',user)  <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;line_item=ZCRMInventoryLineItem.get_instance(ZCRMRecord.get_instance("Products",440872000000224005))<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;line_item.discount=10  <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;line_item.list_price=8  <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;line_item.description='Product Description' <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;line_item.quantity=100  <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;line_item.tax_amount=2.5  <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;taxIns=ZCRMTax.get_instance("Vat")  <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;taxIns.percentage=5  <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;line_item.line_tax.append(taxIns) <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;record.add_line_item(line_item)  <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;record_ins_list.append(record)  <br>
&nbsp;&nbsp;&nbsp;&nbsp;resp=ZCRMModule.get_instance('Invoices').create_records(record_ins_list) <br>
&nbsp;&nbsp;&nbsp;&nbsp;print resp.status_code  <br>
&nbsp;&nbsp;&nbsp;&nbsp;entity_responses=resp.bulk_entity_response  <br>
&nbsp;&nbsp;&nbsp;&nbsp;for entity_response in entity_responses: <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;print entity_response.details  <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;print entity_response.status  <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;print entity_response.message  <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;print entity_response.code  <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;print entity_response.data.entity_id  <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;print entity_response.data.created_by.id  <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;print entity_response.data.created_time  <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;print entity_response.data.modified_by.id  <br>
except ZCRMException as ex:  <br>
&nbsp;&nbsp;&nbsp;&nbsp;print ex.status_code  <br>
&nbsp;&nbsp;&nbsp;&nbsp;print ex.error_message  <br>
&nbsp;&nbsp;&nbsp;&nbsp;print ex.error_code  <br>
&nbsp;&nbsp;&nbsp;&nbsp;print ex.error_details  <br>
&nbsp;&nbsp;&nbsp;&nbsp;print ex.error_content  <br>

Sample code to fetch records:
-----------------------------

>try:  <br>
&nbsp;&nbsp;&nbsp;&nbsp;module_ins=ZCRMModule.get_instance('Products') #module API Name  <br>
&nbsp;&nbsp;&nbsp;&nbsp;resp=module_ins.get_records()  <br>
&nbsp;&nbsp;&nbsp;&nbsp;print resp.status_code  <br>
&nbsp;&nbsp;&nbsp;&nbsp;record_ins_arr=resp.data  <br>
&nbsp;&nbsp;&nbsp;&nbsp;for record_ins in record_ins_arr: <br> 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;print record_ins.entity_id  <br> 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;print record_ins.owner.id  <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;print record_ins.created_by.id <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;print record_ins.modified_by.id  <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;print record_ins.created_time <br> 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;print record_ins.modified_time  <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;product_data=record_ins.field_data  <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;for key in product_data:  <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;print key+":"+str(product_data[key]) <br>
except ZCRMException as ex:  <br>
&nbsp;&nbsp;&nbsp;&nbsp;print ex.status_code  <br>
&nbsp;&nbsp;&nbsp;&nbsp;print ex.error_message  <br>
&nbsp;&nbsp;&nbsp;&nbsp;print ex.error_code  <br>
&nbsp;&nbsp;&nbsp;&nbsp;print ex.error_details  <br>
&nbsp;&nbsp;&nbsp;&nbsp;print ex.error_content  <br>

For more APIs, please refer [this link](https://www.zoho.com/crm/developer/docs/)