# -*- coding: utf-8 -*-
'''
Created on Oct 1, 2013

@author: Alan Tai
'''
from google.appengine.ext.key_range import ndb
import time
import datetime
__author__ = 'Alan Tai'

import webapp2
import jinja2
import os
import json

from google.appengine.api import users, mail, memcache
from app_dict import Key_Value
from models import Size, SUDATrackingNumber_REGULAR, SpearnetPackagesInfo, TWCustomEntryTrackingNumber,\
    ClientsInfo, GeneralClientsPackagesInfo, SUDATrackingNumber_FORMAL,\
    TWCustomEntryInfo, EmployeeInfo

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + '/static/templates')) #append templates' path

#exshipper main index handler
class ExShipperIndexHandler(webapp2.RequestHandler):
    def get(self):
        my_dict = Key_Value() #get key-value pair dictionary
        user_info = get_users_info(self, users)
        index_page = my_dict.exshipper_index_page
        
        template_values = {'title':my_dict.exshipper_index_page_title}
        template_values.update(user_info)
        
        template = jinja_environment.get_template(index_page)
        self.response.out.write(template.render(template_values))

# for handling the exshipper users login process
class ExShipperLoginHandler(webapp2.RequestHandler):
    #login page
    def get(self):
        my_dict = Key_Value()
        user_info = get_users_info(self, users)
        login_page = my_dict.exshipper_login_page
        
        dispatch_token = self.request.get('dispatch_token')
        
        template_values = {'title':my_dict.exshipper_login_page_title, 'dispatch_token':dispatch_token}
        template_values.update(user_info)
        
        template = jinja_environment.get_template(login_page)
        self.response.out.write(template.render(template_values))
        
    #dispatch user to different pages according to the token, account and, password which users submit
    def post(self):
        my_dict = Key_Value()
        user_info = get_users_info(self, users)
        dispatch_token = self.request.get('dispatch_token')
        exshipper_account = self.request.get('exshipper_account')
        exshipper_password = self.request.get('exshipper_password')
        template_values = {}
        
        #set default page source and title as invalid login page
        html_page = my_dict.exshipper_invalid_login_page
        html_page_title = my_dict.exshipper_invalid_login_page_title
        
        # web-pages dispatcher
        # page of creating invoice
        if(dispatch_token == 'exshipper_invoice'):
            if(exshipper_account == 'alantai' and exshipper_password == '1014lct'):
                
                html_page = my_dict.exshipper_invoice_creating_page
                html_page_title = my_dict.exshipper_invoice_creating_page_title
                
        elif(dispatch_token == 'exshipper_create_employee_info'):
            if(exshipper_account == 'alantai' and exshipper_password == '1014lct'):
                html_page = my_dict.exshipper_create_employee_info_page
                html_page_title = my_dict.exshipper_create_employee_info_page_title
                
        #page of creating client info
        elif(dispatch_token == 'exshipper_create_client_info'):
            if(exshipper_account == 'alantai' and exshipper_password == '1014lct'):
                clients_data = ClientsInfo.query()
                template_values.update({'clients_data':clients_data})
                
                html_page = my_dict.exshipper_create_client_info_handler
                html_page_title = my_dict.exshipper_create_client_info_handler_title
                
        #page of uploading suda tracking numbers
        elif(dispatch_token == 'exshipper_suda_tracking_number_upload'):
            if(exshipper_account == 'alantai' and exshipper_password == '1014lct'):
                html_page = my_dict.exshipper_suda_tracking_number_upload_handler_page
                html_page_title = my_dict.exshipper_suda_tracking_number_upload_handler_page_title
                
        #page of uploading tw custom entry numbers
        elif(dispatch_token == 'exshipper_tw_custom_entry_number_upload'):
            if(exshipper_account == 'alantai' and exshipper_password == '1014lct'):
                html_page = my_dict.exshipper_tw_custom_entry_number_handler_page
                html_page_title = my_dict.exshipper_tw_custom_entry_number_handler_page_title
                
        #page of handling spearnet customers packages information
        elif(dispatch_token == 'exshipper_spearnet_customers_packages_info_log'):
            if(exshipper_account == 'alantai' and exshipper_password == '1014lct'):
                html_page = my_dict.exshipper_spearnet_customer_package_info_log_page
                html_page_title = my_dict.exshipper_spearnet_customer_package_info_log_page_title
                
                #use memcache to show information users had read (ignore the error message)
