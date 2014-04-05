# -*- coding: utf-8 -*-
'''
Created on Oct 1, 2013

@author: Alan Tai
'''
from google.appengine.ext.key_range import ndb
from django.contrib.gis.db.models import query
__author__ = 'Alan Tai'

import random
import webapp2
import jinja2
import os
from google.appengine.api import users, mail, memcache
import json

from app_dict import Key_Value
from models import Size, SUDATrackingNumber_REGULAR, SpearnetPackagesInfo, TWCustomEntryTrackingNumber,\
    ClientsInfo, GeneralClientsPackagesInfo, SUDATrackingNumber_FORMAL

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + '/static/templates'))
# jinja_environment = jinja2.Environment(loader = jinja2.FileSystemLoader(os.path.dirname(__file__)+'/static/templates/exshipper'))

class ExShipperIndexHandler(webapp2.RequestHandler):
    def get(self):
        my_dict = Key_Value()
        user_info = get_users_info(self, users)
        index_page = my_dict.exshipper_index_page
        
        template_values = {'title':my_dict.exshipper_index_page_title}
        template_values.update(user_info)
        
        template = jinja_environment.get_template(index_page)
        self.response.out.write(template.render(template_values))

# for handling the login process
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
        
    #dispatch visitor to different pages according to the token users send
    def post(self):
        my_dict = Key_Value()
        user_info = get_users_info(self, users)
        dispatch_token = self.request.get('dispatch_token')
        exshipper_account = self.request.get('exshipper_account')
        exshipper_password = self.request.get('exshipper_password')
        template_values = {}
        
        #set default page as invalid login page
        html_page = my_dict.exshipper_invalid_login_page
        html_page_title = my_dict.exshipper_invalid_login_page_title
        
        # html page dispatching
        if(dispatch_token == 'exshipper_invoice'):
            if(exshipper_account == 'alantai' and exshipper_password == '1014lct'):
                
                html_page = my_dict.exshipper_invoice_creating_page
                html_page_title = my_dict.exshipper_invoice_creating_page_title
                
        elif(dispatch_token == 'exshipper_create_client_info'):
            if(exshipper_account == 'alantai' and exshipper_password == '1014lct'):
                clients_data = ClientsInfo.query()
                template_values.update({'clients_data':clients_data})
                
                html_page = my_dict.exshipper_create_client_info_handler
                html_page_title = my_dict.exshipper_create_client_info_handler_title
                
        elif(dispatch_token == 'exshipper_suda_tracking_number'):
            if(exshipper_account == 'alantai' and exshipper_password == '1014lct'):
                html_page = my_dict.exshipper_suda_tracking_number_handler_page
                html_page_title = my_dict.exshipper_suda_tracking_number_handler_page_title
                
        elif(dispatch_token == 'exshipper_tw_custom_entry_number'):
            if(exshipper_account == 'alantai' and exshipper_password == '1014lct'):
                html_page = my_dict.exshipper_tw_custom_entry_number_handler_page
                html_page_title = my_dict.exshipper_tw_custom_entry_number_handler_page_title
                
        elif(dispatch_token == 'exshipper_spearnet_customers_package_info_log'):
            if(exshipper_account == 'alantai' and exshipper_password == '1014lct'):
                html_page = my_dict.exshipper_spearnet_customer_package_info_log_page
                html_page_title = my_dict.exshipper_spearnet_customer_package_info_log_page_title
                
                #use memcache
