import os
import shutil
import sys

def quick_start(file_userInfo, file_pem):
    try:
        os.mkdir('./ftproot')
        os.mkdir('./ftpsec')
        fp = open(file_userInfo, 'r')
        for i in fp.readlines():
            s = i[:-1].split(',')
            if s != ['']:
                os.mkdir('./ftproot/' + s[0])
        fp.close()
        shutil.copyfile(file_userInfo, './ftpsec/userInfo')
        shutil.copyfile(file_pem, './ftpsec/keycertFTP.pem')
        os.mkdir('./ftproot/.pubkring/')
    except:
        print('Error')


if __name__=='__main__':
    quick_start('./userInfo', './keycertFTP.pem')
