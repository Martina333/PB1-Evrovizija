import baza
import sqlite3
from sqlite3 import IntegrityError
import os.path
from os import path
from pomozne_funkcije import Seznam

conn = sqlite3.connect('baza.db')
baza.ustvari_bazo_ce_ne_obstaja(conn)
conn.execute('PRAGMA foreign_keys = ON')

drzava, izvajalec, tekmovanje, pesem, glasovanje = baza.pripravi_tabele(conn)

class Pesem:
    """
    Razred za pesem.
    """

    def __init__(self, naslov_pesmi, ime_izvajalca, ime_drzave, mesto, tocke_v_finalu):
        """
        Konstruktor pesmi.
        """
        self.naslov_pesmi = naslov_pesmi
        self.ime_izvajalca = ime_izvajalca
        self.ime_drzave = ime_drzave
        self.mesto = mesto
        self.tocke_v_finalu = tocke_v_finalu

    def __str__(self):
        """
        Znakovna predstavitev pesmi.
        Vrne naslov pesmi.
        """
        return self.naslov_pesmi

    @staticmethod
    def najboljse_v_letu(leto):
        """
        Vrne najboljših 5 pesmi v danem letu.
        """
        sql = """
            SELECT naslov_pesmi,
            ime_izvajalca,
            ime_drzave,
            mesto,
            tocke_v_finalu,
            youtube_link
            FROM PESEM
            WHERE leto = ?
            ORDER BY mesto ASC
            LIMIT 5
        """
        for naslov_pesmi, ime_izvajalca, ime_drzave, mesto, tocke_v_finalu, youtube_link in conn.execute(sql, [leto]):
            yield (naslov_pesmi, ime_izvajalca, ime_drzave, mesto, tocke_v_finalu, youtube_link)


class Izvajalec:
    """
    Razred za izvajalca.
    """

    def __init__(self, ime_izvajalca, *, id_izvajalca=None):
        """
        Konstruktor izvajalca.
        """
        self.id_izvajalca = id_izvajalca
        self.ime_izvajalca = ime_izvajalca

    def __str__(self):
        """
        Znakovna predstavitev izvajalca.
        Vrne ime izvajalca.
        """
        return self.ime_izvajalca

    def poisci_pesmi(self):
        """
        Vrne naslov pesmi, ime države, leto, mesto in youtube povezavo izvajalca.
        """
        sql = """
            SELECT naslov_pesmi,
            ime_drzave,
            leto,
            mesto,
            youtube_link
            FROM PESEM
            WHERE ime_izvajalca = ?
            """
        for naslov_pesmi, ime_drzave, leto, mesto, youtube_link in conn.execute(sql, [self.ime_izvajalca]):
            yield (naslov_pesmi, ime_drzave, leto, mesto, youtube_link)

    @staticmethod
    def poisci(niz):
        """
        Vrne vse izvajalce, ki v imenu vsebujejo dani niz.
        """
        sql = "SELECT id_izvajalca, ime_izvajalca FROM IZVAJALEC WHERE ime_izvajalca LIKE ?"
        for id_izvajalca, ime_izvajalca in conn.execute(sql, [f'%{niz}%']):
            yield Izvajalec(ime_izvajalca=ime_izvajalca, id_izvajalca=id_izvajalca)

class Drzava:
    """
    Razred za državo.
    """

    def __init__(self, ime_drzave, leto):
        """
        Konstruktor države.
        """
        
        self.ime_drzave = ime_drzave
        self.leto = leto


    def __str__(self):
        """
        Znakovna predstavitev države.
        Vrne ime države.
        """
        return self.ime_drzave
    
    @staticmethod
    def katere_drzave(leto):
        '''Vrne seznam držav, ki so v določenem letu sodelovale na Evroviziji '''
        sql = """SELECT ime_drzave
                 FROM TEKMOVANJE
                 WHERE leto = ?
                 ORDER BY ime_drzave"""
        for ime_drzave in conn.execute(sql, [leto]):
            yield (ime_drzave)
            
    @staticmethod
    def isci_drzavo(ime_drzave):
        '''Vrne podatke o izbrani državi'''
        sql = """SELECT leto,
                 ime_izvajalca,
                 naslov_pesmi,
                 mesto,
                 tocke_v_finalu
                 FROM PESEM
                 WHERE ime_drzave = ?
                 ORDER BY leto """
        for leto, ime_izvajalca, naslov_pesmi, mesto, tocke_v_finalu in conn.execute(sql, [ime_drzave]):
            yield (leto, ime_izvajalca, naslov_pesmi, mesto, tocke_v_finalu)
        