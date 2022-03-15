import csv

PARAM_FMT = ":{}" # za SQLite

class Tabela:
    """
    Razred, ki predstavlja tabelo v bazi.
    Polja razreda:
    - ime: ime tabele
    - podatki: ime datoteke s podatki ali None
    """
    ime = None
    podatki = None

    def __init__(self, conn):
        """
        Konstruktor razreda.
        """
        self.conn = conn

    def ustvari(self):
        """
        Metoda za ustvarjanje tabele.
        Podrazredi morajo povoziti to metodo.
        """
        raise NotImplementedError

    def izbrisi(self):
        """
        Metoda za brisanje tabele.
        """
        self.conn.execute(f"DROP TABLE IF EXISTS {self.ime};")


    def uvozi(self, encoding="utf-8"):
        """
        Metoda za uvoz podatkov.
        Argumenti:
        - encoding: kodiranje znakov
        """
        if self.podatki is None:
            return
        with open(self.podatki, encoding=encoding) as datoteka:
            podatki = csv.reader(datoteka, delimiter=",") 
            stolpci = next(podatki)
            for vrstica in podatki:
                vrstica = {k: None if v == "" else v for k, v in zip(stolpci, vrstica)}
                self.dodaj_vrstico(**vrstica)

    def izprazni(self):
        """
        Metoda za praznjenje tabele.
        """
        self.conn.execute(f"DELETE FROM {self.ime};")

    def dodajanje(self, stolpci=None):
        """
        Metoda za gradnjo poizvedbe.
        Argumenti:
        - stolpci: seznam stolpcev
        """
        return f"""
            INSERT INTO {self.ime} ({", ".join(stolpci)})
            VALUES ({", ".join(PARAM_FMT.format(s) for s in stolpci)});
        """
    def dodaj_vrstico(self, **podatki):
        """
        Metoda za dodajanje vrstice.
        Argumenti:
        - poimenovani parametri: vrednosti v ustreznih stolpcih
        """
        podatki = {kljuc: vrednost for kljuc, vrednost in podatki.items()
                   if vrednost is not None}

        poizvedba = self.dodajanje(podatki.keys())
        cur = self.conn.execute(poizvedba, podatki)
        return cur.lastrowid


    
class Pesem(Tabela):
    """
    Tabela vseh pesmi.
    """
    ime = "pesem"
    podatki = "pesem.csv"

    def ustvari(self):
        """
        Ustvari tabelo pesmi.
        """
        self.conn.execute("""
            CREATE TABLE PESEM (
                leto      INTEGER REFERENCES TEKMOVANJE(id),
                ime_drzave    TEXT REFERENCES DRZAVA(id),
                ime_izvajalca TEXT REFERENCES IZVAJALEC(id),
                naslov_pesmi    TEXT,
                mesto     INTEGER,
                tocke_v_finalu INTEGER,
                youtube_link TEXT NOT NULL
                
            );
        """)
    def dodaj_vrstico(self, **podatki):
        """
        Doda pesem v bazo.
        
        Argumenti:
        - poimenovani parametri: vrednosti v ustreznih stolpcih
        """
        return super().dodaj_vrstico(**podatki)


class Drzava(Tabela):
    """
    Tabela za drzave.
    """
    ime = "drzava"
    podatki = "drzava.csv"

    def ustvari(self):
        """
        Ustvari tabelo drzava.
        """
        self.conn.execute("""
      CREATE TABLE DRZAVA (
                id_drzave       INTEGER PRIMARY KEY AUTOINCREMENT,
                kratica_drzave  TEXT NOT NULL,
                ime_drzave      TEXT NOT NULL,
                leto            INTEGER
            );
        """)

    def dodaj_vrstico(self, **podatki):
        """
        Doda državo v bazo.
        
        Argumenti:
        - poimenovani parametri: vrednosti v ustreznih stolpcih
        """
        return super().dodaj_vrstico(**podatki)



class Izvajalec(Tabela):
    """
    Tabela vseh izvajalcev.
    """
    ime = "izvajalec"
    podatki = 'izvajalec.csv'

    def ustvari(self):
        """
        Ustvari tabelo vseh izvajalcev.
        """
        self.conn.execute("""
            CREATE TABLE IZVAJALEC (
                id_izvajalca   INTEGER PRIMARY KEY AUTOINCREMENT,
                ime_drzave TEXT NOT NULL,
                ime_izvajalca TEXT NOT NULL
            );
        """)
    def dodaj_vrstico(self, **podatki):
        """
        Doda izvajalca v bazo.
        
        Argumenti:
        - poimenovani parametri: vrednosti v ustreznih stolpcih
        """
        return super().dodaj_vrstico(**podatki)


