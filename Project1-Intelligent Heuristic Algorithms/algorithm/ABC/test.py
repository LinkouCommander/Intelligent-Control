import math
import numpy as np
import Hive 


def F2(x):
    temp1=0
    temp2=1
    for i in range(len(x)):
        temp1+=abs(x[i])
        temp2*=abs(x[i])
    return temp1+temp2

def F3(x):
    temp1=0
    for i in range(len(x)):
        temp2=0
        for j in range(i+1):
            temp2+=x[j]
        temp1+=temp2*temp2
    return temp1

def F11(x):

    temp1=0
    temp2=1
    for i in range(len(x)):
        temp1+=x[i]*x[i]
        temp2*=math.cos(x[i]/pow(i+1,0.5))

    return temp1/4000-temp2+1

def F12(x):
    temp1=0
    temp2=0
    for i in range(len(x)-1):
        temp1+=math.pow(y(x[i])-1,2)*(1+10*math.pow(math.sin(math.pi*y(x[i+1])),2))
    for j in range(len(x)):
        temp2+=u(x[j],10,100,4)
    temp1+=math.pi*1/len(x)*(10*math.pow(math.sin(math.pi*y(x[0])),2)+math.pow(y(x[len(x)-1])-1,2))

    return temp1 + temp2
def y(x):
    return 1+(x+1)/4
    
def F13(x):
    temp1=0
    for i in range(len(x)-1):
        temp1+=math.pow(x[i]-1,2)*(1+math.pow(math.sin(3*math.pi*x[i+1]),2))
    temp1+=0.1*(math.pow(math.sin(3*math.pi*x[0]),2)+math.pow(x[len(x)-1]-1,2)*(1+math.pow(math.sin(2*math.pi*x[len(x)-1]),2)))
    temp2=0
    for j in range(len(x)):
        temp2+=u(x[j],5,100,4)

    return temp1+temp2

def u(x,a,k,m):
    if x>a:
        return k*math.pow(x-a,m)
    elif x<a*-1:
        return k*math.pow(-x-a,m)
    else:
        return 0

def F14(x):
    temp_a1=-32
    temp_a2=0
    a=[[0]*25 for i in range(2)]
    for j in range(25):
        a[0][j]=temp_a1
        temp_a1+=16
        if temp_a1>32:
            temp_a1=-32
    temp_a1=-32
    for j in range(25):
        a[1][j]=temp_a1
        temp_a2+=1
        if temp_a2==5:
            temp_a1+=16
            temp_a2=0

    temp1=0
    for j in range(25):
        temp2=0
        for i in range(len(x)):
            temp2+=math.pow(x[i]-a[i][j],6)
        temp1+=1/(j+temp2+1)
    return math.pow(1/500+temp1,-1)

def F15(x):
    a=[0.1957,0.1947,0.1735,0.16,0.0844,0.0627,0.0456,0.0342,0.0342,0.0235,0.0246]
    b=[4,2,1,1/2,1/4,1/6,1/8,1/10,1/12,1/14,1/16]

    temp1=0
    for i in range(11):
        temp2=x[0]*(b[i]*b[i]+b[i]*x[1])/(b[i]*b[i]+b[i]*x[2]+x[3])
        temp1+=math.pow(a[i]-temp2,2)
    return temp1

def run():
    ndim = int(30)
    model = Hive.BeeHive(lower     = [-10] *ndim ,
                         upper     = [10] *ndim ,
                         fun       = F2 ,
                         numb_bees =  50,
                         max_itrs  =  500,)
    cost = model.run()

    print("Best-so-far solution: {0}".format(model.best))

if __name__ == "__main__":
    run()
