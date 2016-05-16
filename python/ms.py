# -*- coding:utf-8 -*-
import random

class Game(object):
    """docstring for Game"""
    def __init__(self):
        super(Game, self).__init__()

        self.size=()
        self.remain=0
        self.level=0
        self.ans = [] #보여질 퍼즐
        self.pz = [] #답

    def start(self):
        self.size=size=input("지뢰밭의 크기 (ex-20,20) : ")
        self.remain=size[0]*size[1]

        level=input("레벨(1,2,3,4) : ")
        if level==1:
            self.level=0.08
        elif level==2:
            self.level=0.15
        elif level==3:
            self.level=0.20
        else:
            self.level=0.25

        #보여질퍼즐에 빈칸만들기
        for i in range(size[0]) :
            self.ans.append([' ']*size[1])
        self.gen_puzzle()
        self.prt_answer(0)
        while self.run():
            pass

    def run(self):
        end = 1
        flag = 0
        print self.remain,"칸 남음, ",int(self.size[0]*self.size[1]*self.level)-flag,"개 지뢰남음"
        gss=input("입력 (ex-0,0 또는 -1:깃발, -2:주변터뜨리기, -3:위치보기) : ")
        if gss==-1:
            flag += self.gss_flag()
        elif gss==-2:
            end = self.done()
        elif gss==-3:
            self.prt_answer(gss)
        elif (0<=gss[0]<self.size[0])and(0<=gss[1]<self.size[1]):
            end=self.guessing(gss[0],gss[1])
            """
        else: #뭐야 else면 범위 밖을 접근하니까 위험하잖아
            end=self.guessing(gss[0],gss[1])
            """
        self.prt_answer(gss)
        if end==0:
            print "Game Over! :( \n"
            return False
        if self.remain==0:
            print "You Win! :) \n"
            return False
        return True

    #정답퍼즐에 주변의 지뢰수 확인
    def chk_around(self,x,y):
        for i in range(-1,2) :
            #continue: out of range를 피하기위해.
            if (x+i < 0) or (x+i >= self.size[0]) :
                continue
            for j in range(-1,2) :
                if (y+j < 0) or (y+j >= self.size[1]) :
                    continue
                if self.pz[x+i][y+j]=='*':
                    self.pz[x][y]+=1

    #퍼즐생성 : 랜덤으로 지뢰뿌리고, 주변지뢰수적어주고. '남은 지뢰수'확인을 위한 remain++.
    def gen_puzzle(self):
        making=[0]*self.size[0]*self.size[1] #random을 위한 임시공간
        for i in range(int(self.size[0]*self.size[1]*self.level)):
            making[i]='*'
            self.remain-=1
        random.shuffle(making)

        for i in range(self.size[0]):
            self.pz.append(making[self.size[1]*i:self.size[1]*i+self.size[1]])

        for i in range(self.size[0]) :
            for j in range(self.size[1]) :
                if self.pz[i][j]==0:
                    self.chk_around(i,j)

    def prt_where(self,mode,ans,i,j):
        if mode==-3:
            if ans==' ':
                print str(i)+','+str(j),
            else:
                print ' '+str(ans)+' ',
        else:
            print ans,

    #화면에 '보여질퍼즐'출력
    def prt_answer(self,mode):                                           #!! mode가 숫자네. c처럼 enum있었으면.
        for i in range (self.size[0]):
            for j in range (self.size[1]):
                print " - ",
            print "\n"
            for j in range (self.size[1]):
                print "|",
                self.prt_where(mode,self.ans[i][j],i,j)
            print "|"
        for j in range (self.size[1]):
            print " - ",
        print "\n"

    #주변지뢰수가 0일때 열어주기    
    def open_around(self,x,y,mode):
        for i in range(-1,2) :
            #continue: out of range를 피하기위해.
            if (x+i < 0) or (x+i >= self.size[0]) :
                continue
            for j in range(-1,2) :
                if (y+j < 0) or (y+j >= self.size[1]) :
                    continue
                #자기자신은 체크건너뜀. 무한루프에 빠진다.
                if (i==0) and (j==0):
                    continue
                #'보여지는 퍼즐':빈칸, 깃발, 숫자('이미열린칸') / 'mode':guessing=0, 깃발=-1, done=-2, 위치보기=-3. / enum이 필요한 때..헣헣 배열들에선 enum값으로 처리하고, 프린트할 때만 !등 문자로 변경... 일 필요는 없나? 문자 숫자 다 처리 가능하니까?
                #깃발 표시해 둔 칸은 처리 안 해줌.
                if (self.ans[x+i][y+j]=='!'):
                    continue
                #주변지뢰수가 0이고, 보여지는 퍼즐이 빈칸일때 비로소 열어줌. '남은 지뢰수'--.
                #빈칸일 때만? -> 무한루프 방지. 그러나 수동으로 연 칸이 0일 때는 안 열어준다는 단점이 있다.
                if (self.pz[x+i][y+j]==0) and (self.ans[x+i][y+j]==' '):
                    self.ans[x+i][y+j]=0
                    self.remain-=1
                    #재귀함수^^
                    self.open_around(x+i,y+j,0)
                else:
                    if (mode==0):
                        self.guessing(x+i, y+j) #mode==0일 때는 지뢰가 입력될리도 없고, 숫자까지만 나올 것.
                    elif (mode==-2):
                        if (self.pz[x+i][y+j]=='*'):
                            return 0
                        else:               #0이 아닌 숫자인 경우.
                            self.guessing(x+i, y+j)

    #'클릭'했을때 일어나는일.
    def guessing(self,x,y):
        if self.ans[x][y]==' ':
            self.ans[x][y]=self.pz[x][y]
            if self.pz[x][y]=='*':   #지뢰밞음! Game Over, return (end==0).
                return 0
            else:
                self.remain-=1
                if self.pz[x][y]==0:
                    self.open_around(x,y,0)
                return 1
        else: #실수로 다른칸 누른걸 방지, 빈칸아닌칸을 누르면 그냥 무시하고 게임진행(end=1을 반환해서 그냥 게임유지.)
            return 1

    #'좌우클릭'했을때 일어나는일. 죽었는지(end==0) 살았는지(end==1) 반환.
    def done(self):
        gss=input("어딜 터뜨릴까요 (ex-0,0, -2:돌아가기, -3:위치보기) : ")
        end=1
        if gss==-1:
            return 0
        elif gss==-3:               #위치보기도 여러번 가능하고.
            self.prt_answer(gss)
            return self.done()
        self.open_around(gss[0], gss[1], -2)
        #if self.ans[gss[0]][gss[1]]==''

        for i in range(-1,2) :
        #continue: out of range를 피하기위해.
            if (gss[0]+i < 0) or (gss[0]+i >= self.size[0]) :
                continue
            for j in range(-1,2) :
                if (gss[1]+j < 0) or (gss[1]+j >= self.size[1]) :
                    continue
                end=self.guessing(gss[0]+i,gss[1]+j)
                if end:
                    break
            if end:
                break
        return end

    def gss_flag(self):
        gss=input("깃발을 어디에 (ex-0,0, -1:돌아가기, -3:위치보기) : ")  #!! 깃발 취소라니.. 바로 누르는 gui에서는 안 나오겠고, 나눠서 클릭해야 할 모바일에서는 나오겠네. 모바일도 이것 때문에 불편하더라.
        if gss==-1:                 #깃발 취소도 가능하고,
            return 0
        elif gss==-3:               #위치보기도 여러번 가능하고.
            self.prt_answer(gss)
            return self.gss_flag()
        #깃발해제.
        if self.ans[gss[0]][gss[1]]=='!':
            self.ans[gss[0]][gss[1]]=' '
            return -1
        #빈칸일때만 깃발처리. 실수로 이미열린칸 눌렀을 때를 대비.
        elif self.ans[gss[0]][gss[1]]==' ':
            self.ans[gss[0]][gss[1]]='!'
            return +1
