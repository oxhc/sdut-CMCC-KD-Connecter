import requests
import os
import pickle
import json

class Connecter:
    def __init__(self, name : str, passwd : str):
        self.name = name
        self.passwd = passwd
        self.isLogin = False
        self.client = requests.session()
        
    def login(self):
        if self.isLogin == True:
            print('[error] You already in')
            return
        oj_url = 'http://acm.sdut.edu.cn/onlinejudge2'
        redirectUrl = self.client.get(oj_url)
        redirectUrl = redirectUrl.url
        if redirectUrl != oj_url:
            data = {
                'web-auth-user':self.name,
                'web-auth-password':self.passwd,
                'remember-credentials':'false',
                'redirect-url':redirectUrl
            }
            rootUrl = redirectUrl.split('?')
            page = self.client.post(rootUrl[0]+'/web/connect', data)
            self.sessionId = json.loads(page.text)['session']['context']
            self.isLogin = True
            print('[info] Log in CMCC-KD successfully')
        else:
            print('[error] It doesnt redirct to the correct url. Please try again.')
    
    def logout(self):
        if self.isLogin == False:
            print('[error] You have not logged in yet!')
            return
        data = {
            'context':self.sessionId
        }
        self.client.post('http://223.99.141.139:10088/web/disconnect',data)
        self.isLogin = False
        print('Log out successfully')

if __name__ == '__main__':
    if os.path.isfile('user.json'):
        userfile = open('user.json','r')
        filecontent = userfile.read()
        data = json.loads(filecontent)
        user = data['user']
        passwd = data['passwd']
        userfile.close

    else:
        print('CMCC-KD Connecter\n ------- \n')
        user = input('Please input phone number:')
        passwd = input('Please input password:')
        data = {
            'user':user,
            'passwd':passwd
        }
        userfile = open('user.json','w')
        userfile.write(json.dumps(data))
        userfile.close()
    c = Connecter(user,passwd)
    os.system('cls')
    while True:
        print('CMCC-KD Connecter')
        cmd = input('\nPlease type your command:\n1.Log in(Enter)\n2.Log out\n3.Exit\n')
        if cmd == '' or cmd == '1':
            os.system('cls')
            c.login()
            tempFile = open('tempFile.dat','w')
            tempFile.write(c.sessionId)
            tempFile.close()
        elif cmd == '2':
            os.system('cls')
            if os.path.isfile('tempFile.dat'):
                tempFile = open('tempFile.dat','r')
                c.sessionId = tempFile.read()
                tempFile.close()
                c.isLogin = True
                os.remove('tempFile.dat')
            c.logout()
        elif cmd == '3':
            break
        else:
            os.system('cls')
            print('[error] Command error')
        