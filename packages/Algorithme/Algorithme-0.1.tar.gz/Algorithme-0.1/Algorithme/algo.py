def somme(*nombres:int) -> int:
        """some(*nombres): founction qui calcule la somme d'un ou plus des nombre """
        sm=0
        for nombre in nombres:
            sm+=nombre
        return sm


def produit(nomb1:int,nomb2:int) -> int:
        """produit(nomber1,nomber2): founction qui calcule le produit de nomber1 * nomber2"""
        return nomb1*nomb2

    
def puissance(nomber1:int,nombre2:int) -> int:
        """ puissance(A, B): founction qui calcule le puissance A ** B"""
        return nomber1**nombre2

def factorielle(nombre:int) -> int:
        """factorielle(A): founction qui calcule la factorielle d'un nombre A! """
        fact=1
        for i in range(2,nombre+1):
            fact*=i
        return fact


def plusGrand(*nombers:int,inverser=False) -> int:
        """plusGrand(*nombers(n:nomber), inverser=False): founction qui retourner la valeur le plus grand ou plus petit si (inverser=true)"""
        p=[i for i in nombers]
        if inverser:
            return min(p)
        else:
            return max(p)




def valeurAbsolue(nomber):
        """valeurAbsolue(A): founction qui retourner la valeur absolue de A"""
        if nomber<0:
            return -nomber
        else:
            return nomber


def prixTTC(q: int,prix: int,tva,remise=0):
        """prixTTC(qantite,prix de unite , tva en (%), remise=0 (%)): founction qui calcule le prix TTC d un produit"""
        TTC = q*prix+(q*prix*tva)/100
        if remise==0:
            return TTC
        else:
            return TTC - TTC*remise/100


def nomberPremier(nomber:int) -> bool:
        """nomberPremier(A): founction qui vérifie si un nombre est premier(True) ou non(False)"""
        c=0
        for i in range(1,nomber+1):
            if nomber%i==0:
                    c+=1
        if c==2:
            return True
        else:
            return False


def nomberPair(nomber: int) -> bool:
        """nomberPair(A:entier): founction qui vérifie si un nombre est pair(True) ou non(False)"""
        if nomber%2==0:
            return True
        else:
            return False


def nomberImpair(nomber: int) -> bool:
        """nomberImpair(entier): founction qui vérifie si un nombre est Impair(True) ou non(False)"""
        if nomber%2==0:
            return False
        else:
            return True


def nomberParfait(nomber: int) -> bool:
        """nomberParfait(entier): founction qui vérifie si un nombre est Parfait(True) ou non(False)"""
        sm=0
        for i in range(1,nomber):
            if nomber%i ==0:
                sm+=i
        if sm ==nomber:
            return True
        else:
            return False


def doubleNomber(nomber: int) -> int:
        """ doubleNombre(A:entier): founction qui retourner le double d'un nomber"""
        return nomber*2


def toutlesDivi(nomber) -> list:
        """toutlesDivi(nomber): founction qui retourner toute les diviseurs d'un nombre """
        div=[] 
        for i in range(1,nomber+1):
            if nomber%i==0:
                div.append(i)
        return div


def nomberFrere(nomb1: int,nomb2: int) -> bool:
        """nomberFrere(nomberA,nomberB):founction qui vérifie si nomberA est nombreB sont  Frere(True) ou non(False)"""
        c = 0
        nomb1 = list(str(nomb1))
        for i in range(len(nomb1)):
            if nomb1[i] in str(nomb2):
               c+=1
        if c == len(nomb1):
            return True
        else:
            return False


def nombresAmis(numA:int,numB:int) -> bool:
        """nomberAmis(nomberA,nomberB): founction qui vérifie si nomberA est nombreB sont  Amis(True) ou non(False)"""
        deviA = []
        deviB = []
        for i in range(1,numA+1):
            if numA%i==0:
                deviA.append(i)
        for i in range(1,numB+1):
                if numB%i==0:
                    deviB.append(i)
        if sum(deviA) == sum(deviB):
            return True
        else:
            return False

def anneBissextile(anne: int) -> bool:
        """anneBissextile(anne): founction qui vérifie si l'anne est bissextile(True) ou non(False)"""
        if anne % 4 == 0 and anne % 100 != 0:
            return True
        else:
            return False


def triangledePascal(n: int) -> print:
        """triangledePascal(n): founction qui permet de réaliser un triangle de Pascal avec (n) line"""
        l1=[[1],[1,1]]
        for i in range(n-1):
            m=len(l1)
            f=[]
            f.append(1)
            x=0
            for j in range(1,len(l1[m-1])):
                f.append((l1[m-1][x]+l1[m-1][j]))
                x+=1
            f.append(1)
            l1.append(list(f))
        for i in range(len(l1)-1):
            for x in range(len(l1[i])):
                print(l1[i][x],end=' ')
            print()


def PGCD(nomb1: int,nomb2: int) -> int:
        """pgcd(nomberA,nomberB): founction qui retourner le pgcd de deux nombres"""
        pgcd = list()
        d1=toutlesDivi(nomb1)
        d2=toutlesDivi(nomb2)
        for i in d1:
            if i in d2:
                pgcd.append(i)
        return pgcd[-1]

def suitedeFibonacci(n: int,U0: int,U1: int) -> list:
        """suitedeFibonacci(n,UB,UA): return un list des suite de Fibonacci de n nomber, NB: Un=UB+UA"""
        Un=[U1]
        for i in range(n-1):
            UN = U1+U0
            U0=U1
            U1=UN
            Un.append(UN)
        return Un


def nombresPalindrome(nomber:int) -> bool:
    """nombresPalindrome(nomber):founction qui vérifie si un nombre est palindrome(True) ou non(False)"""
    ns=str(nomber)[::-1]
    if int(ns)==nomber:
        return True
    else:
        return False


def calculeMoyenne(*elements):
        p=0
        for ele in elements:
            p+=ele
        return p/len(elements)


def eleveMoyennne(note,coef):
        return (note/coef)


def calculeEquation():
    """calcule les solutions d_une équation du second degré"""
    pass
