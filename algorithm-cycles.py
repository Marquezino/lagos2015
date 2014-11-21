import sys
import random
from math import log,factorial
from sympy.combinatorics import Permutation,Cycle

def main(argv=None):
    f=open('result.txt',mode='w')   

    n = 3
    I = Permutation([], size=2**n)  

    pi = I + 1
    pi_final = I

    while pi!=pi_final:   
    
        print(pi.rank(),' ====> ',pi)   
        dist=calcula_dist(pi)
        if dist==0 and pi!=I:
            print('Error! Could not solve.',file=f,flush=True)
            print('Error! Could not solve.',pi)
            break
        print(dist)
        print(dist,file=f,flush=True)
        search_seq(pi)

        pi=pi+1

def calcula_dist(pi):
    I = Permutation([], size=pi.size)

    countPorts=0    

    while pi != I:
        atempt = search_2move(pi)
        if atempt != None:
            pi = atempt
            countPorts+=1
            continue
        
        atempt = search_0move(pi)
        if atempt != None:
            pi = atempt
            countPorts+=1
            continue

        atemp,aux = search_seq(pi)
        if aux != 0:
            pi = atemp
            countPorts+=aux
            continue

        print('Error! Could not solve.', pi, '\n')
        return 0

    return countPorts


def search_2move(pi):
    I=Permutation([], size=pi.size)
    T_temp=I
    n = int(log(pi.size,2))
    dmin=pi.size
    pi_return = None
    for cycle in pi.cyclic_form:
        for element in cycle:
            for i in range(len(cycle)):
                if element==cycle[i]:
                    d_atual=dh_int_int(cycle[i-1], cycle[i])
            for neighbor in neighbors(element, n):
                piaux = pi*T(element, neighbor)
                if dh_perm_perm(piaux) < dh_perm_perm(pi): 
                    if pi_return == None:   
                        pi_return = piaux
                    if P(piaux)>P(pi) and d_atual<dmin: 
                        dmin=d_atual
                        pi_return=piaux

                    T_temp=T(element, neighbor)
    return pi_return


def search_0move(pi):
    n = int(log(pi.size,2))
    dmin=pi.size
    pi_return = None
    for cycle in pi.cyclic_form:
        for element in cycle:
            for i in range(len(cycle)):
                if element==cycle[i]:
                    d_atual=dh_int_int(cycle[i-1], cycle[i])
            for neighbor in neighbors(element, n):
                piaux = pi*T(element, neighbor)
                if dh_perm_perm(piaux) == dh_perm_perm(pi) and P(piaux) < P(pi):
                    if d_atual<dmin:
                        dmin=d_atual
                        pi_return=piaux
    return pi_return


def search_seq(pi):
    for cycle in pi.cyclic_form:
        countPorts = 0        
        flagServe=0
        if len(cycle)==2:   
            break
        beginSeq = len(cycle)  
        endSeq = len(cycle)    

        for i in range(len(cycle)):
            if dh_int_int(cycle[i-1], cycle[i])!=1:
                if beginSeq == len(cycle):   
                    beginSeq = i-1
                elif endSeq == len(cycle):   
                    endSeq = i-1

                if endSeq<len(cycle):      
                    if dh_int_int(cycle[beginSeq], cycle[endSeq])==1:     
                        piaux=pi
                        for j in range(beginSeq+1,endSeq):
                            piaux = piaux*T(cycle[j],cycle[j+1])   
                            countPorts += 1 

                        print(cycle,beginSeq,endSeq)
                        return piaux,countPorts   
                    else:
                        beginSeq = endSeq      
                        endSeq =len(cycle)+1   

        if beginSeq == len(cycle):  

            piaux=pi
            for i in range(len(cycle)-1):
                piaux = piaux*T(cycle[i-1],cycle[i])
                countPorts += 1

            return piaux,countPorts
        elif endSeq == len(cycle):    

            piaux=pi
            for i in range(beginSeq+1,len(cycle)-1):
                piaux = piaux*T(cycle[i],cycle[i+1])
                countPorts += 1

            for i in range(beginSeq+1):
                piaux = piaux*T(cycle[i-1],cycle[i])
                countPorts += 1

            return piaux,countPorts
    return None,0


def P(perm):
    aux = 0
    for cycle in perm.cyclic_form:
        aux += S(cycle)/len(cycle)
    return aux

def S(cycle):
    size = len(cycle)
    aux = 0
    for i in range(size):
        aux += dh_int_int(cycle[i-1], cycle[i])
    return aux

def neighbors(a, size):
    aux = []
    for i in range(size):
        aux.append(a ^ (1<<i))
    return aux

def dh_perm_perm(p, q=None):

    if q is None:
        q = Permutation([], size=p.size)
    elif p.size != q.size:
        raise ValueError('permutations must be of same sizes')

    dist = 0
    for i in range(p.size):
        pi = p.array_form[i]
        qi = q.array_form[i]
        dist += dh_int_int(pi, qi)

    return dist

def dh_perm_int(p, a):
    return dh_int_int(p.array_form[a], a)

def dh_int_int(a, b, bits=32):
    x = a ^ b
    return sum((x>>i & 1) for i in range(bits))

def T(i,j):
    if dh_int_int(i,j)==1:
        return Permutation(i,j)
    else:
        raise ValueError('Invalid Transposition!!')
        return 0
    
def unicyclic(n,index=0):
    sigma = Permutation([], size=(2**n)-1) 
    sigma = sigma+index
    return Permutation(list(Permutation([sigma.list(2**n)])))

if __name__ == "__main__":
    sys.exit(main())

