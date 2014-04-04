'''
Created on Jan 25, 2014

@author: Alan Tai
'''

from google.appengine.ext import ndb

    
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
    unit_price_fob_us_dollar = ndb.StringProperty()
    deliver_to = ndb.StringProperty()
    shipper_company = ndb.StringProperty()
    shipper_person = ndb.StringProperty()
    shipper_tel = ndb.StringProperty()
    shipper_address_english = ndb.StringProperty()
    shipper_address_chinese = ndb.StringProperty()
    consignee_name_english = ndb.StringProperty()
    consignee_name_chinese = ndb.StringProperty()
    consignee_tel = ndb.StringProperty()
    consignee_address_english = ndb.StringProperty()
    consignee_address_chinese = ndb.StringProperty()
    company_id_or_personal_id = ndb.StringProperty()
    size_accumulation = ndb.StringProperty()
    declaration_need_or_not = ndb.StringProperty()
    duty_paid_by = ndb.StringProperty()
    package_status = ndb.StringProperty()
    pickup_status = ndb.StringProperty()
    signature_img_id = ndb.StringProperty()
    note = ndb.StringProperty()
    date = ndb.DateProperty(auto_now_add = True)
    update_date_time = ndb.DateTimeProperty(auto_now = True)
#en of package information

#Spearnet packages Info
class SpearnetPackagesInfo(PackageInfo):
    pass
#end of Spearnet packages Info
class GeneralClientsPackagesInfo(PackageInfo):
    pass

#for pre-alert and on-hand documents
class TWCustomEntryInfo(ndb.Model):
    barcode_no = ndb.StringProperty()
    mawb = ndb.StringProperty()
    flight_number = ndb.StringProperty()
    from_whom = ndb.StringProperty()
    to_whom = ndb.StringProperty()
    size = ndb.StructuredProperty(Size, repeated = False)
    weight_kg = ndb.StringProperty()
    ctn = ndb.StringProperty()
    flight_date = ndb.StringProperty()
    note = ndb.StringProperty()
    
class ClientsInfo(ndb.Model):
    name = ndb.StringProperty()
    address = ndb.StringProperty()
    phone = ndb.StringProperty()
    signature_img = ndb.BlobProperty()
    signature_str = ndb.StringProperty()
    date = ndb.DateProperty(auto_now_add = True)
    update_date_time = ndb.DateTimeProperty(auto_now = True)
#end of channel