#                 data = memcache.get('spearnet_customer_package_info_log')
#                 if data is not None:
#                     log_spearnet_customer_package_info = data
#                 else:
#                     data = SpearnetPackagesInfo.query()
#                     memcache.add('spearnet_customer_package_info_log',data,1000)
#                     log_spearnet_customer_package_info = data

                spearnet_customer_package_info_log = SpearnetPackagesInfo.query()
                clients_info = ClientsInfo().query()
                template_values.update({'spearnet_customer_package_info_log': spearnet_customer_package_info_log, 'clients_info':clients_info})
                  
        elif(dispatch_token == 'exshipper_general_clients_package_info_log'):
            if(exshipper_account == 'alantai' and exshipper_password == '1014lct'):
                html_page = my_dict.exshipper_general_clients_package_info_log_page
                html_page_title = my_dict.exshipper_general_clients_package_info_log_page_title
                general_clients_packages_info_log = GeneralClientsPackagesInfo.query()
                clients_info = ClientsInfo().query()
                template_values.update({'general_clients_packages_info_log':general_clients_packages_info_log, 'clients_info':clients_info})
                
        elif(dispatch_token == 'exshipper_pre_alert'):
            if(exshipper_account == 'alantai' and exshipper_password == '1014lct'):
                html_page = my_dict.exshipper_pre_alert_page
                html_page_title = my_dict.exshipper_pre_alert_page_title
                
        elif(dispatch_token == 'exshipper_cargo_manifest'):
            if(exshipper_account == 'alantai' and exshipper_password == '1014lct'):
                html_page = my_dict.exshipper_cargo_manifest_page
                html_page_title = my_dict.exshipper_cargo_manifest_page_title
                cargo_manifest = ndb.Query(ndb.OR(kind = 'SpearnetPackagesInfo',
                                                  kind = 'ClientsInfo'))
                template_values.update({'cargo_manifest':cargo_manifest})
        
        else:
            html_page = my_dict.exshipper_invalid_login_page
            html_page_title = my_dict.exshipper_invalid_login_page_title
            
        template_values.update({'title':html_page_title})
        template_values.update(user_info)
        template = jinja_environment.get_template(html_page)
        self.response.out.write(template.render(template_values))
        # end of html page dispatching
        
# end of ExShipperLoginHandler
class ExShipperInvoiceInfoHandler(webapp2.RequestHandler):
    def post(self):
        ajax_data = {'submit_status':'NA'}
        if(self.request.get('fmt') == 'json'):
            
            new_size = Size()
            new_size.length = self.request.get('valid_size_length')
            new_size.width = self.request.get('valid_size_width')
            new_size.height = self.request.get('valid_size_height')
            
            new_size.put()
            package_id = self.request.get('valid_suda_tr_number')
            new_package_info = GeneralClientsPackagesInfo(id=package_id)
            new_package_info.hawb = package_id
            new_package_info.reference_number = self.request.get('valid_ref_number')
            new_package_info.tw_custom_entry_number = 'NA'
            new_package_info.ctn = self.request.get('ctn')
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
            new_package_info.pickup_status = 'TRUE'
            new_package_info.put()
            
            
            ajax_data['submit_status'] = 'Data saved into database'
            self.response.out.headers['Content-Type'] = 'text/json'
            self.response.out.write(json.dumps(ajax_data))

class ExShipperCreateClientInfoHandler(webapp2.RequestHandler):
    def post(self):
        new_client = ClientsInfo()
        new_client.name = self.request.get('client_name')
        new_client.address = self.request.get('client_address')
        new_client.phone = self.request.get('client_phone')
        new_client.signature_str = self.request.get('name_for_signature')
        new_client.signature_img = self.request.get('form_client_signature')
        new_client.put()
        
        my_dict = Key_Value()
        template_values = {}
        user_info = get_users_info(self, users)
        template_values.update(user_info)
        clients_data = ClientsInfo.query()
        template_values.update({'clients_data':clients_data})
                
        template_values.update({'title':my_dict.exshipper_create_client_info_handler_title})
        
        template = jinja_environment.get_template(my_dict.exshipper_create_client_info_handler)
        self.response.out.write(template.render(template_values))
        working_on = ''
        
