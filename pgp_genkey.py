import gnupg
import os


def GPG_GenKey(name_email, passpharse):
    # ---Set GnuPG Home Path---
    gnupg_home = './' + name_email + '/.gnupg'

    # ---Set File Folder---
    try:
        os.mkdir('./' + name_email)
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
    with open('./Server/' + name_email + '_pub_key.asc', 'w') as f:
        f.write(public_key)


def GPG_Encrypt(gnupghome, plaintext_path, recipient, recipient_pk, enctext_path):
    # Init GnuPG Home Path
    gpg = gnupg.GPG(gnupghome=gnupghome)

    # Import Recipient's Public Key
    key_data = open(recipient_pk).read()
    import_result = gpg.import_keys(key_data)
    gpg.trust_keys(import_result.fingerprints, "TRUST_ULTIMATE")

    # Encrypt the data
    fd = open(plaintext_path, 'rb')
    encrypted_data = gpg.encrypt_file(fd, recipients=[recipient], output=enctext_path)
    # print(encrypted_data.ok)
    # print(encrypted_data.stderr)

    # Delete Recipient'sPublic Key
    dstatus = gpg.delete_keys(import_result.fingerprints)

    # Return Encrypt Status
    return encrypted_data.ok


def GPG_Decrypt(gnupghome, enctext_path, passphrase, dectext_path):
    # Init GnuPG Home Path
    gpg_bob = gnupg.GPG(gnupghome=gnupghome)

    # Decrypt the data
    fd = open(enctext_path, 'rb')
    decrypted_data = gpg_bob.decrypt_file(fd, passphrase=passphrase, output=dectext_path)

    # Return Encrypt Status
    return decrypted_data.ok


def Alice_Bob_Test():
    # Parameters
    Sender = 'Alice'
    Sender_Passphrase = '123'
    Recipient = 'Bob'
    Recipient_Passphrase = '321'

    # Server: Generate Key Pair
    os.mkdir('./Server')
    GPG_GenKey('Alice', '123')
    GPG_GenKey('Bob', '321')

    # Alice: Encrypt Recipient: Bob
    encStatus = GPG_Encrypt(gnupghome='./Alice/.gnupg',
                            recipient='Bob', recipient_pk='./Server/Bob_pub_key.asc',
                            plaintext_path='plaintext', enctext_path='plaintext.encrypted'
                            )
    print('Encrypt Status:', encStatus)

    # Bob: Decrypt
    decStatus = GPG_Decrypt(gnupghome='./Bob/.gnupg',
                            enctext_path='plaintext.encrypted', dectext_path='plaintext.decrypted',
                            passphrase='321'
                            )
    print('Decrypt Status:', decStatus)


if __name__ == "__main__":
    Alice_Bob_Test()
