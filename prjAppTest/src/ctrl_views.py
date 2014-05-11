# -*- coding: utf-8 -*-
'''
Created on Oct 1, 2013

@author: Alan Tai
'''
__author__ = 'Alan Tai'
from google.appengine.ext.key_range import ndb
import time
import datetime
import webapp2
import jinja2
import os
import json
from google.appengine.api import users, mail, memcache
from app_dict import Key_Value
from models import Size, SUDATrackingNumber_REGULAR, SpearnetPackagesInfo, TWCustomEntryTrackingNumber, \
    ClientsInfo, GeneralClientsPackagesInfo, SUDATrackingNumber_FORMAL, \
    TWCustomEntryInfo, EmployeeInfo, EmailVerification, SpearnetPackagesInfoLog, \
    GeneralClientsPackagesInfoLog, PackageStatusNotification_Email,\
    TWCustomEntryInfoLog
from general_handlers.users_info_handler import Users_Info_Handler
from general_handlers.emails_handler import Email_Handler
from general_handlers.cron_tasks_handler import Cron_Tasks_Handler
# from app_handlers.cron_tasks_handler import Cron_Tasks_Handler

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + '/static/templates'))  # append templates' path

# exshipper main index handler
class ExShipperIndexHandler(webapp2.RequestHandler):
    def get(self):
        my_dict = Key_Value()  # get key-value pair dictionary
        user_info = Users_Info_Handler().get_users_info(self, users)
        index_page = my_dict.exshipper_index_page
        template_values = {'title':my_dict.exshipper_index_page_title}
        
        #packages summary
        spearnet_customers_packages_info = SpearnetPackagesInfo.query()
        general_clients_packages_info = GeneralClientsPackagesInfo.query()
        tw_custom_entry_packages_info = TWCustomEntryInfo.query()
        
        template_values.update({'spearnet_customers_packages_info':spearnet_customers_packages_info})
        template_values.update({'general_clients_packages_info':general_clients_packages_info})
        template_values.update({'tw_custom_entry_packages_info':tw_custom_entry_packages_info})
        template_values.update(user_info)
        
        template = jinja_environment.get_template(index_page)
        self.response.out.write(template.render(template_values))

# for handling the exshipper users login process
class ExShipperLoginHandler(webapp2.RequestHandler):
    # login page
    def get(self):
        my_dict = Key_Value()
        user_info = Users_Info_Handler().get_users_info(self, users)
        login_page = my_dict.exshipper_login_page
        
        dispatch_token = self.request.get('dispatch_token')
        
        template_values = {'title':my_dict.exshipper_login_page_title, 'dispatch_token':dispatch_token}
        template_values.update(user_info)
        
        template = jinja_environment.get_template(login_page)
        self.response.out.write(template.render(template_values))
        
    # dispatch user to different pages according to the token, account and, password which users submit
    def post(self):
        my_dict = Key_Value()
        user_info = Users_Info_Handler().get_users_info(self, users)
        dispatch_token = self.request.get('dispatch_token')
        exshipper_account = self.request.get('exshipper_account')
        exshipper_password = self.request.get('exshipper_password')
        template_values = {}
        
        # set default page source and title as invalid login page
        html_page = my_dict.exshipper_invalid_login_page
        html_page_title = my_dict.exshipper_invalid_login_page_title
        
        # web-pages dispatcher
        # page of creating invoice
        if(dispatch_token == 'exshipper_create_invoice' and exshipper_account == 'alantai' and exshipper_password == '1014lct'):
            html_page = my_dict.exshipper_invoice_creating_page
            html_page_title = my_dict.exshipper_invoice_creating_page_title
                
        elif(dispatch_token == 'exshipper_create_employee_info' and exshipper_account == 'alantai' and exshipper_password == '1014lct'):
            html_page = my_dict.exshipper_create_employee_info_page
            html_page_title = my_dict.exshipper_create_employee_info_page_title
                
        # page of creating client info
        elif(dispatch_token == 'exshipper_create_client_info' and exshipper_account == 'alantai' and exshipper_password == '1014lct'):
            clients_data = ClientsInfo.query()
            template_values.update({'clients_data':clients_data})
            html_page = my_dict.exshipper_create_client_info_handler
            html_page_title = my_dict.exshipper_create_client_info_handler_title
                
        # page of uploading suda tracking numbers
        elif(dispatch_token == 'exshipper_suda_tracking_number_upload' and exshipper_account == 'alantai' and exshipper_password == '1014lct'):
            html_page = my_dict.exshipper_suda_tracking_number_upload_handler_page
            html_page_title = my_dict.exshipper_suda_tracking_number_upload_handler_page_title
                
        # page of uploading tw custom entry numbers
        elif(dispatch_token == 'exshipper_tw_custom_entry_number_upload' and exshipper_account == 'alantai' and exshipper_password == '1014lct'):
            html_page = my_dict.exshipper_tw_custom_entry_number_handler_page
            html_page_title = my_dict.exshipper_tw_custom_entry_number_handler_page_title
                
        # page of handling spearnet customers packages information
        # packages status are spearnet, pickup, and exshipper
        elif(dispatch_token == 'exshipper_spearnet_customers_packages_info_log_processing' and exshipper_account == 'alantai' and exshipper_password == '1014lct'):
            html_page = my_dict.exshipper_spearnet_customer_package_info_log_page
            html_page_title = my_dict.exshipper_spearnet_customer_package_info_log_page_title
            
            # use memcache to show information users had read (ignore the error message)
#                 data = memcache.get('spearnet_customer_package_info_log')
#                 if data is not None:
#                     log_spearnet_customer_package_info = data
#                 else:
#                     data = SpearnetPackagesInfo.query()
#                     memcache.add('spearnet_customer_package_info_log',data,1000)
#                     log_spearnet_customer_package_info = data

            # query package information (packages' status == spearnet or exshipper)
            spearnet_customer_package_info_log = SpearnetPackagesInfo.query(ndb.OR(SpearnetPackagesInfo.package_status == 'spearnet',
                                                                                   SpearnetPackagesInfo.package_status == 'pickup',
                                                                                   SpearnetPackagesInfo.package_status == 'exshipper'))
            # pass clients informations
            clients_info = ClientsInfo().query()
            template_values.update({'spearnet_customer_package_info_log': spearnet_customer_package_info_log, 'clients_info':clients_info, 'dispatch_token':dispatch_token})
        
        # packages status are apex, sfo, taoyuan international airport, and suda
        elif(dispatch_token == 'exshipper_spearnet_customers_packages_info_log_processed' and exshipper_account == 'alantai' and exshipper_password == '1014lct'):
            html_page = my_dict.exshipper_spearnet_customer_package_info_log_page
            html_page_title = my_dict.exshipper_spearnet_customer_package_info_log_page_title
            

            # query package information (packages' status == spearnet or exshipper)
            spearnet_customer_package_info_log = SpearnetPackagesInfo.query(ndb.OR(SpearnetPackagesInfo.package_status == 'apex',
                                                                                   SpearnetPackagesInfo.package_status == 'sfo_airport',
                                                                                   SpearnetPackagesInfo.package_status == 'taiwan_taoyuan_airport',
                                                                                   SpearnetPackagesInfo.package_status == 'tw_custom_entry',
                                                                                   SpearnetPackagesInfo.package_status == 'tw_logistics'))
            # pass clients informations
            clients_info = ClientsInfo().query()
            template_values.update({'spearnet_customer_package_info_log': spearnet_customer_package_info_log, 'clients_info':clients_info, 'dispatch_token':dispatch_token})
                  
        
        # packages status are apex, sfo, taoyuan international airport, and suda
        elif(dispatch_token == 'exshipper_spearnet_customers_packages_info_log_delivered' and exshipper_account == 'alantai' and exshipper_password == '1014lct'):
            html_page = my_dict.exshipper_spearnet_customer_package_info_log_page
            html_page_title = my_dict.exshipper_spearnet_customer_package_info_log_page_title
            

            # query package information (packages' status == spearnet or exshipper)
            spearnet_customer_package_info_log = SpearnetPackagesInfo.query(ndb.OR(SpearnetPackagesInfo.package_status == 'delivered'))
            # pass clients informations
            clients_info = ClientsInfo().query()
            template_values.update({'spearnet_customer_package_info_log': spearnet_customer_package_info_log, 'clients_info':clients_info, 'dispatch_token':dispatch_token})
                  
            
              
        # page of handling general clients packages information
        elif(dispatch_token == 'exshipper_general_clients_packages_info_log_processing' and exshipper_account == 'alantai' and exshipper_password == '1014lct'):
            html_page = my_dict.exshipper_general_clients_package_info_log_page
            html_page_title = my_dict.exshipper_general_clients_package_info_log_page_title
            
            # query package information (packages' status == spearnet or exshipper)
            general_clients_packages_info_log = GeneralClientsPackagesInfo.query(ndb.OR(GeneralClientsPackagesInfo.package_status == 'client',
                                                                                        GeneralClientsPackagesInfo.package_status == 'pickup',
                                                                                        GeneralClientsPackagesInfo.package_status == 'exshipper'))
            clients_info = ClientsInfo().query()
            template_values.update({'general_clients_packages_info_log':general_clients_packages_info_log, 'clients_info':clients_info, 'dispatch_token':dispatch_token})
           
        elif(dispatch_token == 'exshipper_general_clients_packages_info_log_processed' and exshipper_account == 'alantai' and exshipper_password == '1014lct'):
            html_page = my_dict.exshipper_general_clients_package_info_log_page
            html_page_title = my_dict.exshipper_general_clients_package_info_log_page_title
            
            # query package information (packages' status == spearnet or exshipper)
            general_clients_packages_info_log = GeneralClientsPackagesInfo.query(ndb.OR(GeneralClientsPackagesInfo.package_status == 'apex',
                                                                                        GeneralClientsPackagesInfo.package_status == 'sfo_airport',
                                                                                        GeneralClientsPackagesInfo.package_status == 'taiwan_taoyuan_airport',
                                                                                        GeneralClientsPackagesInfo.package_status == 'tw_custom_entry',
                                                                                        GeneralClientsPackagesInfo.package_status == 'tw_logistics'))
            clients_info = ClientsInfo().query()
            template_values.update({'general_clients_packages_info_log':general_clients_packages_info_log, 'clients_info':clients_info, 'dispatch_token': dispatch_token})
           
        elif(dispatch_token == 'exshipper_general_clients_packages_info_log_delivered' and exshipper_account == 'alantai' and exshipper_password == '1014lct'):
            html_page = my_dict.exshipper_general_clients_package_info_log_page
            html_page_title = my_dict.exshipper_general_clients_package_info_log_page_title
            
            # query package information (packages' status == spearnet or exshipper)
            general_clients_packages_info_log = GeneralClientsPackagesInfo.query(GeneralClientsPackagesInfo.package_status == 'delivered')
            clients_info = ClientsInfo().query()
            template_values.update({'general_clients_packages_info_log':general_clients_packages_info_log, 'clients_info':clients_info, 'dispatch_token': dispatch_token})
              
           
        # page of handling tw custom entry packages information
        # tw custom entry packages; package status exshipper
        elif(dispatch_token == 'exshipper_tw_custom_entry_packages_info_log_processing' and exshipper_account == 'alantai' and exshipper_password == '1014lct'):
            html_page = my_dict.exshipper_tw_custom_entry_packages_info_log_page
            html_page_title = my_dict.exshipper_tw_custom_entry_packages_info_log_page_title
            
            tw_custom_entry_packages_info_log = TWCustomEntryInfo.query(TWCustomEntryInfo.package_status == 'exshipper')
            template_values.update({'tw_custom_entry_packages_info_log':tw_custom_entry_packages_info_log})
            
        # tw custom entry packages; packages status at apex, sfo, tw international airport
        elif(dispatch_token == 'exshipper_tw_custom_entry_packages_info_log_processed' and exshipper_account == 'alantai' and exshipper_password == '1014lct'):
            html_page = my_dict.exshipper_tw_custom_entry_packages_info_log_page
            html_page_title = my_dict.exshipper_tw_custom_entry_packages_info_log_page_title
            
            tw_custom_entry_packages_info_log = TWCustomEntryInfo.query(ndb.OR(TWCustomEntryInfo.package_status == 'apex',
                                                                               TWCustomEntryInfo.package_status == 'sfo_airport',
                                                                               TWCustomEntryInfo.package_status == 'taiwan_taoyuan_airport'))
            template_values.update({'tw_custom_entry_packages_info_log':tw_custom_entry_packages_info_log})
        
        # tw custom entry packages; packages status is delivered
        elif(dispatch_token == 'exshipper_tw_custom_entry_packages_info_log_delivered' and exshipper_account == 'alantai' and exshipper_password == '1014lct'):
            html_page = my_dict.exshipper_tw_custom_entry_packages_info_log_page
            html_page_title = my_dict.exshipper_tw_custom_entry_packages_info_log_page_title
            
            tw_custom_entry_packages_info_log = TWCustomEntryInfo.query(TWCustomEntryInfo.package_status == 'delivered')
            template_values.update({'tw_custom_entry_packages_info_log':tw_custom_entry_packages_info_log})
            
        # page of handling exshipper pre-alert
        elif(dispatch_token == 'exshipper_pre_alert' and exshipper_account == 'alantai' and exshipper_password == '1014lct'):
            html_page = my_dict.exshipper_pre_alert_page
            html_page_title = my_dict.exshipper_pre_alert_page_title
            
            pre_alert_entity = TWCustomEntryInfo.query(TWCustomEntryInfo.package_status == 'exshipper').get()
            pre_alert = TWCustomEntryInfo.query(TWCustomEntryInfo.package_status == 'exshipper')
            
            # check if the packages which will be shipped have different mawb, flight number, or flight date 
            if(pre_alert_entity != None and pre_alert != None):
                # different flight numbers, flight dates, or mawb
                mawb_response = 'Different MAWBs: '
                flight_number_response = 'Different Flight Numbers: '
                flight_date_response = 'Different Flight Dates: '
                has_inconsistent_data = 'no'
                
                # build the array of package information
                for package_info in pre_alert:
                    if(pre_alert_entity.mawb != package_info.mawb):
                        mawb_response = mawb_response + package_info.mawb
                        has_inconsistent_data = 'yes'
                    if(pre_alert_entity.flight_number != package_info.flight_number):
                        flight_number_response = flight_number_response + package_info.flight_number
                        has_inconsistent_data = 'yes'
                    if(pre_alert_entity.flight_date != package_info.flight_date):
                        flight_date_response = flight_date_response + package_info.flight_date
                        has_inconsistent_data = 'yes'
                        
                inconsistent_data_response = mawb_response + '\n' + flight_number_response + '\n' + flight_date_response
                template_values.update({'has_inconsistent_data':has_inconsistent_data, 'inconsistent_data_response':inconsistent_data_response})
                # end of different flight numbers, flight dates, or mawb
                
                flight_number = pre_alert_entity.flight_number
                flight_date = pre_alert_entity.flight_date
                mawb = pre_alert_entity.mawb
                sender = pre_alert_entity.sender
                receiver = pre_alert_entity.receiver
                template_values.update({'flight_number':flight_number, 'flight_date':flight_date, 'mawb':mawb, 'sender':sender, 'receiver':receiver})
                
            template_values.update({'pre_alert':pre_alert})
            
        # page of rendering labels
        elif(dispatch_token == 'exshipper_packages_labels' and exshipper_account == 'alantai' and exshipper_password == '1014lct'):
            html_page = my_dict.exshipper_packages_labels_page
            html_page_title = my_dict.exshipper_packages_labels_page_title
            spearnet_packages_info = SpearnetPackagesInfo.query(ndb.OR(SpearnetPackagesInfo.package_status == 'spearnet',
                                                                       SpearnetPackagesInfo.package_status == 'pickup',
                                                                       SpearnetPackagesInfo.package_status == 'exshipper'))
            
            general_clients_packages_info = GeneralClientsPackagesInfo.query(ndb.OR(GeneralClientsPackagesInfo.package_status == 'client',
                                                                                    GeneralClientsPackagesInfo.package_status == 'exshipper'))
            
            template_values.update({'spearnet_packages_info':spearnet_packages_info, 'general_clients_packages_info':general_clients_packages_info})
    
        # page of generating labels
        elif(dispatch_token == 'exshipper_tw_custom_entry_labels' and exshipper_account == 'alantai' and exshipper_password == '1014lct'):
            html_page = my_dict.exshipper_tw_custom_entry_labels_page
            html_page_title = my_dict.exshipper_tw_custom_entry_labels_page_title
            tw_custom_entry_info = TWCustomEntryInfo.query(TWCustomEntryInfo.package_status == 'exshipper')
            
            # get corresponding packages information 
            tw_custom_entry_packages_set = {}
            for tw_custom_entry_entity in tw_custom_entry_info:
                spearnet_package_query = SpearnetPackagesInfo.query(SpearnetPackagesInfo.tw_custom_entry_number == tw_custom_entry_entity.barcode_number)
                general_client_package_query = GeneralClientsPackagesInfo.query(GeneralClientsPackagesInfo.tw_custom_entry_number == tw_custom_entry_entity.barcode_number)
                packages_suda_numbers_set = []
                if(spearnet_package_query is not None):
                    for spearnet_package_entity in spearnet_package_query:
                        packages_suda_numbers_set.append(str(spearnet_package_entity.hawb))
                if(general_client_package_query is not None):
                    for general_clients_package_entity in general_client_package_query:
                        packages_suda_numbers_set.append(str(general_clients_package_entity.hawb))
                tw_custom_entry_packages_set[str(tw_custom_entry_entity.barcode_number)] = packages_suda_numbers_set
                
            template_values['tw_custom_entry_packages_set'] = tw_custom_entry_packages_set
            template_values.update({'tw_custom_entry_info':tw_custom_entry_info})
            
            
        # page of creating cargo manifest
        elif(dispatch_token == 'exshipper_cargo_manifest' and exshipper_account == 'alantai' and exshipper_password == '1014lct'):
            html_page = my_dict.exshipper_cargo_manifest_page
            html_page_title = my_dict.exshipper_cargo_manifest_page_title
            
            spearnet_customers_package_info_cargo_manifest = SpearnetPackagesInfo.query()
            general_clients_package_info_cargo_manifest = GeneralClientsPackagesInfo.query()
            template_values.update({'cargo_manifest_spearnet':spearnet_customers_package_info_cargo_manifest, 'cargo_manifest_general_clients':general_clients_package_info_cargo_manifest})
    
        else:
            html_page = my_dict.exshipper_invalid_login_page
            html_page_title = my_dict.exshipper_invalid_login_page_title
            
        template_values.update({'title':html_page_title})
        template_values.update(user_info)
        template = jinja_environment.get_template(html_page)
        self.response.out.write(template.render(template_values))
        # end of html page dispatching
        