class GetImage(webapp2.RequestHandler):
    def get(self):
        entity_id = self.request.get('entity_id')
        entity = ndb.Key(urlsafe=entity_id).get()
        if entity and entity.signature_img:
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(entity.signature_img)

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
                suda_number_array = json_obj['suda_tracking_numbers']
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
            
            #check the size of upload numbers
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
                
        elif(dispatch_token == 'exshipper_spearnet_suda_tracking_number_download'):
            if(spearnet_account == 'spearnet' and spearnet_password == 'spearnet1941'):
                html_page = my_dict.exshipper_spearnet_suda_tracking_number_download_page
                suda_tracking_numbers = SUDATrackingNumber_REGULAR.query(SUDATrackingNumber_REGULAR.used_mark == 'FALSE').fetch(1)
                template_values = {'title':my_dict.exshipper_spearnet_suda_tracking_number_download_page_title}
                
                if suda_tracking_numbers:
                    for suda_tracking_number in suda_tracking_numbers:
                        suda_entity = SUDATrackingNumber_REGULAR.get_by_id(suda_tracking_number.tracking_number)
                        suda_entity.used_mark = 'TRUE'
                        suda_entity.put()
                            
                    template_values.update({'suda_numbers':suda_tracking_numbers})
                else:
                    template_values.update({'suda_numbers':'No SUDA TRacking Number Available'})
                    exshipper_send_email('jerry@spearnet-us.com', 'koseioyama@gmail.com', 'Notice for SUDA Tracking Number Shortage', '')
                    
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
                        new_package.pickup_status = 'FALSE'
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
        response = 'NA'
        json_response = {'response':'NA'}
        if(account == 'alantai' and password == '1014'):
            json_obj = json.loads(self.request.get('spearnet_picked_packages'))
            suda_numbers_array = json.loads(json_obj['suda_tracking_numbers'])
            try:
                for key in suda_numbers_array:
                    package_entity = SpearnetPackagesInfo.get_by_id(key)
                    if(package_entity != None and package_entity.package_status == 'spearnet'):
                        package_entity.package_status = 'exshipper'
                        package_entity.put()
                        response = 'Successfully Update Picked Packages Information'
                    else:
                        if(package_entity != None and package_entity.package_status != 'spearnet'):
                            response = 'Tracking Number, '+ key +', is Duplicated!'
                        else:
                            response = "Unknown Package- " + key
                            break
                
            except Exception, e:
                response = 'Error Message: %s' % e
            finally:
                json_response['response'] = response
                
        self.response.headers['Content-Type'] = 'text/json ; charset=UTF-8'
        self.response.write(json.dumps(json_response))
        
#download SUDA tracking number handler
class ExShipperSpearnetSUDATrackingNumberHandler(webapp2.RequestHandler):
    def post(self):
        my_dict = Key_Value()
        user_info = get_users_info(self, users)
        user_account = self.request.get('user_account')
        user_password = self.request.get('user_password')
        suda_tracking_number_type = self.request.get('suda_tracking_number_type')
        ajax_data = {'suda_tracking_number':'NA'}
        if(user_account == 'spearnet' and user_password == 'spearnet1941'):
            html_page = my_dict.exshipper_spearnet_suda_tracking_number_handler_page
            suda_tracking_numbers = SUDATrackingNumber_REGULAR.query(SUDATrackingNumber_REGULAR.used_mark == 'FALSE').fetch(1)
            
            if suda_tracking_numbers:
                for suda_tracking_number in suda_tracking_numbers:
                    suda_entity = SUDATrackingNumber_REGULAR.get_by_id(suda_tracking_number.tracking_number)
                    suda_entity.used_mark = 'TRUE'
                    suda_entity.put()
                        
                template_values = {'title':my_dict.exshipper_invoice_log_title,
                                   'suda_numbers':suda_tracking_numbers}
                template_values.update(user_info)
                    
                template = jinja_environment.get_template(html_page)
                self.response.out.write(template.render(template_values))
            else:
                exshipper_send_email('jerry@spearnet-us.com', 'koseioyama@gmail.com', 'Notice for Running out of SUDA Tracking Number', '')
                
        #download suda tracking number for exshipper
        elif(user_account == 'alantai' and user_password == '1014lct'):
            if(suda_tracking_number_type == 'regular'):
                suda_tracking_numbers = SUDATrackingNumber_REGULAR.query(SUDATrackingNumber_REGULAR.used_mark == 'FALSE').fetch(1)
                if suda_tracking_numbers:
                    suda_entity = SUDATrackingNumber_REGULAR.get_by_id(suda_tracking_numbers[0].tracking_number)
                    suda_entity.used_mark = 'TRUE'
                    suda_entity.put()
                    ajax_data['suda_tracking_number'] = suda_tracking_numbers[0].tracking_number
                    
            elif(suda_tracking_number_type == 'formal'):
                suda_tracking_numbers = SUDATrackingNumber_FORMAL.query(SUDATrackingNumber_FORMAL.used_mark == 'FALSE').fetch(1)
                if suda_tracking_numbers:
                    suda_entity = SUDATrackingNumber_FORMAL.get_by_id(suda_tracking_numbers[0].tracking_number)
                    suda_entity.used_mark = 'TRUE'
                    suda_entity.put()
                    ajax_data['suda_tracking_number'] = suda_tracking_numbers[0].tracking_number
                    
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
                tracking_result = SpearnetPackagesInfo.query(SpearnetPackagesInfo.hawb == self.request.get('customer_tracking_number')).fetch(1)
                if(tracking_result):
                    package_status = tracking_result[0].package_status
                    ajax_data['package_status'] = package_status
        except Exception, e:
            ajax_data['package_status'] = 'Error Message: %s' % e
                           
        self.response.out.headers['Content-Type'] = 'text/json'
        self.response.out.write(json.dumps(ajax_data))
        
