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

from fp import nm, wykres, wielomian, pobierz, pobwiel, pobwiel2, horner, miejscabf, pierwiastkir, mnoz
import code

def main():
    print u"Witam w programie X-enon!"
    opcja = 1000
    while opcja != 0:
        print u"Wpisz liczbę by:"
        print u" 1) Uruchomić Active Shell"
        print u" 2) Dodać / Odjąć / Pomnożyć dwa wielomiany"
        print u" 3) Podzielić dwa wielomiany"
        print u" 4) Podzielić dwa wielomiany metodą Hornera"
        print u" 5) Wymożyć postać iloczynową wielomianu"
        print u" 6) Narysować wykres wielomianu"
        print u" 7) Znaleźć wymierne miejsca zerowe wielomianu o współczynnikach całkowitych"
        print u" 8) Przybliżyć miejsca zerowe wielomianu"
        print u" 9) Rozłożyc wielomian na czynniki"
        print u" 0) Wyjść z programu"
        opcja = pobierz(u"Wybieram ","")
        while opcja<0 or opcja>9 or opcja!=int(opcja):
            print u"Liczba spoza zakresu!"
            opcja = pobierz(u"Wybieram ","")
    
        if opcja == 1:
            code.interact(banner="Python shell with Wielomiany\nImplemented objects: nm, wykres, wielomian, pobierz, pobwiel, pobwiel2, horner, miejscabf, pierwiastkir, mnoz",local=locals())
    	
        elif opcja == 2:
            print u"Wyświetlę wynik z działania W?Q (W,Q - wielomiany, ? - znak działania (+,-,*))"
            z = ""
            while z not in ("+", "-", "*"):
        	z = raw_input("? = ")
                if z not in ("+", "-", "*"):
                    print u"Ta opcja obsługuje tylko dodawanie, odejmowanie i mnożenie!"
            w = pobwiel2("W")
            q = pobwiel2("Q")
            print "W(x) = " + str(w)
            print "Q(x) = " + str(q)
            print "W(x) "+z+" Q(x)","=",eval("w"+z+"q")
	
        elif opcja == 3:
            w = pobwiel2("W")
            q = pobwiel2("Q")
            print "W(x) = " + str(w)
            print "Q(x) = " + str(q)
            r = w.dziel(q)
            rr = ""
            if str(r[1]) != "0":
                rr = "Reszta "+str(r[1]) 
            print "W(x) / Q(x) =", r[0], rr  

        elif opcja == 4:
            print u"Podzielę W(x) przez dwumian (x-r)"
            r = pobierz("r")
            w = pobwiel2("W")
            rr = w.dziel(wielomian(1,r*-1))
            rt = ""
            if str(rr[1]) != "0":
                rt = "Reszta "+str(rr[1])
            print "W(x) = " + str(w)
            print "W(x) / (x-"+str(r)+") =", rr[0], rt
            horner(w, r)
    
        elif opcja == 5:
            r = raw_input("W(x) = ")
            print "W(x) = " + str(mnoz(r))
        
        elif opcja == 6:
            w = pobwiel2("W")
            print "W(x) = " + str(w)
            wyk = wykres()
            wyk.dodaj(w)
            print u"Policzę W(x) jeśli podasz x"
            x = "a"
            while x!="":
                x = raw_input("x = ")
                try:
                    x = float(x)
                    print w(x)
                except ValueError:
                    if x!="":
                        print u"To nie jest liczba!"
		    
        elif opcja == 7:
            s=-1
            while s<0:
                s = pobierz("Stopien wielomianu W")
                if s<0:
                    print u"Stopień wielomianu nie może być ujemny!"
                if int(s)!=s:
                    print u"Stopień wielomianu musi być całkowity!"
                    s=-1
            w = wielomian()
            while s>=0:
                ws = 0.5
                while type(nm(ws)) == float:
                    ws = pobierz("Wspolczynnik W przy x^"+str(int(s)))
                    if type(nm(ws)) == float:
                        print u"Współczynnik musi być całkowity!"
                w.wsp.append(ws)
                s -= 1
            w.wsp.reverse()
            w.nm()
            print "W(x) = " + str(w)
            m = pierwiastkir(w)
            r = "Wymierne miejsca zerowe wielomianu W(x) to "
            for k in m:
                if k is m[0]:
                    r += str(k)
                elif k is m[-1]:
                    r += " i " + str(k)
                else:
                    r += ", " + str(k)
            print r
            
        elif opcja == 8:
            w = pobwiel2("W")
            print "W(x) = " + str(w)
            m = miejscabf(w)
            r = "Miejsca zerowe wielomianu W(x) to "
            for k in m:
                if k is m[0]:
                    r += str(k)
                elif k is m[-1]:
                    r += " i " + str(k)
                else:
                    r += ", " + str(k)
            print r
        
        elif opcja == 9:
            w = pobwiel2("W")
            print "W(x) = " + str(w)
            m = miejscabf(w)
            r = ""
            d = 1*w
            for k in m:
                ws = wielomian(1,-1*k)
                d = d//ws
                r += "(" + str(ws) + ")"
            try:
                if int(str(d)) == -1:
                    r = "-" + r
                elif int(str(d)) == 1:
                    pass
                else:
                    r = str(d) + r
            except ValueError:
                r = "(" + str(d) + ")" + r
            print "W(x) = " + r
    
        if opcja!=0:
            raw_input("-> Menu")

if __name__ == '__main__':
    main()