class ExShipperCreateEmployeeInfoHandler(webapp2.RequestHandler):
    def post(self):
        time_stamp = int(round(time.time())).__str__()
        employee_id = 'ESEMP' + time_stamp
        new_employee = EmployeeInfo(id=employee_id)
        new_employee.id = employee_id
        
        new_employee.account_name = self.request.get('employee_account_name')
        new_employee.password = self.request.get('employee_password')
        new_employee.job_title = self.request.get('employee_job_title')
        new_employee.email = self.request.get('employee_email')
        
        new_employee.first_name = self.request.get('employee_first_name')
        new_employee.last_name = self.request.get('employee_last_name')
        
        birthday_year = int(self.request.get('birthday_year'))
        birthday_month = int(self.request.get('birthday_month'))
        birthday_day = int(self.request.get('birthday_day'))
        new_employee.birthday = datetime.date(birthday_year, birthday_month, birthday_day)
        
        new_employee.gender = self.request.get('employee_gender')
        new_employee.address = self.request.get('employee_address')
        new_employee.phone_number = self.request.get('employee_phone_number')
        new_employee.profile_img = self.request.get('employee_profile_img')
        
        new_employee.access_level = self.request.get('employee_access_level')
        
        new_employee.put()
        
        my_dict = Key_Value()
        template_values = {}
        user_info = Users_Info_Handler().get_users_info(self, users)
        template_values.update(user_info)
        template_values.update({'title':my_dict.exshipper_create_client_info_handler_title})
        template = jinja_environment.get_template(my_dict.exshipper_create_client_info_handler)
        self.response.out.write(template.render(template_values))
     
class ExShipperValidateEmployeeAccountName(webapp2.RequestHandler):
    def post(self):
        employee_account_name = self.request.get('employee_account_name')
        ajax_data = {}
        if(EmployeeInfo.query(EmployeeInfo.account_name == employee_account_name).get() is not None):
            ajax_data.update({'validation_response':'This account name already exists, please select a new one!', 'validation_status':'invalid'})
        else:
            ajax_data.update({'validation_response':'This account name is valid!', 'validation_status':'valid'})
            
        self.response.out.headers['Content-Type'] = 'text/json'
        self.response.out.write(json.dumps(ajax_data))

class ExShipperCreateClientInfoHandler(webapp2.RequestHandler):
    def post(self):
        my_dict = Key_Value()
        template_values = {}
        time_stamp = int(round(time.time())).__str__()
        client_id = 'ESCL' + time_stamp
        new_client = ClientsInfo(id=client_id)
        new_client.id = client_id
            
        new_client.account_name = self.request.get('client_account_name')
        new_client.company_name = self.request.get('client_company_name')
        new_client.password = self.request.get('client_password')
            
        new_client.first_name = self.request.get('client_first_name')
        new_client.last_name = self.request.get('client_last_name')
            
        birthday_year = int(self.request.get('birthday_year'))
        birthday_month = int(self.request.get('birthday_month'))
        birthday_day = int(self.request.get('birthday_day'))
        new_client.birthday = datetime.date(birthday_year, birthday_month, birthday_day)
            
        new_client.gender = self.request.get('client_gender')
        new_client.address = self.request.get('client_address')
        new_client.phone_number = self.request.get('client_phone_number')
        new_client.profile_img = self.request.get('client_profile_img')
            
        new_client.signature_str = self.request.get('client_signature')
        new_client.signature_img = self.request.get('client_signature_img')
        
        new_client.membership_level = self.request.get('client_membership_level')
        
        new_client.put()
        
        template_values.update({'title':my_dict.exshipper_create_client_info_handler_title})
        template = jinja_environment.get_template(my_dict.exshipper_create_client_info_handler)
        self.response.out.write(template.render(template_values))
        

class ExShipperValidateClientAccountNameEmail(webapp2.RequestHandler):
    def post(self):
        account_name = self.request.get('account_name')
#         client_email = self.request.get('email')
#         if(mail.is_email_valid(client_email)):
#             mail.send_mail('rainman.tai@gmail.com', client_email, 'Email Verification', 'Verification ID: ' + Users_Info_Handler().generate_random_registration_id())
        ajax_data = {}
        response = ''
        status = 'valid'
        
        if(ClientsInfo.query(ClientsInfo.account_name == account_name).get() is not None):
            response = 'The account name already exist, please pick up a new one!'
            status = 'invalid'
        else:
            response = 'The account name is valid.'
            
        ajax_data.update({'validation_response':response, 'validation_status':status})
        self.response.out.headers['Content-Type'] = 'text/json'
        self.response.out.write(json.dumps(ajax_data))
# end
    