#                 data = memcache.get('spearnet_customer_package_info_log')
#                 if data is not None:
#                     log_spearnet_customer_package_info = data
#                 else:
#                     data = SpearnetPackagesInfo.query()
#                     memcache.add('spearnet_customer_package_info_log',data,1000)
#                     log_spearnet_customer_package_info = data

                # query package information (packages' status == spearnet or exshipper)
                spearnet_customer_package_info_log = SpearnetPackagesInfo.query(ndb.OR(SpearnetPackagesInfo.package_status == 'spearnet',
                                                                                       SpearnetPackagesInfo.package_status == 'exshipper'))
                # pass clients informations
                clients_info = ClientsInfo().query()
                template_values.update({'spearnet_customer_package_info_log': spearnet_customer_package_info_log, 'clients_info':clients_info})
                  
                  
        #page of handling general clients packages information
        elif(dispatch_token == 'exshipper_general_clients_packages_info_log'):
            if(exshipper_account == 'alantai' and exshipper_password == '1014lct'):
                html_page = my_dict.exshipper_general_clients_package_info_log_page
                html_page_title = my_dict.exshipper_general_clients_package_info_log_page_title
                
                #query package information (packages' status == spearnet or exshipper)
                general_clients_packages_info_log = GeneralClientsPackagesInfo.query(ndb.OR(GeneralClientsPackagesInfo.package_status == 'spearnet',
                                                                                            GeneralClientsPackagesInfo.package_status == 'exshipper'))
                clients_info = ClientsInfo().query()
                template_values.update({'general_clients_packages_info_log':general_clients_packages_info_log, 'clients_info':clients_info})
                
        # page of handling tw custom entry packages information
        elif(dispatch_token == 'exshipper_tw_custom_entry_packages_info_log'):
            if(exshipper_account == 'alantai' and exshipper_password == '1014lct'):
                html_page = my_dict.exshipper_tw_custom_entry_packages_info_log_page
                html_page_title = my_dict.exshipper_tw_custom_entry_packages_info_log_page_title
                
                tw_custom_entry_packages_info_log = TWCustomEntryInfo.query(TWCustomEntryInfo.package_status == 'exshipper')
                template_values.update({'tw_custom_entry_packages_info_log':tw_custom_entry_packages_info_log})
                
        # page of handling exshipper pre-alert
        elif(dispatch_token == 'exshipper_pre_alert'):
            if(exshipper_account == 'alantai' and exshipper_password == '1014lct'):
                html_page = my_dict.exshipper_pre_alert_page
                html_page_title = my_dict.exshipper_pre_alert_page_title
                
                pre_alert_entity = TWCustomEntryInfo.query(TWCustomEntryInfo.package_status == 'exshipper').get()
                pre_alert = TWCustomEntryInfo.query(TWCustomEntryInfo.package_status == 'exshipper')
                
                if(pre_alert_entity != None and pre_alert != None):
                    #different flight numbers, flight dates, or mawb
                    mawb_response = 'Different MAWBs: '
                    flight_number_response = 'Different Flight Numbers: '
                    flight_date_response = 'Different Flight Dates: '
                    has_inconsistent_data = 'no'
                    
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
                            
                    inconsistent_data_response = mawb_response + '\n' + flight_number_response + '\n' +flight_date_response
                    template_values.update({'has_inconsistent_data':has_inconsistent_data,'inconsistent_data_response':inconsistent_data_response})
                    #end of different flight numbers, flight dates, or mawb
                    
                    flight_number = pre_alert_entity.flight_number
                    flight_date = pre_alert_entity.flight_date
                    mawb = pre_alert_entity.mawb
                    sender = pre_alert_entity.sender
                    receiver = pre_alert_entity.receiver
                    template_values.update({'flight_number':flight_number, 'flight_date':flight_date, 'mawb':mawb, 'sender':sender, 'receiver':receiver})
                    
                template_values.update({'pre_alert':pre_alert})
                
        #page of rendering labels
        elif(dispatch_token == 'exshipper_packages_labels'):
            if(exshipper_account == 'alantai' and exshipper_password == '1014lct'):
                html_page = my_dict.exshipper_packages_labels_page
                html_page_title = my_dict.exshipper_packages_labels_page_title
                spearnet_packages_info = SpearnetPackagesInfo.query(ndb.OR(SpearnetPackagesInfo.package_status == 'spearnet',
                                                                           SpearnetPackagesInfo.package_status == 'exshipper'))
                
                general_clients_packages_info = GeneralClientsPackagesInfo.query(ndb.OR(GeneralClientsPackagesInfo.package_status == 'client',
                                                                                        GeneralClientsPackagesInfo.package_status == 'exshipper'))
                
                template_values.update({'spearnet_packages_info':spearnet_packages_info, 'general_clients_packages_info':general_clients_packages_info})
        
        #page of generating labels
        elif(dispatch_token == 'exshipper_tw_custom_entry_labels'):
            if(exshipper_account == 'alantai' and exshipper_password == '1014lct'):
                html_page = my_dict.exshipper_tw_custom_entry_labels_page
                html_page_title = my_dict.exshipper_tw_custom_entry_labels_page_title
                tw_custom_entry_info = TWCustomEntryInfo.query(TWCustomEntryInfo.package_status == 'exshipper')
                template_values.update({'tw_custom_entry_info':tw_custom_entry_info})
                
        #page of creating cargo manifest
        elif(dispatch_token == 'exshipper_cargo_manifest'):
            if(exshipper_account == 'alantai' and exshipper_password == '1014lct'):
                html_page = my_dict.exshipper_cargo_manifest_page
                html_page_title = my_dict.exshipper_cargo_manifest_page_title
                
                spearnet_customers_package_info_cargo_manifest = SpearnetPackagesInfo.query()
                general_clients_package_info_cargo_manifest = GeneralClientsPackagesInfo.query()
#                 cargo_manifest.update(spearnet_customers_package_info_cargo_manifest)
#                 cargo_manifest.update(general_clients_package_info_cargo_manifest)
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
        employee_id = 'ESEMP'+ time_stamp
        new_employee = EmployeeInfo(employee_id)
        new_employee.id = employee_id
        
        new_employee.account_name = self.request.get('employee_account_name')
        new_employee.password = self.request.get('employee_password')
        new_employee.job_title = self.request.get('employee_job_title')
        
        new_employee.first_name = self.request.get('employee_first_name')
        new_employee.last_name = self.request.get('employee_last_name')
        
        birthday_year = self.request.get('birthday_year')
        birthday_month = self.request.get('birthday_month')
        birthday_day = self.request.get('birthday_day')
        
        new_employee.birthday = datetime.date(birthday_year, birthday_month, birthday_day)
        
        new_employee.gender = self.request.get('employee_gender')
        new_employee.address = self.request.get('employee_address')
        new_employee.phone_number = self.request.get('employee_phone_number')
        new_employee.profile_img = self.request.get('employee_profile_img')
        
        new_employee.put()
        
        my_dict = Key_Value()
        template_values = {}
        user_info = get_users_info(self, users)
        template_values.update(user_info)
        template_values.update({'title':my_dict.exshipper_create_client_info_handler_title})
        template = jinja_environment.get_template(my_dict.exshipper_create_client_info_handler)
        self.response.out.write(template.render(template_values))
        

