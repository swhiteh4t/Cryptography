#!/usr/bin/env python
# coding: utf-8

# # Module 2:
# 
# Score rules. Please solve exercises worth at most 10 pts. For each correct execution you will receive an assigned number of points. Its sum will determine the final score.
# 
# 1. Algorithm which generates a random elliptic curve (missing: 0 pts, implmentation up to 2 pts)
# 2. Algorithm which finds a random point on an elliptic curve (missing: 0 pts, implmentation up to 1 pts)
# 3. Algorithm checking whether a point belongs to the curve (missing: 0 pts, implmentation up to 1 pts)
# 4. Algoritm generating the opposite of a point (missing: 0 pts, implmentation up to 1 pts)
# 5. Algorithm which adds two points on the curve (missing: 0 pts, implmentation up to 5 pts)
# 
# In addition, you can obtain a full score on the test no 2 (worth 10pts) if the implementation of the functions in 1-5 will use your own arithmetic implementation on large integers (which was prepared for Module 1). If you have not done such an implementation for Module 1, you can still do it in this task.

# # 1. Algorithm which generates a random elliptic curve
# Input: natural number $k>2$ which denotes the number of bits.
# 
# Output: 
# 1. Randomly chosen prime number $p$, which has $k$ bits and satisfies the condition $p\equiv 3(\textrm{mod }4)$.
# 2. Natural numbers $A,B$ in the range $0\leq A,B\leq p-1$ such that $Y^2=X^3+AX+B$ is an elliptic curve.
# 
# <b>Hint:</b> you need to check the condition $4A^3+27B^2\equiv 0(\textrm{mod }p)$. If it is true, then choose another pair, until you find $A,B for which the congruence is false.
# 
# For the prime number generation use the Fermat primality test discussed in Module 1.

# In[339]:


#Import the necesary libs
import random
import sympy as sp


# In[419]:


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


# <b> Test the generators<b>

# In[420]:


def TestFermatFun(n):
    return FermatTest(n,10000) == sp.isprime(n)

def TestPrimeGenMod4(size):
    num = PrimeGenMod4(size);
    return num,sp.isprime(num) and (num%4 == 3)

def TestPrime2GenMod4(size):
    num = PrimeGenMod4(size);
    return sp.isprime(num) and (num%4 == 3)

def primeMod4(size):
    prime = sp.randprime(3,2**size-1);
    while not(prime%4 == 3):
        prime = sp.randprime(3,2**size-1);
    return prime;
    


# In[421]:


#Check FermatTest
#all([TestFermatFun(k) for k in range(2,1000)])
#[TestFermatFun(k) for k in range(2,1000)]
#Check PrimeGen 
#[TestPrimeGenMod4(k) for k in range(4,100)]
#all([TestPrime2GenMod4(k) for k in range(4,100)])


# In[430]:


#assert 0 < a and a < p and 0 < b and b < p and p > 2
def RandEllCurve(k):
    p = PrimeGenMod4(k);
    A=random.randrange(0,p-1)
    B=random.randrange(0,p-1)
    while (((4*(A**3) + 27*(B**2))%p) == 0):
        A=random.randrange(0,p-1)
        B=random.randrange(0,p-1)
    return [A , B , p]


# In[431]:


RandEllCurve(4)


# <b> Test the implementation <b>

# In[405]:


def is_valid(a,b, q):
    return (4 * (a ** 3) + 27 * (b ** 2))  % q != 0

def validate(r):
    for i in range(4,r):
        valid = True;
        E = RandEllCurve(i);
        valid = valid and is_valid(E[0],E[1],E[2]);
    return valid;

all([validate(k) for k in range(5,30)])


# Test cases in the format `<line>` = A B p

# In[286]:


def RandABp(size):
    p=primeMod4(size);
    A=random.randrange(0,p-1)
    B=random.randrange(0,p-1)
    try:
        assert (p%4)==3
        E=EllipticCurve([GF(p)(A),B])
        return "{} {} {}".format(A,B,p)
    except:
        pass
    


# In[287]:


for _ in range(0,30):
    s=RandABp(random.choice([10,100,300]))
    if not(s==None):
        print(s)
        print("")


# # 2. Algorithm which finds a random point on an elliptic curve
# Input: 
# 1. Natural number $p$ which is prime and satisfies the condition $p\equiv 3(\textrm{mod }4)$.
# 2. Natural numbers $A,B$ in the range $0\leq A,B\leq p-1$.
# 
# Output: Randomly chosen integers $x,y$ in the range $0\leq x,y\leq p-1$ such that $(x,y)$ is a point on the elliptic curve $y^2=x^3+Ax+B$.

