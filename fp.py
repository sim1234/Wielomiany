#!/usr/bin/python
# coding: utf-8

#       This file is part of X-enon.

#        X-enon is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.

#       X-enon is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.

#       You should have received a copy of the GNU General Public License
#       along with X-enon; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from math import sqrt, fabs
import pygame, copy, threading, re, wx

def nm(z):
    z = float(z)
    if z==int(z):
        z = int(z)
    return z

def sr(z, pr="+"):
    z = nm(z)
    if z>=0:
        return pr+str(z)
    else:
        return str(z)
def ig(z, inn, isf=None, sf="", pr="+"):
    z = nm(z)
    if z==inn:
        return ""
    elif abs(z)==isf:
        c=sr(z, pr)[0]
        if c in ("+", "-"):
            return c + sf
        else:
            return sf
    else:
        return sr(z, pr) + sf

class funkcja(object):
    def __init__(self, f, px, py, color=(0,0,255), s=1):
        self.f = f
        self.px = px
        self.py = py
        self.s = s
        self.c = color
        if type(self.f) != int:
            self.pkt = []
            for x in range(px,py+1):
                print x
                self.pkt.append((x, 200.0-f(x/(10.0*s)-20.0/s)*10.0*s))
            
    def rysuj(self, srfc):
        if type(self.f) != int:
            pygame.draw.aalines(srfc, self.c, 0, self.pkt, 1)
        else:
            pygame.draw.circle(srfc, self.c, (self.px, self.py), self.f)

