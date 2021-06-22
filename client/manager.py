import paramiko
import os
from tkinter import *


#SSH
def ssh(cmd, hostname, port, username, password):
    # 创建一个ssh的客户端，用来连接服务器
    ssh = paramiko.SSHClient()
    # 创建一个ssh的白名单
    know_host = paramiko.AutoAddPolicy()
    # 加载创建的白名单
    ssh.set_missing_host_key_policy(know_host)

    # 连接服务器
    ssh.connect(
        hostname=hostname,
        port=port,
        username=username,
        password=password
    )

    # 执行命令
    stdin, stdout, stderr = ssh.exec_command(cmd)
    # stdin  标准格式的输入，是一个写权限的文件对象
    # stdout 标准格式的输出，是一个读权限的文件对象
    # stderr 标准格式的错误，是一个写权限的文件对象
    str = stdout.read().decode()
    ssh.close()
    return str

def get_path(path):
    r=os.path.abspath(path)
    return r

# GUI
class PopupWindows(Toplevel):
    def __init__(self, parent, str):
        super().__init__()
        self.title('数据一览')
        self.parent = parent # 显式地保留父窗口
        dirFrame = Frame(self)
        dirFrame.pack(fill="x")

        scr = Text(dirFrame)
        scr.pack()
        scr.configure(state=NORMAL)
        scr.insert(END, str)
        scr.configure(state=DISABLED)


class Reg(Frame):
    def __init__(self, master):
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
        self.button = Button(frame, text="查看用户", command=self.userInfo)
        self.button.grid(row=4, column=0, sticky=E)
        self.button = Button(frame, text="查看日志", command=self.log)
        self.button.grid(row=4, column=1, sticky=E)

    def userInfo(self):
        ip = self.ent_ip.get()
        port = self.ent_port.get()
        id = self.ent_id.get()
        pwd = self.ent_pwd.get()

        cmd = 'cat ' + get_path('/home/hyb/PGP_FTP/server/ftpsec/userInfo')
        log = ssh(cmd, ip, port, id, pwd)
        PopupWindows(Frame, log)


    def log(self):
        ip = self.ent_ip.get()
        port = self.ent_port.get()
        id = self.ent_id.get()
        pwd = self.ent_pwd.get()

        cmd = 'cat ' + get_path('/home/hyb/PGP_FTP/server/ftpsec/pyftpd.log')
        log = ssh(cmd, ip, port, id, pwd)
        PopupWindows(Frame, log)




root = Tk()
root.title("审计端")
app = Reg(root)
root.mainloop()