# In[393]:


#Square root modulo
def sqrt(n, p):
    assert n < p
    for i in range(1, p):
        if i * i % p == n:
            return (i, p - i)
        pass
    return -1,-1

def RandomPoint(A,B,p):
    cond = A < p-1 and B < p-1 and A > 0 and B > 0;
    #Natural number p which is prime and satisfies the condition p mod 4 = 3.
    if(cond and (p%4!=3) and not FermatTest(p)):
        raise Exception("Conditions are not met")
    x = random.randrange(0,p-1)
    sq = (x ** 3 + A * x + B) % p
    y1, y2 = sqrt(sq, p)
    while y1 == -1:
        x = random.randrange(0,p-1)
        sq = (x ** 3 + A * x + B) % p
        y1, y2 = sqrt(sq, p)
    y = random.choice([y1,y2]);
    return x,y
        


# In[396]:


RandomPoint(50286, 150346, 373063)


# Test cases in the format `<line>` = A B p x y

# In[67]:


def RandABpxy(size):
    p=random_prime(2**size-1,proof=True,lbound=5)
    A=randint(0,p-1)
    B=randint(0,p-1)
    try:
        assert (p%4)==3
        E=EllipticCurve([GF(p)(A),B])
        P=E.random_point()
        return "{} {} {} {} {}".format(A,B,p,P[0],P[1])
    except:
        pass
    
for _ in range(0,30):
    s=RandABpxy(random.choice([10,100,300]))
    if not(s==None):
        print(s)
        print("")


# # 3. Algorithm checking whether a point belongs to the curve
# Input: 
# 1. Natural number $p$ which is prime and satisfies the condition $p\equiv 3(\textrm{mod }4)$.
# 2. Natural numbers $A,B$ in the range $0\leq A,B\leq p-1$.
# 3. Natural numbers $x,y$ in the range $0\leq x,y\leq p-1$.
# 
# Output: TRUE, if $(x,y)$ is a point on the elliptic curve $y^2=x^3+Ax+B$.
# FALSE, otherwise.

# In[444]:


def IsPtOnEll(A,B,p,x,y):
    cond = A < p-1 and B < p-1 and A > 0 and B > 0;
    if (cond and (p%4!=3) and not FermatTest(p) ):
        raise Exception("Conditions are not met")
    return ((y**2)%p == (x**3 + A*x + B)%p)


# <b> Test all the functions together <b>

# In[447]:


def TestFunctions(r):
    res = []
    for i in range(4,r):
        EC = RandEllCurve(i);
        x,y = RandomPoint(EC[0],EC[1],EC[2])
        value = IsPtOnEll(EC[0],EC[1],EC[2],x,y)
        res.append(value)
    return res

TestFunctions(30)


# Test cases in the format `<line>` = A B p x y TRUE/FALSE

# In[88]:


def RandABpxyYN(size):
    p=random_prime(2**size-1,proof=True,lbound=5)
    A=randint(0,p-1)
    B=randint(0,p-1)
    x=randint(0,p-1)
    y=randint(0,p-1)
    try:
        assert (p%4)==3
        E=EllipticCurve([GF(p)(A),B])
        if E.is_on_curve(x,y):
            return "{} {} {} {} {} {}".format(A,B,p,x,y,"TRUE")
        else:
            return "{} {} {} {} {} {}".format(A,B,p,x,y,"FALSE")
    except:
        pass
    
for _ in range(0,30):
    s=RandABpxyYN(random.choice([10,100,300]))
    if not(s==None):
        print(s)
        print("")


# # 4. Algoritm generating the opposite of a point
# Input: 
# 1. Natural number $p$ which is prime and satisfies the condition $p\equiv 3(\textrm{mod }4)$.
# 2. Natural numbers $x,y$ in the range $0\leq x,y\leq p-1$.
# 
# Output: Pair of integers $(x_1,y_1) = (x,-y)$ such that $x\equiv x_1(\textrm{mod }p)$ and $y\equiv -y_1(\textrm{mod }p)$. 

# In[49]:


def OppPt(x,y,p):
    res = (x-p);
    return [(x,y),(y,res)]


# In[54]:


lines = [];
with open('4.txt','r') as f:
    lines = f.readlines()

