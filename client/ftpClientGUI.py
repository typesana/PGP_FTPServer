from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import ftpClient

# PGP_FTP_sendFile(self, filePath, pubkPath, recipient)
class PopupUpload(Toplevel):
    def __init__(self, parent, ftp, username):
        super().__init__()
        self.username = username
        self.title('上传文件')
        self.parent = parent # 显式地保留父窗口
        frame = Frame(self)
        frame.pack()
        # 待上传文件路径
        self.lab_fp = Label(frame, text="上传文件路径:")
        self.lab_fp.pack()
        self.ent_fp = Entry(frame)
        self.ent_fp.pack()
        # 接收方
        self.lab_rn = Label(frame, text="接收方:")
        self.lab_rn.pack()
        self.ent_rn = Entry(frame)
        self.ent_rn.pack()
        # 输入口令
        self.lab_pp = Label(frame, text="口令:")
        self.lab_pp.pack()
        self.ent_pp = Entry(frame)
        self.ent_pp.pack()
        # 按钮
        self.button = Button(frame, text="上传文件", command=self.upload)
        self.button.pack()
        self.lab_status = Label(frame, text="")
        self.lab_status.pack()

    def upload(self):
        filePath = self.ent_fp.get()
        rname = self.ent_rn.get()
        pubkPath = './' + self.username + '/' + rname + '_pub_key.asc'
        passphrase = self.ent_pp.get()
        try:
            ftp.PGP_FTP_sendFile(filePath, pubkPath, rname, passphrase)
            self.lab_status.configure(fg='green')
            self.lab_status["text"] = "Good"
        except:
            self.lab_status.configure(fg='red')
            self.lab_status["text"] = "Bad"


# PGP_FTP_downloadFile(self, pubkPath, sender, filename, passphrase):
class PopupDownload(Toplevel):
    def __init__(self, parent, ftp, username):
        super().__init__()
        self.username = username
        self.title('下载文件')
        self.parent = parent  # 显式地保留父窗口
        frame = Frame(self)
        frame.pack()
        # 待上传文件路径
        self.lab_fp = Label(frame, text="下载文件:")
        self.lab_fp.pack()
        self.ent_fp = Entry(frame)
        self.ent_fp.pack()
        # 发送方
        self.lab_rn = Label(frame, text="发送人:")
        self.lab_rn.pack()
        self.ent_rn = Entry(frame)
        self.ent_rn.pack()
        # 输入口令
        self.lab_pp = Label(frame, text="口令:")
        self.lab_pp.pack()
        self.ent_pp = Entry(frame)
        self.ent_pp.pack()
        # 按钮
        self.button = Button(frame, text="下载文件", command=self.download)
        self.button.pack()
        # 输入口令
        self.lab_de = Label(frame, text="解密结果:")
        self.lab_de.pack()
        # 消息读取
        self.scr = Text(frame, relief='sunken', bd=3)
        self.scr.pack()
        self.scr.configure(state=DISABLED)


    def download(self):
        filePath = self.ent_fp.get()
        rname = self.ent_rn.get()
        pubkPath = './' + self.username + '/' + rname + '_pub_key.asc'
        passphrase = self.ent_pp.get()
        try:
            ok, valid, trust_text = ftp.PGP_FTP_downloadFile(pubkPath, rname, filePath, passphrase)
            self.scr.configure(state=NORMAL)
            res = open('./' + self.username + '/' + filePath + '.decrypted').read()
            if valid:
                self.scr.delete(1.0, END)
                self.scr.insert(END, res)
                self.scr.configure(fg='black')
                self.scr.configure(state=DISABLED)
            else:
                self.scr.delete(1.0, END)
                self.scr.insert(END, res+'\n(Sender Signature Invalid)')
                self.scr.configure(fg='red')
                self.scr.configure(state=DISABLED)
        except:
            self.scr.configure(state=NORMAL)
            self.scr.delete(1.0, END)
            self.scr.insert(END, "Download or Decrypte Error!")
            self.scr.configure(fg='red')
            self.scr.configure(state=DISABLED)



class PopupGenKey(Toplevel):
    def __init__(self, parent, ftp, username):
        super().__init__()
        self.username = username
        self.title('生成密钥')
        self.parent = parent # 显式地保留父窗口
        frame = Frame(self)
        frame.pack()
        # 提示
        self.lab_conn = Label(frame, text="这会覆盖你之前的密钥，导致之前的文件无法解密。请谨慎！")
        self.lab_conn.pack()
        # 输入口令
        self.lab_pp = Label(frame, text="Passphrase(口令):")
        self.lab_pp.pack()
        self.ent_pp = Entry(frame)
        self.ent_pp.pack()
        # 按钮
        self.button = Button(frame, text="生成新的密钥", command=self.genKey)
        self.button.pack()

    def genKey(self):
        print(self.username)
        print(self.ent_pp.get())
        pubkPath = './'+ self.username +'/'+ self.username + '_pub_key.asc'
        ftp.PGP_GenKey(headpath='./',
                       name_email=self.username,
                       passphrase=self.ent_pp.get(),
                       pubkOutPath=pubkPath
                       )
        ftp.PGP_FTP_uploadPublicKey(pubkPath=pubkPath)

