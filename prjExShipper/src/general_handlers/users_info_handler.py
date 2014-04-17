# -*- coding: utf-8 -*-
'''
Created on Apr 1, 2014

@author: Alan Tai
'''
from app_dict import Key_Value
import string
import random
__author__ = 'Alan Tai'

class Users_Info_Handler():
    def __init__(self):
        pass
    # get users info
    def get_users_info(self, request_handler, users):
        my_dict = Key_Value()
        if users.get_current_user():
            user_account = users.get_current_user()
            url = users.create_logout_url(request_handler.request.uri)
        else:
            user_account = my_dict.unknown_user
            url = users.create_login_url(request_handler.request.uri)
            
        values = {
                  'user_account': user_account,
                  'url': url}
        return values
    
    #id generator
    def generate_random_registration_id(self, size=15, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))  
     
    # end of self-defined functions