class Tekmovanje(Tabela):
    """
    Tabela vseh tekmovanj.
    """
    ime = "tekmovanje"
    podatki = 'tekmovanje.csv'
    def ustvari(self):
        """
        Ustvari tabelo vseh tekmovanj.
        """
        self.conn.execute("""
           CREATE TABLE TEKMOVANJE(
           id_tekmovanja INTEGER PRIMARY KEY AUTOINCREMENT,
           leto INTEGER,
           ime_drzave TEXT REFERENCES DRZAVA(id)
            );
        """)
    def dodaj_vrstico(self, **podatki):
        """
        Doda tekmovanje v bazo.
        
        Argumenti:
        - poimenovani parametri: vrednosti v ustreznih stolpcih
        """
        return super().dodaj_vrstico(**podatki)

        
class Glasovanje(Tabela):
    """
    Tabela vseh glasov.
    """
    ime = "glasovanje"
    podatki = 'glasovanje.csv'

    def ustvari(self):
        """
        Ustvari tabelo vseh glasov.
        """
        self.conn.execute("""
            CREATE TABLE GLASOVANJE (
                leto INTEGER,
                kdo  TEXT REFERENCES DRZAVA(id),
                komu TEXT,
                tocke INTEGER NOT NULL,
                FOREIGN KEY (komu, leto) REFERENCES PESEM(ime_drzave, leto)

            );
        """)
    def dodaj_vrstico(self, **podatki):
        """
        Doda glasovanje v bazo.
        
        Argumenti:
        - poimenovani parametri: vrednosti v ustreznih stolpcih
        """
        return super().dodaj_vrstico(**podatki)


# class Izvaja(Tabela):
#     """
#     Tabela za relacijo med izvajalcem in pesmijo.
#     """
#     ime = "izvaja"
#     #podatki = "izvajalec.csv"
# 
#     def __init__(self, conn, Izvajalec):
#         """
#         Konstruktor tabele pripadnosti izvajalec-pesem.
#         Argumenti:
#         - conn: povezava na bazo
#         - Izvajalec: tabela vseh izvajalcev
#         """
#         super().__init__(conn)
#         self.izvajalec = Izvajalec
# 
#     def ustvari(self):
#         """
#         Ustvari tabelo IZVAJA.
#         """
#         self.conn.execute("""
#             CREATE TABLE IZVAJA (
#                 IZVAJALEC TEXT REFERENCES IZVAJALEC(ime_drzave),
#                 PESEM TEXT REFERENCES PESEM(ime_drzave)
#             );
#         """)
#     def dodaj_vrstico(self, **podatki):
#         """
#         Dodaj pripadnost lokacije in pripadajoce vrste.
#         Argumenti:
#         - podatki: slovar s podatki o pripadnosti
#         """
#         return super().dodaj_vrstico(**podatki)


def ustvari_tabele(tabele):
    """
    Ustvari podane tabele.
    """
    for t in tabele:
        t.ustvari()


def izbrisi_tabele(tabele):
    """
    Izbriši podane tabele.
    """
    for t in tabele:
        t.izbrisi()


def uvozi_podatke(tabele):
    """
    Uvozi podatke v podane tabele.
    """
    for t in tabele:
        t.uvozi()


def izprazni_tabele(tabele):
    """
    Izprazni podane tabele.
    """
    for t in tabele:
        t.izprazni()


def ustvari_bazo(conn):
    """
    Izvede ustvarjanje baze.
    """
    tabele = pripravi_tabele(conn)
    izbrisi_tabele(tabele)
    ustvari_tabele(tabele)
    uvozi_podatke(tabele)


def pripravi_tabele(conn):
    """
    Pripravi objekte za tabele.
    """
    drzava = Drzava(conn)
    pesem = Pesem(conn)
    tekmovanje = Tekmovanje(conn)
    izvajalec = Izvajalec(conn)
    glasovanje = Glasovanje(conn)
    #izvaja = Izvaja(conn, izvajalec)

    return [drzava, izvajalec, tekmovanje, pesem, glasovanje]


def ustvari_bazo_ce_ne_obstaja(conn):
    """
    Ustvari bazo, če ta še ne obstaja.
    """
    with conn:
        cur = conn.execute("SELECT COUNT(*) FROM sqlite_master")
        if cur.fetchone() == (0, ):
            ustvari_bazo(conn)