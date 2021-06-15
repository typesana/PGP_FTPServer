# coding:utf-8
from ftplib import FTP, FTP_TLS
import sys
from pgp import GPG_GenKey, GPG_Decrypt, GPG_Encrypt

class FTPClient():
    def __init__(self):
        self.ftp = FTP_TLS()

    # ----------FTP Module----------
    def FTP_Connect(self, ip, port):
        try:
            self.ftp.connect(ip, port)
            return True
        except:
            print('Connection refused')
            return False

    def FTP_Login(self, username, password):
        try:
            self.ftp.login(username, password)
            self.ftp.prot_p()
            self.username = username
            return True
        except:
            print('Authentication failed')
            return False

    def FTP_DeleteFile(self, filename):
        try:
            self.ftp.delete('./' + self.username + '/' + filename)
            return True
        except:
            return False

    def FTP_GetDir(self, path):
        path = './' + self.username + '/' + path
        try:
            dir_res = []
            self.ftp.dir(path, dir_res.append)
            return dir_res
        except:
            return None

    # ----------PGP Module (Keys)----------
    def PGP_GenKey(self, headpath, name_email, passphrase, pubkOutPath):
        GPG_GenKey(headpath=headpath, name_email=name_email, passpharse=passphrase, pubkOutPath=pubkOutPath)

    # ----------PGP_FTP Module----------
    # PGP Public Key Upload
    def PGP_FTP_uploadPublicKey(self, pubkPath):
        file_handle = open(pubkPath, "rb")
        filename = pubkPath.split('/')[-1]
        res = self.ftp.storbinary("STOR ./.pubkring/" + filename, file_handle, 1024)
        if res.find('226') != -1:
            file_handle.close()
            return True
        file_handle.close()
        return False

    # Encrypted File & Upload to the destination
    def PGP_FTP_sendFile(self, filePath, pubkPath, recipient):
        # Step1: Get Public Key
        file_handle = open(pubkPath, 'wb')
        RecipentPK = recipient + '_pub_key.asc'
        self.ftp.retrbinary("RETR ./.pubkring/"+RecipentPK, file_handle.write)
        file_handle.close()

        # Step2: Encrypt
        GPG_Encrypt(gnupghome='./'+self.username+'/.gnupg', plaintext_path=filePath,
                    recipient=recipient, recipient_pk=pubkPath,
                    enctext_path=filePath+'.encrypted'
                    )

        # Step3: Upload Encrypted File
        encPath = filePath+'.encrypted'
        filename = encPath.split('/')[-1]
        file_handle = open(filePath+'.encrypted', 'rb')
        res = self.ftp.storbinary("STOR ./" + recipient + '/' + filename, file_handle, 1024)
        if res.find('226') != -1:
            file_handle.close()
            return True
        file_handle.close()
        return False


    # Download File & Decrypted
    def PGP_FTP_downloadFile(self, pubkPath, sender, filename, passphrase):
        # Step1: Get Public Key
        file_handle = open(pubkPath, 'wb')
        senderPK = sender + '_pub_key.asc'
        self.ftp.retrbinary("RETR ./.pubkring/" + senderPK, file_handle.write)
        file_handle.close()

        # Step2: Get File
        encPath = './'+self.username+'/'+filename
        file_handle = open(encPath, 'wb')
        self.ftp.retrbinary("RETR ./" + self.username + "/" + filename, file_handle.write)
        file_handle.close()

        # Step3: Decrypt
        GPG_Decrypt(gnupghome='./' + self.username + '/.gnupg', enctext_path=encPath,
                    passphrase=passphrase, sender_pk=pubkPath,
                    dectext_path=encPath+'.decrypted')