# end of ExShipperLoginHandler
class ExShipperGeneralClientsCreateInvoiceInfoHandler(webapp2.RequestHandler):
    def post(self):
        ajax_data = {'submit_status':'NA'}
        # package size
        new_size = Size()
        new_size.length = self.request.get('valid_size_length')
        new_size.width = self.request.get('valid_size_width')
        new_size.height = self.request.get('valid_size_height')
        new_size.put()
        
        # package information
        package_id = self.request.get('valid_suda_tr_number')
        new_package_info = GeneralClientsPackagesInfo(id=package_id)
        new_package_info.hawb = package_id
        new_package_info.reference_number = self.request.get('valid_ref_number')
        new_package_info.tw_custom_entry_number = 'NA'
        new_package_info.ctn = self.request.get('valid_ctn')
        new_package_info.note = self.request.get('valid_note')
        new_package_info.size = new_size
        new_package_info.weight_kg = self.request.get('valid_weight')
        new_package_info.weight_lb = 'NA'
        new_package_info.commodity_detail = self.request.get('valid_commodity_detail')
        new_package_info.pcs = self.request.get('valid_pcs')
        new_package_info.unit = self.request.get('valid_unit')
        new_package_info.original = 'USA'
        new_package_info.unit_price_fob_us_dollar = self.request.get('valid_unit_price_fob_us_dollar')
        new_package_info.deliver_to = self.request.get('valid_deliver_to')
        
        new_package_info.shipper_company = self.request.get('valid_shipper_company')
        new_package_info.shipper_person = self.request.get('valid_shipper_person')
        new_package_info.shipper_tel = self.request.get('valid_shipper_phone_number')
        new_package_info.shipper_address_english = self.request.get('valid_shipper_address_english')
        new_package_info.shipper_address_chinese = self.request.get('valid_shipper_address_chinese')
        
        new_package_info.consignee_name_english = self.request.get('valid_consignee_name_english')
        new_package_info.consignee_name_chinese = self.request.get('valid_consignee_name_chinese')
        new_package_info.consignee_tel = self.request.get('valid_consignee_phone_number')
        new_package_info.consignee_address_english = self.request.get('valid_consignee_address_english')
        new_package_info.consignee_address_chinese = self.request.get('valid_consignee_address_chinese')
        
        new_package_info.company_id_or_personal_id = 'NA'
        new_package_info.size_accumulation = self.request.get('valid_size_accumulation')
        new_package_info.declaration_need_or_not = 'NLR-NO SED REQIRED NOEEI 30.37(A)'
        new_package_info.duty_paid_by = 'Shipper'
        new_package_info.package_status = 'client'
        
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_access_info = {'access_info':[{'person':'alantai', 'date_time':current_time}]}
        new_package_info.access_info = json.dumps(new_access_info)
        
        new_package_info.put()
        try:
            # shipper email
            shipper_email = self.request.get('valid_shipper_email')
            if(mail.is_email_valid(shipper_email)):
                # email customer shipping confirmation
                email_body = 'Package SUDA Tracking Number: ' + self.request.get('valid_suda_tr_number') + '\n' + 'Package Reference Number: ' + self.request.get('valid_ref_number')
                mail.send_mail(Key_Value().host_email, shipper_email, 'Shipping Confirmation', email_body)
                mail.send_mail(Key_Value().host_email, 'exshipper@gmail.com', 'New Shipping Request', 'Shipper\'s Phone Number: ' + self.request.get('valid_shipper_phone_number'))
                
                #create notification entity
                new_notification_email = PackageStatusNotification_Email(id=package_id)
                new_notification_email.tracking_number = package_id
                new_notification_email.package_status = 'client'
                new_notification_email.receiver_name = self.request.get('valid_shipper_person')
                new_notification_email.email = shipper_email
                new_notification_email.put()
                
            ajax_data['submit_status'] = 'success'
        except Exception, e:
            ajax_data['submit_status'] = 'fail to send email to shipper ; Error Message: %s' % e
        
#         ajax_data['submit_status'] = 'success'
        self.response.out.headers['Content-Type'] = 'text/json'
        self.response.out.write(json.dumps(ajax_data))


# SUDA Tracking Number Handler (For uploading number)
class ExShipperSUDATrackingNumberHandler(webapp2.RequestHandler):
    def get(self):
        my_dict = Key_Value()
        user_info = Users_Info_Handler().get_users_info(self, users)
        suda_tracking_number_handler_page = my_dict.exshipper_suda_tracking_number_handler_page
            
        template_values = {'title':my_dict.exshipper_suda_tracking_number_handler_page_title}
        template_values.update(user_info)
            
        template = jinja_environment.get_template(suda_tracking_number_handler_page)
        self.response.out.write(template.render(template_values))
        
    def post(self):
        ajax_data = {'submit_status':'NA'}
        if(self.request.get('fmt') == 'json'):
            try:
                json_obj = json.loads(self.request.get('json_info'))
                tracking_number_type = json_obj.keys()[0]
                
                if(tracking_number_type == 'regular_suda_tracking_numbers'):
                    suda_number_array = json_obj['regular_suda_tracking_numbers']
                    duplicated_numbers = ''
                    for row_info in suda_number_array:
                        if(SUDATrackingNumber_REGULAR.get_by_id(row_info['suda_number'])):
                            duplicated_numbers += 'Duplicated Number: ' + row_info['suda_number'] + '\n'
                        else:
                            new_suda_tr_number = SUDATrackingNumber_REGULAR(id=row_info['suda_number'])
                            new_suda_tr_number.tracking_number = row_info['suda_number']
                            new_suda_tr_number.used_mark = row_info['used_mark']
                            new_suda_tr_number.put()
                            ajax_data['submit_status'] = 'Data saved into database:\n %s' % duplicated_numbers
                            
                elif(tracking_number_type == 'formal_suda_tracking_numbers'):
                    suda_number_array = json_obj['formal_suda_tracking_numbers']
                    ary_length = suda_number_array.__len__()
                    if(ary_length > 200):
                        ajax_data['submit_status'] = 'Please Keep the upload tracking numbers lower than 200'
                    
                    duplicated_numbers = ''
                    for row_info in suda_number_array:
                        if(SUDATrackingNumber_FORMAL.get_by_id(row_info['suda_number'])):
                            duplicated_numbers += 'Duplicated Number: ' + row_info['suda_number'] + '\n'
                        else:
                            new_suda_tr_number = SUDATrackingNumber_FORMAL(id=row_info['suda_number'])
                            new_suda_tr_number.tracking_number = row_info['suda_number']
                            new_suda_tr_number.used_mark = row_info['used_mark']
                            new_suda_tr_number.put()
                            ajax_data['submit_status'] = 'Data saved into database:\n %s' % duplicated_numbers
                            
                elif(tracking_number_type == 'tw_custom_entry_numbers'):
                    tw_custom_entry_number_array = json_obj['tw_custom_entry_numbers']
                    ary_length = tw_custom_entry_number_array.__len__()
                    if(ary_length > 200):
                        ajax_data['submit_status'] = 'Please Keep the upload tracking numbers lower than 200'
                    else:
                        duplicated_numbers = ''
                        try:
                            for row_info in tw_custom_entry_number_array:
                                if(TWCustomEntryTrackingNumber.get_by_id(row_info['tw_custom_entry_number'])):
                                    duplicated_numbers += 'Duplicated Number: ' + row_info['tw_custom_entry_number'] + '\n'
                                    ajax_data['submit_status'] = 'Duplicated Numbers:\n %s' % duplicated_numbers
                                else:
                                    new_suda_tr_number = TWCustomEntryTrackingNumber(id=row_info['tw_custom_entry_number'])
                                    new_suda_tr_number.tracking_number = row_info['tw_custom_entry_number']
                                    new_suda_tr_number.used_mark = row_info['used_mark']
                                    new_suda_tr_number.put()
                                    ajax_data['submit_status'] = 'Data are saved into database'
                        except Exception, e:
                            ajax_data['submit_status'] = 'Error Message: %s' % e  
                        
                else:
                    ajax_data['submit_status'] = 'File Key- ' + tracking_number_type + ' is invalid!'
                # end of 
                
            except Exception, e:
                ajax_data['suda_tracking_number_submission'] = 'Error Message: %s' % e
            
        self.response.out.headers['Content-Type'] = 'text/json'
        self.response.out.write(json.dumps(ajax_data))
# end of SUDA Tracking Number Handler

# TW Custom Entry Handler (For uploading number)
class ExShipperTWCustomEntryNumberHandler(webapp2.RequestHandler):
    def get(self):
        my_dict = Key_Value()
        user_info = Users_Info_Handler().get_users_info(self, users)
        suda_tracking_number_handler_page = my_dict.exshipper_tw_custom_entry_number_handler_page
            
        template_values = {'title':my_dict.exshipper_tw_custom_entry_number_handler_page_title}
        template_values.update(user_info)
            
        template = jinja_environment.get_template(suda_tracking_number_handler_page)
        self.response.out.write(template.render(template_values))
        
    def post(self):
        ajax_data = {'tw_custom_entry_number_submission':'NA'}
        if(self.request.get('fmt') == 'json'):
            # get jsonObj from client side
            try:
                json_obj = json.loads(self.request.get('json_info'))
                tw_custom_entry_number_array = json_obj['tw_custom_entry_numbers']
            except Exception, e:
                ajax_data['tw_custom_entry_number_submission'] = 'Error Message: %s' % e
            
            # check the size of upload numbers; limit the number no more than 200
            ary_length = tw_custom_entry_number_array.__len__()
            if(ary_length > 200):
                ajax_data['tw_custom_entry_number_submission'] = 'Size of upload numbers is not more than 200!'
            else:
                duplicated_numbers = ''
                try:
                    for row_info in tw_custom_entry_number_array:
                        if(TWCustomEntryTrackingNumber.get_by_id(row_info['tw_custom_entry_number'])):
                            duplicated_numbers += 'Duplicated Number: ' + row_info['tw_custom_entry_number'] + '\n'
                            ajax_data['tw_custom_entry_number_submission'] = 'Duplicated Numbers:\n' + '%s' % duplicated_numbers
                        else:
                            new_suda_tr_number = TWCustomEntryTrackingNumber(id=row_info['tw_custom_entry_number'])
                            new_suda_tr_number.tracking_number = row_info['tw_custom_entry_number']
                            new_suda_tr_number.used_mark = row_info['used_mark']
                            new_suda_tr_number.put()
                            ajax_data['tw_custom_entry_number_submission'] = 'Data are saved into database'
                except Exception, e:
                    ajax_data['tw_custom_entry_number_submission'] = 'Error Message: %s' % e
                
            self.response.out.headers['Content-Type'] = 'text/json'
            self.response.out.write(json.dumps(ajax_data))


# download SUDA tracking number handler
class ExShipperSUDATrackingNumberDownloadHandler(webapp2.RequestHandler):
    def post(self):
        user_account = self.request.get('user_account')
        user_password = self.request.get('user_password')
        suda_tracking_number_type = self.request.get('suda_tracking_number_type')
        ajax_data = {'suda_tracking_number':'NA'}
        
        # check suda tracking numbers quantity
        query_length = SUDATrackingNumber_REGULAR.query(SUDATrackingNumber_REGULAR.used_mark == 'FALSE').count()
        if(query_length < 50):
            Email_Handler().exshipper_send_email('winever.tw@gmail.com', 'koseioyama@gmail.com', 'Regular SUDA Tracking Numbers Shortage', 'There are/is just ' + query_length.__str__() + ' SUDA tracking numbers left.')
        
        query_length = SUDATrackingNumber_FORMAL.query(SUDATrackingNumber_FORMAL.used_mark == 'FALSE').count()
        if(query_length < 20):
            Email_Handler().exshipper_send_email('winever.tw@gmail.com', 'koseioyama@gmail.com', 'Formal SUDA TRacking Numbers Shortage', 'There are/is just ' + query_length.__str__() + ' SUDA tracking numbers.')
                
        # send the tracking number to users
        if(user_account == 'spearnet' and user_password == 'spearnet1941'):
            if(suda_tracking_number_type == 'regular'):
                suda_tracking_number_regular_entity = SUDATrackingNumber_REGULAR.query(SUDATrackingNumber_REGULAR.used_mark == 'FALSE').get()
                if suda_tracking_number_regular_entity != None:
                    regular_suda_entity = SUDATrackingNumber_REGULAR.get_by_id(suda_tracking_number_regular_entity.tracking_number)
                    regular_suda_entity.used_mark = 'TRUE'
                    regular_suda_entity.put()
                    ajax_data['suda_tracking_number'] = suda_tracking_number_regular_entity.tracking_number
                else:
                    Email_Handler().exshipper_send_email('support.tw@spearnet-us.com', 'koseioyama@gmail.com', 'Notice of Running out of Regular SUDA Tracking Number', 'No Regular Regular SUDA Tracking Number Available! ')
                    
            elif(suda_tracking_number_type == 'formal'):
                suda_tracking_number_formal_entity = SUDATrackingNumber_FORMAL.query(SUDATrackingNumber_FORMAL.used_mark == 'FALSE').get()
                if suda_tracking_number_formal_entity != None:
                    formal_suda_entity = SUDATrackingNumber_FORMAL.get_by_id(suda_tracking_number_formal_entity.tracking_number)
                    formal_suda_entity.used_mark = 'TRUE'
                    formal_suda_entity.put()
                    ajax_data['suda_tracking_number'] = suda_tracking_number_formal_entity.tracking_number
                else:
                    Email_Handler().exshipper_send_email('jerry@spearnet-us.com', 'koseioyama@gmail.com', 'Notice for Running out of Formal SUDA Tracking Number', 'No Regular SUDA Tracking Number Available! ')
                    
            self.response.out.headers['Content-Type'] = 'text/json; charset=UTF-8'
            self.response.out.write(json.dumps(ajax_data))
        # download suda tracking number for exshipper
        elif(user_account == 'alantai' and user_password == '1014lct'):
            if(suda_tracking_number_type == 'regular'):
                suda_tracking_number_regular_entity = SUDATrackingNumber_REGULAR.query(SUDATrackingNumber_REGULAR.used_mark == 'FALSE').get()
                if suda_tracking_number_regular_entity != None:
                    regular_suda_entity = SUDATrackingNumber_REGULAR.get_by_id(suda_tracking_number_regular_entity.tracking_number)
                    regular_suda_entity.used_mark = 'TRUE'
                    regular_suda_entity.put()
                    ajax_data['suda_tracking_number'] = suda_tracking_number_regular_entity.tracking_number
                else:
                    Email_Handler().exshipper_send_email('winever.tw@gmail.com', 'koseioyama@gmail.com', 'Notice for Running out of Regular SUDA Tracking Number', 'No Regular Regular SUDA Tracking Number Available! ')
                    
            elif(suda_tracking_number_type == 'formal'):
                suda_tracking_number_formal_entity = SUDATrackingNumber_FORMAL.query(SUDATrackingNumber_FORMAL.used_mark == 'FALSE').get()
                if suda_tracking_number_formal_entity != None:
                    formal_suda_entity = SUDATrackingNumber_FORMAL.get_by_id(suda_tracking_number_formal_entity.tracking_number)
                    formal_suda_entity.used_mark = 'TRUE'
                    formal_suda_entity.put()
                    ajax_data['suda_tracking_number'] = suda_tracking_number_formal_entity.tracking_number
                else:
                    Email_Handler().exshipper_send_email('winever.tw@gmail.com', 'koseioyama@gmail.com', 'Notice for Running out of Formal SUDA Tracking Number', 'No Regular SUDA Tracking Number Available! ')
                    
            self.response.out.headers['Content-Type'] = 'text/json; charset=UTF-8'
            self.response.out.write(json.dumps(ajax_data))
        else:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write('Account or Password Are Incorrect!')
            
            


