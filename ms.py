# -*- coding:utf-8 -*-
import random
from sys import stdout
# 실패1 : #shuffle 실패 & 4칸만 지뢰 형성되는 게 아님ㅠ  #입력하면 한 '열'이 다 열림

n=20
making=[0]*n*n #실패1해결.
pz = []
ans=[]
for i in range(n) :
	ans.append([' ']*n)

def gen_puzzle():
	#16%만큼 지뢰(*)형성
	for i in range (int(n*0.4)**2):
		making[i]='*'
	random.shuffle(making)

	for i in range(n):
		pz.append(making[n*i:n*i+n])

	for i in range(n) :
		for j in range(n) :
			if pz[i][j]==0:
				chk_around(i,j)
"""
	for i in range(n):
		for j in range(n) :
			stdout.write("%3s" % pz[i][j])
		print("")
"""

def chk_around(x,y):
	#여기가 짜증남, 일일이 범위 나누고 체크 일일이 써줘야 하나?
	for i in range(-1,2) :
		if (x+i < 0) or (x+i >= n) :
			continue
		for j in range(-1,2) :
			if (y+j < 0) or (y+j >= n) :
				continue
			if pz[x+i][y+j]=='*':
				pz[x][y]+=1


def prt_puzzle():
	for i in range (n):
		for j in range (n):
			print " - ",
		print "\n"
		for j in range (n):
			print "|",ans[i][j],
		print "|"
	for j in range (n):
		print " - ",
	print "\n"

def guessing(x,y):
	if pz[x][y]=='*':
		ans[x][y]=pz[x][y]
		return 1
	else:
		ans[x][y]=pz[x][y]
		return 0
	#지뢰면 1반환, 아니면 화면에 주변지뢰개수를 출력하고 0반환

gen_puzzle()

# (입력받고, 지뢰인지 확인하고, 주변지뢰수 출력)을 (전체칸-지뢰수)만큼
# 구현 못 함ㅠㅠ : 주변지뢰수가 0일때 주변8칸 다열여주고 for문의 횟수 8번 줄이기 (tr+=8해보려했으나 다음 반복에서 다시 다음수로 넘어감)
for tr in range ((n*n)-int(n*0.16)):
	prt_puzzle()
	gss=input("입력 (ex-0,0) : ")
	bmb=guessing(gss[0],gss[1])
	if bmb:
		prt_puzzle()
		print "Game Over!"
		break
	
# 횟수를 다 채웠다 <=> 지뢰빼고 다 눌렀다 <=> 이겼다
if tr==n*n-int(n*0.16)-1:
	print "You Win! :)"
