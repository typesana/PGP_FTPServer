import gnupg
import os


def GPG_GenKey(name_email, passpharse):
    # ---Set GnuPG Home Path---
    gnupg_home = name_email + '/.gnupg'

    # ---Set File Folder---
    try:
        os.mkdir(gnupg_home)
    except:
        pass

    # ---Init GnuPG Object---
    gpg = gnupg.GPG(gnupghome=gnupg_home)
    gpg.encode = 'utf-8'

    # ---Key Settings---
    key_settings = gpg.gen_key_input(
        key_type   = 'RSA',         # 密钥类型
        name_email = name_email,    # 唯一标识符 UID
        passphrase = passpharse,    # 口令
        key_length = 1024           # 密钥长度
    )

    # ---Generate Key Pair---
    key = gpg.gen_key(key_settings)
    # print(key)

    # ---Export Public Key---
    public_key = gpg.export_keys(str(key))
    with open(name_email + '_pub_key.asc', 'w') as f:
        f.write(public_key)