# -- Client Spearnet Session
class ExShipperSpearnetIndexHandler(webapp2.RequestHandler):
    def get(self):
        my_dict = Key_Value()
        user_info = Users_Info_Handler().get_users_info(self, users)
        exshipper_spearnet_index_page = my_dict.exshipper_spearnet_index_page
        
        template_values = {'title':my_dict.exshipper_spearnet_index_page_title}
        template_values.update(user_info)
        
        template = jinja_environment.get_template(exshipper_spearnet_index_page)
        self.response.out.write(template.render(template_values))

class ExShipperSpearnetLoginHandler(webapp2.RequestHandler):
    def get(self):
        my_dict = Key_Value()
        user_info = Users_Info_Handler().get_users_info(self, users)
        html_page = my_dict.exshipper_spearnet_login_page
        template_values = {}
        dispatch_token = self.request.get('dispatch_token')
        if(dispatch_token == 'exshipper_spearnet_packages_labels'):
            html_page = my_dict.exshipper_spearnet_packages_labels_page
            html_page_title = my_dict.exshipper_spearnet_packages_labels_page_title
            
            spearnet_packages_info = SpearnetPackagesInfo.query(SpearnetPackagesInfo.package_status == 'spearnet')
            template_values.update({'spearnet_packages_info':spearnet_packages_info})
    
        else:
            html_page = my_dict.exshipper_spearnet_login_page
            html_page_title = my_dict.exshipper_spearnet_login_page_title
            
        template_values.update({'title':html_page_title, 'dispatch_token':dispatch_token})
        template_values.update(user_info)
        template = jinja_environment.get_template(html_page)
        self.response.out.write(template.render(template_values))
        
    def post(self):
        my_dict = Key_Value()
        user_info = Users_Info_Handler().get_users_info(self, users)
        dispatch_token = self.request.get('dispatch_token')
        spearnet_account = self.request.get('spearnet_account')
        spearnet_password = self.request.get('spearnet_password')
        template_values = {}
        
        html_page = my_dict.exshipper_invalid_login_page
        html_page_title = my_dict.exshipper_invalid_login_page_title
        
        # html page dispatching
        if(dispatch_token == 'exshipper_spearnet_data_exchange' and spearnet_account == 'spearnet' and spearnet_password == '1941dataexchange'):
            html_page = my_dict.exshipper_spearnet_data_exchange_page
            html_page_title = my_dict.exshipper_spearnet_data_exchange_page_title
            
        elif(dispatch_token == 'exshipper_spearnet_create_invoice_info' and spearnet_account == 'spearnet' and spearnet_password == '1941spearnet'):
            html_page = my_dict.exshipper_spearnet_create_invoice_info_page
            html_page_title = my_dict.exshipper_spearnet_create_invoice_info_page_title
            
        elif(dispatch_token == 'exshipper_spearnet_packages_labels' and spearnet_account == 'spearnet' and spearnet_password == '1941spearnet'):
            html_page = my_dict.exshipper_spearnet_packages_labels_page
            html_page_title = my_dict.exshipper_spearnet_packages_labels_page_title
            spearnet_packages_info = SpearnetPackagesInfo.query(SpearnetPackagesInfo.package_status == 'spearnet')
            template_values.update({'spearnet_packages_info':spearnet_packages_info})
            
        else:
            html_page = my_dict.exshipper_invalid_login_page
            html_page_title = my_dict.exshipper_invalid_login_page_title
            
        template_values.update({'title':html_page_title})
        template_values.update(user_info)
        template = jinja_environment.get_template(html_page)
        self.response.out.write(template.render(template_values))
        # end of html page dispatching

# exshipper spearnet data-exchange handler
class ExShipperSpearnetDataExchangeDispatcher(webapp2.RequestHandler):
    def post(self):
        my_dict = Key_Value()
        user_info = Users_Info_Handler().get_users_info(self, users)
        data_format = self.request.get('XLSX_XLS')
        
        if(data_format == 'XLS'):
            parser_page = my_dict.exshipper_spearnet_xls_page
            parser_page_title = my_dict.exshipper_spearnet_xls_title
        elif (data_format == 'XLSX'):
            parser_page = my_dict.exshipper_spearnet_xlsx_page
            parser_page_title = my_dict.exshipper_spearnet_xlsx_title
            
        template_values = {'title':parser_page_title}
        template_values.update(user_info)
            
        template = jinja_environment.get_template(parser_page)
        self.response.out.write(template.render(template_values))

class ExShipperSpearnetDataExchangeHandler(webapp2.RequestHandler):
    def post(self):
        ajax_data = {'spearnet_packages_info_upload_status':'NA', 'print_action':'off'}
        try:
            if(self.request.get('fmt') == 'json'):
                json_obj = json.loads(self.request.get('packages_data'))
                packages_array = json_obj['spearnet_invoice']
                is_hawb_blank = True
                duplication = True
                for package in packages_array:
                    if(package['hawb'] == ''):
                        is_hawb_blank = True
                        ajax_data['spearnet_packages_info_upload_status'] = 'One hawb field is blank!'
                        ajax_data['print_action'] = 'off'
                        break
                    else:
                        is_hawb_blank = False
                    query_result = SpearnetPackagesInfo.get_by_id(package['hawb'])
                    if(query_result):
                        duplication = True;
                        ajax_data['spearnet_packages_info_upload_status'] = 'You have a duplicated tracking number and please replace it with a new tracking number- %s.' % query_result.hawb
                        ajax_data['print_action'] = 'off'
                        break;
                    else:
                        duplication = False;
                        
                if(duplication == False and is_hawb_blank == False):
                    for package in packages_array:
                        new_package = SpearnetPackagesInfo(id=package['hawb'])
                        new_package.reference_number = package['reference_number']
                        new_package.tw_custom_entry_number = 'NA'
                        new_package.hawb = package['hawb']
                        new_package.ctn = package['ctn']
                        new_package.weight_kg = package['g/w(kg)']
                        new_package.weight_lb = 'NA'
                        new_package.commodity_detail = package['commodity_detail']
                        new_package.pcs = 'NA'
                        new_package.unit = package['unit']
                        new_package.original = package['original']
                        new_package.unit_price_fob_us_dollar = 'NA'
                        new_package.deliver_to = package['deliver_to']
                        
                        new_package.shipper_company = package['shipper_company']
                        new_package.shipper_person = 'NA'
                        new_package.shipper_tel = '510-351-8903'
                        new_package.shipper_address_english = '1941 W Ave 140th, San Leandro, CA 94577'
                        new_package.shipper_address_chinese = '1941號  第140西街, 勝利安卓, 加州 94577'
                        
                        new_package.consignee_name_english = package['consignee_name_english']
                        new_package.consignee_name_chinese = package['consignee_name_chinese']
                        new_package.consignee_tel = package['consignee_tel']
                        new_package.consignee_address_english = package['consignee_address_english']
                        new_package.consignee_address_chinese = package['consignee_address_chinese']
                        
                        new_package.company_id_or_personal_id = 'NA'
                        new_package.size_accumulation = package['size_accumulation']
                        new_package.declaration_need_or_not = package['declaration_need_or_not']
                        new_package.duty_paid_by = package['duty_paid_by']
                        new_package.package_status = 'spearnet'
                        new_package.note = '常溫'
                        
                        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        new_access_info = {'access_info':[{'person':'spearnet', 'date_time':current_time}]}
                        new_package.access_info = json.dumps(new_access_info)
                        
                        new_package.put()
                        
                    ajax_data['spearnet_packages_info_upload_status'] = 'Data saved into database'
                    ajax_data['print_action'] = 'on'
        except Exception, e:
            ajax_data['spearnet_packages_info_upload_status'] = 'Error Message: %s' % e
            
        self.response.out.headers['Content-Type'] = 'text/json; charset=UTF-8'
        self.response.out.write(json.dumps(ajax_data))
        
   
# end of ExShipperLoginHandler
class ExShipperSpearnetCreateInvoiceInfoHandler(webapp2.RequestHandler):
    def post(self):
        ajax_data = {'submit_status':'NA'}
        
        # package information
        package_id = self.request.get('valid_suda_tr_number')  # required
        new_package_info = SpearnetPackagesInfo(id=package_id)
        new_package_info.hawb = package_id
        new_package_info.reference_number = self.request.get('valid_ref_number')  # required
        new_package_info.tw_custom_entry_number = 'NA'  # required
        new_package_info.ctn = self.request.get('valid_ctn')  # required
        
        new_package_info.weight_kg = self.request.get('valid_weight')  # required
        new_package_info.weight_lb = 'NA'
        new_package_info.commodity_detail = self.request.get('valid_commodity_detail')  # reqiured
        new_package_info.pcs = self.request.get('valid_pcs')  # required
        new_package_info.unit = 'pcs'
        new_package_info.original = 'USA'  # required
        new_package_info.unit_price_fob_us_dollar = self.request.get('valid_unit_price_fob_us_dollar')  # required
        new_package_info.deliver_to = 'SUDA'
        
        new_package_info.shipper_company = 'Spearnet'
        new_package_info.shipper_person = 'NA'
        new_package_info.shipper_tel = '510-351-8903'
        new_package_info.shipper_address_english = '1941 W Ave 140th, San Leandro, CA 94577'
        new_package_info.shipper_address_chinese = '1941號  第140西街, 勝利安卓, 加州 94577'
        
        new_package_info.consignee_name_english = self.request.get('valid_consignee_name_english')
        new_package_info.consignee_name_chinese = self.request.get('valid_consignee_name_chinese')
        new_package_info.consignee_tel = self.request.get('valid_consignee_phone_number')
        new_package_info.consignee_address_english = self.request.get('valid_consignee_address_english')
        new_package_info.consignee_address_chinese = self.request.get('valid_consignee_address_chinese')
        
        new_package_info.company_id_or_personal_id = 'NA'
        new_package_info.size_accumulation = 'NA'
        new_package_info.declaration_need_or_not = 'NLR-NO SED REQIRED NOEEI 30.37(A)'
        new_package_info.duty_paid_by = 'Shipper'
        new_package_info.package_status = 'spearnet'
        new_package_info.note = self.request.get('valid_note')
        
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_access_info = {'access_info':[{'person':'spearnet', 'date_time':current_time}]}
        new_package_info.access_info = json.dumps(new_access_info)
        
        new_package_info.put()
        
        
        ajax_data['submit_status'] = 'success'
        self.response.out.headers['Content-Type'] = 'text/json'
        self.response.out.write(json.dumps(ajax_data))
        
        
