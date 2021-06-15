import gnupg
import os


def GPG_GenKey(headpath, name_email, passpharse, pubkOutPath):
    # ---Set GnuPG Home Path---
    gnupg_home = headpath + name_email + '/.gnupg'

    # ---Set File Folder---
    try:
        os.mkdir(headpath + name_email)
        os.mkdir(gnupg_home)
    except:
        print('GnuPG File Already Existed.')
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
    with open(pubkOutPath, 'w') as f:
        f.write(public_key)


def GPG_Encrypt(gnupghome, plaintext_path, recipient, recipient_pk, enctext_path):
    # Init GnuPG Home Path
    gpg = gnupg.GPG(gnupghome=gnupghome)

    # Init Sender's Key to Sign
    fp = gpg.list_keys(True).fingerprints[0]

    # Import Recipient's Public Key
    key_data = open(recipient_pk).read()
    import_result = gpg.import_keys(key_data)
    gpg.trust_keys(import_result.fingerprints, "TRUST_ULTIMATE")

    # Encrypt the data
    fd = open(plaintext_path, 'rb')
    encrypted_data = gpg.encrypt_file(fd, recipients=[recipient], sign=fp, passphrase='123', output=enctext_path)
    # print(encrypted_data.ok)
    # print(encrypted_data.stderr)

    # Delete Recipient'sPublic Key
    dstatus = gpg.delete_keys(import_result.fingerprints)

    # Return Encrypt Status
    return encrypted_data.ok


def GPG_Decrypt(gnupghome, enctext_path, passphrase, sender_pk, dectext_path):
    # Init GnuPG Home Path
    gpg = gnupg.GPG(gnupghome=gnupghome)

    # Import Sender's Public Key
    key_data = open(sender_pk).read()
    import_result = gpg.import_keys(key_data)
    gpg.trust_keys(import_result.fingerprints, "TRUST_ULTIMATE")

    # Decrypt the data
    fd = open(enctext_path, 'rb')
    decrypted_data = gpg.decrypt_file(fd, passphrase=passphrase, output=dectext_path)

    # Delete Sender's Public Key
    dstatus = gpg.delete_keys(import_result.fingerprints)

    # Return Encrypt Status
    return decrypted_data.ok, decrypted_data.valid, decrypted_data.trust_text


def Alice_Bob_Test():
    # Parameters
    Sender = 'Alice'
    Sender_Passphrase = '123'
    Recipient = 'Bob'
    Recipient_Passphrase = '321'

    # Server: Generate Key Pair
    try:
        os.rmdir('./test')
    except:
        pass
    try:
        os.mkdir('./test')
        os.mkdir('./test/Server')
        fp = open('./test/plaintext', 'w')
        plaintext = "To Bob:\nHello GnuPG!\nSent by Alice"
        fp.write(plaintext)
        fp.close()
        GPG_GenKey(headpath='./test/', name_email='Alice',
                   passpharse='123', pubkOutPath='./test/Server/Alice_pub_key.asc')
        GPG_GenKey(headpath='./test/', name_email='Bob',
                   passpharse='321', pubkOutPath='./test/Server/Bob_pub_key.asc')
    except:
        pass

    # Alice: Encrypt Recipient: Bob
    encStatus = GPG_Encrypt(gnupghome='./test/Alice/.gnupg',
                            recipient='Bob', recipient_pk='./test/Server/Bob_pub_key.asc',
                            plaintext_path='./test/plaintext', enctext_path='./test/plaintext.encrypted'
                            )
    print('Encrypt Status:', encStatus)

    # Bob: Decrypt
    decStatus = GPG_Decrypt(gnupghome='./test/Bob/.gnupg',
                            enctext_path='./test/plaintext.encrypted', dectext_path='./test/plaintext.decrypted',
                            passphrase='321', sender_pk='./test/Server/Alice_pub_key.asc'
                            )
    print('Decrypt Status:', decStatus)


if __name__ == "__main__":
    Alice_Bob_Test()
