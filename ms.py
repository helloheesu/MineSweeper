# -*- coding:utf-8 -*-
import random

global remain

size=[]
size=input("지뢰밭의 크기 (ex-20,20) : ")
level=input("레벨(1,2,3,4) : ")

if level==1:
	level=0.08
elif level==2:
	level=0.15
elif level==3:
	level=0.20
else:
	level=0.25

making=[0]*size[0]*size[1] #random을 위한 임시공간
pz = [] #답
ans = [] #보여질 퍼즐
#보여질퍼즐에 빈칸만들기
for i in range(size[0]) :
	ans.append([' ']*size[1])

#정답퍼즐에 주변의 지뢰수 확인
def chk_around(x,y):
	for i in range(-1,2) :
		#continue: out of range를 피하기위해.
		if (x+i < 0) or (x+i >= size[0]) :
			continue
		for j in range(-1,2) :
			if (y+j < 0) or (y+j >= size[1]) :
				continue
			if pz[x+i][y+j]=='*':
				pz[x][y]+=1

#퍼즐생성 : 랜덤으로 지뢰뿌리고, 주변지뢰수적어주고. '남은 지뢰수'확인을 위한 remain++.
def gen_puzzle():
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

def prt_where(mode,ans,i,j):
	if mode==-3:
		if ans==' ':
			print str(i)+','+str(j),
		else:
			print ' '+str(ans)+' ',
	else:
		print ans,

#화면에 '보여질퍼즐'출력
def prt_answer(mode):											#!! mode가 숫자네. c처럼 enum있었으면.
	for i in range (size[0]):
		for j in range (size[1]):
			print " - ",
		print "\n"
		for j in range (size[1]):
			print "|",
			prt_where(mode,ans[i][j],i,j)
		print "|"
	for j in range (size[1]):
		print " - ",
	print "\n"

#주변지뢰수가 0일때 열어주기	
def open_around(x,y):
	chk=[]
	for i in range(-1,2) :
		#continue: out of range를 피하기위해.
		if (x+i < 0) or (x+i >= size[0]) :
			continue
		for j in range(-1,2) :
			if (y+j < 0) or (y+j >= size[1]) :
				continue
			#자기자신은 체크건너뜀. 무한루프에 빠진다.
			if (i==0) and (j==0):
				continue
			#주변지뢰수가 0이고, 보여지는 퍼즐이 빈칸일때 비로소 열어줌. '남은 지뢰수'--.
			if (pz[x+i][y+j]==0) and (ans[x+i][y+j]==' '):
				ans[x+i][y+j]=0
				global remain
				remain-=1
				#재귀함수^^
				open_around(x+i,y+j)
			else:
				guessing(x+i,y+j)

#'클릭'했을때 일어나는일.
def guessing(x,y):
	if ans[x][y]==' ':
		ans[x][y]=pz[x][y]
		if pz[x][y]=='*':
			print "Game Over! :( \n"
			return 0
		else:
			global remain
			remain-=1
			if pz[x][y]==0:
				open_around(x,y)
			return 1
	else: #실수로 다른칸 누른걸 방지, 빈칸아닌칸을 누르면 그냥 무시하고 게임진행(end=1을 반환해서 그냥 게임유지.)
		return 1


def done(x,y):
	end=1
	for i in range(-1,2) :
	#continue: out of range를 피하기위해.
		if (x+i < 0) or (x+i >= size[0]) :
			continue
		for j in range(-1,2) :
			if (y+j < 0) or (y+j >= size[1]) :
				continue
			end=guessing(x+i,y+j)
			if end:
				break
		if end:
			break
	return end


remain=size[0]*size[1]
gen_puzzle()
prt_answer(0)
end=1
flag=0

def gss_flag():
	gss=input("깃발을 어디에 (ex-0,0, -1:깃발 모드 취소, -3:위치보기) : ")	#!! 깃발 취소라니.. 바로 누르는 gui에서는 안 나오겠고, 나눠서 클릭해야 할 모바일에서는 나오겠네. 모바일도 이것 때문에 불편하더라.
	if gss==-1:					#깃발 취소도 가능하고,
		return 0
	elif gss==-3:				#위치보기도 여러번 가능하고.
		prt_answer(gss)
		return gss_flag()
	#깃발해제.
	if ans[gss[0]][gss[1]]=='!':
		ans[gss[0]][gss[1]]=' '
		return -1
	#빈칸일때만 깃발처리. 실수로 이미열린칸 눌렀을 때를 대비.
	elif ans[gss[0]][gss[1]]==' ':
		ans[gss[0]][gss[1]]='!'
		return +1


while(end):
	print remain,"칸 남음, ",int(size[0]*size[1]*level)-flag,"개 지뢰남음"
	gss=input("입력 (ex-0,0 또는 -1:깃발, -3:위치보기) : ")
	if gss==-1:
		flag += gss_flag()
		"""
	elif gss==-2:
		gss=input("어딜 터뜨릴까요 (ex-0,0) : ")
		end = done(gss[0],gss[1])
		"""
	elif gss==-3:
		prt_answer(gss)
	elif (0<=gss[0]<size[0])and(0<=gss[1]<size[1]):
		end=guessing(gss[0],gss[1])
		"""
	else: #뭐야 else면 범위 밖을 접근하니까 위험하잖아
		end=guessing(gss[0],gss[1])
		"""
	prt_answer(gss)
	if remain==0:
		print "You Win! :) \n"
		end=0