class ExShipperSpearnetPackagesPickupHandler(webapp2.RequestHandler):
    def post(self):
        account = self.request.get('account')
        password = self.request.get('password')
        response = {}
        json_response = {'response':'NA'}
        if(account == 'alantai' and password == '1014'):
            json_obj = json.loads(self.request.get('spearnet_picked_packages'))
            suda_numbers_array = json.loads(json_obj['suda_tracking_numbers'])
            package_tracking_numbers = ''
            total_packages = 0
            
            try:
                for key in suda_numbers_array:
                    package_entity = SpearnetPackagesInfo.get_by_id(key)
                    if(package_entity != None and package_entity.package_status == 'spearnet'):
                        package_entity.package_status = 'pickup'
                        
                        if(package_entity.access_info != None):
                            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            old_access_info = package_entity.access_info
                            old_access_info_dict = json.loads(old_access_info)
                            person = ''
                            old_access_info_dict['access_info'].append({'person':'alantai', 'date_time':current_time})
                            package_entity.access_info = json.dumps(old_access_info_dict)
                        else:
                            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            new_access_info = {'access_info':[{'person':'alantai', 'date_time':current_time}]}
                            package_entity.access_info = json.dumps(new_access_info)
                            
                        package_entity.pickup_date_time = datetime.datetime.now()
                        package_entity.put()
                        package_tracking_numbers = package_tracking_numbers + key + '\n'
                        total_packages = total_packages + 1
                        response.update({'result':'Successfully Update Picked Packages Information', 'key':'success'})
                        
                    elif(package_entity != None and package_entity.package_status != 'spearnet'):
                        response.update({'result':'Tracking Number, ' + key + ', is Duplicated!', 'key':'duplicated_number'})
                        break
                    else:
                        response.update({'result':'Unknown Package- ' + key, 'key':'unknown_number'})
                        break
                    
            except Exception, e:
                result = 'Error Message: %s' % e
                response.update({'result':result, 'key':'na'})
            finally:
                if(response['key'] == 'success'):
                    response_to_spearnet = 'Packages SUDA Tracking Numbers:\n' + package_tracking_numbers + '\n' + 'Total Amount: ' + total_packages.__str__()
                    Email_Handler().exshipper_send_email('support.tw@spearnet-us.com', 'koseioyama@gmail.com', 'Package Pickup Done', 'Packages Pickup Done by ExShipper!\n' + 'Detail is as follows:' + '\n' + response_to_spearnet)
                    
                json_response['response'] = response
                
        self.response.headers['Content-Type'] = 'text/json ; charset=UTF-8'
        self.response.write(json.dumps(json_response))
        
# Spearnet Services Handlers
# working on
class ExShipperSpearnetCustomerIndexHandler(webapp2.RequestHandler):
    def get(self):
        my_dict = Key_Value()
        user_info = Users_Info_Handler().get_users_info(self, users)
        html_page = my_dict.exshipper_spearnet_customer_index_page
        
        template_values = {'title':my_dict.exshipper_spearnet_customer_index_page_title}
        template_values.update(user_info)
        template = jinja_environment.get_template(html_page)
        self.response.out.write(template.render(template_values))   
            
# spearnet customer services handler
class ExShipperSpearnetCustomerServicesHandler(webapp2.RequestHandler):
    def post(self):
        my_dict = Key_Value()
        template_values = {}
        user_info = Users_Info_Handler().get_users_info(self, users)
        template_values.update(user_info)
        account = self.request.get('spearnet_customer_account')
        password = self.request.get('spearnet_customer_password')
        
        if(account == 'spearnetcustomer' and password == 'spearnetcustomer1941'):
            html_page = my_dict.exshipper_spearnet_customer_services_handler_page
            page_title = 'ExShipper Spearnet Customer Service Page'
        else:
            html_page = my_dict.exshipper_invalid_login_page
            page_title = 'Invalid Login Page'
        
        template_values.update({'title':page_title})
        template = jinja_environment.get_template(html_page)
        self.response.out.write(template.render(template_values))

# spearnet custom package tracking handler
class ExShipperSpearnetCustomerPackageTrackingHandler(webapp2.RequestHandler):
    def post(self):
        ajax_data = {'package_status':'NA'}
        try:
            if(self.request.get('fmt') == 'json'):
                tracking_result_entity = SpearnetPackagesInfo.query(SpearnetPackagesInfo.hawb == self.request.get('customer_tracking_number')).get()
                if(tracking_result_entity):
                    package_status = tracking_result_entity.package_status
                    ajax_data['package_status'] = package_status
        except Exception, e:
            ajax_data['package_status'] = 'Error Message: %s' % e
                           
        self.response.out.headers['Content-Type'] = 'text/json'
        self.response.out.write(json.dumps(ajax_data))
        
class ExShipperSpearnetCustomerPackageInfoUpdateHandler(webapp2.RequestHandler):
    def post(self):
        try:
            ajax_data = {'update_status':'NA'}
            if(self.request.get('fmt') == 'json'):
                update_packages_info = self.request.get('update_packages_info')
                json_obj = json.loads(update_packages_info)
                json_obj_tw_custom_entry_number = json_obj['tw_custom_entry_numbers']
                json_obj_package_status = json_obj['packages_status']
                json_obj_clients_signature = json_obj['clients_signature']
                json_obj_notes = json_obj['notes']
                
                if(json_obj_tw_custom_entry_number != 'NA'):
                    for key in json_obj_tw_custom_entry_number:
                        package_entity = SpearnetPackagesInfo.get_by_id(key)
                        package_entity.tw_custom_entry_number = json_obj_tw_custom_entry_number[key]
                        if(package_entity.access_info != None):
                            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            old_access_info = package_entity.access_info
                            old_access_info_dict = json.loads(old_access_info)
                            person = ''
                            old_access_info_dict['access_info'].append({'person':'alantai', 'date_time':current_time})
                            package_entity.access_info = json.dumps(old_access_info_dict)
                        else:
                            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            new_access_info = {'access_info':[{'person':'alantai', 'date_time':current_time}]}
                            package_entity.access_info = json.dumps(new_access_info)
                        
                        package_entity.put()
                
                if(json_obj_package_status != 'NA'):
                    for key in json_obj_package_status:
                        package_entity = SpearnetPackagesInfo.get_by_id(key)
                        package_entity.package_status = json_obj_package_status[key]
                        if(package_entity.access_info != None):
                            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            old_access_info = package_entity.access_info
                            old_access_info_dict = json.loads(old_access_info)
                            person = ''
                            old_access_info_dict['access_info'].append({'person':'alantai', 'date_time':current_time})
                            package_entity.access_info = json.dumps(old_access_info_dict)
                        else:
                            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            new_access_info = {'access_info':[{'person':'alantai', 'date_time':current_time}]}
                            package_entity.access_info = json.dumps(new_access_info)
                        
                        package_entity.put()
                         
                if(json_obj_clients_signature != 'NA'):
                    for key in json_obj_clients_signature:
                        package_entity = SpearnetPackagesInfo.get_by_id(key)
                        package_entity.signature_img_id = json_obj_clients_signature[key]
                        if(package_entity.access_info != None):
                            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            old_access_info = package_entity.access_info
                            old_access_info_dict = json.loads(old_access_info)
                            person = ''
                            old_access_info_dict['access_info'].append({'person':'alantai', 'date_time':current_time})
                            package_entity.access_info = json.dumps(old_access_info_dict)
                        else:
                            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            new_access_info = {'access_info':[{'person':'alantai', 'date_time':current_time}]}
                            package_entity.access_info = json.dumps(new_access_info)
                        
                        package_entity.put()
                         
                if(json_obj_notes != 'NA'):
                    for key in json_obj_notes.keys():
                        package_entity = SpearnetPackagesInfo.get_by_id(key)
                        package_entity.note = json_obj_notes[key]
                        if(package_entity.access_info != None):
                            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            old_access_info = package_entity.access_info
                            old_access_info_dict = json.loads(old_access_info)
                            person = ''
                            old_access_info_dict['access_info'].append({'person':'alantai', 'date_time':current_time})
                            package_entity.access_info = json.dumps(old_access_info_dict)
                        else:
                            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            new_access_info = {'access_info':[{'person':'alantai', 'date_time':current_time}]}
                            package_entity.access_info = json.dumps(new_access_info)
                        
                        package_entity.put()
                        
                    
                ajax_data['update_status'] = 'Successfully update the packages status!'
                
        except Exception, e:
                ajax_data['update_status'] = 'Error Message: %s' % e
                
        self.response.out.headers['Content-Type'] = 'text/json'
        self.response.out.write(json.dumps(ajax_data))
# end of exshipper & spearnet

# exshipper tw custom entry login handler
class ExShipperTWCustomEntryIndexHandler(webapp2.RequestHandler):
    def get(self):
        my_dict = Key_Value()
        user_info = Users_Info_Handler().get_users_info(self, users)
        login_page = my_dict.exshipper_tw_custom_entry_index_page
        
        template_values = {'title':my_dict.exshipper_tw_custom_entry_index_page_title}
        template_values.update(user_info)
        
        template = jinja_environment.get_template(login_page)
        self.response.out.write(template.render(template_values))
        
class ExShipperTWCustomEntryLoginHandler(webapp2.RequestHandler):
    def get(self):
        my_dict = Key_Value()
        user_info = Users_Info_Handler().get_users_info(self, users)
        login_page = my_dict.exshipper_tw_custom_entry_login_page
        
        dispatch_token = self.request.get('dispatch_token')
        
        template_values = {'title':my_dict.exshipper_tw_custom_entry_login_page_title, 'dispatch_token':dispatch_token}
        template_values.update(user_info)
        
        template = jinja_environment.get_template(login_page)
        self.response.out.write(template.render(template_values))
        
    def post(self):
        my_dict = Key_Value()
        user_info = Users_Info_Handler().get_users_info(self, users)
        dispatch_token = self.request.get('dispatch_token')
        tw_custom_entry_account = self.request.get('tw_custom_entry_account')
        tw_custom_entry_password = self.request.get('tw_custom_entry_password')
        template_values = {}
        
        html_page = my_dict.exshipper_invalid_login_page
        html_page_title = my_dict.exshipper_invalid_login_page_title
        
        # html page dispatching
        if(dispatch_token == 'exshipper_tw_custom_entry_invoice_log' and tw_custom_entry_account == 'alantai' and tw_custom_entry_password == '1014lct'):
            html_page = my_dict.exshipper_tw_custom_entry_invoice_log_page
            html_page_title = my_dict.exshipper_tw_custom_entry_invoice_log_page_title
            spearnet_customer_package_info_log = SpearnetPackagesInfo.query(ndb.OR(SpearnetPackagesInfo.package_status == 'apex',
                                                                                               SpearnetPackagesInfo.package_status == 'sfo_airport',
                                                                                               SpearnetPackagesInfo.package_status == 'taiwan_taoyuan_airport'))
            general_client_package_info_log = GeneralClientsPackagesInfo.query(ndb.OR(GeneralClientsPackagesInfo.package_status == 'apex',
                                                                                               GeneralClientsPackagesInfo.package_status == 'sfo_airport',
                                                                                               GeneralClientsPackagesInfo.package_status == 'taiwan_taoyuan_airport'))
            template_values.update({'spearnet_customer_package_info_log':spearnet_customer_package_info_log, 'general_client_package_info_log':general_client_package_info_log})
            # use memcache
