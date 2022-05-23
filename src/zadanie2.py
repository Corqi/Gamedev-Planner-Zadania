# TODO:
#   Zadanie 2 - Szyfrowanie danych
#   Z modułu cryptography.fernet, zaimportuj Fernet, a następnie
#   za jego pomocą zaszyfruj oraz odszyfruj dowolną wiadomość.

from cryptography.fernet import Fernet

message = b'Hello World!'

# generate key
key = Fernet.generate_key()

# assign key to variable
fernet = Fernet(key)

# encrypt a message
message_encrypted = fernet.encrypt(message)

print(message_encrypted)

# decrypt message
message_decrypted = fernet.decrypt(message_encrypted)

print(message_decrypted)