def test():
    ftp = FTP_TLS()
    # ftp.set_debuglevel(2)  # 打开调试级别2，显示详细信息
    ftp.connect("127.0.0.1", 2121)  # 连接的ftp sever和端口
    ftp.login("admin", "password")  # 连接的用户名，密码
    print(ftp.getwelcome())  # 打印出欢迎信息

    ftp.dir()
    try:
        print(ftp.nlst('Alice'))
    except:
        print('No perm')

    print(ftp.nlst('Bob'))

    file_handle = open("/Users/hyb/PycharmProjects/pyftp/test", "rb")  # 以写模式在本地打开文件
    ftp.nlst()
    res = ftp.storbinary("STOR 123", file_handle, 1024)  # 上传目标文件
    if res.find('226') != -1:
        print('upload file complete')

    print("ok!")

def UnitTest_admin_login(ip, port):
    ftpClient = FTPClient()
    connStatus = ftpClient.FTP_Connect(ip, port)
    logStatus = ftpClient.FTP_Login('admin', 'password')
    return connStatus & logStatus

def UnitTest_user_login():
    ftpClient = FTPClient()
    connStatus = ftpClient.FTP_Connect("127.0.0.1", 2121)
    logStatus = ftpClient.FTP_Login('Alice', '123')
    return connStatus & logStatus

def UnitTest_deleteFile():
    ftpClient = FTPClient()
    connStatus = ftpClient.FTP_Connect("127.0.0.1", 2121)
    logStatus = ftpClient.FTP_Login('Alice', '123')
    print(ftpClient.FTP_DeleteFile('123'))
    print(ftpClient.FTP_DeleteFile('132'))

def UnitTest_getDir():
    ftpClient = FTPClient()
    connStatus = ftpClient.FTP_Connect("127.0.0.1", 2121)
    logStatus = ftpClient.FTP_Login('Alice', '123')
    return ftpClient.FTP_GetDir('.')

def UnitTest_genKey():
    ftpClient = FTPClient()
    connStatus = ftpClient.FTP_Connect("127.0.0.1", 2121)
    logStatus = ftpClient.FTP_Login('Alice', '123')
    ftpClient.PGP_GenKey(headpath='./', name_email='Alice',
                         passphrase='123', pubkOutPath='./Alice/Alice_pub_key.asc')

def UnitTest_UploadPK(ip, port):
    ftpClient = FTPClient()
    connStatus = ftpClient.FTP_Connect(ip, port)
    logStatus = ftpClient.FTP_Login('Alice', '123')
    ftpClient.PGP_GenKey(headpath='./', name_email='Alice',
                         passphrase='123', pubkOutPath='./Alice/Alice_pub_key.asc')
    ftpClient.PGP_FTP_uploadPublicKey(pubkPath='./Alice/Alice_pub_key.asc')

def UnitTest_Encrypt(ip, port):
    ftpClient = FTPClient()
    connStatus = ftpClient.FTP_Connect(ip, port)
    logStatus = ftpClient.FTP_Login('Bob', '234')
    ftpClient.PGP_GenKey(headpath='./', name_email='Bob',
                         passphrase='123', pubkOutPath='./Bob/Bob_pub_key.asc')
    ftpClient.PGP_FTP_uploadPublicKey(pubkPath='./Bob/Bob_pub_key.asc')
    ftpClient.PGP_FTP_sendFile(filePath='client.py', pubkPath='./Bob/Alice_pub_key.asc', recipient='Alice')

def UnitTest_Decrypt(ip, port):
    ftpClient = FTPClient()
    connStatus = ftpClient.FTP_Connect(ip, port)
    logStatus = ftpClient.FTP_Login('Alice', '123')
    ftpClient.PGP_FTP_downloadFile(pubkPath='./Alice/Bob_pub_key.asc', sender='Bob',
                                   filename='client.py.encrypted', passphrase='123')

if __name__ == "__main__":
    UnitTest_admin_login(sys.argv[1], int(sys.argv[2]))
    #UnitTest_UploadPK("192.168.142.99", 2121)
    #UnitTest_Encrypt("192.168.142.99", 2121)
    #UnitTest_Decrypt("192.168.142.99", 2121)