#                 data = memcache.get('tw_custom_entry_invoice_log')
#                 if data != None:
#                     log_spearnet_customer_package_info = data
#                 else:
#                     data = SpearnetPackagesInfo.query()
#                     memcache.add('tw_custom_entry_invoice_log',data,500)
#                     log_spearnet_customer_package_info = data
#                 template_values.update({'spearnet_customer_package_info_log':log_spearnet_customer_package_info})

        elif(dispatch_token == 'exshipper_tw_custom_entry_cargo_manifest' and tw_custom_entry_account == 'alantai' and tw_custom_entry_password == '1014lct'):
            html_page = my_dict.exshipper_tw_custom_entry_manifest_page
            html_page_title = my_dict.exshipper_tw_custom_entry_manifest_page_title
            
            spearnet_customers_package_info_cargo_manifest = SpearnetPackagesInfo.query(ndb.OR(SpearnetPackagesInfo.package_status == 'apex',
                                                                                               SpearnetPackagesInfo.package_status == 'sfo_airport',
                                                                                               SpearnetPackagesInfo.package_status == 'taiwan_taoyuan_airport'))
            general_clients_package_info_cargo_manifest = GeneralClientsPackagesInfo.query(ndb.OR(GeneralClientsPackagesInfo.package_status == 'apex',
                                                                                               GeneralClientsPackagesInfo.package_status == 'sfo_airport',
                                                                                               GeneralClientsPackagesInfo.package_status == 'taiwan_taoyuan_airport'))
            template_values.update({'cargo_manifest_spearnet':spearnet_customers_package_info_cargo_manifest, 'cargo_manifest_general_clients':general_clients_package_info_cargo_manifest})
            
        elif(dispatch_token == 'exshipper_tw_custom_entry_suda_manifest' and tw_custom_entry_account == 'alantai' and tw_custom_entry_password == '1014lct'):
            html_page = my_dict.exshipper_tw_custom_entry_suda_page
            html_page_title = my_dict.exshipper_tw_custom_entry_suda_page_title
            
            spearnet_customers_package_info_cargo_manifest = SpearnetPackagesInfo.query(ndb.OR(SpearnetPackagesInfo.package_status == 'apex',
                                                                                               SpearnetPackagesInfo.package_status == 'sfo_airport',
                                                                                               SpearnetPackagesInfo.package_status == 'taiwan_taoyuan_airport'))
            general_clients_package_info_cargo_manifest = GeneralClientsPackagesInfo.query(ndb.OR(GeneralClientsPackagesInfo.package_status == 'apex',
                                                                                               GeneralClientsPackagesInfo.package_status == 'sfo_airport',
                                                                                               GeneralClientsPackagesInfo.package_status == 'taiwan_taoyuan_airport'))
            template_values.update({'cargo_manifest_spearnet':spearnet_customers_package_info_cargo_manifest, 'cargo_manifest_general_clients':general_clients_package_info_cargo_manifest})
            
        elif(dispatch_token == 'exshipper_tw_custom_entry_onhand_manifest' and tw_custom_entry_account == 'alantai' and tw_custom_entry_password == '1014lct'):
            html_page = my_dict.exshipper_tw_custom_entry_onhand_page
            html_page_title = my_dict.exshipper_tw_custom_entry_onhand_page_title
            
            onhand_manifest = TWCustomEntryInfo.query(ndb.OR(TWCustomEntryInfo.package_status == 'apex',
                                                             TWCustomEntryInfo.package_status == 'sfo_airport',
                                                             TWCustomEntryInfo.package_status == 'taiwan_taoyuan_airport'))
            
            # get corresponding packages information 
            tw_custom_entry_packages_set = {}
            for tw_custom_entry_entity in onhand_manifest:
                spearnet_package_query = SpearnetPackagesInfo.query(SpearnetPackagesInfo.tw_custom_entry_number == tw_custom_entry_entity.barcode_number)
                general_client_package_query = GeneralClientsPackagesInfo.query(GeneralClientsPackagesInfo.tw_custom_entry_number == tw_custom_entry_entity.barcode_number)
                packages_suda_numbers_set = []
                if(spearnet_package_query is not None):
                    for spearnet_package_entity in spearnet_package_query:
                        packages_suda_numbers_set.append(str(spearnet_package_entity.hawb))
                if(general_client_package_query is not None):
                    for general_clients_package_entity in general_client_package_query:
                        packages_suda_numbers_set.append(str(general_clients_package_entity.hawb))
                tw_custom_entry_packages_set[str(tw_custom_entry_entity.barcode_number)] = packages_suda_numbers_set
                
            template_values['tw_custom_entry_packages_set'] = tw_custom_entry_packages_set
            template_values.update({'onhand_manifest':onhand_manifest})


        else:
            html_page = my_dict.exshipper_invalid_login_page
            html_page_title = my_dict.exshipper_invalid_login_page_title
            
        template_values.update({'title':html_page_title})
        template_values.update(user_info)
        template = jinja_environment.get_template(html_page)
        self.response.out.write(template.render(template_values))
        # end of html page dispatching

# end of exshipper tw custom entry login handler

# custom entry handler
class ExshipperTWCustomEntryHandler(webapp2.RequestHandler):
    def post(self):
        account = self.request.get('account')
        password = self.request.get('password')
        token = self.request.get('token')
        ajax_data = {}
        
        # tw custom entry handler for getting a number
        if(account == 'alantai' and password == '1014' and token == 'tw_custom_entry_handler_get_number'):
            try:
                tw_custom_entry_number = 'NA'
                query_length = TWCustomEntryTrackingNumber.query().count(20)
                if(query_length < 20):
                    body = 'There are/is only ' + query_length.__str__() + ' TW Custom Entry tracking numbers left.'
                    Email_Handler().exshipper_send_email('winever.tw@gmail.com', 'koseioyama@gmail.com', 'TW Custom Entry Barcode Number Shortage', body)
                
                tracking_number_entity = TWCustomEntryTrackingNumber.query(TWCustomEntryTrackingNumber.used_mark == 'FALSE').get()
                if(tracking_number_entity != None):
                    tracking_number_entity.used_mark = 'TRUE'
                    tracking_number_entity.put()
                    tw_custom_entry_number = tracking_number_entity.tracking_number
                else:
                    tw_custom_entry_number = 'NA'
            except Exception, e:
                tw_custom_entry_number = 'Error Message: %s' % e
            finally:
                response = tw_custom_entry_number
                ajax_data.update({'response':response})
                
        # tw custom entry handler for submitting packages info
        elif(account == 'alantai' and password == '1014' and token == 'tw_custom_entry_handler_submit_packages_sets'):
            try:
                json_obj_packages_sets = json.loads(self.request.get('tw_custom_entry_packages_sets'))
                json_obj_packages_size_weight = json.loads(self.request.get('tw_custom_entry_packages_size_weight'))
                has_unknown_number = 'no'
                tw_custom_package = ''
                tw_custom_entry_submit_response = {}
                response_result = ''
                
                for key in json_obj_packages_sets.keys():
                    json_obj_packages_size_length = json_obj_packages_size_weight[key]['strObj']['length']
                    json_obj_packages_size_width = json_obj_packages_size_weight[key]['strObj']['width']
                    json_obj_packages_size_height = json_obj_packages_size_weight[key]['strObj']['height']
                    json_obj_packages_weight = json_obj_packages_size_weight[key]['strObj']['weight']
                    
                    for package_number in json_obj_packages_sets[key].keys():
                        response_result += 'Package NO.' + package_number + ';'
                        spearnet_package_entity = SpearnetPackagesInfo.get_by_id(package_number)
                        general_client_package_entity = GeneralClientsPackagesInfo.get_by_id(package_number)
                        if(spearnet_package_entity == None and general_client_package_entity == None):
                            unknown_package_response = 'Unknown Number- ' + package_number
                            has_unknown_number = 'yes'
                            break;
                        elif(spearnet_package_entity != None):
                            spearnet_package_entity.tw_custom_entry_number = key
                            spearnet_package_entity.put()
                        elif(general_client_package_entity != None):
                            general_client_package_entity.tw_custom_entry_number = key
                            general_client_package_entity.put()
                        
                    if(has_unknown_number == 'yes'):
                        tw_custom_entry_submit_result = unknown_package_response
                        tw_custom_entry_submit_response.update({'result':tw_custom_entry_submit_result.__str__()})
                        tw_custom_entry_submit_response['key'] = 'unknown_package'
                        break;
                    else:
                        # create new tw customentry package information
                        tw_custom_entry_package = TWCustomEntryInfo.get_by_id(key)
                        if(tw_custom_entry_package == None):
                            tw_custom_entry_package = TWCustomEntryInfo(id=key)
                        
                        tw_custom_entry_package.barcode_number = key
                        tw_custom_entry_package.sender = 'Ezship2u'
                        tw_custom_entry_package.receiver = 'EHU (Hung Lun)'
                        tw_custom_entry_package.weight_kg = json_obj_packages_weight.__str__()
                        new_size = Size()
                        new_size.length = json_obj_packages_size_length.__str__()
                        new_size.width = json_obj_packages_size_width.__str__()
                        new_size.height = json_obj_packages_size_height.__str__()
                        new_size.put()
                        tw_custom_entry_package.size = new_size
                        tw_custom_entry_package.package_status = 'exshipper'
                        tw_custom_entry_package.note = 'NLR-NO SED REQIRED NOEEI 30.37(A)'
                        tw_custom_entry_package.ctn = '1'
                        
                        if(tw_custom_entry_package.access_info != None):
                            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            old_access_info = tw_custom_entry_package.access_info
                            old_access_info_dict = json.loads(old_access_info)
                            person = ''
                            old_access_info_dict['access_info'].append({'person':'alantai', 'date_time':current_time})
                            tw_custom_entry_package.access_info = json.dumps(old_access_info_dict)
                        else:
                            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            new_access_info = {'access_info':[{'person':'alantai', 'date_time':current_time}]}
                            tw_custom_entry_package.access_info = json.dumps(new_access_info)
                        
                        
                        tw_custom_entry_package.put()
                        tw_custom_package = tw_custom_package + 'TW Custom Entry Package- ' + key + ';\n'
                
                        tw_custom_entry_submit_result = tw_custom_package
                        tw_custom_entry_submit_response.update({'result':tw_custom_entry_submit_result})
                        tw_custom_entry_submit_response['key'] = 'success'
                        
            except:
                tw_custom_entry_submit_result = 'Fail to submit the data'
                tw_custom_entry_submit_response.update({'result':tw_custom_entry_submit_result})
                tw_custom_entry_submit_response['key'] = 'na'
            finally:
                tw_custom_entry_submit_response.update({'result':tw_custom_entry_submit_result})
                response = tw_custom_entry_submit_response
                ajax_data.update({'response':response})
                
        self.response.headers['Content-Type'] = 'text/plain ; charset=UTF-8'
        self.response.write(json.dumps(ajax_data))
        
        
class ExShipperTWCustomEntryPackageInfoUpdateHandler(webapp2.RequestHandler):
    def post(self):
        try:
            ajax_data = {'update_status':'NA'}
            if(self.request.get('fmt') == 'json'):
                update_packages_info = self.request.get('update_packages_info')
                json_obj = json.loads(update_packages_info)
                json_obj_package_status = json_obj['packages_status']
                json_obj_mawbs = json_obj['mawbs']
                json_obj_flight_numbers = json_obj['flight_numbers']
                json_obj_flight_dates = json_obj['flight_dates']
                
                if(json_obj_package_status != 'NA'):
                    for key in json_obj_package_status:
                        package_entity = TWCustomEntryInfo.get_by_id(key)
                        package_entity.package_status = json_obj_package_status[key]
                        package_entity.put()
                          
                if(json_obj_mawbs != 'NA'):
                    for key in json_obj_mawbs:
                        package_entity = TWCustomEntryInfo.get_by_id(key)
                        package_entity.mawb = json_obj_mawbs[key]
                        package_entity.put()
                          
                if(json_obj_flight_numbers != 'NA'):
                    for key in json_obj_flight_numbers:
                        package_entity = TWCustomEntryInfo.get_by_id(key)
                        package_entity.flight_number = json_obj_flight_numbers[key]
                        package_entity.put()
                        
                if(json_obj_flight_dates != 'NA'):
                    for key in json_obj_flight_dates:
                        package_entity = TWCustomEntryInfo.get_by_id(key)
                        flight_date = datetime.datetime.strptime(json_obj_flight_dates[key], '%m/%d/%Y').date()
                        package_entity.flight_date = flight_date
                        package_entity.put()
                    
                ajax_data['update_status'] = 'Successfully update the packages information!'
                
        except Exception, e:
                ajax_data['update_status'] = 'Error Message: %s' % e
                
        self.response.out.headers['Content-Type'] = 'text/json'
        self.response.out.write(json.dumps(ajax_data))
        
