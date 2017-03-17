import requests
from HTMLParser import HTMLParser


class loginAndGetName:
    class Parser(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.readyForName = False
            self.login = False
            self.res = ''

        def handle_starttag(self, tag, attrs):
            # print "Encountered a start tag:", tag
            if tag == 'a':
                for attr in attrs:
                    if attr == (u'class', u'pointer icon_menu'):
                        self.readyForName = True

        def handle_endtag(self, tag):
            # print "Encountered an end tag :", tag
            pass

        def handle_data(self, data):
            # print "Encountered some data  :", data
            if self.readyForName:
                self.readyForName = False
                self.login = True
                self.res = data

        def getRes(self):
            return self.login, self.res

    @staticmethod
    def login(username, password):
        headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
        res = requests.post('https://id.tsinghua.edu.cn/do/off/ui/auth/login/post/fa8077873a7a80b1cd6b185d5a796617/0?/j_spring_security_thauth_roaming_entry', data={'i_user': username, 'i_pass': password}, headers=headers)
        return res.text

    def __init__(self):
        pass

    def __call__(self, username, password):
        parser = loginAndGetName.Parser()
        self.u = username
        self.p = password
        parser.feed(loginAndGetName.login(self.u, self.p))
        parser.close()
        return parser.getRes()

loginHelper = loginAndGetName()

if __name__ == '__main__':
    print loginHelper('2013011356', '')