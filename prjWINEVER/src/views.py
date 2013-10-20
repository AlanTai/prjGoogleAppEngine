#-*- coding: utf-8 -*-

import webapp2
import jinja2
import os
from google.appengine.api import users

jinja_environment = jinja2.Environment(loader = jinja2.FileSystemLoader(os.path.dirname(__file__)+'/static/templates'))

class ExWINE(webapp2.RequestHandler):
    def get(self):
        if users.get_current_user():
            user_account = users.get_current_user()
            url = users.create_logout_url(self.request.uri)
            url_linktxt = 'Logout'
        else:
            user_account = 'Unknown_User'
            url = users.create_login_url(self.request.uri)
            url_linktxt = 'Login'
            
        template_values = {
                           'title' : 'ExWINE',
                           'user_account': user_account,
                           'url': url,
                           'url_linktxt': url_linktxt}
        
        template = jinja_environment.get_template('exwine_index_2.html')
        self.response.out.write(template.render( template_values))
        
class InfoPageDispatcher(webapp2.RedirectHandler):
    
    def get(self):
        
        if users.get_current_user():
            user_account = users.get_current_user()
            url = users.create_logout_url(self.request.uri)
            url_linktxt = 'Logout'
        else:
            user_account = 'Unknown_User'
            url = users.create_login_url(self.request.uri)
            url_linktxt = 'Login'
        
        info_page = 'exwine_index_2.html'
        title_page = 'ExWINE'
        request_page = self.request.get('info_page_request')
        if request_page:
            if request_page == 'services':
                info_page = 'exwine_info_services.html'
                title_page = 'ExWINE Service'
                
            elif request_page == 'logistics':
                info_page = 'exwine_info_logistics.html'
                title_page = 'ExWINE Logistics'
                
            elif request_page == 'logistics_requirement':
                info_page = 'exwine_info_logistics_requirement.html'
                title_page = 'ExWINE Logistics Requirement'
                
            elif request_page == 'question_answer':
                info_page = 'exwine_info_question_answer.html'
                title_page = 'ExWINE Question & Answer'
            
        template_values = {'title': title_page,
                           'user_account': user_account,
                           'url': url,
                           'url_linktxt': url_linktxt }
        
        template = jinja_environment.get_template(info_page)
        self.response.out.write(template.render(template_values))
        
        
app = webapp2.WSGIApplication([('/exwine', ExWINE), ('/info_page_dispatcher',InfoPageDispatcher)], debug=True)