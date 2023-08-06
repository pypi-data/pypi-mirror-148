from mpmath import *
import numpy as np 
import math
from scipy.fftpack import fft,ifft

#定义π
pi=math.pi

#定义取最小值函数
def get_s(a,b):
    if a<b:
        return a
    else:
        return b

#定义取共轭函数
def Conjugate(s):
    return s.real-j*s.imag

#定义Gaver-Stehfest算法
def GS_1d(f,t,M):
    #计算节点数M，取值为正偶数
    #推荐取值M=14,16,18
    M=int(M)
    #避免t=0的情况
    if t==0:
        t=10**(-4)
    sum=0
    
    for m in np.arange(1,M+1):
        #计算权重系数c
        c=0
        for k in np.arange( math.floor( (m+1)/2 ) , get_s(m,M/2) +1 ):
            c+=k**(M/2)*math.factorial(k*2)/math.factorial(M/2-k)/math.factorial(k)/math.factorial(k-1)/math.factorial(m-k)/math.factorial(2*k-m)
        c*=(0-1)**(m+M/2)
        #一维求和
        sum+=c*f(m*math.log(2)/t)
    sum*=math.log(2)/t
    return float(sum)

#定义欧拉算法
def Euler_1d(f,t,M):
    #计算节点数M，正整数
    #推荐取值M=17,19
    M=int(M)
    #避免t=0的情况
    if t==0:
        t=10**(-4)
    sum=0
    #计算权重系数中间变量E
    E=np.zeros(2*M+1)
    #权重计算c
    c=np.zeros(2*M+1)
    E[0]=0.5
    E[2*M]=(1/2)**M
    for i in np.arange(1,M+1):
        E[i]=1
    for m in np.arange(1,M):
        E[2*M-m]=E[2*M-m+1]+((1/2)**M)*math.factorial(M)/(math.factorial(m)*math.factorial(M-m))
    for m in np.arange(0,2*M+1):
        c[m]=(-1)**m*E[m]
    #一维求和
    for m in np.arange(0,2*M+1):
        sum+=c[m]*(      f(      complex( M*math.log(10)/3,m*math.pi)    /  t         )       ).real
    sum*=10**(M/3)/t
    return sum

#定义Talbot算法
def Talbot_1d(f,t,M):
    #计算节点数M，正整数
    #推荐取值21
    M=int(M)
    sum=0
    #计算节点a
    a=list(range(M))
    #权重系数c
    c=list(range(M))
    a[0]=M*2/5
    for m in np.arange(1,M):
        a[m]=2*m*math.pi/5*complex(  math.cos(m*math.pi/M)/math.sin(m*math.pi/M) , 1  )
    c[0]=exp(a[0])/2
    for m in np.arange(1,M):
        cot=math.cos(m*math.pi/M)/math.sin(m*math.pi/M)
        c[m]=complex(1,m*math.pi/M*(1+cot**2)-cot)*exp(a[m])
    #一维求和
    for m in np.arange(0,M):
        sum+=(c[m]*f(a[m]/t)).real
    sum*=2/5/t
    return sum

#定义傅里叶级数法二维求逆
def series_2d(f,t1,t2,N,c1,c2):
    #计算节点数N，取值为正整数
    N=int(N)
    #积分路径(实轴坐标)
    c1=float(c1)
    c2=float(c2)
    #二维求和
    def OneToN(N):
        sum=0
        sum+=0.5*f(c1,c2)
        for m in np.arange(1,N+1):
            sum+=f(c1,c2+j*m*pi/T).real * math.cos(m*pi*t2/T) - f(c1,c2+j*m*pi/T).imag*math.sin(m*pi*t2/T)
        for n in np.arange(1,N+1):
            sum+=f(c1+j*n*pi/T,c2).real * math.cos(n*pi*t1/T) - f(c1+j*n*pi/T,c2).imag*math.sin(n*pi*t1/T)
        for n in np.arange(1,N+1):
            for m in np.arange(1,N+1):
                sum+=f(c1+j*n*pi/T,c2+j*m*pi/T).real * math.cos(n*pi*t1/T + m*pi*t2/T)
                sum+=f(c1+j*n*pi/T,c2-j*m*pi/T).real * math.cos(n*pi*t1/T - m*pi*t2/T)
                sum-=f(c1+j*n*pi/T,c2+j*m*pi/T).imag * math.sin(n*pi*t1/T + m*pi*t2/T)
                sum-=f(c1+j*n*pi/T,c2-j*m*pi/T).imag * math.sin(n*pi*t1/T - m*pi*t2/T)
        sum=sum/(2*T*T)
        sum=sum*exp(c1*t1+c2*t2)
        return sum
    if t1>t2:
        T=2.5*t1
    else:
        T=2.5*t2


    return float(OneToN(N))

