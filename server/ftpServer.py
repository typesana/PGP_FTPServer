import os
import sys

import logging
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.handlers import TLS_FTPHandler
from pyftpdlib.servers import ThreadedFTPServer

class ftp_server:
   def add_user_from_file(self, userInfoFile):
       fp = open(userInfoFile, 'r')
       usr = []
       for i in fp.readlines():
           s = i[:-1].split(',')
           if s != ['']:
               usr.append(s)
               self.authorizer.add_user(s[0], s[1], './ftproot/', perm='elradfmwM')
       for user in usr:
           for other in usr:
               if user[0] != other[0]:
                   self.authorizer.override_perm(user[0],  './ftproot/'+other[0], perm='w')

   def __init__(self):
       self.authorizer = DummyAuthorizer()
       self.authorizer.add_user('admin', 'password', './ftproot/', perm='elradfmwM')
       self.add_user_from_file('./ftpsec/userInfo')
       # print(self.authorizer.user_table)

   def run(self, ip, port):
       self.handler = TLS_FTPHandler
       self.handler.authorizer = self.authorizer
       logging.basicConfig(filename='./ftpsec/pyftpd.log',
                           level=logging.INFO,
                           format="%(asctime)s - %(levelname)-8s - %(name)s.%(funcName)s - %(message)s")
       self.handler.certfile = './ftpsec/keycertFTP.pem'
       self.handler.tls_data_required = True
       self.address = (ip, port)
       self.server = ThreadedFTPServer(self.address, self.handler)
       print("Service Start On: ", ip, ":", port)
       self.server.serve_forever()


if __name__=='__main__':
    this_ftp = ftp_server()
    print(sys.argv[1], sys.argv[2])
    this_ftp.run(sys.argv[1], sys.argv[2])

