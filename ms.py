# -*- coding:utf-8 -*-
import random

# 실패 : #shuffle 실패 & 4칸만 지뢰 형성되는 게 아님ㅠ  #입력하면 한 '열'이 다 열림

n=20
pz=[[0]*n]*n
ans=[[' ']*n]*n

def gen_puzzle():
	#16%만큼 지뢰(*)형성
	for i in range (int(n*0.4)):
		for j in range (int(n*0.4)):
			pz[i][j]='*'
	random.shuffle(pz)
	#shuffle 실패 & 4칸만 지뢰 형성되는 게 아님ㅠ
	for i in range(n):
		for j in range(n):
			if pz[i][j]==0:
				chk_around(i,j)

def chk_around(x,y):
	#여기가 짜증남, 일일이 범위 나누고 체크 일일이 써줘야 하나?
	if x==0:
		if y==0:
			for i in range (x,x+2):
				for j in range (y,y+2):
					if pz[i][j]=='*':
						pz[x][y]+=1
		elif y==n-1:
			for i in range (x,x+2):
				for j in range (y-1,y+1):
					if pz[i][j]=='*':
						pz[x][y]+=1
		else:
			for i in range (x,x+2):
				for j in range (y-1,y+2):
					if pz[i][j]=='*':
						pz[x][y]+=1
	elif x==n-1:
		if y==0:
			for i in range (x-1,x+1):
				for j in range (y,y+2):
					if pz[i][j]=='*':
						pz[x][y]+=1
		elif y==n-1:
			for i in range (x-1,x+1):
				for j in range (y-1,y+1):
					if pz[i][j]=='*':
						pz[x][y]+=1
		else:
			for i in range (x-1,x+1):
				for j in range (y-1,y+2):
					if pz[i][j]=='*':
						pz[x][y]+=1
	else:
		if y==0:
			for i in range (x-1,x+2):
				for j in range (y,y+2):
					if pz[i][j]=='*':
						pz[x][y]+=1
		elif y==n-1:
			for i in range (x-1,x+2):
				for j in range (y-1,y+1):
					if pz[i][j]=='*':
						pz[x][y]+=1
		else:
			for i in range (x-1,x+2):
				for j in range (y-1,y+2):
					if pz[i][j]=='*':
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

def guessing(x,y):
	if pz[x][y]=='*':
		return 1
	else:
		ans[x][y]=pz[x][y]
		return 0
	#지뢰면 1반환, 아니면 화면에 주변지뢰개수를 출력하고 0반환

# (입력받고, 지뢰인지 확인하고, 주변지뢰수 출력)을 (전체칸-지뢰수)만큼
# 구현 못 함ㅠㅠ : 주변지뢰수가 0일때 주변8칸 다열여주고 for문의 횟수 8번 줄이기 (tr+=8해보려했으나 다음 반복에서 다시 다음수로 넘어감)
for tr in range (n*n-int(n*0.16)):
	prt_puzzle()
	gss=input("입력 (ex-0,0) : ")
	bmb=guessing(gss[0],gss[1])
	if bmb:
		print "Game Over!"
		break
	
# 횟수를 다 채웠다 <=> 지뢰빼고 다 눌렀다 <=> 이겼다
if tr==n*n-int(n*0.16)-1:
	print "You Win! :)"