class ExShipperCreateClientInfoHandler(webapp2.RequestHandler):
    def post(self):
        time_stamp = int(round(time.time())).__str__()
        client_id = 'ESCL'+ time_stamp
        new_client = ClientsInfo(id=client_id)
        new_client.id = client_id
        
        new_client.account_name = self.request.get('client_account_name')
        new_client.company_name = self.request.get('client_company_name')
        new_client.password = self.request.get('client_password')
        new_client.email = self.request.get('client_email')
        
        new_client.first_name = self.request.get('client_first_name')
        new_client.last_name = self.request.get('client_last_name')
        
        birthday_year = self.request.get('birthday_year')
        birthday_month = self.request.get('birthday_month')
        birthday_day = self.request.get('birthday_day')
        new_client.birthday = datetime.date(birthday_year, birthday_month, birthday_day)
        
        new_client.gender = self.request.get('client_gender')
        new_client.address = self.request.get('client_address')
        new_client.phone_number = self.request.get('client_phone_number')
        new_client.profile_img = self.request.get('client_profile_img')
        
        new_client.signature_str = self.request.get('client_signature')
        new_client.signature_img = self.request.get('client_signature_img')
        new_client.put()
        
        my_dict = Key_Value()
        template_values = {}
        user_info = get_users_info(self, users)
        template_values.update(user_info)
        template_values.update({'title':my_dict.exshipper_create_client_info_handler_title})
        template = jinja_environment.get_template(my_dict.exshipper_create_client_info_handler)
        self.response.out.write(template.render(template_values))

class ExShipperValidateClientAccountNameEmail(webapp2.RequestHandler):
    def post(self):
        account_name = self.request.get('account_name')
        email = self.request.get('email')
        ajax_data = {}
        response = 'Your account name and email are valid'
        
        if(ClientsInfo.query(ClientsInfo.account_name == account_name) != None):
            response = 'The Account name already exist, please pick up a new one!'
        elif not mail.is_email_valid(email):
            response = 'The email address is invalid!'
        elif(ClientsInfo.query(ClientsInfo.email == email) != None):
            response = response + 'The email already exist, please pick up a new one!'
            
        ajax_data.update({'validation_response':response})
        self.response.out.headers['Content-Type'] = 'text/json'
        self.response.out.write(json.dumps(ajax_data))
#end
       
        
        
# end of ExShipperLoginHandler
class ExShipperGeneralClientsCreateInvoiceInfoHandler(webapp2.RequestHandler):
    def post(self):
        ajax_data = {'submit_status':'NA'}
        if(self.request.get('fmt') == 'json'):
            
            #package size
            new_size = Size()
            new_size.length = self.request.get('valid_size_length')
            new_size.width = self.request.get('valid_size_width')
            new_size.height = self.request.get('valid_size_height')
            new_size.put()
            
            #package information
            package_id = self.request.get('valid_suda_tr_number')
            new_package_info = GeneralClientsPackagesInfo(id=package_id)
            new_package_info.hawb = package_id
            new_package_info.reference_number = self.request.get('valid_ref_number')
            new_package_info.tw_custom_entry_number = 'NA'
            new_package_info.ctn = self.request.get('valid_ctn')
            new_package_info.ctn = self.request.get('valid_note')
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
            new_package_info.size_accumulation = 'NA'
            new_package_info.declaration_need_or_not = 'NLR-NO SED REQIRED NOEEI 30.37(A)'
            new_package_info.duty_paid_by = 'Shipper'
            new_package_info.package_status = 'exshipper'
            new_package_info.put()
            
            
            ajax_data['submit_status'] = 'Data saved into database'
            self.response.out.headers['Content-Type'] = 'text/json'
            self.response.out.write(json.dumps(ajax_data))


#SUDA Tracking Number Handler (For uploading number)
class ExShipperSUDATrackingNumberHandler(webapp2.RequestHandler):
    def get(self):
        my_dict = Key_Value()
        user_info = get_users_info(self, users)
        suda_tracking_number_handler_page = my_dict.exshipper_suda_tracking_number_handler_page
            
        template_values = {'title':my_dict.exshipper_suda_tracking_number_handler_page_title}
        template_values.update(user_info)
            
        template = jinja_environment.get_template(suda_tracking_number_handler_page)
        self.response.out.write(template.render(template_values))
        
    def post(self):
        ajax_data = {'suda_tracking_number_submission':'NA'}
        if(self.request.get('fmt') == 'json'):
            try:
                json_obj = json.loads(self.request.get('json_info'))
                suda_tracking_number_type = json_obj.keys()[0]
                
                if(suda_tracking_number_type == 'regular_suda_tracking_numbers'):
                    suda_number_array = json_obj['regular_suda_tracking_numbers']
                    duplicated_numbers = ''
                    for row_info in suda_number_array:
                        if(SUDATrackingNumber_REGULAR.get_by_id(row_info['suda_number'])):
                            duplicated_numbers += 'Duplicated Number: '+ row_info['suda_number'] +'\n'
                        else:
                            new_suda_tr_number = SUDATrackingNumber_REGULAR(id=row_info['suda_number'])
                            new_suda_tr_number.tracking_number = row_info['suda_number']
                            new_suda_tr_number.used_mark = row_info['used_mark']
                            new_suda_tr_number.put()
                            ajax_data['suda_tracking_number_submission'] = 'Data saved into database'+ '\n' + duplicated_numbers
                            
                if(suda_tracking_number_type == 'formal_suda_tracking_numbers'):
                    suda_number_array = json_obj['formal_suda_tracking_numbers']
                    duplicated_numbers = ''
                    for row_info in suda_number_array:
                        if(SUDATrackingNumber_FORMAL.get_by_id(row_info['suda_number'])):
                            duplicated_numbers += 'Duplicated Number: '+ row_info['suda_number'] +'\n'
                        else:
                            new_suda_tr_number = SUDATrackingNumber_FORMAL(id=row_info['suda_number'])
                            new_suda_tr_number.tracking_number = row_info['suda_number']
                            new_suda_tr_number.used_mark = row_info['used_mark']
                            new_suda_tr_number.put()
                            ajax_data['suda_tracking_number_submission'] = 'Data saved into database'+ '\n' + duplicated_numbers
                            
            except Exception, e:
                ajax_data['suda_tracking_number_submission'] = 'Error Message: %s' % e
            
        self.response.out.headers['Content-Type'] = 'text/json'
        self.response.out.write(json.dumps(ajax_data))
