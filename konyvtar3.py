import sqlite3
from tkinter import *
from filedialog import *

class konyvtar():
    '''Könyvtárkezelő adatbázis'''
    def __init__(self):
        self.ablak = Tk() #ablak definiálás
        self.ablak.title('Könyvtár') #ablak címe
        self.adatok = [['Szerző', 'ismeretlen'],['Cím', 'ismeretlen'],['Kiadás éve', '-1'],['Műfaj', 'ismeretlen'],['Kinél van', 'nálam']] #könyvtulajdonságok és alapértelmezett értékeik
        self.a, self.c, self.e, self.m, self.k = StringVar(), StringVar(), StringVar(), StringVar(), StringVar() #változók a beíró mezőkhöz
        self.valt = [self.a, self.c, self.e, self.m, self.k] #a fenti változók listába rendezve
        self.szurval = StringVar() #a rádiógombok változója
        self.szurval.set(self.adatok[0][0]) #a rádiógombok változójának alapértelmezett értéke
        self.conn = sqlite3.connect('konyvtar.sqlite') #alapértelmezett adatbázishoz kapcsolódás
        self.cur = self.conn.cursor()

        for i in range(5): #öt rádiógomb és beíró mező létrehozása az ötféle adathoz
            Radiobutton(self.ablak, text=self.adatok[i][0], variable=self.szurval, value=self.adatok[i][0], command=self.szurval.get()).grid(row=i, column=0, sticky=W)
            self.valt[i].set(self.adatok[i][1])
            Entry(self.ablak, textvariable=self.valt[i], width=40).grid(row=i, column=1, sticky=W)

        Label(self.ablak, text='Könyvek száma').grid(row=5, column=0) #az adatbázisban lévő összes könyv számát adja meg
        self.szam = Label(self.ablak, text='0')
        self.szam.grid(row=5, column=1, sticky=W)

        self.gombok1 = ['Beolvasás', 'Törlés', 'Szűrés', 'Ellenszűrés', 'Frissítés', 'Súgó'] #gombok az egyes funkciókhoz
        self.parancsok1 = [self.beolvasas, self.torles, self.szures, self.ellenszures, self.frissites, self.sugo] #parancsok az egyes funkciókhoz
        for i in range(len(self.gombok1)): #létrehozó ciklus
            Button(self.ablak, text=self.gombok1[i], command=self.parancsok1[i]).grid(row=i, column=2)

        self.load = Button(self.ablak, text='Betöltés', command=self.betoltes) #'Betöltés' gomb, hogy lehessen rá hivatkozni a kiiras metódusban
        self.load.grid(row=0, column=3)
        
        self.gombok2 = ['Betöltés', 'Kiírás', 'Mentés', 'Visszaállítás', 'Mindent törlés', 'Mentés txt-be']
        self.parancsok2 = [self.betoltes, self.kiiras, self.mentes, self.visszaallitas, self.mindenttorles, self.exportalas]
        for i in range(1,len(self.gombok2)):
            Button(self.ablak, text=self.gombok2[i], command=self.parancsok2[i]).grid(row=i, column=3)
        
        self.listv = StringVar() #szövegmezőhöz tartozó változó
        self.listv.set(('Nincs kiíratva semmi.', ))
        self.listb = Listbox(self.ablak, width=80, height=30, listvariable=self.listv, selectmode=MULTIPLE) #szövegmező az adatbázis tartalmának kiírásához
        self.listb.grid(row=6, column=0, rowspan=10, columnspan=5)
        
        self.scroll = Scrollbar(self.ablak, orient=VERTICAL, command=self.listb.yview) #szövegmezőhöz tartozó függőleges görgetősáv
        self.scroll.grid(row=6, column=3, rowspan=10, sticky=N+S+E)
        self.listb['yscrollcommand'] = self.scroll.set
        
        Button(self.ablak, text='Kilépés', command=self.kilepes).grid(row=18, column=3, sticky=E) #kilépés gomb
    
    def beolvasas(self): #a beíró mezőkben lévő adatokat rakja bele az adatbázisba
        self.sor = (self.a.get(), self.c.get(), self.e.get(), self.m.get(), self.k.get())
        try:
            self.cur.execute('INSERT INTO Könyvek (szerzo, cim, kiadas, mufaj, kinel) VALUES (?, ?, ?, ?, ?)', (self.sor[0], self.sor[1], self.sor[2], self.sor[3], self.sor[4]))
        except:
            self.listv.set(('Nincs betöltve adatbázis.', ))

    def torles(self): #törli a kijelölt mezőnek megfelelő bejegyzéseket az adatbázisból
        '''Törölni egyszerre csak egy kritérium szerint lehet, célszerű cím szerint'''
        if self.szurval.get()=='Szerző':
            self.cur.execute('DELETE FROM Könyvek WHERE szerzo = ?', (self.a.get(), ))
        elif self.szurval.get()=='Cím':
            self.cur.execute('DELETE FROM Könyvek WHERE cim = ?', (self.c.get(), ))
        elif self.szurval.get()=='Kiadás éve':
            self.cur.execute('DELETE FROM Könyvek WHERE kiadas = ?', (self.e.get(), ))
        elif self.szurval.get()=='Műfaj':
            self.cur.execute('DELETE FROM Könyvek WHERE mufaj = ?', (self.m.get(), ))
        elif self.szurval.get()=='Kinél van':
            self.cur.execute('DELETE FROM Könyvek WHERE kinel = ?', (self.k.get(), ))
        #self.cur.execute('DELETE FROM Könyvek WHERE szerzo = ? AND cim = ?', (self.a.get(), self.c.get()))

    def szures(self): #szűr a kijelölt mezőnek megfelelő bejegyzésekre
        '''Csak a kiválasztott tulajdonságnak megfelelő beírt adatokat írja ki'''
        self.tup = []
        if self.szurval.get()=='Szerző':
            self.cur.execute('SELECT szerzo, cim, kiadas, mufaj, kinel FROM Könyvek WHERE szerzo = ? ORDER BY szerzo', (self.a.get(), ))
            for row in self.cur:
                self.tup.append(row)
        elif self.szurval.get()=='Cím':
            self.cur.execute('SELECT szerzo, cim, kiadas, mufaj, kinel FROM Könyvek WHERE cim = ? ORDER BY szerzo', (self.c.get(), ))
            for row in self.cur:
                self.tup.append(row)
        elif self.szurval.get()=='Kiadás éve':
            self.cur.execute('SELECT szerzo, cim, kiadas, mufaj, kinel FROM Könyvek WHERE kiadas = ? ORDER BY szerzo', (self.e.get(), ))
            for row in self.cur:
                self.tup.append(row)
        elif self.szurval.get()=='Műfaj':
            self.cur.execute('SELECT szerzo, cim, kiadas, mufaj, kinel FROM Könyvek WHERE mufaj = ? ORDER BY szerzo', (self.m.get(), ))
            for row in self.cur:
                self.tup.append(row)
        elif self.szurval.get()=='Kinél van':
            self.cur.execute('SELECT szerzo, cim, kiadas, mufaj, kinel FROM Könyvek WHERE kinel = ? ORDER BY szerzo', (self.k.get(), ))
            for row in self.cur:
                self.tup.append(row)
        self.listv.set(self.tup)

    def ellenszures(self): #szűr a kijelölt mezőnek nem megfelelő bejegyzésekre
        '''Arra van, hogy megnézzem, melyik könyv nincs nálam'''
        if self.szurval.get()=='Kinél van':
            self.cur.execute('SELECT szerzo, cim, kiadas, mufaj, kinel FROM Könyvek WHERE kinel != ? ORDER BY szerzo', (self.k.get(), ))
