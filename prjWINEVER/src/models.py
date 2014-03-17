'''
Created on Jan 25, 2014

@author: Alan Tai
'''

from google.appengine.ext import ndb

    
#invoice model
class Size(ndb.Model):
    length = ndb.StringProperty()
    width = ndb.StringProperty()
    height = ndb.StringProperty()

class InvoiceInfo(ndb.Model):
    yamato_tr_number = ndb.StringProperty()
    ref_number = ndb.StringProperty()
    shipper = ndb.StringProperty()
    consignee_english = ndb.StringProperty()
    consignee_chinese = ndb.StringProperty()
    address = ndb.StringProperty(indexed = False)
    consignee_phone_number = ndb.StringProperty()
    
    size = ndb.StructuredProperty(Size, repeated = False)
    weight = ndb.StringProperty()
    
    date_time = ndb.DateTimeProperty(auto_now_add = True)
    update_date_time = ndb.DateTimeProperty(auto_now = True)
#end of invoice model

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
#end of tracking number basic class

#SUDA tracking number
class SUDATrackingNumber_REGULAR(TrackingNumber):
    pass
#end if SUDA tracking number


#package information
class PackageInfo(ndb.Model):
    index = ndb.StringProperty()
    barcode_no  = ndb.StringProperty()
    hawb = ndb.StringProperty()
    ctn = ndb.StringProperty()
    weight_kg = ndb.StringProperty() #g/w(kg)
    weight_lb = ndb.StringProperty()
    commodity_name = ndb.JsonProperty()
    pcs = ndb.StringProperty()
    unit = ndb.StringProperty()
    original = ndb.StringProperty()
    unit_price_fob_us_dollar = ndb.StringProperty()
    deliver_to = ndb.StringProperty()
    shipper_name = ndb.StringProperty()
    shipper_person = ndb.StringProperty()
    shipper_tel = ndb.StringProperty()
    shipper_address_english = ndb.StringProperty()
    shipper_address_chinese = ndb.StringProperty()
    consignee_english_name = ndb.StringProperty()
    consignee_chinese_name = ndb.StringProperty()
    consignee_tel = ndb.StringProperty()
    consignee_address_english = ndb.StringProperty()
    consignee_address_chinese = ndb.StringProperty()
    company_id_or_personal_id = ndb.StringProperty()
    remark = ndb.StringProperty()
    declaration_need_or_not = ndb.StringProperty()
    duty_paid_by = ndb.StringProperty()
    package_status = ndb.StringProperty()
    pickup_status = ndb.StringProperty()
    signature_img = ndb.BlobProperty()
    date = ndb.DateProperty(auto_now_add = True)
    shipping_date = ndb.StringProperty()
    update_date_time = ndb.DateTimeProperty(auto_now = True)
#en of package information

#Spearnet packages Info
class SpearnetPackagesInfo(PackageInfo):
    pass
#end of Spearnet packages Info


#end of channel