#end of SUDA Tracking Number Handler

#TW Custom Entry Handler (For uploading number)
class ExShipperTWCustomEntryNumberHandler(webapp2.RequestHandler):
    def get(self):
        my_dict = Key_Value()
        user_info = get_users_info(self, users)
        suda_tracking_number_handler_page = my_dict.exshipper_tw_custom_entry_number_handler_page
            
        template_values = {'title':my_dict.exshipper_tw_custom_entry_number_handler_page_title}
        template_values.update(user_info)
            
        template = jinja_environment.get_template(suda_tracking_number_handler_page)
        self.response.out.write(template.render(template_values))
        
    def post(self):
        ajax_data = {'tw_custom_entry_number_submission':'NA'}
        if(self.request.get('fmt') == 'json'):
            #get jsonObj from client side
            try:
                json_obj = json.loads(self.request.get('json_info'))
                tw_custom_entry_number_array = json_obj['tw_custom_entry_numbers']
            except Exception, e:
                ajax_data['tw_custom_entry_number_submission'] = 'Error Message: %s' % e
            
            #check the size of upload numbers; limit the number no more than 200
            ary_length = tw_custom_entry_number_array.__len__()
            if(ary_length > 200):
                ajax_data['tw_custom_entry_number_submission'] = 'Size of upload numbers is not more than 200!'
            else:
                duplicated_numbers = ''
                try:
                    for row_info in tw_custom_entry_number_array:
                        if(TWCustomEntryTrackingNumber.get_by_id(row_info['tw_custom_entry_number'])):
                            duplicated_numbers += 'Duplicated Number: '+ row_info['tw_custom_entry_number'] +'\n'
                            ajax_data['tw_custom_entry_number_submission'] = 'Duplicated Numbers:\n'+'%s' % duplicated_numbers
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
#end of TW Custom Entry Handler

# -- Client Spearnet Session
class ExShipperSpearnetIndexHandler(webapp2.RequestHandler):
    def get(self):
        my_dict = Key_Value()
        user_info = get_users_info(self, users)
        exshipper_spearnet_index_page = my_dict.exshipper_spearnet_index_page
        
        template_values = {'title':my_dict.exshipper_spearnet_index_page_title}
        template_values.update(user_info)
        
        template = jinja_environment.get_template(exshipper_spearnet_index_page)
        self.response.out.write(template.render(template_values))

class ExShipperSpearnetLoginHandler(webapp2.RequestHandler):
    def get(self):
        my_dict = Key_Value()
        user_info = get_users_info(self, users)
        login_page = my_dict.exshipper_spearnet_login_page
        
        dispatch_token = self.request.get('dispatch_token')
        
        template_values = {'title':my_dict.exshipper_spearnet_login_page_title, 'dispatch_token':dispatch_token}
        template_values.update(user_info)
        
        template = jinja_environment.get_template(login_page)
        self.response.out.write(template.render(template_values))
        
    def post(self):
        my_dict = Key_Value()
        user_info = get_users_info(self, users)
        dispatch_token = self.request.get('dispatch_token')
        spearnet_account = self.request.get('spearnet_account')
        spearnet_password = self.request.get('spearnet_password')
        template_values = {}
        
        html_page = my_dict.exshipper_invalid_login_page
        html_page_title = my_dict.exshipper_invalid_login_page_title
        
        # html page dispatching
        if(dispatch_token == 'exshipper_spearnet_data_exchange'):
            if(spearnet_account == 'spearnet' and spearnet_password == '1941dataexchange'):
                html_page = my_dict.exshipper_spearnet_data_exchange_page
                html_page_title = my_dict.exshipper_spearnet_data_exchange_page_title
                
