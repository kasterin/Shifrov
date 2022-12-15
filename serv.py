import random
import pickle
import socket
import time

class Crypto:
    def __init__(self, g=12, p=80, rmin=1, rmax=10):
        self.g = g
        self.p = p
        self.secret_key = random.randint(rmin, rmax)

    def open_key(self):
        self.open_key = self.g ** self.secret_key % self.p
        return self.open_key, self.g, self.p

    def decrypt(self, B):
        return B ** self.secret_key % self.p

    def shared_key(self, A, g, p):
        return g ** self.secret_key % p, A ** self.secret_key % p

def encryption(mes, k):
    return [chr((ord(i) + k) % 65536) for i in mes]

def decryption(mes, k):
    return [chr((65536 + (ord(i) - k) % 65536) % 65536) for i in mes]

c = Crypto()
sock = socket.socket()
print(f'---\nStart Server')
ip = ''
port = 9090
sock.bind((ip, port))
print(f'Open socket\nip: {ip}\nport: {port}')
sock.listen(1)
print(f'Listening socket')
conn, addr = sock.accept()
print(f'Accept new connection\nconn: {conn}\naddress: {addr}')
data = conn.recv(1024)
data = pickle.loads(data)
if data[0] == 'open_key':
    open_key = data[1]
print(f'Get Client open key: {open_key}')
(B, K) = crypto.shared_key(*open_key)
key_client = K
conn.send(pickle.dumps(["open_key", crypto.open_key(), B]))
print(f'Send Server open key: {crypto.open_key()}\n---')
while True:
    data = conn.recv(1024)
    get_time = time.localtime()
    data = pickle.loads(data)
    K = crypto.decrypt(data[2])
    mesin = data[1]
    print(f'Получено: {mesin}')
    print(f'Encryption')
    mesin = ''.join(decryption(decryption(mesin, K), key_client))
    print(mesin)
    print(f'---')
    if "exit" in mesin.lower():
        conn.close()
        exit()
    mout = f'Client {addr} send message :: {mesin}'
    data = ["message", encryption(encryption(mout, K), key_client)]
    conn.send(pickle.dumps(data))
    if "exit" in mout.lower():
        conn.close()
        exit()