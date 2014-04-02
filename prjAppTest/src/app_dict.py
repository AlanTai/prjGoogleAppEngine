# -*- coding: utf-8 -*-
'''
Created on Oct 1, 2013

@author: Alan Tai
'''
class Key_Value():
    def __init__(self):
        #login information
        self.unknown_user = 'unknown_user'
        
        #email
        self.email_delivery_status_success = 'success'
        self.email_delivery_status_fail = 'fail'
        #exshipper specific terms
        self.exshipper_index_page = '/exshipper/exshipper_index.html'
        self.exshipper_index_page_title = 'ExShipper Index Page'
        self.exshipper_login_page = '/exshipper/exshipper_login.html'
        self.exshipper_login_page_title = 'ExShipper Login Page'
        self.exshipper_invalid_login_page = '/exshipper/exshipper_invalid_login_page.html'
        self.exshipper_invalid_login_page_title = 'Invalid Login Page'
        self.exshipper_invoice_creating_page = '/exshipper/exshipper_invoice.html'
        self.exshipper_invoice_creating_page_title = 'ExShipper Create Invoice Page'
        self.exshipper_invoice_log_page = '/exshipper/exshipper_invoice_log.html'
        self.exshipper_invoice_log_title = 'ExShipper Invoice Log'
        self.exshipper_suda_tracking_number_handler_page = '/exshipper/exshipper_suda_tracking_number_handler.html'
        self.exshipper_suda_tracking_number_handler_page_title = 'ExShipper SUDA Tracking Number Handler'
        
        #taiwan custom entry
        self.exshipper_tw_custom_entry_number_handler_page = '/exshipper/exshipper_tw_custom_entry_number_handler.html'
        self.exshipper_tw_custom_entry_number_handler_page_title = 'ExShipper TW Custom Entry Number Handler'
        
        self.exshipper_create_client_info_handler = '/exshipper/exshipper_create_client_info_handler.html'
        self.exshipper_create_client_info_handler_title = 'ExShipper Create Client Information Handler'
        
        self.exshipper_tw_custom_entry_login_page = '/exshipper/exshipper_tw_custom_entry_login.html'
        self.exshipper_tw_custom_entry_login_page_title = 'Taiwan Custom Entry Login'
        
        #spearnet
        self.exshipper_spearnet_index_page = '/exshipper/exshipper_spearnet_index.html'
        self.exshipper_spearnet_index_page_title = 'ExShipper Spearnet Index Page'
        self.exshipper_spearnet_data_exchange_page = '/exshipper/exshipper_spearnet_data_exchange_page.html'
        self.exshipper_spearnet_data_exchange_page_title = 'ExShipper SpearNet Data Exchange Page'
             
        self.exshipper_spearnet_login_page = '/exshipper/exshipper_spearnet_login.html'
        self.exshipper_spearnet_login_page_title = 'ExShipper Spearnet Login Page'
             
        self.exshipper_spearnet_xls_page = '/exshipper/exshipper_xls_parser.html'
        self.exshipper_spearnet_xls_title = 'XLS Parser'
        self.exshipper_spearnet_xlsx_page = '/exshipper/exshipper_xlsx_parser.html'
        self.exshipper_spearnet_xlsx_title = 'XLSX Parser'
             
        self.exshipper_spearnet_suda_tracking_number_handler_page = '/exshipper/exshipper_spearnet_suda_tracking_number_handler.html'
        self.exshipper_spearnet_suda_tracking_number_handler_page_title = 'ExShipper Spearnet SUDA Tracking Number'
             
        self.exshipper_spearnet_suda_tracking_number_download_page = '/exshipper/exshipper_spearnet_suda_tracking_number_download.html'
        self.exshipper_spearnet_suda_tracking_number_download_page_title = 'SUDA Tracking Number Download'
             
        self.exshipper_spearnet_customer_index_page = '/exshipper/exshipper_spearnet_customer_index.html'
        self.exshipper_spearnet_customer_index_page_title = 'Spearnet Customer Page'
        self.exshipper_spearnet_customer_services_handler_page = '/exshipper/exshipper_spearnet_customer_services.html'
        self.exshipper_spearnet_customer_services_handler_page_title = 'ExShipper Spearnet Customer Services'
             
        self.exshipper_spearnet_customer_package_info_log_page = '/exshipper/exshipper_spearnet_customer_package_info_log.html'
        self.exshipper_spearnet_customer_package_info_log_page_title = 'ExShipper Spearnet Customer Package Information Log'
        
        #general clients
        self.exshipper_general_clients_index_page = '/exshipper/exshipper_general_clients_index.html'
        self.exshipper_general_clients_index_page_title = 'ExShipper Clients Page'
        
        self.exshipper_general_clients_login_page = '/exshipper/exshipper_general_clients_login.html'
        self.exshipper_general_clients_login_page_title = 'General Clients Login'
        
        self.exshipper_general_clients_create_invoice_page = '/exshipper/exshipper_general_clients_create_invoice.html'
        self.exshipper_general_clients_create_invoice_page_title = 'Invoice Log (General Clients)'
        
        self.exshipper_general_clients_track_package_status_page = '/exshipper/exshipper_general_clients_track_package_status.html'
        self.exshipper_general_clients_track_package_status_page_title = 'Track Package Status (General Clients)'