#         elif(dispatch_token == 'exshipper_spearnet_suda_tracking_number_download'):
#             if(spearnet_account == 'spearnet' and spearnet_password == 'spearnet1941'):
#                 html_page = my_dict.exshipper_spearnet_suda_tracking_number_download_page
#                 
#                 working_on = ''
#                 suda_tracking_numbers = SUDATrackingNumber_REGULAR.query(SUDATrackingNumber_REGULAR.used_mark == 'FALSE').fetch(1)
#                 template_values = {'title':my_dict.exshipper_spearnet_suda_tracking_number_download_page_title}
#                 
#                 if suda_tracking_numbers:
#                     for suda_tracking_number in suda_tracking_numbers:
#                         suda_entity = SUDATrackingNumber_REGULAR.get_by_id(suda_tracking_number.tracking_number)
#                         suda_entity.used_mark = 'TRUE'
#                         suda_entity.put()
#                             
#                     template_values.update({'suda_numbers':suda_tracking_numbers})
#                 else:
#                     template_values.update({'suda_numbers':'No SUDA TRacking Number Available'})
#                     send_email('jerry@spearnet-us.com', 'koseioyama@gmail.com', 'Notice for SUDA Tracking Number Shortage', 'There is no SUDA tracking number available')
 
                template_values.update(user_info)
                template = jinja_environment.get_template(html_page)
                self.response.out.write(template.render(template_values))
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
        user_info = get_users_info(self, users)
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
        ajax_data = {'spearnet_packages_info_upload_status':'NA','print_action':'off'}
        try:
            if(self.request.get('fmt') == 'json'):
                json_obj = json.loads(self.request.get('packages_data'))
                packages_array = json_obj['spearnet_invoice']
                for package in packages_array:
                    query_result = SpearnetPackagesInfo.get_by_id(package['hawb'])
                    if(query_result):
                        duplication = True;
                        ajax_data['spearnet_packages_info_upload_status']='You have a duplicated tracking number and please replace it with a new tracking number!'
                        ajax_data['print_action']='off'
                        break;
                    else:
                        duplication = False;
                        
                if(duplication == False):
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
                        
                        new_package.put()
                        
                    ajax_data['spearnet_packages_info_upload_status'] = 'Data saved into database'
                    ajax_data['print_action']='on'
        except Exception, e:
            ajax_data['spearnet_packages_info_upload_status'] = 'Error Message: %s' % e
            
        self.response.out.headers['Content-Type'] = 'text/json; charset=UTF-8'
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
            pickup_status = ''
            
            try:
                for key in suda_numbers_array:
                    package_entity = SpearnetPackagesInfo.get_by_id(key)
                    if(package_entity != None and package_entity.package_status == 'spearnet'):
                        package_entity.package_status = 'pickup'
                        
                        current_date_time = datetime.datetime.now()
                        package_entity.access_info = json.dumps({'access_info':[{'person':'alantai', 'date_time':current_date_time.__str__()}]})
                        package_entity.pickup_date_time = datetime.datetime.now()
                        package_entity.put()
                        pickup_status = 'success'
                        package_tracking_numbers = package_tracking_numbers + key + '\n'
                        response.update({'result':'Successfully Update Picked Packages Information', 'key':'success'})
                        
                    elif(package_entity != None and package_entity.package_status != 'spearnet'):
                        response.update({'result':'Tracking Number, '+ key +', is Duplicated!', 'key':'duplicated_number'})
                        pickup_status = 'fail'
                        break
                    else:
                        response.update({'result':'Unknown Package- ' + key, 'key':'unknown_number'})
                        pickup_status = 'fail'
                        break
                    
                    if(pickup_status == 'success'):
                        email_response = response['result'] + '\n' + 'SUDA Tracking Numbers: ' + '\n' + package_tracking_numbers
                        send_email('receiver', 'sender', 'Package Pickup Status', email_response)
            except Exception, e:
                result = 'Error Message: %s' % e
                response.update({'result':result, 'key':'na'})
            finally:
                if(response['key'] == 'success'):
                    send_email('jerry@spearnet-us.com', 'winever.tw@gmail.com', 'Package Pickup Done', 'Packages Pickup Done by ExShipper')
                json_response['response'] = response
                
        self.response.headers['Content-Type'] = 'text/json ; charset=UTF-8'
        self.response.write(json.dumps(json_response))
        
#download SUDA tracking number handler
class ExShipperSUDATrackingNumberDownloadHandler(webapp2.RequestHandler):
    def post(self):
        user_account = self.request.get('user_account')
        user_password = self.request.get('user_password')
        suda_tracking_number_type = self.request.get('suda_tracking_number_type')
        ajax_data = {'suda_tracking_number':'NA'}
        
        #check suda tracking numbers quantity
        query_length = len(SUDATrackingNumber_REGULAR.query().fetch(100))
        if(query_length < 100):
            send_email('winever.tw@gmail.com', 'koseioyama@gmail.com', 'SUDA TRacking Numbers Shrtage', 'There are/is just ' + query_length.__str__() + ' SUDA tracking numbers left.')
        query_length = len(SUDATrackingNumber_FORMAL.query().fetch(50))
        if(query_length < 50):
            send_email('winever.tw@gmail.com', 'koseioyama@gmail.com', 'Regular SUDA TRacking Numbers Shortage', 'There are/is just ' + query_length.__str__() + ' SUDA tracking numbers.')
                
        #send the tracking number to users
        if(user_account == 'spearnet' and user_password == 'spearnet1941'):
            if(suda_tracking_number_type == 'regular'):
                suda_tracking_number_regular_entity = SUDATrackingNumber_REGULAR.query(SUDATrackingNumber_REGULAR.used_mark == 'FALSE').get()
                if suda_tracking_number_regular_entity != None:
                    regular_suda_entity = SUDATrackingNumber_REGULAR.get_by_id(suda_tracking_number_regular_entity.tracking_number)
                    regular_suda_entity.used_mark = 'TRUE'
                    regular_suda_entity.put()
                    ajax_data['suda_tracking_number'] = suda_tracking_number_regular_entity.tracking_number
                else:
                    send_email('jerry@spearnet-us.com', 'koseioyama@gmail.com', 'Notice for Running out of Regular SUDA Tracking Number', 'No Regular Regular SUDA Tracking Number Available! ')
                    
            elif(suda_tracking_number_type == 'formal'):
                suda_tracking_number_formal_entity = SUDATrackingNumber_FORMAL.query(SUDATrackingNumber_FORMAL.used_mark == 'FALSE').get()
                if suda_tracking_number_formal_entity != None:
                    formal_suda_entity = SUDATrackingNumber_FORMAL.get_by_id(suda_tracking_number_formal_entity.tracking_number)
                    formal_suda_entity.used_mark = 'TRUE'
                    formal_suda_entity.put()
                    ajax_data['suda_tracking_number'] = suda_tracking_number_formal_entity.tracking_number
                else:
                    send_email('jerry@spearnet-us.com', 'koseioyama@gmail.com', 'Notice for Running out of Formal SUDA Tracking Number', 'No Regular SUDA Tracking Number Available! ')
                    
            
        #download suda tracking number for exshipper
        elif(user_account == 'alantai' and user_password == '1014lct'):
            if(suda_tracking_number_type == 'regular'):
                suda_tracking_number_regular_entity = SUDATrackingNumber_REGULAR.query(SUDATrackingNumber_REGULAR.used_mark == 'FALSE').get()
                if suda_tracking_number_regular_entity != None:
                    regular_suda_entity = SUDATrackingNumber_REGULAR.get_by_id(suda_tracking_number_regular_entity.tracking_number)
                    regular_suda_entity.used_mark = 'TRUE'
                    regular_suda_entity.put()
                    ajax_data['suda_tracking_number'] = suda_tracking_number_regular_entity.tracking_number
                else:
                    send_email('winever.tw@gmail.com', 'koseioyama@gmail.com', 'Notice for Running out of Regular SUDA Tracking Number', 'No Regular Regular SUDA Tracking Number Available! ')
                    
            elif(suda_tracking_number_type == 'formal'):
                suda_tracking_number_formal_entity = SUDATrackingNumber_FORMAL.query(SUDATrackingNumber_FORMAL.used_mark == 'FALSE').get()
                if suda_tracking_number_formal_entity != None:
                    formal_suda_entity = SUDATrackingNumber_FORMAL.get_by_id(suda_tracking_number_formal_entity.tracking_number)
                    formal_suda_entity.used_mark = 'TRUE'
                    formal_suda_entity.put()
                    ajax_data['suda_tracking_number'] = suda_tracking_number_formal_entity.tracking_number
                else:
                    send_email('winever.tw@gmail.com', 'koseioyama@gmail.com', 'Notice for Running out of Formal SUDA Tracking Number', 'No Regular SUDA Tracking Number Available! ')
                    
            self.response.out.headers['Content-Type'] = 'text/json; charset=UTF-8'
            self.response.out.write(json.dumps(ajax_data))
        else:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write('Account or Password Are Incorrect!')
     