# end of custom entry handler

class ExShipperGeneralClientsIndexHandler(webapp2.RequestHandler):
    def get(self):
        my_dict = Key_Value()
        user_info = Users_Info_Handler().get_users_info(self, users)
        exshipper_general_clients_index_page = my_dict.exshipper_general_clients_index_page
        
        template_values = {'title':my_dict.exshipper_general_clients_index_page_title}
        template_values.update(user_info)
        
        template = jinja_environment.get_template(exshipper_general_clients_index_page)
        self.response.out.write(template.render(template_values))
    
class ExShipperGeneralClientsLoginHandler(webapp2.RequestHandler):
    def get(self):
        my_dict = Key_Value()
        user_info = Users_Info_Handler().get_users_info(self, users)
        login_page = my_dict.exshipper_general_clients_login_page
        
        dispatch_token = self.request.get('dispatch_token')
        
        template_values = {'title':my_dict.exshipper_general_clients_login_page_title, 'dispatch_token':dispatch_token}
        template_values.update(user_info)
        
        template = jinja_environment.get_template(login_page)
        self.response.out.write(template.render(template_values))
        
    def post(self):
        my_dict = Key_Value()
        user_info = Users_Info_Handler().get_users_info(self, users)
        dispatch_token = self.request.get('dispatch_token')
        general_client_account_name = self.request.get('general_clients_entry_account')
        general_client_password = self.request.get('general_clients_entry_password')
        template_values = {}
        
        html_page = my_dict.exshipper_invalid_login_page
        html_page_title = my_dict.exshipper_invalid_login_page_title
        
        # html page dispatching
        if(dispatch_token == 'creating_client_info'):
            if(general_client_account_name == 'alantai' and general_client_password == '1014lct'):
                html_page = my_dict.exshipper_general_clients_create_client_info_page
                html_page_title = my_dict.exshipper_general_clients_create_client_info_page_title
        
        elif(dispatch_token == 'creating_invoice'):
            if(general_client_account_name == 'alantai' and general_client_password == '1014lct'):
                html_page = my_dict.exshipper_general_clients_create_invoice_page
                html_page_title = my_dict.exshipper_general_clients_create_invoice_page_title
                
        elif(dispatch_token == 'track_package_status'):
            if(general_client_account_name == 'alantai' and general_client_password == '1014lct'):
                html_page = my_dict.exshipper_general_clients_track_package_status_page
                html_page_title = my_dict.exshipper_general_clients_track_package_status_page_title
                
        else:
            html_page = my_dict.exshipper_invalid_login_page
            html_page_title = my_dict.exshipper_invalid_login_page_title
            
        template_values.update({'title':html_page_title})
        template_values.update(user_info)
        template = jinja_environment.get_template(html_page)
        self.response.out.write(template.render(template_values))
        # end of html page dispatching
        
class ExShipperGeneralClientsCreateClientInfoHandler(webapp2.RequestHandler):
    def post(self):
        client_verification_code = self.request.get('client_verification_code')
        client_email = self.request.get('client_email')
        query_entity = EmailVerification.query(ndb.AND(EmailVerification.email == client_email,
                                                       EmailVerification.verification_code == client_verification_code)).get()
                                       
        if(query_entity != None):
            my_dict = Key_Value()
            template_values = {}
            time_stamp = int(round(time.time())).__str__()
            client_id = 'ESCL' + time_stamp
            new_client = ClientsInfo(id=client_id)
            new_client.id = client_id
            
            new_client.account_name = self.request.get('client_account_name')
            new_client.company_name = self.request.get('client_company_name')
            new_client.password = self.request.get('client_password')
            new_client.email = self.request.get('client_email')
            
            new_client.first_name = self.request.get('client_first_name')
            new_client.last_name = self.request.get('client_last_name')
            
            birthday_year = int(self.request.get('birthday_year'))
            birthday_month = int(self.request.get('birthday_month'))
            birthday_day = int(self.request.get('birthday_day'))
            new_client.birthday = datetime.date(birthday_year, birthday_month, birthday_day)
            
            new_client.gender = self.request.get('client_gender')
            new_client.address = self.request.get('client_address')
            new_client.phone_number = self.request.get('client_phone_number')
            new_client.profile_img = self.request.get('client_profile_img')
            
            new_client.signature_str = self.request.get('client_signature')
            new_client.signature_img = self.request.get('client_signature_img')
            new_client.put()
        
            template_values.update({'title':my_dict.exshipper_create_client_info_handler_title})
            template = jinja_environment.get_template(my_dict.exshipper_create_client_info_handler)
            self.response.out.write(template.render(template_values))
        else:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write('Verification Code and Email Do Not Match!')
        

class ExShipperGeneralClientsValidateClientAccountNameEmail(webapp2.RequestHandler):
    def post(self):
        account_name = self.request.get('account_name')
        email = self.request.get('email')
        ajax_data = {}
        response = 'Verification Code was sent to the email account you provided'
        status = 'valid'
        
        if(ClientsInfo.query(ClientsInfo.account_name == account_name).get() is not None):
            response = 'The Account name already exist, please pick up a new one!'
            status = 'invalid_account_name'
        elif(ClientsInfo.query(ClientsInfo.email == email).get() is not None):
            response = response + 'The email already exist, please pick up a new one!'
            status = 'invalid_email'
        else:
            try:
                verification_code = Cron_Tasks_Handler().generate_random_registration_id().__str__()
                if(EmailVerification.query(EmailVerification.email == email).get() is not None):
                    verification_pair_entity = EmailVerification.query(EmailVerification.email == email).get()
                else:
                    verification_pair_entity = EmailVerification()
                
                verification_pair_entity.email = email
                verification_pair_entity.verification_code = verification_code
                verification_pair_entity.put()
                
                mail.send_mail('rainman.tai@gmail.com', email, 'Email Verification', 'Your Verification Code is: ' + verification_code)
            except Exception, e:
                response = response + 'The email is invalid; ' + e
                status = 'invalid_email'
            
        ajax_data.update({'validation_response':response, 'validation_status':status})
        self.response.out.headers['Content-Type'] = 'text/json'
        self.response.out.write(json.dumps(ajax_data))
        
class ExShipperGeneralClientsPackageInfoUpdateHandler(webapp2.RequestHandler):
    def post(self):
        try:
            ajax_data = {'update_status':'NA'}
            if(self.request.get('fmt') == 'json'):
                update_packages_status = self.request.get('update_packages_info')
                json_obj = json.loads(update_packages_status)
                json_obj_package_status = json_obj['packages_status']
                json_obj_tw_custom_entry_number = json_obj['tw_custom_entry_numbers']
                json_obj_clients_signature = json_obj['clients_signature']
                json_obj_notes = json_obj['notes']
                
                if(json_obj_tw_custom_entry_number != 'NA'):
                    for key in json_obj_tw_custom_entry_number:
                        package_entity = GeneralClientsPackagesInfo.get_by_id(key)
                        package_entity.tw_custom_entry_number = json_obj_tw_custom_entry_number[key]
                        if(package_entity.access_info != None):
                            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            old_access_info = package_entity.access_info
                            old_access_info_dict = json.loads(old_access_info)
                            person = ''
                            old_access_info_dict['access_info'].append({'person':'alantai', 'date_time':current_time})
                            package_entity.access_info = json.dumps(old_access_info_dict)
                        else:
                            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            new_access_info = {'access_info':[{'person':'alantai', 'date_time':current_time}]}
                            package_entity.access_info = json.dumps(new_access_info)
                        
                        package_entity.put()
                
                
                if(json_obj_package_status != 'NA'):
                    for key in json_obj_package_status:
                        package_entity = GeneralClientsPackagesInfo.get_by_id(key)
                        
                        #update package info
                        package_entity.package_status = json_obj_package_status[key]
                        if(package_entity.access_info != None):
                            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            old_access_info = package_entity.access_info
                            old_access_info_dict = json.loads(old_access_info)
                            person = ''
                            old_access_info_dict['access_info'].append({'person':'alantai', 'date_time':current_time})
                            package_entity.access_info = json.dumps(old_access_info_dict)
                        else:
                            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            new_access_info = {'access_info':[{'person':'alantai', 'date_time':current_time}]}
                            package_entity.access_info = json.dumps(new_access_info)
                            
                        package_entity.put()
                        
                        #email customer the notification of package status
                        notification_email_entity = PackageStatusNotification_Email.get_by_id(key)
                        if(notification_email_entity != None and mail.is_email_valid(notification_email_entity.email)):
                            notification_email_entity.package_status = json_obj_package_status[key]
                            notification_email_entity.put()
                            
                            #email customer the notification of package status
                            email_content = 'Dear Customer, ' + notification_email_entity.receiver_name + ', your package- ' + notification_email_entity.tracking_number + ' is ' + Key_Value().package_status_dict[json_obj_package_status[key]]
                            mail.send_mail(Key_Value().host_email, notification_email_entity.email , 'Notification of Package Status Update', email_content)
                          
                if(json_obj_clients_signature != 'NA'):
                    for key in json_obj_clients_signature:
                        package_entity = GeneralClientsPackagesInfo.get_by_id(key)
                        package_entity.signature_img_id = json_obj_clients_signature[key]
                        
                        if(package_entity.access_info != None):
                            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            old_access_info = package_entity.access_info
                            old_access_info_dict = json.loads(old_access_info)
                            person = ''
                            old_access_info_dict['access_info'].append({'person':'alantai', 'date_time':current_time})
                            package_entity.access_info = json.dumps(old_access_info_dict)
                        else:
                            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            new_access_info = {'access_info':[{'person':'alantai', 'date_time':current_time}]}
                            package_entity.access_info = json.dumps(new_access_info)
                            
                        package_entity.put()
                          
                if(json_obj_notes != 'NA'):
                    for key in json_obj_notes:
                        package_entity = GeneralClientsPackagesInfo.get_by_id(key)
                        package_entity.note = json_obj_notes[key]
                        
                        if(package_entity.access_info != None):
                            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            old_access_info = package_entity.access_info
                            old_access_info_dict = json.loads(old_access_info)
                            person = ''
                            old_access_info_dict['access_info'].append({'person':'alantai', 'date_time':current_time})
                            package_entity.access_info = json.dumps(old_access_info_dict)
                        else:
                            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            new_access_info = {'access_info':[{'person':'alantai', 'date_time':current_time}]}
                            package_entity.access_info = json.dumps(new_access_info)
                        
                        package_entity.put()
                    
                ajax_data['update_status'] = 'Successfully update the packages status!'
                
        except Exception, e:
                ajax_data['update_status'] = 'Error Message: %s' % e
                
        self.response.out.headers['Content-Type'] = 'text/json'
        self.response.out.write(json.dumps(ajax_data))
        
        
class ExShipperGeneralClientsPackageTrackingHandler(webapp2.RequestHandler):
    def post(self):
        ajax_data = {'package_status':'NA'}
        hawb = self.request.get('customer_tracking_number')
        try:
            if(self.request.get('fmt') == 'json'):
                tracking_result_entity = SpearnetPackagesInfo.query(SpearnetPackagesInfo.hawb == hawb).get()
                if(tracking_result_entity != None):
                    package_status = tracking_result_entity.package_status
                    ajax_data['package_status'] = package_status
                
                tracking_result_entity = GeneralClientsPackagesInfo.query(GeneralClientsPackagesInfo.hawb == hawb).get()
                if(tracking_result_entity != None):
                    package_status = tracking_result_entity.package_status
                    ajax_data['package_status'] = package_status
                    
        except Exception, e:
            ajax_data['package_status'] = 'Error Message: %s' % e
                           
        self.response.out.headers['Content-Type'] = 'text/json'
        self.response.out.write(json.dumps(ajax_data))
# end of general clients
        
        
# function classes
# get image
class GetImage(webapp2.RequestHandler):
    def get(self):
        entity_id = self.request.get('entity_id')
        entity = ndb.Key(urlsafe=entity_id).get()
        if entity and entity.signature_img:
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(entity.signature_img)
            
# get reference numbers
class GetReferenceNumber(webapp2.RequestHandler):
    def post(self):
        ajax_data = {}
        if(self.request.get('key') == 'get_package_reference_number'):
            time_stamp = int(round(time.time())).__str__()
            exshipper_package_number = 'ESPKG' + time_stamp
            ajax_data.update({'exshipper_package_number':exshipper_package_number})
            
            self.response.headers['Content-Type'] = 'text/json'
            self.response.out.write(json.dumps(ajax_data))
