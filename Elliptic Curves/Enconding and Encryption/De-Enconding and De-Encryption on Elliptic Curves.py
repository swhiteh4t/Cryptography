#!/usr/bin/env python
# coding: utf-8

# # Module 3:
# 
# Score rules. Please solve exercises worth at most 20 pts. For each correct execution you will receive an assigned number of points. Its sum will determine the final score.
# 
# 1. Algorithm which implements fast addition on an elliptic curve (missing: 0 pts, implmentation up to 4 pts)
# 2. Algorithm which generates generates public and private keys in the Elgamal cryptosystem (missing: 0 pts, implmentation up to 4 pts)
# 3. Algorithm which encodes and decodes a message on an elliptic curve (missing: 0 pts, implmentation up to 4 pts)
# 4. Algoritm which performs Elgamal encryption on an elliptic curve (missing: 0 pts, implmentation up to 4 pts)
# 5. Algorithm which performs Elgamal decryption on an elliptic curve (missing: 0 pts, implmentation up to 4 pts)

# In[2]:


import random


# # 1. Algorithm which implements fast addition on an elliptic curve
# Input: 
# 1. Natural number $p$ which is an odd prime.
# 2. Natural numbers $A,B$ in the range $0\leq A,B\leq p-1$ which determine an elliptic curve $E:y^2=x^3+Ax+B$.
# 3. A point $P\in E(\mathbb{F}_{p})$
# 4. An integer $n$.
# 
# Output: Point $n\cdot P$.
# 
# Hint: fast addition means that this is a "fast exponentiation for the additive group", e.g. when computing a multiple $17P$ of a given point P, run the following steps $P_n$:
# * $P_1=P$
# * $P_2=2P$
# * $P_3=2P_2$
# * $P_4=2P_3$
# * $P_5=2P_4$
# * $P_6=P_1+P_5$
# 
# In fast addition the number of actual elliptic curve additions need to compute $nP$ is equal to approximately $\log_{2}(n)$.

# In[3]:


def ExtendedGCD(a,b):
    r,r1=a,b
    s,s1=1,0 #s*a+t*b == a
    t,t1=0,1 #s1*a+t1*b == b
    while not(r1==0):
        q,r2=r//r1,r % r1
        r,s,t,r1,s1,t1=r1,s1,t1,r2,s-s1*q,t-t1*q
    d=r
    return d,s,t #s*a+t*b=d, d=GCD(a,b)

def inv(a,p):
    d,i,_ = ExtendedGCD(a,p);
    if(d!=1):
        raise Exception("The number a and p are not coprime")
    return i%p;

#Dividing is the same as multiplying by the inv
def PtSum(A,B,p,x1,y1,x2,y2):
    def zero(x,y):
        return x == 0  and y == 0;
    if(zero(x1,y1)):
        return [x2,y2]
    if(zero(x2,y2)):
        return [x1,y1]
    if x1 == x2 and (y1 != y2 or y1 == 0):
        return [0,0] #p1 + (-p1) 
    if(x1 == x2 and y1 == y2):
        resX = ((3*x1**2 + A) * inv(2*y1,p))%p
        x3 = ((resX * resX) - 2 * x1) % p
        y3 = (resX * (x1-x3) - y1) %p
        return [x3,y3]
    else:
        resX = ((y2-y1) * inv(x2-x1,p))%p
        x3 =  (resX * resX - x1 -x2)%p
        y3 = ((y2 -y1) * inv(x2-x1,p)*(x1-x3)-y1)%p
        return [x3,y3]
    
def OppPt(x,y,p):
    return [x, (-y % p)]


# In[4]:


def MultPoint(E,P,n):
        result = [0,0]
        m2 = P 
        # O(log2(n)) add
        i = abs(n)
        while 0 < i:
            if i & 1 == 1:
                result = PtSum(E[0],E[1],E[2],result[0],result[1],m2[0],m2[1])
                pass
            i, m2 = i >> 1, PtSum(E[0],E[1],E[2],m2[0],m2[1],m2[0],m2[1])
            pass
        return result if(n>0) else OppPt(result[0],result[1],E[2])
        


# <b> Test the first function <b>

# In[39]:


#114 22 149 96 19 94 51 -88
[MultPoint([114,22,149],[96,19],-88) == [94,51]
#594 434 887 507 524 337 838 772
#33 54 71 15 44 5 42 35
,MultPoint([33,54,71],[15,44],35) == [5,42]]


