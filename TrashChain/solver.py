from Crypto.Util.number import *
from functools import reduce
from operator import mul
from itertools import combinations
import sys
import socket, struct, telnetlib

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

A = 340282366920938460843936948965011886881
B = 127605873542257115442148455720344860097
a1 = 18446744073709551533
a2 = A//a1
assert a1*a2 == A
phia = (a1-1)*(a2-1)
k = inverse(B,phia)
#HOSTはIPアドレスでも可
cnt = 2
while True:
	HOST, PORT = "umbccd.io", 3100
	s, f = sock(HOST, PORT)
	for _ in range(8): print(read_until(f))

	#phase1
	print(read_until(f))
	print(read_until(f,"> "))
	x = cnt**4
	t = pow(x,k,A)
	t -= 1
	s.send(str(t).encode()+b"\n")
	t += 1
	assert pow(t,B,A) == x

	print(read_until(f,"> "))
	s.send(b"done\n")

	#phase2
	print(read_until(f))
#inv4 = inverse(2,A)
#print("inverse :", inv4)
#k = 467*33331*52216263142726016043295368973
#l = 157
#temp = pow(inv4,(B-k),A)
	temp = pow(cnt,k,A)
	for i in range(4):
		temp -= 1
		print(read_until(f,"> "))
		s.send(str(temp).encode()+b"\n")

	print(read_until(f,"> "))
	s.send(b"done\n")
	recv_m = read_until(f).split()
	print(recv_m)
	if "smallest" in recv_m:
		s.close()
		cnt += 1
	else:
		break	

while True: print(read_until(f))

#read_untilの使い方
#返り値があるのでprintするか、何かの変数に入れる
#1行読む：read_until(f)
#特定の文字まで読む：read_until(f,"input")
#配列に格納する：recv_m = read_until(f).split() or .strip()

#サーバーに何か送るとき
#s.send(b'1\n') : 1を送っている
#バイト列で送ること。str->bytesにするには、変数の後に.encode()
#必ず改行を入れること。終了ポイントが分からなくなる。ex) s.send(flag.encode() + b'\n')