##            self.tup = []
##            for r in self.cur.fetchall(): #a fetchall() metódussal formázható a kimenet
##                rr = str(r[0]) + ' : ' + str(r[1]) + ' ( ' + str(r[2]) + ', ' + str(r[3]) + ', ' + str(r[4]) + ' )' #formázott kimenet
##                self.tup.append(rr)
            self.tup = [str(r[0]) + ' : ' + str(r[1]) + ' ( ' + str(r[2]) + ', ' + str(r[3]) + ', ' + str(r[4]) + ' )' for r in self.cur.fetchall()]
        self.listv.set(self.tup)

    def frissites(self): #bejegyzés kijelölt adatát frissíti annak címe alapján 
        '''Könyv címe alapján átírhatók más adatok (ha a címet írod be rosszul, elbasztad, törlés)'''
        if self.szurval.get()=='Szerző':
            self.t = (self.a.get(), self.c.get())
            self.cur.execute('UPDATE Könyvek SET szerzo = ? WHERE cim = ?', self.t)
        elif self.szurval.get()=='Kiadás éve':
            self.t = (self.e.get(), self.c.get())
            self.cur.execute('UPDATE Könyvek SET kiadas = ? WHERE cim = ?', self.t)
        elif self.szurval.get()=='Műfaj':
            self.t = (self.m.get(), self.c.get())
            self.cur.execute('UPDATE Könyvek SET mufaj = ? WHERE cim = ?', self.t)
        elif self.szurval.get()=='Kinél van':
            self.t = (self.k.get(), self.e.get())
            self.cur.execute('UPDATE Könyvek SET kinel = ? WHERE cim = ?', self.t)

    def sugo(self): #súgó a használathoz
        self.ablak2 = Tk() #másik ablakban nyílik meg
        self.ablak2.title('Súgó')
        self.txt = '''        Betöltés: adatbázis betöltése. Alapértelmezésben az adott mappában lévő konyvtar.sqlite adatbázissal dolgozik.\n
        Beolvasás: a beírt adatokat rögzíti.\n
        Kiírás: kiírja az adatbázisban lévő összes könyv adatait.\n
        Mentés: a beolvasott adatokat rögzíti az adatbázisba.\n
        Visszaállítás: a legutóbbi mentés óta történt módosításokat állítja vissza.\n
        Mindent törlés: az adatbázis teljes tartalmát törli.\n
        Törlés: a beállított adattípushoz beírt szövegnek megfelelő bejegyzéseket törli.\n
        Szűrés: a beállított adattípushoz beírt szövegnek megfelelő bejegyzéseket írja ki.\n
        Ellenszűrés: a beállított adattípushoz beírt szövegnek nem megfelelő bejegyzéseket írja ki.\n
        Frissítés: a beírt címhez tartozó, a beállított adattípusnak megfelelő adatot frissíti.\n
        Mentés txt-be: az adatbázis tartalmát menti ki fájlba. Alapértelmezésben az adott mappában lévő Könyvek.txt fájllal dolgozik.\n
        Súgó: megnyitja ezt a súgót.'''
        Label(self.ablak2, text=self.txt, justify=LEFT).pack()
        self.ablak2.mainloop()

    def betoltes(self): #adatbázis betöltésére
        self.filename = askopenfilename(title='Adatbázis kiválasztása') #a filedialog modulból
        try:
            self.conn = sqlite3.connect(self.filename) #kapcsolódik a kijelölt adatbázishoz
            self.cur = self.conn.cursor()
        except:
            self.listv.set(('Nincs betöltve adatbázis.', ))

    def kiiras(self): #az adatbázis teljes tartalmát jeleníti meg
        try: #ha van beöltve adatbázis
            self.cur.execute('SELECT szerzo, cim, kiadas, mufaj, kinel FROM Könyvek ORDER BY szerzo') #szerző szerint rendezve írja ki
            self.tup = [str(r[0]) + ' : ' + str(r[1]) + ' ( ' + str(r[2]) + ', ' + str(r[3]) + ', ' + str(r[4]) + ' )' for r in self.cur.fetchall()]
            self.cur.execute('SELECT COUNT(*) FROM Könyvek')
            self.sz = self.cur.fetchone()[0]
            self.listv.set(self.tup)
            self.szam.configure(text=str(self.sz)) #az adatbázisban lévő könyvek számát írja ki
        except: #ha nincs betöltve adatbázis
            self.listv.set(('Nincs betöltve adatbázis.', ))
            self.load.configure(activebackground='red')
            self.load.flash() #a 'Betöltés' gombot villogtatja
            self.load.configure(activebackground='grey')

    def mentes(self): #elmenti az adatbázisban legutóbbi mentés óta eltelt változtatásokat
        self.conn.commit()

    def visszaallitas(self): #visszaállítja az adatbázist a legutóbbi mentés állapotába
        self.conn.rollback()

    def mindenttorles(self): #mindent töröl az adatbázisból
        self.cur.execute('DELETE FROM Könyvek')

    def exportalas(self): #txt fájlba menti ki az adatbázis tartalmát, a kiírt formában
        self.filename = asksaveasfilename(title='Szövegfájl mentése', filetypes=[('txt', '*.txt')], defaultextension='.txt') #a filedialog modulból
        if self.filename == '': #ha visszalép a felugró ablakból, alapértelmezésként csinálja ezt a fájlnevet, hogy ne legye error
            self.filename = 'Könyvek.txt'
        self.file = open(self.filename, 'w')
        self.cur.execute('SELECT szerzo, cim, kiadas, mufaj, kinel FROM Könyvek ORDER BY szerzo')
        self.tup = []
        self.sz = 0
        for r in self.cur.fetchall(): #a fetchall() metódussal formázható a kimenet
            self.rr = str(r[0]) + ' : ' + str(r[1]) + ' ( ' + str(r[2]) + ', ' + str(r[3]) + ', ' + str(r[4]) + ' )' #formázott kimenet
            self.sz = self.sz + 1
            try:
                self.file.write(self.rr+'\n') #van vmi karakterkonvertálási hiba
            except:
                self.rr = self.rr.replace('Ő','Õ') #a karakterkódolási bajokat nem tudom máshogy megoldani
                self.rr = self.rr.replace('Ű','Û')
                self.rr = self.rr.replace('ű','û')
                self.rr = self.rr.replace('ő','õ')
                self.file.write(self.rr+'\n')
        self.file.write(str(self.sz) + ' db könyv van.')
        self.file.close()
        print('Kiírás kész.')

    def kilepes(self): #kilépés a programból
        self.conn.close() #bezárja az adatbázist
        self.ablak.destroy() #bezárja az ablakot
        
if __name__ == '__main__':
    k = konyvtar()
    k.ablak.mainloop
