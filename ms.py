# -*- coding:utf-8 -*-
import random
from sys import stdout

global remain

size=[]
size=input("지뢰밭의 크기 (ex-20,20) : ")
level=input("레벨(1,2,3) : ")

if level==1:
	level=0.10
elif level==2:
	level=0.25
else:
	level=0.40

making=[0]*size[0]*size[1] #random을 위한 임시공간
pz = [] #답
ans = [] #보여질 퍼즐
for i in range(size[0]) :
	ans.append([' ']*size[1])

def chk_around(x,y):
	for i in range(-1,2) :
		if (x+i < 0) or (x+i >= size[0]) :
			continue
		for j in range(-1,2) :
			if (y+j < 0) or (y+j >= size[1]) :
				continue
			if pz[x+i][y+j]=='*':
				pz[x][y]+=1

def gen_puzzle():
	#16%만큼 지뢰(*)형성
	for i in range(int(size[0]*size[1]*level)):
		making[i]='*'
		global remain
		remain-=1
	random.shuffle(making)

	for i in range(size[0]):
		pz.append(making[size[1]*i:size[1]*i+size[1]])

	for i in range(size[0]) :
		for j in range(size[1]) :
			if pz[i][j]==0:
				chk_around(i,j)

def prt_answer():
	for i in range (size[0]):
		for j in range (size[1]):
			print " - ",
		print "\n"
		for j in range (size[1]):
			print "|",ans[i][j],
		print "|"
	for j in range (size[1]):
		print " - ",
	print "\n"

def guessing(x,y):
	if ans[x][y]==' ':
		ans[x][y]=pz[x][y]
		if pz[x][y]=='*':
			print "Game Over! :( \n"
			return 0
		else:
			global remain
			remain-=1
			return 1
	else:
		return 1

remain=size[0]*size[1]
gen_puzzle()
prt_answer()
end=1
flag=0
while(end):
	print remain,"칸 남음, ",int(size[0]*size[1]*level)-flag,"개 지뢰남음"
	gss=input("입력 (ex-0,0 또는 -1:깃발) : ")
	if gss==-1:
		gss=input("깃발을 어디에 (ex-0,0) : ")
		if ans[gss[0]][gss[1]]=='!':
			ans[gss[0]][gss[1]]=' '
			flag-=1
		elif ans[gss[0]][gss[1]]==' ':
			ans[gss[0]][gss[1]]='!'
			flag+=1
	else:
		end=guessing(gss[0],gss[1])
	prt_answer()
	if remain==0:
		print "You Win! :) \n"
		end=0