# In[41]:


lines = [];
with open('1.txt','r') as f:
    lines = f.readlines()

result =[]
for line in lines:
    l = line.split();
    x,y = MultPoint([int(l[0]),int(l[1]),int(l[2])],[int(l[3]),int(l[4])],int(l[7]));
    if(int(l[5]) == x and y == int(l[6])):
        result.append(True)
    else:
        result.append(False)
print(result)
    


# Test cases in the format `<line>` = A B p xcoo(P) ycoo(P) xcoo(nP) ycoo(nP) n

# In[5]:


def RandABpxy(size):
    p=random_prime(2**size-1,proof=True,lbound=5)
    A=randint(0,p-1)
    B=randint(0,p-1)
    try:
        E=EllipticCurve([GF(p)(A),B])
        P=E.random_point()
        n=randint(-p,p)
        Q=n*P
        return "{} {} {} {} {} {} {} {}".format(A,B,p,P[0],P[1],Q[0],Q[1],n)
    except:
        return None
    
    
for _ in range(0,20):
    s=RandABpxy(random.choice([10,50,100]))
    if not(s==None):
        print(s)


# # 2. Algorithm which generates generates public and private keys in the Elgamal cryptosystem
# Input: natural number $k>2$ which denotes the number of bits.
# 
# Output: 
# 1. Randomly chosen prime number $p$, which has $k$ bits and satisfies the condition $p\equiv 3(\textrm{mod }4)$.
# 2. Natural numbers $A,B$ in the range $0\leq A,B\leq p-1$ such that $Y^2=X^3+AX+B$ is an elliptic curve.
# 3. Random element $Q\in E(\mathbb{F}_{p})$ such that the order $q$ of the point $Q$ is large ($q$ has at least $k/4$ bits)
# 4. Random number $x$ in the range $1\leq x\leq q-1$.
# 5. Element $P=x\cdot Q$.
# 
# Public key is $[A,B,p,Q,P]$
# 
# Private key is $[A,B,p,Q,P,x]$
# 
# Remark: represent an elliptic curve as a triple $[A,B,p]$.

# In[5]:


#Random k-bit number generator
def gennum(size):
    li=[random.choice([0,1]) for k in range(0,size-2)]
    li.append(1)
    num=li[0]
    for el in li[1:]:
        num<<=1
        num^=el
    return num

def gcd(a,b):
    while b:
        a,b = b,a % b;
    return abs(a);

def get_coprime(n):
    while True:
        coprime = random.randrange(2,n)
        if gcd(coprime, n) == 1:
            return coprime
        else:
            return -1
        
#Returns true if prime after count rounds 
def FermatTest(n,count=100000):
    if n == 1 or n == 2: return True;
    for i in range(count):
        a = get_coprime(n)
        if(a < 0 or pow(a,n-1,n) != 1):
            return False
    return True;

def PrimeGen(size):
    num=gennum(size)
    while not FermatTest(num,size):
        num=gennum(size)
    return num

def PrimeGenMod4(size):
    if(size < 4): raise Exception("Size should be >= 4");
    num = PrimeGen(size);
    while (num <= 3) or (num%4 != 3):
        num = PrimeGen(size);
    return num

def RandEllCurve(k):
    p = PrimeGenMod4(k);
    A=random.randint(0,p-1)
    B=random.randint(0,p-1)
    while (((4*(A**3) + 27*(B**2))%p) == 0):
        A=random.randint(0,p-1)
        B=random.randint(0,p-1)
    return [A , B , p]

def zero(p):
    return p[0] == 0  and p[1] == 0;

def orderPoint(E,g):
        assert not zero(g)
        P = g;
        for i in range(1, E[2] + 1):
            P = MultPoint(E,g,i);
            if zero(P):
                return i
        return -1


