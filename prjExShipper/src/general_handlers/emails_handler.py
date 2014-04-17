# -*- coding: utf-8 -*-
'''
Created on Apr 1, 2014

@author: Alan Tai
'''
__author__ = 'Alan Tai'
from app_dict import Key_Value
from google.appengine.api import mail

class Email_Handler():
    def __init__(self):
        pass
    
    def exshipper_send_email(self, receiver, sender, subject, body):
        my_dict = Key_Value()
        result = {'email_status':'unknown'}
        email_host = 'winever.tw@gmail.com'
        if not mail.is_email_valid(receiver):
            result['email_status'] = 'invalid_email'
        else:
            try:
                receiver_email_content = body
                mail.send_mail(email_host, receiver, subject, receiver_email_content)
                sender_email_content = body
                mail.send_mail(email_host, receiver, subject, sender_email_content)
                result['email_status'] = my_dict.email_delivery_status_success
            except:
                result['email_status'] = my_dict.email_delivery_status_fail
        return result