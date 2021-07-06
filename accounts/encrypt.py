from djangoencryptfile import EncryptionService
from django.core.files import File

password = '1234'
service = EncryptionService(raise_exception=False)

open('code for crypto', 'rb') as inputfile:
    usefile = File(inputfile, name='readme.md')
    encrypted_file = service.encrypt_file(useFile, password, extension='enc')  # it will save readme.md.enc
    decrypt_file = service.decrypt_file(encrypted_file, password, extension='.enc') # it will remove .enc extension