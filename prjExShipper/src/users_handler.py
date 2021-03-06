# -*- coding: utf-8 -*-
'''
Created on Apr 1, 2014

@author: Alan Tai
'''
from app_dict import Key_Value
__author__ = 'Alan Tai'

class Users_Handler():
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