class wykres(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.x = 400
        self.y = 400
        self.s = 1
        self.start()
        self.fn = []

    def dodaj(self, f, px=None, py=None, color=(0,0,255)):
        if px == None:
              px = 0
        if py == None:
              py = self.x+1
        self.fn.append(funkcja(f,px,py,color,self.s))
        
    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((self.x,self.y))
        pygame.display.set_caption("Wykres")
        clock = pygame.time.Clock()
        q = 0
        while not q:
            clock.tick(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    q = 1
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                        q = 1
 
            screen.fill((255,255,255))
            pygame.draw.line(screen, (0,0,0), (0,self.y/2), (self.x,self.y/2),1) #x
            pygame.draw.lines(screen, (0,0,0), 0, ((self.x-10,self.y/2-10), (self.x,self.y/2), (self.x-10,self.y/2+10)), 1)
            for y in range(0, 41):
                if y%5==0:
                    pygame.draw.line(screen, (0,0,0), (self.x/2-5,y*10*self.s), (self.x/2+5,y*10*self.s),1)
                else:
                    pygame.draw.line(screen, (0,0,0), (self.x/2-2,y*10*self.s), (self.x/2+2,y*10*self.s),1)
            for x in range(0, 41):
                if x%5==0:
                    pygame.draw.line(screen, (0,0,0), (x*10*self.s,self.y/2-5), (x*10*self.s,self.y/2+5),1)
                else:
                    pygame.draw.line(screen, (0,0,0), (x*10*self.s,self.y/2-2), (x*10*self.s,self.y/2+2),1)
            pygame.draw.line(screen, (0,0,0), (self.x/2,0), (self.x/2,self.y),1) #y
            pygame.draw.lines(screen, (0,0,0), 0, ((self.x/2-10,10), (self.x/2,0), (self.x/2+10,10)), 1)
            font = pygame.font.Font(None, 20)
            text = font.render("X",True,(0,0,0))
            screen.blit(text, (self.x-20,self.y/2-12))
            text = font.render("Y",True,(0,0,0))
            screen.blit(text, (self.x/2+1,10))
            text = font.render(str(int(self.s)),True,(0,0,0))
            screen.blit(text, (self.x/2+6,self.y/2-15))
            for k in self.fn:
                k.rysuj(screen)
            
            pygame.display.flip()
 
        pygame.quit()

class wielomian(object):
    def __init__(self, *args): # inicjalizacja. Podawać współczynniki malejąco
        self.wsp = []
        for k in args:
            self.wsp.append(k)
        self.wsp.reverse()
        self.nm()

    def nm(self):
        while len(self.wsp)>1 and self.wsp[-1]==0:
            self.wsp.pop(-1)
        x = len(self.wsp)-1
        while x>=0:
            self.wsp[x] = nm(self.wsp[x])
            x -= 1

    def stopien(self):
        return len(self.wsp)
    
    def __str__(self):
        l = len(self.wsp)-1
        i = l
        r = ""
        if l>=2:
            r += ig(self.wsp[i], 0, 1, "x^"+str(i), "")
            i -= 1
        while i > 1:
            r += ig(self.wsp[i], 0, 1, "x^"+str(i))
            i -= 1
        if l>1:
            r += ig(self.wsp[1], 0, 1, "x")
        if l==1:
            r += ig(self.wsp[1], 0, 1, "x", "")
        if l>0:
            r += ig(self.wsp[0], 0)
        else:
            r += str(nm(self.wsp[0]))
        return r

    def __repr__(self):
        return self.__str__()
    
    def __call__(self, x):
        r = 0
        i = 0
        for k in self.wsp:
            r += k*(x**i)
            i += 1
        return r

    def __getitem__(self, key):
        if type(key)==int:
            if key<len(self.wsp):
                return self.wsp[key]
            else:
                return 0
        else:
            raise TypeError, "Expected int, got " + str(type(key))
        
    def __setitem__(self, key, value):
        self.wsp[key] = value
        self.nm()
        
    def dowsp(self, value):
        self.wsp.append(value)
        self.nm()

    def __add__(self, other):
        if type(other) in (int, float):
            a = copy.deepcopy(self)
            a.wsp[0] += other
            a.nm()
            return a
        elif type(other)==wielomian:
            if len(self.wsp)>=len(other.wsp):
                a = copy.deepcopy(self)
                b = other
            else:
                a = copy.deepcopy(other)
                b = self
            i = 0
            while i<len(b.wsp):
                a.wsp[i] += b.wsp[i]
                i += 1
            a.nm()
            return a 
        else:
            raise TypeError, "Expected int, long, float or wielomian, got " + str(type(other))
        
    def __sub__(self, other):
        if type(other) in (int, float, long, wielomian):
            return self.__add__(other*-1)
        else:
            raise TypeError, "Expected int, long, float or wielomian, got " + str(type(other))
        
    def __mul__(self, other):
        if type(other) in (int, float, long):
            a = copy.deepcopy(self)
            i = 0
            while i<len(a.wsp):
                a.wsp[i] *= other
                i += 1
            a.nm()
            return a
        elif type(other) == wielomian:
            a = wielomian()
            a.wsp = [0]*(len(self.wsp)+len(other.wsp)-1)
            i = len(self.wsp)-1
            while i>=0:
                j = len(other.wsp)-1
                while j>=0:
                    a.wsp[i+j]+=self.wsp[i]*other.wsp[j]
                    j -= 1
                i -= 1
            a.nm()
            return a
        else:
            raise TypeError, "Expected int, long, float or wielomian, got " + str(type(other))
        
    def dziel(self, other):
        a = copy.deepcopy(self)
        wn = wielomian(0)
        wn.wsp = [0]*len(a.wsp)
        while len(a.wsp)>=len(other.wsp):
            c = wielomian(0)
            c.wsp = [0]*(len(a.wsp)-len(other.wsp)+1)
            c.wsp[len(a.wsp)-len(other.wsp)] = a.wsp[-1]/float(other.wsp[-1])
            wn += c
            a -= other*c
        wn.nm()
        return (wn, a)
    
    def __divmod__(self, other):
        if type(other) in (int, float, long):
            a = self*(1.0/other)           
            return (a,0)
        elif type(other) == wielomian:
            return self.dziel(other)
        else:
            raise TypeError, "Expected int, long, float or wielomian, got " + str(type(other))
        
        
    def __floordiv__(self, other):
        return self.__divmod__(other)[0]
    
    def __mod__(self, other):
        return self.__divmod__(other)[1]

    def __div__(self, other):
        r = self.__divmod__(other)
        if str(r[1]) == "0":
            return r[0]
        else:
            raise ValueError, "Can't divide, polynomial is indivisible by "+str(other)

    def __pow__(self, other):
        if type(other) == int:
            if other >= 1:
                r = 1
                for k in range(0, other):
                    r = self*r
                return r
            elif other == 0:
                return 1
            else:
                raise ValueError, "Can't power, number is negative"
        else:
            raise TypeError, "Expected int got " + str(type(other))
        
    def __coerce__(self, other):
        if type(other) in (int, float, long):
            other = wielomian(other)
            return (self, other)
        elif type(other) == wielomian:
            return (self, other)
        else:
            return None
        
    def __radd__(self, other):
        return self.__add__(other)
    
    def __rsub__(self, other):
        return self*-1+other
    
    def __rmul__(self, other):
        return self.__mul__(other)

    def __neg__(self):
        return self*-1
    
    def __pos__(self):
        return self
    
    
    
def pobierz(t, s=" = "):
    try:
        r = raw_input(t + s)
        r = r.replace(",", ".")
        r = eval(r)
        return nm(float(r))
    except (ValueError, SyntaxError, NameError):
        print u"To nie jest liczba!"
        return pobierz(t, s)

def pobwiel(nazwa = "W"):
    s=-1
    while s<0:
        s = pobierz("Stopien wielomianu "+nazwa)
        if s<0:
            print u"Stopień wielomianu nie może być ujemny!"
        if int(s)!=s:
            print u"Stopień wielomianu musi być całkowity!"
            s=-1
    w = wielomian()
    while s>=0:
        w.wsp.append(pobierz("Wspolczynnik "+nazwa+" przy x^"+str(int(s))))
        s -= 1
    w.wsp.reverse()
    w.nm()
    return w

def horner(w, r):
        a = w.wsp[::-1]
        c = a[:]
        b = a[:]
        for k in range(1,len(w.wsp)):
            b[k-1] = r*c[k-1]
            c[k] = a[k]+b[k-1]
        pygame.init()
        wi = 50*len(w.wsp)+50
        screen = pygame.display.set_mode((wi,150))
        pygame.display.set_caption("Tabela Hornera")
        clock = pygame.time.Clock()
        q = 0
        while not q:
            clock.tick(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    q = 1
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        q = 1
 
            screen.fill((255,255,255))
            pygame.draw.line(screen, (0,0,0), (0,50), (wi,50),1)
            pygame.draw.line(screen, (0,0,0), (0,100), (wi,100),1)
            for k in range(1,wi/50+2):
                pygame.draw.line(screen, (0,0,0), (k*50,0), (k*50,150),1)
            font = pygame.font.Font(None, 40)
            text = font.render(str(r),True,(0,0,0))
            screen.blit(text, (5,63))
            t = 0
            while t<len(a):
                text = font.render(str(a[t]),True,(0,0,0))
                screen.blit(text, (55+t*50,13))
                text = font.render(str(b[t]),True,(0,0,0))
                screen.blit(text, (55+(t+1)*50,63))
                text = font.render(str(c[t]),True,(0,0,0))
                screen.blit(text, (55+t*50,113))
                t += 1
            
            pygame.display.flip()
 
        pygame.quit()

def mzbf(f, a, b):
    t = 0
    lewy = a
    prawy = b
    flewy = f(lewy)
    fprawy = f(prawy)
    x = (a+b)/2.0
    e = (b-a)/2.0
    while (0 != e) and t<10000:
	fx = f(x)
	if ( abs(fx) == 0 ):
		return x
	if ( fx>0 and flewy<0) or (fx<0 and flewy>0):
		prawy = x
		fprawy = fx
	else:
		lewy = x
		flewy = fx
	x = (lewy+prawy)/2.0
	e = e/2.0
	t += 1
    return x

def miejscabf(w, d=0.01, start=-100, stop=100):
    mz = []
    x1 = w(start)
    m = start + d
    while m<=stop:
        x2 = w(m)
        if (x1>0 and x2<0) or (x1<0 and x2>0):
            mz.append(nm(mzbf(w,m-d,m)))
        x1 = x2
        m += d
    return mz

def pierwiastkir(self):
        dzielnikia = []
        dzielnikib = []
        pprzezq = []
        for i in range(1,int(fabs(self.wsp[0]))+1):
            if (self.wsp[0] % i) == 0:
                dzielnikia.append(i)
                dzielnikia.append(i*(-1))
        for i in range(1,int(fabs(self.wsp[-1]))+1):
            if (self.wsp[-1] % i) == 0:
                dzielnikib.append(i)
                dzielnikib.append(i*(-1))
        for i in range(0,len(dzielnikia)):
            for j in range(0,len(dzielnikib)):
                pprzezq.append(dzielnikia[i]/float(dzielnikib[j]))
        pprzezq = list(set(pprzezq))
        miejsca = []
        for i in range(0, len(pprzezq)):
            if float("%+.2f" % (self(pprzezq[i]))) == 0:
                miejsca.append(nm(pprzezq[i]))
        return miejsca

def mnoz(s, rw=1):
    s = re.sub(r"(\d)x", r"\1*x", s)
    s = re.sub(r"(\d)\(", r"\1*(", s)
    s = s.replace(")(", ")*(")
    s = s.replace("^", "**")
    s = s.replace("xx", "x*x")
    s = s.replace("xx", "x*x")
    s = s.replace(",", ".")
    if rw:
        x = wielomian(1,0)
        return (eval(s)*x)/x
    else:
        return s

def pobwiel2(nazwa = "W"):
    return mnoz(raw_input(nazwa + "(x) = "))