# working on
class ExShipperSpearnetCustomerIndexHandler(webapp2.RequestHandler):
    def get(self):
        my_dict = Key_Value()
        user_info = get_users_info(self, users)
        html_page = my_dict.exshipper_spearnet_customer_index_page
        
        template_values = {'title':my_dict.exshipper_spearnet_customer_index_page_title}
        template_values.update(user_info)
        template = jinja_environment.get_template(html_page)
        self.response.out.write(template.render(template_values))   
            
#
class ExShipperSpearnetCustomerServicesHandler(webapp2.RequestHandler):
    def post(self):
        my_dict = Key_Value()
        user_info = get_users_info(self, users)
        account = self.request.get('spearnet_customer_account')
        password = self.request.get('spearnet_customer_password')
        
        if(account == 'spearnetcustomer' and password == 'spearnetcustomer1941'):
            html_page = my_dict.exshipper_spearnet_customer_services_handler_page
            page_title = 'ExShipper Spearnet Customer Service Page'
        else:
            html_page = my_dict.exshipper_invalid_login_page
            page_title = 'Invalid Login Page'
        
        template_values = {'title':page_title}
        template_values.update(user_info)
        template = jinja_environment.get_template(html_page)
        self.response.out.write(template.render(template_values))

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
                json_obj_package_status = json_obj['packages_status']
                json_obj_clients_signature = json_obj['clients_signature']
                json_obj_notes = json_obj['notes']
                
                
                if(json_obj_package_status != 'NA'):
                    for key in json_obj_package_status:
                        package_entity = SpearnetPackagesInfo.get_by_id(key)
                        package_entity.package_status = json_obj_package_status[key]
                        package_entity.put()
                         
                if(json_obj_clients_signature != 'NA'):
                    for key in json_obj_clients_signature:
                        package_entity = SpearnetPackagesInfo.get_by_id(key)
                        package_entity.signature_img_id = json_obj_clients_signature[key]
                        package_entity.put()
                         
                if(json_obj_notes != 'NA'):
                    for key in json_obj_notes.keys():
                        package_entity = SpearnetPackagesInfo.get_by_id(key)
                        package_entity.note = json_obj_notes[key]
                        package_entity.put()
                    
                ajax_data['update_status'] = 'Successfully update the packages status!'
                
        except Exception, e:
                ajax_data['update_status'] = 'Error Message: %s' % e
                
        self.response.out.headers['Content-Type'] = 'text/json'
        self.response.out.write(json.dumps(ajax_data))
# end of exshipper & spearnet

#exshipper tw custom entry login handler
class ExShipperTWCustomEntryIndexHandler(webapp2.RequestHandler):
    def get(self):
        my_dict = Key_Value()
        user_info = get_users_info(self, users)
        login_page = my_dict.exshipper_tw_custom_entry_index_page
        
        template_values = {'title':my_dict.exshipper_tw_custom_entry_index_page_title}
        template_values.update(user_info)
        
        template = jinja_environment.get_template(login_page)
        self.response.out.write(template.render(template_values))
        
class ExShipperTWCustomEntryLoginHandler(webapp2.RequestHandler):
    def get(self):
        my_dict = Key_Value()
        user_info = get_users_info(self, users)
        login_page = my_dict.exshipper_tw_custom_entry_login_page
        
        dispatch_token = self.request.get('dispatch_token')
        
        template_values = {'title':my_dict.exshipper_tw_custom_entry_login_page_title, 'dispatch_token':dispatch_token}
        template_values.update(user_info)
        
        template = jinja_environment.get_template(login_page)
        self.response.out.write(template.render(template_values))
        
    def post(self):
        my_dict = Key_Value()
        user_info = get_users_info(self, users)
        dispatch_token = self.request.get('dispatch_token')
        tw_custom_entry_account = self.request.get('tw_custom_entry_account')
        tw_custom_entry_password = self.request.get('tw_custom_entry_password')
        template_values = {}
        
        html_page = my_dict.exshipper_invalid_login_page
        html_page_title = my_dict.exshipper_invalid_login_page_title
        
        # html page dispatching
        if(dispatch_token == 'exshipper_tw_custom_entry_invoice_log'):
            if(tw_custom_entry_account == 'alantai' and tw_custom_entry_password == '1014lct'):
                html_page = my_dict.exshipper_tw_custom_entry_invoice_log_page
                html_page_title = my_dict.exshipper_tw_custom_entry_invoice_log_page_title
                spearnet_customer_package_info_log = SpearnetPackagesInfo.query()
                general_client_package_info_log = GeneralClientsPackagesInfo.query()
                
                template_values.update({'spearnet_customer_package_info_log':spearnet_customer_package_info_log, 'general_client_package_info_log':general_client_package_info_log})
                #use memcache