# end of function classes

# cron task
# migrate packages data
class ExShipperPackagesInfoLogMigrationHandler(webapp2.RequestHandler):
    def get(self):
        general_clients_packages_info_for_migration = SpearnetPackagesInfo.query(SpearnetPackagesInfo.package_status == 'delivered')
        if(general_clients_packages_info_for_migration.count() > 0):
            for package_info_entity in general_clients_packages_info_for_migration:
                new_package_info_log = SpearnetPackagesInfoLog(id=package_info_entity.hawb)
                new_package_info_log.reference_number = package_info_entity.reference_number
                new_package_info_log.tw_custom_entry_number = package_info_entity.tw_custom_entry_number
                new_package_info_log.hawb = package_info_entity.hawb
                new_package_info_log.ctn = package_info_entity.ctn
                new_package_info_log.size = package_info_entity.size
                new_package_info_log.weight_kg = package_info_entity.weight_kg
                new_package_info_log.weight_lb = package_info_entity.weight_lb
                new_package_info_log.commodity_detail = package_info_entity.commodity_detail
                new_package_info_log.pcs = package_info_entity.pcs
                new_package_info_log.unit = package_info_entity.unit
                new_package_info_log.original = package_info_entity.original
                new_package_info_log.deliver_to = package_info_entity.deliver_to
                new_package_info_log.unit_price_fob_us_dollar = package_info_entity.unit_price_fob_us_dollar
                
                new_package_info_log.shipper_company = package_info_entity.shipper_company
                new_package_info_log.shipper_person = package_info_entity.shipper_person
                new_package_info_log.shipper_tel = package_info_entity.shipper_tel
                new_package_info_log.shipper_address_english = package_info_entity.shipper_address_english
                new_package_info_log.shipper_address_chinese = package_info_entity.shipper_address_chinese
                
                new_package_info_log.consignee_tel = package_info_entity.consignee_tel
                new_package_info_log.consignee_name_english = package_info_entity.consignee_name_english
                new_package_info_log.consignee_name_chinese = package_info_entity.consignee_name_chinese
                new_package_info_log.consignee_address_english = package_info_entity.consignee_address_english
                new_package_info_log.consignee_address_chinese = package_info_entity.consignee_address_chinese
                
                new_package_info_log.company_id_or_personal_id = package_info_entity.company_id_or_personal_id
                new_package_info_log.size_accumulation = package_info_entity.size_accumulation
                new_package_info_log.declaration_need_or_not = package_info_entity.declaration_need_or_not
                new_package_info_log.duty_paid_by = package_info_entity.duty_paid_by
                new_package_info_log.signature_img_id = package_info_entity.signature_img_id
                new_package_info_log.note = package_info_entity.note
                
                new_package_info_log.package_status = package_info_entity.package_status
                new_package_info_log.pickup_date_time = package_info_entity.pickup_date_time
                
                new_package_info_log.access_info = package_info_entity.access_info
                new_package_info_log.original_create_date_time = package_info_entity.create_date_time
                new_package_info_log.original_update_date_time = package_info_entity.update_date_time
                
                new_package_info_log.put()
                
                package_info_entity.key.delete()
                
        # general clients package info log
        general_clients_packages_info_for_migration = GeneralClientsPackagesInfo.query(GeneralClientsPackagesInfo.package_status == 'delivered')
        if(general_clients_packages_info_for_migration.count() > 0):
            for package_info_entity in general_clients_packages_info_for_migration:
                new_package_info_log = GeneralClientsPackagesInfoLog(id=package_info_entity.hawb)
                new_package_info_log.reference_number = package_info_entity.reference_number
                new_package_info_log.tw_custom_entry_number = package_info_entity.tw_custom_entry_number
                new_package_info_log.hawb = package_info_entity.hawb
                new_package_info_log.ctn = package_info_entity.ctn
                new_package_info_log.size = package_info_entity.size
                new_package_info_log.weight_kg = package_info_entity.weight_kg
                new_package_info_log.weight_lb = package_info_entity.weight_lb
                new_package_info_log.commodity_detail = package_info_entity.commodity_detail
                new_package_info_log.pcs = package_info_entity.pcs
                new_package_info_log.unit = package_info_entity.unit
                new_package_info_log.original = package_info_entity.original
                new_package_info_log.deliver_to = package_info_entity.deliver_to
                new_package_info_log.unit_price_fob_us_dollar = package_info_entity.unit_price_fob_us_dollar
                
                new_package_info_log.shipper_company = package_info_entity.shipper_company
                new_package_info_log.shipper_person = package_info_entity.shipper_person
                new_package_info_log.shipper_tel = package_info_entity.shipper_tel
                new_package_info_log.shipper_address_english = package_info_entity.shipper_address_english
                new_package_info_log.shipper_address_chinese = package_info_entity.shipper_address_chinese
                
                new_package_info_log.consignee_tel = package_info_entity.consignee_tel
                new_package_info_log.consignee_name_english = package_info_entity.consignee_name_english
                new_package_info_log.consignee_name_chinese = package_info_entity.consignee_name_chinese
                new_package_info_log.consignee_address_english = package_info_entity.consignee_address_english
                new_package_info_log.consignee_address_chinese = package_info_entity.consignee_address_chinese
                
                new_package_info_log.company_id_or_personal_id = package_info_entity.company_id_or_personal_id
                new_package_info_log.size_accumulation = package_info_entity.size_accumulation
                new_package_info_log.declaration_need_or_not = package_info_entity.declaration_need_or_not
                new_package_info_log.duty_paid_by = package_info_entity.duty_paid_by
                new_package_info_log.signature_img_id = package_info_entity.signature_img_id
                new_package_info_log.note = package_info_entity.note
                
                new_package_info_log.package_status = package_info_entity.package_status
                new_package_info_log.pickup_date_time = package_info_entity.pickup_date_time
                
                new_package_info_log.access_info = package_info_entity.access_info
                new_package_info_log.original_create_date_time = package_info_entity.create_date_time
                new_package_info_log.original_update_date_time = package_info_entity.update_date_time
                
                new_package_info_log.put()
                package_info_entity.key.delete()
                
        tw_cusotm_entry_packages_info = TWCustomEntryInfo.query(TWCustomEntryInfo.package_status == 'delivered')
        if(tw_cusotm_entry_packages_info.count() > 0):
            for tw_custom_entry_package_info in tw_cusotm_entry_packages_info:
                new_package_info_log = TWCustomEntryInfoLog(id=tw_custom_entry_package_info.barcode_number)
                new_package_info_log.barcode_number = tw_custom_entry_package_info.barcode_number
                new_package_info_log.mawb = tw_custom_entry_package_info.mawb
                new_package_info_log.sender = tw_custom_entry_package_info.sender
                new_package_info_log.receiver = tw_custom_entry_package_info.receiver
                new_package_info_log.size = tw_custom_entry_package_info.size
                new_package_info_log.weight_kg = tw_custom_entry_package_info.weight_kg
                new_package_info_log.ctn = tw_custom_entry_package_info.ctn
                new_package_info_log.note = tw_custom_entry_package_info.note
                new_package_info_log.flight_number = tw_custom_entry_package_info.flight_number
                new_package_info_log.flight_date = tw_custom_entry_package_info.flight_date
                new_package_info_log.package_status = tw_custom_entry_package_info.package_status
                new_package_info_log.access_info = tw_custom_entry_package_info.access_info
                new_package_info_log.original_create_date_time = tw_custom_entry_package_info.create_date_time
                new_package_info_log.original_update_date_time = tw_custom_entry_package_info.update_date_time
                
                new_package_info_log.put()
                tw_custom_entry_package_info.key.delete()
                
        
class ExShipperTrackingNumbersDeletion(webapp2.RequestHandler):
    def get(self):
        tracking_numbers = SUDATrackingNumber_REGULAR.query(SUDATrackingNumber_REGULAR.used_mark == 'TRUE')
        if(tracking_numbers != None):
            for tracking_number_entity in tracking_numbers:
                tracking_number_entity.key.delete()
        tracking_numbers = SUDATrackingNumber_FORMAL.query(SUDATrackingNumber_FORMAL.used_mark == 'TRUE')
        if(tracking_numbers != None):
            for tracking_number_entity in tracking_numbers:
                tracking_number_entity.key.delete()
        tracking_numbers = TWCustomEntryTrackingNumber.query(TWCustomEntryTrackingNumber.used_mark == 'TRUE')
        if(tracking_numbers != None):
            for tracking_number_entity in tracking_numbers:
                tracking_number_entity.key.delete()
        
# set url
app = webapp2.WSGIApplication([('/exshipper_index', ExShipperIndexHandler),
                               ('/exshipper_login_handler', ExShipperLoginHandler),
                               ('/exshipper_invoice_info_handler', ExShipperGeneralClientsCreateInvoiceInfoHandler),
                               ('/exshipper_create_employee_info_handler', ExShipperCreateEmployeeInfoHandler),
                               ('/exshipper_validate_employee_account_name', ExShipperValidateEmployeeAccountName),
                               ('/exshipper_create_client_info_handler', ExShipperCreateClientInfoHandler),
                               ('/exshipper_validate_client_account_name_email', ExShipperValidateClientAccountNameEmail),
                               ('/exshipper_suda_tracking_number_handler', ExShipperSUDATrackingNumberHandler),
                               ('/exshipper_tw_custom_entry_number_handler', ExShipperTWCustomEntryNumberHandler),
                               ('/exshipper_suda_tracking_number_download_handler', ExShipperSUDATrackingNumberDownloadHandler),
                               ('/exshipper_spearnet_index_page', ExShipperSpearnetIndexHandler),
                               ('/exshipper_spearnet_login_handler', ExShipperSpearnetLoginHandler),
                               ('/exshipper_spearnet_data_exchange_page', ExShipperSpearnetDataExchangeDispatcher),
                               ('/exshipper_spearnet_data_exchange_handler', ExShipperSpearnetDataExchangeHandler),
                               ('/exshipper_spearnet_create_invoice_info_handler', ExShipperSpearnetCreateInvoiceInfoHandler),
                               ('/exshipper_spearnet_customer_index_page', ExShipperSpearnetCustomerIndexHandler),
                               ('/exshipper_spearnet_customer_services_handler', ExShipperSpearnetCustomerServicesHandler),
                               ('/exshipper_spearnet_customer_package_tracking_handler', ExShipperSpearnetCustomerPackageTrackingHandler),
                               ('/exshipper_spearnet_customer_packages_info_update_handler', ExShipperSpearnetCustomerPackageInfoUpdateHandler),
                               ('/exshipper_spearnet_packages_pickup_handler', ExShipperSpearnetPackagesPickupHandler),
                               ('/exshipper_tw_custom_entry_handler', ExshipperTWCustomEntryHandler),
                               ('/exshipper_tw_custom_entry_index_page', ExShipperTWCustomEntryIndexHandler),
                               ('/exshipper_tw_custom_entry_login_handler', ExShipperTWCustomEntryLoginHandler),
                               ('/exshipper_tw_custom_entry_packages_info_update_handler', ExShipperTWCustomEntryPackageInfoUpdateHandler),
                               ('/exshipper_general_clients_index_page', ExShipperGeneralClientsIndexHandler),
                               ('/exshipper_general_clients_login_handler', ExShipperGeneralClientsLoginHandler),
                               ('/exshipper_general_clients_create_client_info_handler', ExShipperGeneralClientsCreateClientInfoHandler),
                               ('/exshipper_general_clients_validate_client_account_name_email', ExShipperGeneralClientsValidateClientAccountNameEmail),
                               ('/exshipper_general_clients_packages_info_update_handler', ExShipperGeneralClientsPackageInfoUpdateHandler),
                               ('/exshipper_general_clients_packages_tracking_handler', ExShipperGeneralClientsPackageTrackingHandler),
                               ('/img', GetImage),
                               ('/get_ref_number', GetReferenceNumber),
                               ('/exshipper_migrate_packages_information_handler', ExShipperPackagesInfoLogMigrationHandler),
                               ('/exshipper_delete_tracking_numbers_handler', ExShipperTrackingNumbersDeletion)], debug=True)
