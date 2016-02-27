import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import requests
import urllib
import getpass
import warnings
warnings.filterwarnings("ignore")

def check_user(target_user):
    result = requests.get(target_user,  auth=('desdm-ro', 'matias'))
    return result.status_code

def check_password(target_pass, xml_request):
    headers={'Content-Type': 'application/xml'}
    result = requests.post(target_pass,  auth=('desdm-ro', 'matias'), data=xml_request, headers=headers)
    return result.status_code

class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        return self.get_secure_cookie("user")

class AuthLoginHandler(BaseHandler):
    def get(self):
        try:
            errormessage = self.get_argument("error")
            print(errormessage)
        except:
            errormessage = ""
        try:
            next_url = self.get_argument("next")
            print(next_url)
            #self.redirect(next_url)
        except:
            pass
            
        self.render("login.html", errormessage=errormessage)

    def check_permission(self, password, user):
        target_pass = "https://opensource.ncsa.illinois.edu/crowd/rest/usermanagement/latest/authentication?username=%s" % user
        target_user = "https://opensource.ncsa.illinois.edu/crowd/rest/usermanagement/latest/user?username=%s" % user
        xml_request = """<?xml version="1.0" encoding="UTF-8"?><password><value>%s</value></password>""" % password
        temp1=check_user(target_user)
        if temp1==200:
            temp2=check_password(target_pass, xml_request )
            if temp2 == 200:
                return True, ""
            else:
                return False, "Incorrect user/password"
        else:
            return False, "User does not exist"


    def post(self):
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")
        nxt = self.get_argument("next")
        auth, err = self.check_permission(password, username)
        if auth:
            self.set_current_user(username, password)
            self.redirect(self.get_argument("next"))
            #self.redirect("/internal")
            #next_msg = u"?next=" + tornado.escape.url_escape(err)
            #self.redirect(u"/auth/login/" + error_msg)
            #return
            #self.set_status(200)
            #self.flush()
            #self.finish()
            #self.render("index.html")
            #print('so?')
        else:
            error_msg = u"?error=" + tornado.escape.url_escape(err) + "&next=" + tornado.escape.url_escape(nxt) 
            self.redirect(u"/auth/login/" + error_msg)

    def set_current_user(self, user, passwd):
        if user:
            self.set_secure_cookie("user", tornado.escape.json_encode(user))
            self.set_secure_cookie("pass", tornado.escape.json_encode(passwd))
        else:
            self.clear_cookie("user")
            self.clear_cookie("pass")


class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.clear_cookie("pass")
        self.redirect(self.get_argument("next", "/"))