#                 data = memcache.get('tw_custom_entry_invoice_log')
#                 if data != None:
#                     log_spearnet_customer_package_info = data
#                 else:
#                     data = SpearnetPackagesInfo.query()
#                     memcache.add('tw_custom_entry_invoice_log',data,500)
#                     log_spearnet_customer_package_info = data
#                 template_values.update({'spearnet_customer_package_info_log':log_spearnet_customer_package_info})

        elif(dispatch_token == 'exshipper_tw_custom_entry_cargo_manifest'):
            if(tw_custom_entry_account == 'alantai' and tw_custom_entry_password == '1014lct'):
                html_page = my_dict.exshipper_cargo_manifest_page
                html_page_title = my_dict.exshipper_cargo_manifest_page_title
                
                spearnet_customers_package_info_cargo_manifest = SpearnetPackagesInfo.query()
                general_clients_package_info_cargo_manifest = GeneralClientsPackagesInfo.query()
#                 cargo_manifest.update(spearnet_customers_package_info_cargo_manifest)
#                 cargo_manifest.update(general_clients_package_info_cargo_manifest)
                template_values.update({'cargo_manifest_spearnet':spearnet_customers_package_info_cargo_manifest, 'cargo_manifest_general_clients':general_clients_package_info_cargo_manifest})

        else:
            html_page = my_dict.exshipper_invalid_login_page
            html_page_title = my_dict.exshipper_invalid_login_page_title
            
        template_values.update({'title':html_page_title})
        template_values.update(user_info)
        template = jinja_environment.get_template(html_page)
        self.response.out.write(template.render(template_values))
        # end of html page dispatching

#end of exshipper tw custom entry login handler

# custom entry handler
class ExshipperTWCustomEntryHandler(webapp2.RequestHandler):
    def post(self):
        account = self.request.get('account')
        password = self.request.get('password')
        token = self.request.get('token')
        ajax_data = {}
        
        #tw custom entry handler for getting a number
        if(account == 'alantai' and password == '1014' and token == 'tw_custom_entry_handler_get_number'):
            try:
                tw_custom_entry_number = 'NA'
                query_length = TWCustomEntryTrackingNumber.query().fetch(30).count(30)
                if(query_length < 30):
                    body = 'There are/is only '+ query_length.__str__() +' TW Custom Entry tracking numbers left.'
                    email_status = send_email('winever.tw@gmail.com', 'koseioyama@gmail.com', 'TW Custom Entry Barcode Number Shortage', body)
                
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
                
        #tw custom entry handler for submitting packages info
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
                        response_result += 'Package NO.'+package_number + ';'
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
                        tw_custom_entry_package.put()
                        tw_custom_package = tw_custom_package + 'TW Custom Entry Package- ' + key + ' ; ' + response_result
                
                        tw_custom_entry_submit_result = tw_custom_package
                        tw_custom_entry_submit_response.update({'result':tw_custom_entry_submit_result})
                        tw_custom_entry_submit_response['key'] = 'success'
                        
                        working_on = ''
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
                        package_entity.flight_date = json_obj_flight_dates[key]
                        package_entity.put()
                    
                ajax_data['update_status'] = 'Successfully update the packages information!'
                
        except Exception, e:
                ajax_data['update_status'] = 'Error Message: %s' % e
                
        self.response.out.headers['Content-Type'] = 'text/json'
        self.response.out.write(json.dumps(ajax_data))
        
#end of custom entry handler

class ExShipperGeneralClientsIndexHandler(webapp2.RequestHandler):
    def get(self):
        my_dict = Key_Value()
        user_info = get_users_info(self, users)
        exshipper_general_clients_index_page = my_dict.exshipper_general_clients_index_page
        
        template_values = {'title':my_dict.exshipper_general_clients_index_page_title}
        template_values.update(user_info)
        
        template = jinja_environment.get_template(exshipper_general_clients_index_page)
        self.response.out.write(template.render(template_values))
    
class ExShipperGeneralClientsLoginHandler(webapp2.RequestHandler):
    def get(self):
        my_dict = Key_Value()
        user_info = get_users_info(self, users)
        login_page = my_dict.exshipper_general_clients_login_page
        
        dispatch_token = self.request.get('dispatch_token')
        
        template_values = {'title':my_dict.exshipper_general_clients_login_page_title, 'dispatch_token':dispatch_token}
        template_values.update(user_info)
        
        template = jinja_environment.get_template(login_page)
        self.response.out.write(template.render(template_values))
        
    def post(self):
        my_dict = Key_Value()
        user_info = get_users_info(self, users)
        dispatch_token = self.request.get('dispatch_token')
        tw_custom_entry_account = self.request.get('general_clients_entry_account')
        tw_custom_entry_password = self.request.get('general_clients_entry_password')
        template_values = {}
        
        html_page = my_dict.exshipper_invalid_login_page
        html_page_title = my_dict.exshipper_invalid_login_page_title
        
        # html page dispatching
        if(dispatch_token == 'creating_invoice'):
            if(tw_custom_entry_account == 'alantai' and tw_custom_entry_password == '1014lct'):
                html_page = my_dict.exshipper_general_clients_create_invoice_page
                html_page_title = my_dict.exshipper_general_clients_create_invoice_page_title
                
        elif(dispatch_token == 'track_package_status'):
            if(tw_custom_entry_account == 'alantai' and tw_custom_entry_password == '1014lct'):
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
        