class ExShipperSpearnetCustomerPackageStatusHandler(webapp2.RequestHandler):
    def post(self):
        ajax_data = {'update_status':'NA'}
        if(self.request.get('fmt') == 'json'):
            update_packages_status = self.request.get('update_packages_status')
            json_obj = json.loads(update_packages_status)
            for key in json_obj.keys():
                package_entity = SpearnetPackagesInfo.get_by_id(key)
                package_entity.package_status = json_obj[key]
                package_entity.put()
                
            ajax_data['update_status'] = 'Successfully update the packages status!'
                
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
                html_page = my_dict.exshipper_tw_custom_entry_login_page
                html_page_title = my_dict.exshipper_general_clients_login_page_title
                
                #use memcache
                data = memcache.get('tw_custom_entry_invoice_log')
                if data is not None:
                    log_spearnet_customer_package_info = data
                else:
                    data = SpearnetPackagesInfo.query()
                    memcache.add('tw_custom_entry_invoice_log',data,500)
                    log_spearnet_customer_package_info = data
                template_values.update({'spearnet_customer_package_info_log':log_spearnet_customer_package_info})
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
        
        #tw custom entry handler for getting a number
        if(account == 'alantai' and password == '1014' and token == 'tw_custom_entry_handler_get_number'):
            tw_custom_entry_number = 'NA'
            try:
                tracking_number = TWCustomEntryTrackingNumber.query(TWCustomEntryTrackingNumber.used_mark == 'FALSE').fetch(1)
                if(tracking_number):
                    tw_custom_entry_number = tracking_number
                else:
                    tw_custom_entry_number = 'NA'
            except:
                tw_custom_entry_number = 'NA'
            finally:
                tw_custom_entry_number = random.randint(10000,99999)
                response = tw_custom_entry_number
        #tw custom entry handler for submitting packages info
        elif(account == 'alantai' and password == '1014' and token == 'tw_custom_entry_handler_submit_packages_sets'):
            response_result = ''
            try:
                json_obj_packages_sets = json.loads(self.request.get('tw_custom_entry_packages_sets'))
                json_obj_packages_size_weight = json.loads(self.request.get('tw_custom_entry_packages_size_weight'))
                
                has_duplicated_number = 'no'
                
                for key in json_obj_packages_sets.keys():
                    json_obj_packages_size_weight = json_obj_packages_size_weight[key]['strObj']['length']
                    
                    for package_number in json_obj_packages_sets[key].keys():
                        response_result += 'Package NO.'+package_number + ';'
                        spearnet_package_entity = SpearnetPackagesInfo.get_by_id(package_number)
                        general_client_package_entity = GeneralClientsPackagesInfo.get_by_id(package_number)
                        if(spearnet_package_entity == None and general_client_package_entity == None):
                            duplicated_response = 'Unknown Number- ' + package_number
                            has_duplicated_number = 'yes'
                            break;
                        
                    if(has_duplicated_number == 'yes'):
                        tw_custom_package = duplicated_response
                        break;
                    
                    tw_custom_package = 'TW Custom Entry Package- ' + key + ', Length: ' + json_obj_packages_size_weight.__str__() + ' ; ' + response_result
                
                tw_custom_entry_submit_result = tw_custom_package
            except:
                tw_custom_entry_submit_result = 'NA'
            finally:
                response = tw_custom_entry_submit_result
                
        self.response.headers['Content-Type'] = 'text/plain ; charset=UTF-8'
        self.response.write('{"response":"'+ response.__str__() +'"}')
        return
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
        
        working_on = ''
        
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
        
        
#send email
def exshipper_send_email(receiver, sender, subject, body):
    my_dict = Key_Value()
    result = {'email_status':'unknown'}
    email_host = 'rainman.tai@gmail.com'
    if not mail.is_email_valid(receiver):
        result['email_status'] = 'invalid_email'
    else:
        try:
            receiver_email_content = 'Notice: The SUDA tracking number ran out and new numbers will be ready soon. If you have further questions, please contact ExShipper.'
            mail.send_mail(email_host, receiver, subject, receiver_email_content)
            sender_email_content = 'Notice: The SUDA tracking number ran out. Please update the database!'
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
# end of self-defined functions


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
                               ('/exshipper_invoice_info_handler', ExShipperInvoiceInfoHandler),
                               ('/exshipper_create_client_info_handler', ExShipperCreateClientInfoHandler),
                               ('/img', GetImage),
                               ('/exshipper_spearnet_index_page', ExShipperSpearnetIndexHandler),
                               ('/exshipper_spearnet_login_handler', ExShipperSpearnetLoginHandler),
                               ('/exshipper_spearnet_data_exchange_page', ExShipperSpearnetDataExchangeDispatcher),
                               ('/exshipper_spearnet_data_exchange_handler', ExShipperSpearnetDataExchangeHandler),
                               ('/exshipper_suda_tracking_number_handler', ExShipperSUDATrackingNumberHandler),
                               ('/exshipper_tw_custom_entry_number_handler', ExShipperTWCustomEntryNumberHandler),
                               ('/exshipper_spearnet_suda_tracking_number_handler', ExShipperSpearnetSUDATrackingNumberHandler),
                               ('/exshipper_tw_custom_entry_handler', ExshipperTWCustomEntryHandler),
                               ('/exshipper_spearnet_customer_index_page', ExShipperSpearnetCustomerIndexHandler),
                               ('/exshipper_spearnet_customer_services_handler', ExShipperSpearnetCustomerServicesHandler),
                               ('/exshipper_spearnet_customer_package_tracking_handler', ExShipperSpearnetCustomerPackageTrackingHandler),
                               ('/exshipper_spearnet_customer_packages_status_handler',ExShipperSpearnetCustomerPackageStatusHandler),
                               ('/exshipper_spearnet_packages_pickup_handler',ExShipperSpearnetPackagesPickupHandler),
                               ('/exshipper_tw_custom_entry_index_page',ExShipperTWCustomEntryIndexHandler),
                               ('/exshipper_tw_custom_entry_login_handler',ExShipperTWCustomEntryLoginHandler),
                               ('/exshipper_exshipper_general_clients_index_page', ExShipperGeneralClientsIndexHandler),
                               ('/exshipper_general_clients_login_handler', ExShipperGeneralClientsLoginHandler),
                               ('/exshipper_test', TestHandler)], debug=True)
