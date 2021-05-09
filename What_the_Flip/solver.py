from Crypto.Util.number import *
from functools import reduce
from operator import mul
from itertools import combinations
import sys
import socket, struct, telnetlib
from tqdm import tqdm

# --- common funcs ---
def sock(remoteip, remoteport):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((remoteip, remoteport))
	return s, s.makefile('rw')

def read_until(f, delim='\n'):
	data = ''
	while not data.endswith(delim):
		data += f.read(1)
	return data

	
#HOSTはIPアドレスでも可
HOST, PORT = "umbccd.io", 3000
s, f = sock(HOST, PORT)
for k in range(5): read_until(f)
read_until(f,"username: ")
s.send(b"admin&parsword=goBigDawgs123\n")
read_until(f,"password: ")
s.send(b"test\n")
recv_m = read_until(f).split()
c1 = recv_m[-1]
print(c1)
ct = c1[:16] + str(hex(int(c1[16:18],16)^ord("r")^ord("s")))[2:] + c1[18:]
print(ct)
print(read_until(f,"ciphertext: "))
s.send(ct.encode()+b"\n")
print(read_until(f))
print(read_until(f,"}"))

#read_untilの使い方
#返り値があるのでprintするか、何かの変数に入れる
#1行読む：read_until(f)
#特定の文字まで読む：read_until(f,"input")
#配列に格納する：recv_m = read_until(f).split() or .strip()

#サーバーに何か送るとき
#s.send(b'1\n') : 1を送っている
#バイト列で送ること。str->bytesにするには、変数の後に.encode()
#必ず改行を入れること。終了ポイントが分からなくなる。ex) s.send(flag.encode() + b'\n')