class ExShipperGeneralClientsPackageInfoUpdateHandler(webapp2.RequestHandler):
    def post(self):
        try:
            ajax_data = {'update_status':'NA'}
            if(self.request.get('fmt') == 'json'):
                update_packages_status = self.request.get('update_packages_info')
                json_obj = json.loads(update_packages_status)
                json_obj_package_status = json_obj['packages_status']
                json_obj_clients_signature = json_obj['clients_signature']
                json_obj_notes = json_obj['notes']
                
                if(json_obj_package_status != 'NA'):
                    for key in json_obj_package_status:
                        package_entity = GeneralClientsPackagesInfo.get_by_id(key)
                        package_entity.package_status = json_obj_package_status[key]
                        package_entity.put()
                          
                if(json_obj_clients_signature != 'NA'):
                    for key in json_obj_clients_signature:
                        package_entity = GeneralClientsPackagesInfo.get_by_id(key)
                        package_entity.signature_img_id = json_obj_clients_signature[key]
                        package_entity.put()
                          
                if(json_obj_notes != 'NA'):
                    for key in json_obj_notes:
                        package_entity = GeneralClientsPackagesInfo.get_by_id(key)
                        package_entity.note = json_obj_notes[key]
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
#end of general clients
        
        
#function classes block
#get image
class GetImage(webapp2.RequestHandler):
    def get(self):
        entity_id = self.request.get('entity_id')
        entity = ndb.Key(urlsafe=entity_id).get()
        if entity and entity.signature_img:
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(entity.signature_img)
            
#get reference numbers
class GetReferenceNumber(webapp2.RequestHandler):
    def post(self):
        ajax_data = {}
        if(self.request.get('key') == 'get_package_reference_number'):
            time_stamp = int(round(time.time())).__str__()
            exshipper_package_number = 'EXPKG' + time_stamp
            ajax_data.update({'exshipper_package_number':exshipper_package_number})
            
            self.response.headers['Content-Type'] = 'text/json'
            self.response.out.write(json.dumps(ajax_data))
# end of function classes
        

#temporary functions block (will be moved to the cooresponding handlers)
#send email
def send_email(receiver, sender, subject, body):
    my_dict = Key_Value()
    result = {'email_status':'unknown'}
    email_host = 'winever.tw@gmail.com'
    if not mail.is_email_valid(receiver):
        result['email_status'] = 'invalid_email'
    else:
        try:
            receiver_email_content = body + 'Notice: The SUDA tracking number ran out and new numbers will be ready soon. If you have further questions, please contact ExShipper.'
            mail.send_mail(email_host, receiver, subject, receiver_email_content)
            sender_email_content = body + 'Notice: The SUDA tracking number ran out. Please update the database!'
            mail.send_mail(email_host, receiver, subject, sender_email_content)
            result['email_status'] = my_dict.email_delivery_status_success
        except:
            result['email_status'] = my_dict.email_delivery_status_fail
    return result

# get users info
def get_users_info(self, users):
    my_dict = Key_Value()
    if users.get_current_user():
        user_account = users.get_current_user()
        url = users.create_logout_url(self.request.uri)
    else:
        user_account = my_dict.unknown_user
        url = users.create_login_url(self.request.uri)
        
    values = {
              'user_account': user_account,
              'url': url}
    return values
# end of #temporary functions block


#test class
class TestHandler(webapp2.RequestHandler):
    def get(self):
        my_dict = Key_Value()
        user_info = get_users_info(self, users)
        test_page = '/exshipper/exshipper_test.html'
            
        template_values = {'title':my_dict.exshipper_invoice_log_title}
        template_values.update(user_info)
            
        template = jinja_environment.get_template(test_page)
        self.response.out.write(template.render(template_values))
#end of test class


# set url
app = webapp2.WSGIApplication([('/exshipper_index', ExShipperIndexHandler),
                               ('/exshipper_login_handler', ExShipperLoginHandler),
                               ('/exshipper_invoice_info_handler', ExShipperGeneralClientsCreateInvoiceInfoHandler),
                               ('/exshipper_create_client_info_handler', ExShipperCreateClientInfoHandler),
                               ('/img', GetImage),
                               ('/get_ref_number', GetReferenceNumber),
                               ('/exshipper_spearnet_index_page', ExShipperSpearnetIndexHandler),
                               ('/exshipper_spearnet_login_handler', ExShipperSpearnetLoginHandler),
                               ('/exshipper_spearnet_data_exchange_page', ExShipperSpearnetDataExchangeDispatcher),
                               ('/exshipper_spearnet_data_exchange_handler', ExShipperSpearnetDataExchangeHandler),
                               ('/exshipper_suda_tracking_number_handler', ExShipperSUDATrackingNumberHandler),
                               ('/exshipper_tw_custom_entry_number_handler', ExShipperTWCustomEntryNumberHandler),
                               ('/exshipper_suda_tracking_number_download_handler', ExShipperSUDATrackingNumberDownloadHandler),
                               ('/exshipper_tw_custom_entry_handler', ExshipperTWCustomEntryHandler),
                               ('/exshipper_spearnet_customer_index_page', ExShipperSpearnetCustomerIndexHandler),
                               ('/exshipper_spearnet_customer_services_handler', ExShipperSpearnetCustomerServicesHandler),
                               ('/exshipper_spearnet_customer_package_tracking_handler', ExShipperSpearnetCustomerPackageTrackingHandler),
                               ('/exshipper_spearnet_customer_packages_info_update_handler',ExShipperSpearnetCustomerPackageInfoUpdateHandler),
                               ('/exshipper_spearnet_packages_pickup_handler',ExShipperSpearnetPackagesPickupHandler),
                               ('/exshipper_tw_custom_entry_index_page',ExShipperTWCustomEntryIndexHandler),
                               ('/exshipper_tw_custom_entry_login_handler',ExShipperTWCustomEntryLoginHandler),
                               ('/exshipper_tw_custom_entry_packages_info_update_handler', ExShipperTWCustomEntryPackageInfoUpdateHandler),
                               ('/exshipper_general_clients_index_page', ExShipperGeneralClientsIndexHandler),
                               ('/exshipper_general_clients_login_handler', ExShipperGeneralClientsLoginHandler),
                               ('/exshipper_general_clients_packages_info_update_handler', ExShipperGeneralClientsPackageInfoUpdateHandler),
                               ('/exshipper_general_clients_packages_tracking_handler', ExShipperGeneralClientsPackageTrackingHandler),
                               ('/exshipper_test', TestHandler)], debug=True)