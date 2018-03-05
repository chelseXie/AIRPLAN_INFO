# autor xiehao
# 网络最大流问题Ford-fulkserson算法
c = [[0,3,5,0],
	[0,0,4,2],
	[0,0,0,4],
	[0,0,0,0]]
c1=[[0,0,0,0],
	[0,0,0,0],
	[0,0,0,0],
	[0,0,0,0]]
used=[]
f=[]
max=[]

def fds(c ,f,startIndex,endIndex):
	for x in range(0,endIndex+1):
		if c[startIndex][x]>0 and not used[x]:

			used[x]=True
			if f==0:
				f= c[startIndex][x]
			if f>=c[startIndex][x]:
				f=c[startIndex][x]
			if x==endIndex:
					c[startIndex][x]-=f
					c[x][startIndex]+=f
					return f
			fm=fds(c,f,x,endIndex)
			if fm>0:
				if fm>f:
					c[startIndex][x]-=f
					c[x][startIndex]+=f
					return f
				else:
					c[startIndex][x]-=fm
					c[x][startIndex]+=fm
					return fm
		elif x==endIndex:
			return 0
def fort_fulkerson(c,f,startIndex,endIndex):
	maxf=0
	while 1==1:
		used[0:4]=[False,False,False,False]
		ff =fds(c,0,0,3,)
		print(c[0:4])
		print("曾广路径流："+str(ff))
		maxf+=ff
		if ff==0:
			return maxf

fff=fort_fulkerson(c,f,0,3)
print("总的最大流："+str(fff))				