#!/usr/bin/python
#-*- coding: UTF-8 -*-

import poplib
import os
import sys
import email
import base64
from email import parser
from time import strftime

class GMailParser(object):

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password
        self.messages = None
        self.mServer = None
        self.dirPath = "./%s" % strftime("%Y-%m-%d %H:%M:%S")
        if os.path.isdir(self.dirPath) == 0:
            os.mkdir(self.dirPath)
        self.mail = {
            'Mail':[]
        }
    def login(self):
        self.mServer = poplib.POP3_SSL('pop.gmail.com', '995')
        print self.mServer.getwelcome()
        self.mServer.user(self.username)
        self.mServer.pass_(self.password)
        numMessages = len(self.mServer.list()[1])
        print "You have %d messages." % (numMessages)

    def getMessage(self):

        self.messages = [self.mServer.retr(i) for i in range(1, len(self.mServer.list()[1]) + 1)]
        self.messages = ["\n".join(mssg[1]) for mssg in self.messages]

    def parseMessage(self):
        i = 0
        for message in self.messages:
            # print message
            path = os.path.join(self.dirPath,str(i))
            msg = email.message_from_string(message)
            subject = ''
            content = ''
            encode = 'None'
            for part in msg.walk():
                if part.has_key('Subject'):
                    subject = part.get('Subject')
                    if subject.find('UTF-8') >0:
                        subject = subject[10:].decode('base64').decode('UTF-8')
                        encode = 'UTF'
                    if subject.find('GBK') >0:
                        subject = subject[8:].decode('base64').decode('gbk')
                        encode = 'GBK'
                if part.get_content_type() == 'text/plain' and part.get_filename() == None:
                    if encode == 'GBK':
                        content= part.get_payload(decode=True).decode('gbk')
                    elif encode == 'UTF':
                        content= part.get_payload(decode=True).decode('utf8')
                    else:
                        content= part.get_payload(decode=True)

                if part.get_filename() != None:
                    if os.path.isdir(path) == 0:
                        os.mkdir(path)
                    fp = open(path+'/%s' %part.get_filename(), 'wb')
                    fp.write(part.get_payload(decode=1))
                    fp.close()
            text = """%s\n%s"""%(subject.encode('utf8'),content.encode('utf8'))
            fp = open(path+'/mail.txt', 'wb')
            fp.write(text)
            fp.close()        
            i += 1

    def quit(self):
        self.mServer.quit()
if __name__ == "__main__":
    r = GMailParser('YourAccount@gmail.com','YourPassword')
    r.login()
    r.getMessage()
    r.parseMessage()