for line in lines:
    l = line.split();
    _,y = OppPt(int(l[0]),int(l[1]),int(l[2]));
    print(int(l[3])==y[0] and int(l[4]) == y[1])
    #print(int(l[2]),y[0],y[1],l[3],l[4])


# Test cases in the format `<line>` = p x y x1 y1

# In[92]:


def Randpxyx1y1(size):
    p=random_prime(2**size-1,proof=True,lbound=5)
    x=randint(0,p-1)
    y=randint(0,p-1)
    return "{} {} {} {} {}".format(p,x,y,Integers(p)(x),Integers(p)(-y))
    
for _ in range(0,10):
    s=Randpxyx1y1(random.choice([10,100,300]))
    print(s)
    print("")


# # 5. Algorithm which adds two points on the curve
# Input: 
# 1. Natural number $p$ which is prime and satisfies the condition $p\equiv 3(\textrm{mod }4)$.
# 2. Natural numbers $A,B$ in the range $0\leq A,B\leq p-1$.
# 3. Natural numbers $x_1,y_1$ in the range $0\leq x_1,y_1\leq p-1$.
# 4. Natural numbers $x_2,y_2$ in the range $0\leq x_2,y_2\leq p-1$.
# 
# Pairs $P=(x_1,y_1)$ and $Q=(x_2,y_2)$ determine two points on the elliptic curve $E:y^2=x^3+Ax+B$ over the finite field $\mathbb{F}_{p}$.
# 
# Output: Coordinates $(x_3,y_3)$ which satisfy the condition $(x_3,y_3) = P\oplus Q$, where $\oplus$ denotes the addition on the elliptic curve $E$.
# 
# Hint: implement all cases, including $P=Q$ and $P=-Q$.

# In[13]:


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

def zero(x,y):
    return x == 0  and y == 0;

#Dividing is the same as multiplying by the inv
def PtSum(A,B,p,x1,y1,x2,y2):
    if(zero(x1,y1) or zero(x2,y2)):
        return (0,0)
    if x1 == x2 and (y1 != y2 or y1 == 0):
        return ("inf","inf") #p1 + (-p1) 
    if(x1 == x2 and y1 == y2):
        resX = ((3*x1**2 + A) * inv(2*y1,p))%p
        x3 = ((resX * resX) - 2 * x1) % p
        y3 = (resX * (x1-x3) - y1) %p
        return x3,y3
    else:
        resX = ((y2-y1) * inv(x2-x1,p))%p
        x3 =  (resX * resX - x1 -x2)%p
        y3 = ((y2 -y1) * inv(x2-x1,p)*(x1-x3)-y1)%p
        return x3,y3


# <b> Test sum function <b>

# In[20]:


lines = [];
with open('5.txt','r') as f:
    lines = f.readlines()

for line in lines:
    l = line.split();
    x,y = PtSum(int(l[0]),int(l[1]),int(l[2]),int(l[3]),int(l[4]),int(l[5]),int(l[6]));
    if(l[7] == "inf"):
        print(l[7]==x and l[8] == y)
    else:
        print(int(l[7])==x and int(l[8]) == y)


# Test cases in the format `<line>` = A B p x1 y1 x2 y2 x3 y3
# 
# Remark: x3 = inf, y3=inf denotes that the sum of points P and Q equals zero (i.e. x1=x2 mod p and x2=-y2 mod p)

# In[103]:


def SumPtABpx1y1x2y2x3y3(size):
    p=random_prime(2**size-1,proof=True,lbound=5)
    A=randint(0,p-1)
    B=randint(0,p-1)
    try:
        assert (p%4)==3
        E=EllipticCurve([GF(p)(A),B])
        P=E.random_point()
        Q=E.random_point()
        R=P+Q
        print("{} {} {} {} {} {} {} {} {}".format(A,B,p,P[0],P[1],Q[0],Q[1],R[0],R[1]))
        print("")
        P=E.random_point()
        R=P+P
        print("{} {} {} {} {} {} {} {} {}".format(A,B,p,P[0],P[1],P[0],P[1],R[0],R[1]))
        print("")
        P=E.random_point()
        Q=-P
        print("{} {} {} {} {} {} {} {} {}".format(A,B,p,P[0],P[1],Q[0],Q[1],"inf","inf"))
        print("")    
    except:
        pass
    
for _ in range(0,20):
    SumPtABpx1y1x2y2x3y3(random.choice([10,20,100]))

