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

def fibo(n):
	fib = [0,1]
	for i in range(2,n):
		x = fib[i-1] + fib[i-2]
		fib.append(x)

	return fib

fib = fibo(10000)
#print(fib)
#HOSTはIPアドレスでも可
HOST, PORT = "umbccd.io", 6000
s, f = sock(HOST, PORT)
for _ in range(10): print(read_until(f))
cnt = 0
for i in range(100):
	recv_m = read_until(f).split()
	#print(recv_m)
	a = int(recv_m[0][1:-1])
	b = int(recv_m[1][:-1])
	c = int(recv_m[2][:-1])
	#print(a,b,c)
	#print(read_until(f,">> "))
	if a in fib: s.send(str(a).encode()+b"\n")
	elif b in fib: s.send(str(b).encode()+b"\n")
	else: s.send(str(c).encode()+b"\n")
	for _ in range(2): read_until(f)
	cnt += 1
	print(cnt)

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