class PopupFTPDir(Toplevel):
    def __init__(self, parent, ftp):
        super().__init__()
        self.title('文件一览')
        self.parent = parent # 显式地保留父窗口
        dirFrame = Frame(self)
        dirFrame.pack(fill="x")

        scr = Text(dirFrame)
        scr.pack()
        scr.configure(state=NORMAL)
        dir = ""
        for i in ftp.FTP_GetDir('.'):
            scr.insert("end", i + '\n')
        print(dir)
        scr.configure(state=DISABLED)

class PopupFTP(Toplevel):
    def __init__(self, parent, ftp, username):
        super().__init__()
        self.username = username
        self.title('FTP 操作界面')
        self.parent = parent # 显式地保留父窗口
        frame = Frame(self)
        frame.pack()
        self.lab_conn = Label(frame, text="Hello, "+username)
        self.lab_conn.pack()
        self.button1 = Button(frame, text="查看目录", width=30, command=self.showDir)
        self.button1.pack()
        self.button2 = Button(frame, text="生成密钥", width=30, command=self.showGenKey)
        self.button2.pack()
        self.button3 = Button(frame, text="下载文件", width=30, command=self.showDownload)
        self.button3.pack()
        self.button4 = Button(frame, text="上传文件", width=30, command=self.showUpload)
        self.button4.pack()

    def showDir(self):
        PopupFTPDir(Toplevel, ftp)

    def showUpload(self):
        PopupUpload(Toplevel, ftp, self.username)

    def showDownload(self):
        PopupDownload(Toplevel, ftp, self.username)

    def showGenKey(self):
        PopupGenKey(Toplevel, ftp, self.username)


class Reg(Frame):
    def __init__(self, master, ftp):
        frame = Frame(master)
        frame.pack()
        self.lab_ip = Label(frame, text="IP :")
        self.lab_ip.grid(row=0, column=0, sticky=E)
        self.ent_ip = Entry(frame)
        self.ent_ip.grid(row=0, column=1, sticky=E)
        self.lab_port = Label(frame, text="端口:")
        self.lab_port.grid(row=1, column=0, sticky=E)
        self.ent_port = Entry(frame)
        self.ent_port.grid(row=1, column=1, sticky=E)
        self.lab_id = Label(frame, text="账户:")
        self.lab_id.grid(row=2, column=0, sticky=E)
        self.ent_id = Entry(frame)
        self.ent_id.grid(row=2, column=1, sticky=E)
        self.lab_pwd = Label(frame, text="密码:")
        self.lab_pwd.grid(row=3, column=0, sticky=E)
        self.ent_pwd = Entry(frame, show="*")
        self.ent_pwd.grid(row=3, column=1, sticky=E)
        self.button = Button(frame, text="登录", command=self.Submit)
        self.button.grid(row=4, column=0, sticky=E)
        self.lab_conn = Label(frame, text="")
        self.lab_conn.grid(row=4, column=1, sticky=E)
        self.lab_login = Label(frame, text="")
        self.lab_login.grid(row=5, column=1, sticky=E)

        self.ftp = ftp

    def Submit(self):
        ip = self.ent_ip.get()
        port = self.ent_port.get()
        id = self.ent_id.get()
        pwd = self.ent_pwd.get()

        # 连接
        if port != '':
            port_int = int(port)
        else:
            return False

        conn = ftp.FTP_Connect(ip, port_int)
        if conn:
            self.lab_conn["text"] = "连接成功"
        else:
            self.lab_conn["text"] = "连接失败"
            return False

        # 登陆
        logInStatus = ftp.FTP_Login(id, pwd)
        if logInStatus:
            self.lab_login["text"] = "登陆成功"
        else:
            self.lab_login["text"] = "登陆失败"
            return False

        # print(ftp.FTP_GetDir('.'))
        pw = PopupFTP(Frame, ftp, id)

        self.ent_ip.delete(0, len(ip))
        self.ent_port.delete(0, len(port))
        self.ent_id.delete(0, len(id))
        self.ent_pwd.delete(0, len(pwd))


ftp = ftpClient.FTPClient()
root = Tk()
root.title("用户登录")
app = Reg(root, ftp)
root.mainloop()
