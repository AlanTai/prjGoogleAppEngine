# -*- coding: utf-8 -*-
'''
Created on Jan 25, 2014

@author: Alan Tai
'''
from google.appengine.ext import ndb
from google.appengine.ext.ndb.model import JsonProperty

    
#employee
class PersonInfo(ndb.Model):
    id = ndb.StringProperty()
    account_name = ndb.StringProperty()
    password = ndb.StringProperty()
    
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    birthday = ndb.DateProperty()
    gender = ndb.StringProperty()
    address = ndb.StringProperty()
    phone_number = ndb.StringProperty()
    email = ndb.StringProperty()
    google_account = ndb.StringProperty()
    profile_img = ndb.BlobProperty()
    
    create_date_time = ndb.DateTimeProperty(auto_now_add = True)
    update_date_time = ndb.DateTimeProperty(auto_now = True)

class EmployeeInfo(PersonInfo):
    job_title = ndb.StringProperty()
    access_level = ndb.StringProperty()
    
class ClientsInfo(PersonInfo):
    company_name = ndb.StringProperty()
    signature_img = ndb.BlobProperty()
    signature_str = ndb.StringProperty()
    membership_level = ndb.StringProperty()
    
    
class EmailVerification(ndb.Model):
    email = ndb.StringProperty()
    verification_code = ndb.StringProperty()
    
#end of person information
    
#tracking number basic class
class TrackingNumber(ndb.Model):
    tracking_number = ndb.StringProperty()
    used_mark = ndb.StringProperty()
    date_time = ndb.DateTimeProperty(auto_now_add = True)
    update_date_time = ndb.DateTimeProperty(auto_now = True)
#end of tracking number basic class

#tracking number basic class
class TWCustomEntryTrackingNumber(TrackingNumber):
    pass

#SUDA tracking number
class SUDATrackingNumber_REGULAR(TrackingNumber):
    pass

class SUDATrackingNumber_FORMAL(TrackingNumber):
    pass
#end if SUDA tracking number


#package information

#invoice model
class Size(ndb.Model):
    length = ndb.StringProperty()
    width = ndb.StringProperty()
    height = ndb.StringProperty()


class PackageInfo(ndb.Model):
    reference_number = ndb.StringProperty()
    tw_custom_entry_number  = ndb.StringProperty()
    hawb = ndb.StringProperty()
    ctn = ndb.StringProperty()
    size = ndb.StructuredProperty(Size, repeated = False)
    weight_kg = ndb.StringProperty()
    weight_lb = ndb.StringProperty()
    commodity_detail = ndb.JsonProperty()
    pcs = ndb.StringProperty()
    unit = ndb.StringProperty()
    original = ndb.StringProperty()
    deliver_to = ndb.StringProperty()
    unit_price_fob_us_dollar = ndb.StringProperty()
    
    shipper_company = ndb.StringProperty()
    shipper_person = ndb.StringProperty()
    shipper_tel = ndb.StringProperty()
    shipper_address_english = ndb.StringProperty()
    shipper_address_chinese = ndb.StringProperty()
    
    consignee_tel = ndb.StringProperty()
    consignee_name_english = ndb.StringProperty()
    consignee_name_chinese = ndb.StringProperty()
    consignee_address_english = ndb.StringProperty()
    consignee_address_chinese = ndb.StringProperty()
    
    company_id_or_personal_id = ndb.StringProperty()
    size_accumulation = ndb.StringProperty()
    declaration_need_or_not = ndb.StringProperty()
    duty_paid_by = ndb.StringProperty()
    signature_img_id = ndb.StringProperty()
    note = ndb.StringProperty()
    
    package_status = ndb.StringProperty()
    pickup_date_time = ndb.DateTimeProperty()
    
    access_info = JsonProperty()
    create_date_time = ndb.DateTimeProperty(auto_now_add = True)
    update_date_time = ndb.DateTimeProperty(auto_now = True)
#en of package information

#Spearnet packages Info
class SpearnetPackagesInfo(PackageInfo):
    pass
#end of Spearnet packages Info
class GeneralClientsPackagesInfo(PackageInfo):
    pass

class PackagsInfoLog(PackageInfo):
    original_create_date_time = ndb.DateTimeProperty()
    original_update_date_time = ndb.DateTimeProperty()

class SpearnetPackagesInfoLog(PackagsInfoLog):
    pass

class GeneralClientsPackagesInfoLog(PackagsInfoLog):
    pass

#for pre-alert and on-hand documents
class TWCustomEntryInfo(ndb.Model):
    barcode_number = ndb.StringProperty()
    mawb = ndb.StringProperty()
    
    sender = ndb.StringProperty()
    receiver = ndb.StringProperty()
    size = ndb.StructuredProperty(Size, repeated = False)
    weight_kg = ndb.StringProperty()
    ctn = ndb.StringProperty()
    note = ndb.StringProperty()
    
    flight_number = ndb.StringProperty()
    flight_date = ndb.DateProperty()
    package_status = ndb.StringProperty()
    access_info = JsonProperty()
    
    create_date_time = ndb.DateProperty(auto_now_add = True)
    update_date_time = ndb.DateTimeProperty(auto_now = True)
    
class PackageStatusNotification(ndb.Model):
    tracking_number = ndb.StringProperty()
    package_status = ndb.StringProperty()
    create_date_time = ndb.DateProperty(auto_now_add = True)
    update_date_time = ndb.DateTimeProperty(auto_now = True)
    
class PackageStatusNotification_Email(PackageStatusNotification):
    email = ndb.StringProperty()
    receiver_name = ndb.StringProperty()
    