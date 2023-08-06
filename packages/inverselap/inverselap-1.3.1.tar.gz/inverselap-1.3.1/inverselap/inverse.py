from mpmath import *
import numpy as np 
import math
from scipy.fftpack import fft,ifft
from unittest import result
import scipy


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

    #定义π
pi=math.pi

def conj(x):
    return x.real-j*x.imag

def fs_2d(s1,s2):
    s1=complex(s1.real,s1.imag)
    s2=complex(s2.real,s2.imag)
    return exp(0-2*s1-s2)/s1/s2

def epsilon(f,t1,t2,alpha1,alpha2):

    def get_G1(P,M1,N1,N2,Fv1,T1,Omega1):
        #epsilonG1 = zeros(2*P+1,2*P+2,M1,N2+2*P)
        epsilonG1=[[[[0+0*j for i in np.arange(N2+2*P)] for i in np.arange(M1)] for i in np.arange(2*P+2)] for i in np.arange(2*P+1)]
        #epsilonG1(:,1,:,:) = zeros(2*P+1,M1,N2+2*P)
        
        
        for n2 in np.arange(1,N2+2*P+1):

            TEMP = np.fft.fft( Fv1[0:N1][n2-1 ] )
            for i in np.arange(N1):
                TEMP[i]=conj(TEMP[i])
            TEMP[1:N1]= TEMP[1:N1][::-1]  
   
            for i in np.arange(M1):
                

                epsilonG1[0][1][int(i)][int(n2-1)]=TEMP[int(i)]
            

        for s in np.arange(1,2*P+1):
            En1k1=[ math.exp(j*(N1+s-1)*k*T1*Omega1) for k in np.arange(M1)  ]
            #epsilonG1(s+1,2,:,:) = epsilonG1(s,2,:,:) + reshape(kron(Fv1(N1+s,:),En1k1'),1,1,M1,N2+2*P);
            epsilonG1[s,1,:,:]=epsilonG1[s-1,1,:,:]+(np.kron( Fv1[N1+s-1,:],np.matrix(En1k1).T.conjugate() )).reshape(1,1,M1,N2+2*P)
        
        for r in np.arange(1,2*P+1):
            for s in np.arange(2*P-r+1):
                # epsilonG1(s+1,r+2,:,:) = epsilonG1(s+2,r,:,:) + (epsilonG1(s+2,r+1,:,:) - epsilonG1(s+1,r+1,:,:)).^-1
                temp=epsilonG1[s+1,r,:,:] - epsilonG1[s,r,:,:]
                for i in np.arange(len(epsilonG1[s+1,r,:,0])):
                    for k in np.arange(len(epsilonG1[s+1,r,0,:])):
                        temp[i,k]=1/(temp[i,k])
                epsilonG1[s,r+1,:,:]=epsilonG1[s+1,r-1,:,:]+ temp
        G1 = np.array(epsilonG1[int(0)][int(2*P+1)][:][:]).reshape(int(M1),int(N2+2*P))
        
        return G1
        
        
    

    
    def get_G2(Fv2,P,M2,N1,N2,T2,Omega2):

        epsilonG2=[[[[0+0*j for i in np.arange(M2)] for i in np.arange(N1+2*P)] for i in np.arange(2*P+2)] for i in np.arange(2*P+1)]

        for n1 in np.arange(1,N1+2*P+1):
            TEMP = np.fft.fft(Fv2[int(n1-1)][0:int(N2)])
         
            for i in np.arange(M2):

                epsilonG2[0][1][int(n1-1)][int(i)]=TEMP[int(i)]
        
        for s in np.arange(1,2*P+1):
            En2k2_herm =matrix([math.exp(j*(N2+s-1)*k*T2*Omega2) for k in np.arange(M2)]).conjugate() 
            epsilonG2[s,1,:,:] = epsilonG2[s-1,1,:,:] + (np.kron(Fv2[:,N2+s-1],En2k2_herm)).reshape(1,1,N2+2*P,M2)
        for r in np.arange(1,2*P+1):
            for s in np.arange(2*P-r+1):
                temp=epsilonG2[s+1,r,:,:] - epsilonG2[s,r,:,:]
                for i in np.arange(len(epsilonG2[s+1,r,:,0])):
                    for k in np.arange(len(epsilonG2[s+1,r,0,:])):
                        temp[i,k]=1/(temp[i,k])
                epsilonG2[s,r+1,:,:] = epsilonG2[s+1,r-1,:,:] + temp
        G2 = np.array(epsilonG2[0][int(2*P+1)][:][:]).reshape(int(N1+2*P),int(M2))
        return G2

    def get_G12(G1,P,M1,M2,N2,T2,Omega2):
        
        G1_herm = matrix(G1).conjugate()
        epsilonG12=[[[[0+0*j for i in np.arange(M2)] for i in np.arange(M1)] for i in np.arange(2*P+2)] for i in np.arange(2*P+1)]
        
        
        for n1 in np.arange(1,M1+1):
            TEMP = np.fft.fft(G1_herm[n1-1,0:N2])


            for i in np.arange(M2):
                epsilonG12[0][1][int(n1-1)][int(i)]=TEMP[int(i)]

        for s in np.arange (1,2*P+1):
            En2k2_herm =  matrix([ math.exp(j*(N2+s-1)*k*T2*Omega2) for k in np.arange(M2) ] ) .conjugate() 
            epsilonG12[s,1,:,:] = epsilonG12[s-1,1,:,:] + np.kron(G1_herm[:,N2+s-1],En2k2_herm).reshape(1,1,M1,M2)                   
        for r in np.arange(1,2*P+1):
            for s in np.arange(2*P-r+1):
                temp=epsilonG12[s+1,r,:,:] - epsilonG12[s,r,:,:]
                for i in np.arange(len(epsilonG12[s+1,r,:,0])):
                    for k in np.arange(len(epsilonG12[s+1,r,0,:])):
                        temp[i,k]=1/(temp[i,k])
                epsilonG12[s,r+1,:,:] = epsilonG12[s+1,r-1,:,:]+temp
        G12 = np.array(epsilonG12[0][int(2*P+1)][:][:]).reshape(int(M1),int(M2))
        return G12

    def get_G21(G2,P,M1,M2,N1,T1,Omega1):
        epsilonG21=[[[[0+0*j for i in np.arange(M2)] for i in np.arange(M1)] for i in np.arange(2*P+2)] for i in np.arange(2*P+1)]
        
        for n2 in np.arange(1,M2+1):
            TEMP = np.fft.fft(G2[0:int(N1),int(n2-1)])
            
            for i in np.arange(M2):
                epsilonG21[0][1][int(i)][int(n2-1)]=TEMP[int(i)]
      
        for s in np.arange(1,2*P+1):
            En1k1 = [math.exp(j*(N1+s-1)*k*T1*Omega1) for k in np.arange(M1)]
            epsilonG21[s,1,:,:] = epsilonG21[s-1,2-1,:,:] + np.kron(G2[N1+s-1,:],np.array(matrix(En1k1).T.conjugate()) ).reshape(1,1,M1,M2)
        for r in np.arange(1,2*P+1):
            for s in np.arange(2*P-r+1):
                temp=epsilonG21[s+1,r,:,:] - epsilonG21[s,r,:,:]
                for i in np.arange(len(epsilonG21[s+1,r,:,0])):
                    for k in np.arange(len(epsilonG21[s+1,r,0,:])):
                        temp[i,k]=1/(temp[i,k])
                epsilonG21[s,r+1,:,:] = epsilonG21[s+1,r-1,:,:] +temp
        G21 = np.array(epsilonG21[0][int(2*P+2-1)][:][:]).reshape(int(M1),int(M2))

        return G21

    P=0
    m1=7
    m2=7
    N1=2**m1
    N2=2**m2
    M1=N1/2
    M2=N2/2
    t1_max=2*t1
    t2_max=2*t2
    T1=t1_max/(M1-1)
    T2=t2_max/(M2-1)
    Omega1=2*pi/N1/T1
    Omega2=2*pi/N2/T2
    alpha1=0
    alpha2=0
    err=10**(-2)
    c1=alpha1-Omega1/2/pi*math.log(err/2)
    c2=alpha2-Omega2/2/pi*math.log(err/2)

    Fv1=[[0 for i in np.arange(N2+2*P)] for i in np.arange(N1+2*P)]
    Fv2=[[0 for i in np.arange(N2+2*P)] for i in np.arange(N1+2*P)]
    G1 =[[0 for i in np.arange(N2    )] for i in np.arange(N1    )]

    for n1 in np.arange(1,N1+2*P+1):
        for n2 in np.arange(1,N2+2*P+1):
            
            Fv1[n1-1][n2-1]=f(c1-j*(n1-1)*Omega1,c2+j*(n2-1)*Omega2)
            Fv2[n1-1][n2-1]=f(c1-j*(n1-1)*Omega1,c2-j*(n2-1)*Omega2)
   
    Ck1=[0 for i in np.arange(M1)]
    for k in np.arange(M1):
        Ck1[int(k)]=Omega1/2/pi*math.exp(c1*k*T1)
    Ck1=np.array(matrix(Ck1).T.conjugate())

    Ck2=[0 for i in np.arange(M2)]
    for k in np.arange(M2):
        Ck2[int(k)]=Omega2/2/pi*math.exp(c2*k*T1)

    Ck12=np.kron(Ck1,Ck2)
    
    Fv1_00=Fv1[0][0]
    G00 = [[Fv1_00 for i in np.arange(M2)] for i in np.arange(M1)]

    G1 = get_G1(P,M1,N1,N2,Fv1,T1,Omega1)
    G12 = get_G12(G1,P,M1,M2,N2,T2,Omega2)
    G2 = get_G2(Fv2,P,M2,N1,N2,T2,Omega2)
    G21 = get_G21(G2,P,M1,M2,N1,T1,Omega1)

    G11 = np.kron(np.ones(int(M2)),np.array(G1[0:int(M1),0]))
    G22 = np.kron(np.ones((int(M1),1)),np.array(G2[0,0:int(M2)]))
    temp=matrix(G11.reshape(int(2**m1/2),int(2**m2/2))).T
    G11=[[0+0*j for i in np.arange(int(2**m2/2))] for i in np.arange(int(2**m1/2))]
    for i in np.arange(int(2**m1/2)):
        for k in np.arange(int(2**m2/2)):

            G11[i][k]=temp[i,k]
    TEMP=G12[0:int(M1)][0:int(M2)] + G21[0:int(M1)][0:int(M2)] - G11 - G22
    TEMP=matrix(TEMP)+matrix(TEMP).conjugate()
    ans = Ck12.reshape(int(2**m1/2),int(2**m2/2)) * ( np.array(TEMP).reshape((int(2**m1/2),int(2**m2/2))) + np.array(G00)  )
    posit1=int(t1/T1)
    posit2=int(t2/T2)
    return ans[posit1][posit2].real