def Partial_2d(f,t1,t2,N,par1,par2):
    N=int(N)
    par1=float(par1)
    par2=float(par2)
    def f1(s):
        sum=0  
        sum-=f(c1,s)

        d=[0]*7
        e0=[0]*7;e1=[0]*5;e2=[0]*3;e3=[0]*1
        q1=[0]*6;q2=[0]*4;q3=[0]*2
        for i in np.arange(6):
            q1[i]=f(c1-j*(N+i+1)*omega,s)/f(c1-j*(N+i)*omega,s)
        for i in np.arange(5):
            e1[i]=q1[i+1]-q1[i]+e0[i+1]
        for i in np.arange(4):
            q2[i]=q1[i+1]*e1[i+1]/e1[i]
        for i in np.arange(3):
            e2[i]=q2[i+1]-q2[i]+e1[i+1]
        for i in np.arange(2):  
            q3[i]=q2[i+1]*e2[i+1]/e2[i]  
        for i in np.arange(1):
            e3[i]=q3[i+1]-q3[i]+e2[i+1]  
        d[0]=f(c1-j*N*omega,s);d[1]=0-q1[0];d[2]=0-e1[0];d[3]=0-q2[0];d[4]=0-e2[0]
        d[5]=0-q3[0];d[6]=0-e3[0]

        A=[0]*7;B=[0]*7
        A[0]=d[0];A[1]=d[0];B[0]=1;B[1]=B[0]+d[1]*exp(0-j*k1*T*omega)
        for n in np.arange(2,7):
            A[n]=A[n-1]+d[n]*exp(0-j*k1*T*omega)*A[n-2]
            B[n]=B[n-1]+d[n]*exp(0-j*k1*T*omega)*B[n-2]
        sum+=A[6]/B[6]

        for n in np.arange(N):  
            sum+=f(c1-j*n*omega,s) * ( exp( (-1)*j*k1*T*omega )**n )
            sum+=f(c1+j*n*omega,s) * (   exp((-1)*j*k1*T*omega)**(0-n)   )

        sum=sum*omega*exp(c1*k1*T)/(2*pi)
        return sum

    if t1==0:
        t1=0.0005
    if t2==0:
        t2=0.0005

    if t1>t2:
        T=2*t1/(N-2)
    else:
        T=2*t2/(N-2)



    c1=par1-(1/(T*(N-2)/2))*math.log(0.0852/2)
    c2=par2-(1/(T*(N-2)/2))*math.log(0.0852/2)

    omega=2*pi/N/T

    k1=int(t1/T)
    k2=int(t2/T)

    sum=0
    sum-=f1(c2)
    d=[0]*7
    e0=[0]*7;e1=[0]*5;e2=[0]*3;e3=[0]*1
    q1=[0]*6;q2=[0]*4;q3=[0]*2
    for i in np.arange(6):
        q1[i]=f1(c2-j*(N+i+1)*omega)/f1(c2-j*(N+i)*omega)
    for i in np.arange(5):
        e1[i]=q1[i+1]-q1[i]+e0[i+1]
    for i in np.arange(4):
        q2[i]=q1[i+1]*e1[i+1]/e1[i]
    for i in np.arange(3):
        e2[i]=q2[i+1]-q2[i]+e1[i+1]
    for i in np.arange(2):  
        q3[i]=q2[i+1]*e2[i+1]/e2[i]  
    for i in np.arange(1):
        e3[i]=q3[i+1]-q3[i]+e2[i+1]  
    d[0]=f1(c2-j*N*omega);d[1]=0-q1[0];d[2]=0-e1[0];d[3]=0-q2[0];d[4]=0-e2[0]
    d[5]=0-q3[0];d[6]=0-e3[0]

    A=[0]*7;B=[0]*7
    A[0]=d[0];A[1]=d[0];B[0]=1;B[1]=B[0]+d[1]*exp(0-j*k2*T*omega)
    for n in np.arange(2,7):
        A[n]=A[n-1]+d[n]*exp(0-j*k2*T*omega)*A[n-2]
        B[n]=B[n-1]+d[n]*exp(0-j*k2*T*omega)*B[n-2]
    sum+=A[6]/B[6]
    for n in np.arange(N):  
        sum+=f1(c2-j*n*omega)* ( exp((-1)*j*k2*T*omega)**n )
        sum+=f1(c2+j*n*omega)* ( exp((-1)*j*k2*T*omega)**(0-n) )
    sum=sum*omega*exp(c2*k2*T)/(2*pi)

    Re=sum.real
    Im=sum.imag

    if (Re+Im)>0:
        return abs(sum)
    else:
        return (0-1)*abs(sum)

def Talbot_2d(f,t1,t2,M):
    M=int(M)

    a=list(range(M))
    c=list(range(M))
    a[0]=M*2/5


    for m in np.arange(1,M):
        a[m]=2*m*math.pi/5*complex(  math.cos(m*math.pi/M)/math.sin(m*math.pi/M) , 1  )
    c[0]=exp(a[0])/2
    for m in np.arange(1,M):
        cot=math.cos(m*math.pi/M)/math.sin(m*math.pi/M)
        c[m]=complex(1, m*math.pi/M*(1+cot**2) - cot)*exp(a[m])

    solut=0
    for k1 in np.arange(M):
        sum=0
        for k2 in np.arange(M):
            sum+=c[k2]*f(a[k1]/t1,a[k2]/t2)+Conjugate(c[k2])*f(a[k1]/t1,Conjugate(a[k2])/t2)
        sum*=c[k1]
        solut+=sum.real
    solut*=2/25/t1/t2
    return solut

def Euler_2d(f,t1,t2,M):

    M=int(M)

    beta=np.array([ M*math.log(10)/3+j*pi*k for k in np.arange(2*M+1)])
    E=np.zeros(2*M+1)
    c=np.zeros(2*M+1)
    E[0]=0.5
    E[2*M]=(1/2)**M
    for i in np.arange(1,M+1):
        E[i]=1
    for m in np.arange(1,M):
        E[2*M-m]=E[2*M-m+1]+((1/2)**M)*math.factorial(M)/(math.factorial(m)*math.factorial(M-m))
    for m in np.arange(0,2*M+1):
        c[m]=(-1)**m*E[m]
    solut=0
    for k1 in np.arange(2*M+1):
        sum=0
        for k2 in np.arange(2*M+1):
            sum+=((f(beta[k1]/t1,beta[k2]/t2)+f(beta[k1]/t1,Conjugate(beta[k2])/t2)).real)*c[k2]
        solut+=c[k1]*sum
    solut*=10**(2*M/3)/2/t1/t2
    return float(solut)