#Square root modulo
#We assume that p is prime since condition 1 has to be met
def sqrt(a, p):

    def legendre_symbol(a, p):
        ls = pow(a, (p - 1) // 2, p)
        return -1 if ls == p - 1 else ls

    if legendre_symbol(a, p) != 1:
        return -1, -1
    elif a == 0:
        return -1- -1
    elif p == 2:
        return p
    elif p % 4 == 3:
        result = pow(a, (p + 1) // 4, p)
        return result, abs(p-result)

    s = p - 1
    e = 0
    while s % 2 == 0:
        s //= 2
        e += 1
    n = 2
    while legendre_symbol(n, p) != -1:
        n += 1
    x = pow(a, (s + 1) // 2, p)
    b = pow(a, s, p)
    g = pow(n, s, p)
    r = e

    while True:
        t = b
        m = 0
        for m in range(r):
            if t == 1:
                break
            t = pow(t, 2, p)

        if m == 0:
            return x,abs(p-x)

        gs = pow(g, 2 ** (r - m - 1), p)
        g = (gs * gs) % p
        x = (x * gs) % p
        b = (b * g) % p
        r = m

def RandomPointOrder(A,B,p,k):
    cond = A < p-1 and B < p-1 and A > 0 and B > 0;
    #Natural number p which is prime and satisfies the condition p mod 4 = 3.
    if(cond and (p%4!=3) and not FermatTest(p)):
        raise Exception("Conditions are not met")
    order =  k.bit_length()//4
    x = random.randint(1,p-1)
    sq = (x ** 3 + A * x + B) % p
    y1,y2 = sqrt(sq, p)
    while y1 == -1 and orderPoint([A,B,p],[x,y1]) > order:
        x = random.randrange(0,p-1)
        sq = (x ** 3 + A * x + B) % p
        y1,y2 = sqrt(sq, p)
    y = random.choice([y1,y2])
    return [x,y]
        


# <b> Test the order function

# In[93]:


#637318695 515358174 708231451 647398183 120145790 236078193
#orderPoint([637318695,515358174,708231451],[647398183,120145790])

#MultPoint([637318695,515358174, 708231451],[343306980,95157981],236078193)
#RandomPointOrder(637318695,515358174, 708231451,236078193)


# In[14]:


def ordGen(size):
        p=random_prime(2**size-1,proof=True,lbound=5)
        A=randint(0,p-1)
        B=randint(0,p-1)
        E=EllipticCurve([GF(p)(A),B])
        Q=E.random_point()
        Qord=Q.order()
        return "{} {} {} {} {} {}".format(A,B,p,Q[0],Q[1],Qord)

for _ in range(0,10):
    s=ordGen(random.choice([30,50,100]))
    if not(s==None):
        print(s)


# In[1]:


def ElgamalPubPrivateKey(k):
    E = RandEllCurve(k);
    Q = RandomPointOrder(E[0],E[1],E[2],k)
    x = randint(1,E[2]-1)
    P = MultPoint(E,Q,x)
    return [E[0],E[1],E[2],Q[0],Q[1],P[0],P[1]],[E[0],E[1],E[2],Q[0],Q[1],P[0],P[1],x]


# <b> Test the Public and Private key generation <b>

# In[ ]:





# Test cases in the format `<line>` = A B p xcoo(Q) ycoo(Q) xcoo(P) ycoo(P) x

# In[6]:


def RandABp(size):
    p=random_prime(2**size-1,proof=True,lbound=5)
    A=randint(0,p-1)
    B=randint(0,p-1)
    try:
        assert (p%4)==3
        E=EllipticCurve([GF(p)(A),B])
        return "{} {} {}".format(A,B,p),E,size
    except:
        return None, None, None


# In[64]:


for _ in range(0,30):
    sE,E,k=RandABp(random.choice([10,50,100]))
    if not(sE==None):
        Q=E.random_point()
        Qord=Q.order()
        if log(Qord,2)>k/4:
            x=randint(1,Qord-1)
            P=x*Q
            print(sE+" {} {}".format(str(Q[0]),str(Q[1]))+" {} {}".format(str(P[0]),str(P[1]))+" "+str(x))


# # 3. Algorithm which encodes and decodes a message on an elliptic curve
# Input: 
# 1. Natural number $p$ which is prime and satisfies the condition $p\equiv 3(\textrm{mod }4)$.
# 2. Natural numbers $A,B$ in the range $0\leq A,B\leq p-1$ which determine an elliptic curve $y^2=x^3+Ax+B$.
# 3. Message $M$ represented as an integer $0\leq M\leq p-1$.
# 
# Output: A point $P\in E(\mathbb{F}_{p})$ which uniquely corresponds to the message $M$.
# 
# A decoding function which extracts $M$ from the point $P$ should be implemented accordingly.
# 
# Hint: Use the following Koblitz method for the encoding:
# 
# We encode our message $M$ as a point on the curve. The first coordinate is going to be $\kappa\cdot M+j$, where our message should be $M<p/\kappa$ and $0\leq j\leq \kappa$. This guarantees we will find a suitable point in the randomized procedure (with chance of success $1-1/2^\kappa$. Coordinate $y$ is chosen in such a way that $y^2=x^3+Ax+B$, where $A,B$ are fixed, and $x=\kappa\cdot M+j$ for a fixed $j$.
# 
# Decoding procedure is very simple. We compute the floor of the expression $x/\kappa$, where $x$ is the first coordinate of a point treated as an integer.

# Koblitz’s Method for Encoding Plaintext:  
# <b>Step1: </b>Pick an elliptic curve Ep(a,b).  
# 
# <b>Step 2:</b> Let us say that E has N points on it.  
# 
# <b>Step 3:</b> Let us say that our alphabet consists of the digits 0,1,2,3,4,5,6,7,8,9 and the letters A,B,C,. . . , X,Y,Z coded as 10,11,. . . , 35.  
# 
# <b>Step 4:</b> This converts our message into a series of numbers between 0 and 35.  
# 
# <b>Step 5:</b> Now choose an auxiliary base parameter, for example k = 20. ( both parties should agree upon this)
# 
# <b>Step 6:</b> For each number mk (say), take x=mk + 1 and try to solve for y.  
# 
# <b>Step 7:</b> If you can't do it, then try x = mk +2 and then x = mk +3 until you can solve for y. 
# 
# <b>Step 8:</b> In practice, you will find  such a y before you hit x = mk + k - 1. Then take the point (x,y). This now converts the number m into a point on the elliptic curve. In this way, the entire message becomes a sequence of points.
# 

# In[42]:


kappa = 100
def EncodeMessage(A,B,p,M):
    i = 0;
    cond = A < p-1 and B < p-1 and A > 0 and B > 0;
    #Natural number p which is prime and satisfies the condition p mod 4 = 3.
    if(cond and (p%4!=3) and not FermatTest(p)):
        raise Exception("Conditions are not met")
    x = M*kappa + i;
    assert M <= p*1.0/kappa
    sq = (x ** 3 + A * x + B) % p
    y1,y2= sqrt(sq, p)
    while y1 == -1:
        i +=1;
        x = M*kappa + i;
        sq = (x ** 3 + A * x + B) % p
        y1,y2 = sqrt(sq, p)
    y = random.choice([y1,y2]);
    return [x,y] #Randomly return the two solutions


# <b>Decoding</b>: Consider each point (x,y) and set m to be the greatest integer less than (x-1)/k. Then the point (x,y) decodes as the symbol m. 

# In[43]:


def DecodeMessage(A,B,p,P):
    return (P[0]//kappa)


# In[50]:


#1423240 53550948 79956061 100 451086 45108600 27258717 True
#226183941 153555317 1058172317 100 10430154 1043015400 131170301 True
#A,B,p,kappa_default,M,P[0],P[1],floor(int(P[0])/kappa_default)==M
#EncodeMessage(1423240,53550948,79956061,451086)
EncodeMessage(226183941,153555317,1058172317,10430154)


# <b> Test encoding and decoding

# In[161]:


lines = [];
with open('3.txt','r') as f:
    lines = f.readlines()
#Format: A,B,p,kappa_default,M,P[0],P[1],floor(int(P[0])/kappa_default
for line in lines:
    l = line.split();
    P = EncodeMessage(int(l[0]),int(l[1]),int(l[2]),int(l[4]));
    M = DecodeMessage(int(l[0]),int(l[1]),int(l[2]),P)
    if(M == int(l[4])):
        print("Decoding True")
    #We check if encode using the one of the square roots(both are valid)
    if(P[0] ==int(l[5]) and (P[1] == int(l[6]) or  P[1] == (int(l[2])- int(l[6])))):
        print("Encoding True")
    else:
        print(False)


# Test cases in the format `<line>` = A B p kappa M xcoo(P) ycoo(P) floor(xcoo(P)/kappa)==M

# In[ ]:


kappa_default=100
def EncodePoint(E,M,kappa=kappa_default): #default choice of 
    p=E.base_field().characteristic() #field characteristic
    assert M <= p*1.0/kappa
    pol=E.defining_polynomial()
    for i in range(0,kappa):
        val=-pol([kappa*M+i,0,1])
        if val.is_square():
            sq=sqrt(val)
            P=E([kappa*M+i,sq,1])
            break;
    return P

def RandABpM(size):
    p=random_prime(2**size-1,proof=True,lbound=5)
    A=randint(0,p-1)
    B=randint(0,p-1)
    M=randint(0,p//kappa_default-1)
    try:
        E=EllipticCurve([GF(p)(A),B])
        P=EncodePoint(E,M)
        #P=E.random_point()
        return "{} {} {} {} {} {} {} {}".format(A,B,p,kappa_default,M,P[0],P[1],floor(int(P[0])/kappa_default)==M)
    except:
        return None
    
for _ in range(0,50):
    s=RandABpM(random.choice([30,50,100]))
    if not(s==None):
        print(s)


# # 4. Algoritm which performs Elgamal encryption on an elliptic curve
# Input: 
# 1. Elgamal public key: [A,B,p,Q,P]
# 2. Message $M$ in the range $0\leq M< p/\kappa$.
# 
# Output: Pair of two points $[C_1,C_2]$ such that $C_1,C_2\in E(\mathbb{F}_{p})$, where $E:y^2=x^3+Ax+B$. Points $C_1$ and $C_2$ are generated in the Elgamal encryption:
# 
# * $C_1= kQ$
# * $C_2= P_M+kP$
# where $P_M$ is the point in $E(\mathbb{F}_{p})$ which corresponds to the message $M$ via Koblitz method. Number $k$ is a random integer in the range $1\leq k\leq q-1$ where $q$ is the order of the group spanned by the point $Q$.

# In[60]:


#The parameter k is used for testing purpose
def ElgamalEncryption(pubKey,M,k = None):
    if k is None:
        ordQ = orderPoint([pubKey[0],pubKey[1],pubKey[2]],[pubKey[3],pubKey[4]])
        k = randint(1,ordQ-1)
    C1 = MultPoint([pubKey[0],pubKey[1],pubKey[2]],[pubKey[3],pubKey[4]],k)
    kP = MultPoint([pubKey[0],pubKey[1],pubKey[2]],[pubKey[5],pubKey[6]],k)
    Pm = EncodeMessage(pubKey[0],pubKey[1],pubKey[2],M)
    C2 = PtSum(pubKey[0],pubKey[1],pubKey[2],kP[0],kP[1],Pm[0],Pm[1])
    return C1,C2


# <b> Test the encryption

# In[67]:


# Format A,B,p,k,Q[0],Q[1],P[0],P[1],M,C1[0],C1[1],C2[0],C2[1]
#72430575234 388902348160 957539244583 541519234450 702908564070 
#285673913620 105397737825 862356557624 992924412 789931156438 753079547362 681436617015 178076914511

#A 899032443106465921 B 745977192800804106 p 1051129676017180999 
#Q 540127693309210187 Q 547626402986451839 P 474853327894596912 P 696364976948956441 
#C1 1029806611001703874 C1 641200053906280815 C2 784621230359049493 C2 613185836129273435 
#M 9569093767723591 x 92619739148387228 k 114545422595536685
C1,C2 = ElgamalEncryption([899032443106465921,745977192800804106,1051129676017180999
                           ,540127693309210187,547626402986451839,
                           474853327894596912,696364976948956441,
                  ],9569093767723591,114545422595536685);
print(C1[0],C1[1],C2[0],C2[1])
print(C1[0]==1029806611001703874 and C1[1]==641200053906280815 and C2[0]==784621230359049493 and C2[1] == 613185836129273435)


# In[68]:


lines = [];
with open('4.txt','r') as f:
    lines = f.readlines()
#Format: format(A,B,p,k,Q[0],Q[1],P[0],P[1],M,C1[0],C1[1],C2[0],C2[1])
for line in lines:
    l = line.split();
    i = 0;
    #Try more than once to find the square root modulo p that we expect
    while True:
        C1,C2 = ElgamalEncryption([int(l[0]),int(l[1]),int(l[2]),int(l[4]),int(l[5]),int(l[6]),int(l[7]),
                                  ],int(l[8]),int(l[3]));
        i +=1;
        if(C1[0] == int(l[9]) and C1[1] == int(l[10]) and C2[0] == int(l[11]) and C2[1] == int(l[12])):
            print(True)
            break;
        if(i ==20):
            print(False)
            break;


# Test cases in the format `<line>` = A B p xcoo(Q) ycoo(Q) xcoo(P) ycoo(P) M xcoo(C1) ycoo(C1) xcoo(C2) ycoo(C2)

# In[ ]:


kappa_default=100
def EncodePoint(E,M,kappa=kappa_default): #default choice of 
    p=E.base_field().characteristic() #field characteristic
    assert M <= p*1.0/kappa
    pol=E.defining_polynomial()
    for i in range(0,kappa):
        val=-pol([kappa*M+i,0,1])
        if val.is_square():
            sq=sqrt(val)
            P=E([kappa*M+i,sq,1])
            break;
    return P

def RandABpQPMC1C2(size):
    p=random_prime(2**size-1,proof=True,lbound=5)
    A=randint(0,p-1)
    B=randint(0,p-1)
    try:
        assert (p%4)==3
        E=EllipticCurve([GF(p)(A),B])
        Q=E.random_point()
        Qord=Q.order()
        assert log(Qord,2)>size/4
        x=randint(1,Qord-1)
        P=x*Q
        M=randint(0,p//kappa_default-1)
        PM=EncodePoint(E,M)
        k=randint(1,Qord-1)
        C1=k*Q
        C2=PM+k*P
        return "{} {} {} {} {} {} {} {} {} {} {} {} {}".format(A,B,p,k,Q[0],Q[1],P[0],P[1],M,C1[0],C1[1],C2[0],C2[1])
    except:
        return None
for _ in range(0,30):
    s=RandABpQPMC1C2(random.choice([40,60,100]))
    if not(s==None):
        print(s)


# # 5. Algorithm which performs Elgamal decryption on an elliptic curve
# Input: 
# 1. Elgamal private key: $[A,B,p,Q,P,x]$
# 2. Elgamal encryption pair: $[C_1,C_2]$
# 
# Output: Plain message $M$ represented by an integer in the range $0\leq M\leq p/\kappa$.
# 
# Elgamal decryption follows the steps:
# * $P_M=C_2-xC_1$
# * $M=\textrm{floor}(x(P_M)/\kappa)$

# In[158]:


kappa =100
def DecryptElgamal(privKey,cryptogram):
    xC1 = MultPoint([privKey[0],privKey[1],privKey[2]],[cryptogram[0],cryptogram[1]],privKey[7]);
    Pm = PtSum(privKey[0],privKey[1],privKey[2],cryptogram[2],cryptogram[3],xC1[0],-xC1[1])
    return DecodeMessage(privKey[0],privKey[1],privKey[2],
        MultPoint([privKey[0],privKey[1],privKey[2]],Pm,privKey[7]))


# In[160]:


#A 899032443106465921 B 745977192800804106 p 1051129676017180999 
#Q 540127693309210187 Q 547626402986451839 P 474853327894596912 P 696364976948956441 
#C1 1029806611001703874 C1 641200053906280815 C2 784621230359049493 C2 613185836129273435 
#M 9569093767723591 x 92619739148387228 k 114545422595536685


# Test cases in the format `<line>` = A B p xcoo(C1) ycoo(C1) xcoo(C2) ycoo(C2) M

# In[5]:


import random
kappa_default=100
def EncodePoint(E,M,kappa=kappa_default): #default choice of 
    p=E.base_field().characteristic() #field characteristic
    assert M <= p*1.0/kappa
    pol=E.defining_polynomial()
    for i in range(0,kappa):
        val=-pol([kappa*M+i,0,1])
        if val.is_square():
            sq=sqrt(val)
            P=E([kappa*M+i,sq,1])
            break;
    return P

def RandABpC1C2M(size):
    p=random_prime(2**size-1,proof=True,lbound=5)
    A=randint(0,p-1)
    B=randint(0,p-1)
    try:
        assert (p%4)==3
        E=EllipticCurve([GF(p)(A),B])
        Q=E.random_point()
        Qord=Q.order()
        assert log(Qord,2)>size/4
        x=randint(1,Qord-1)
        P=x*Q
        M=randint(0,p//kappa_default-1)
        PM=EncodePoint(E,M)
        k=randint(1,Qord-1)
        C1=k*Q
        C2=PM+k*P
        assert floor(int((C2-x*C1)[0])/kappa_default)==M
        return "A {} B {} p {} Q {} Q {} P {} P {} C1 {} C1 {} C2 {} C2 {} M {} x {} k {} \n".format(A,B,p,Q[0],Q[1],P[0],P[1],C1[0],C1[1],C2[0],C2[1],M,x,k)
    except:
        return None
for _ in range(0,40):
    s=RandABpC1C2M(random.choice([40,60,100]))
    if not(s==None):
        print(s)


# In[ ]:




