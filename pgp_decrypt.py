import gnupg

gpg = gnupg.GPG(gnupghome=".gnupg")

fd = open('plaintext.encrypted', 'rb')
status = gpg.decrypt_file(fd, passphrase='mypassphrase', output='plaintext.decrypted')

print(status.ok)
print(status.stderr)