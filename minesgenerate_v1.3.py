import numpy as np
import matplotlib.pyplot as plt
import random
import math

class Map():
    def __init__(self,num_mine,num_hero):
        self.num_mine = num_mine
        self.num_hero = num_hero
        self.mines = []
        self.heros = []
        self.align = []
        self.flag=0
        self.init_map()
        for i in self.heros:
            self.align.append([])

    def mines_generate(self,num_cluster=5,num_mines_each_cluster=100):
        mines_list = []
        #随机生成num_cluster个正态分布的参数
        for i in range(num_cluster):
            mu = np.random.randn(2)
            std = np.random.random([2,2])
            std_limit = np.sqrt(std[0,0]*std[1,1])

            std[0,1] = -std_limit + 2*std_limit*np.random.random()
            std[1,0] = std[0,1]
            #print(mu)
            #print(std)
            mines = np.random.multivariate_normal(mu,std,size=num_mines_each_cluster)
            #print(mines)
            mines_list.append(mines)
        return mines_list

    def init_map(self):
        mines_list=self.mines_generate(self.num_hero,self.num_mine)
        for i in range(len(mines_list)):
            j=mines_list[i].tolist()
            for k in j:
                self.mines.append(k)
        for i in range(self.num_hero):    
            self.heros.append(random.choice(self.mines))

    def hero_move(self):
        k=0
        for i in self.align:
            x_num=0
            y_num=0
            for j in i:
                x_num+=j[0]
                y_num+=j[1]
            x_num/=len(i)
            y_num/=len(i)
            if int((self.heros[k][0]-x_num)*10000)==0 and int((self.heros[k][1]- y_num)*10000)==0:#如果与上次的位置（精度为0.00001）相同，则不用换
                self.flag+=1
            else:
                self.heros[k]=[x_num,y_num]
            k+=1
        return self.flag,len(self.heros)   

    def mine_align(self):
        for i in range(self.num_hero):  #每次开始清空上一次英雄所得的矿
            self.align[i]=[]

        for i in self.mines:
            self.path=[]
            for j in self.heros:
                self.path.append(math.sqrt((i[0]-j[0])**2+(i[1]-j[1])**2))
            self.min=self.path.index(min(self.path))
            self.align[self.min].append(i)

    def map_visualization(self):
        color=['r','b','g']
        k=0
        for i in self.align:
            tmp=np.array(i)
            X=tmp[:,0]
            Y=tmp[:,1]
            plt.plot(X,Y,color[k]+'*')
            k+=1

        k=0
        color1=['y','k','m']
        for i in self.heros:
            tmp=np.array(i)
            X = tmp[0]
            Y = tmp[1]
            plt.plot(X, Y, color1[k]+'x')  
            k+=1
        
        plt.show()
 
def main():
    map = Map(num_mine=100,num_hero=3)
    while True:
        map.mine_align()
        i,j=map.hero_move()
        #map.map_visualization()
        if i==j:   #当三个点位置固定了，则退出循环
            break
    map.map_visualization()
        


if __name__=='__main__':
    main()