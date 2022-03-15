from pomozne_funkcije import Meni, prekinitev
from model import Pesem, Izvajalec, Drzava

def vnesi_izbiro(moznosti):
    """
    Uporabniku da na izbiro podane možnosti.
    """
    moznosti = list(moznosti)
    for i, moznost in enumerate(moznosti, 1):
        print(f'{i}) {moznost}')
    izbira = None
    while True:
        try:
            izbira = int(input('> ')) - 1
            return moznosti[izbira]
        except (ValueError, IndexError):
            print("Napačna izbira!")


def izpisi_pesmi(izvajalec):
    """
    Izpiše naslov pesmi, leto, mesto youtube povezavo in ime države podanega izvajalca.
    """
    print(izvajalec.ime_izvajalca)
    for naslov_pesmi, ime_drzave, leto, mesto, youtube_link in izvajalec.poisci_pesmi():
        print(f'- naslov pesmi: {naslov_pesmi}, država: {ime_drzave}, leto: {leto}, {mesto}. mesto, povezava: {youtube_link}')


def poisci_izvajalca():
    """
    Poišče izvajalca, ki ga vnese uporabnik.
    """
    while True:
        ime_izvajalca = input('Kdo te zanima? ')
        izvajalci = list(Izvajalec.poisci(ime_izvajalca))
        if len(izvajalci) == 1:
            return izvajalci[0]
        elif len(izvajalci) == 0:
            print('Tega izvajalca ne najdem. Poskusi znova.')
        else:
            print('Našel sem več izvajalcev, kateri od teh te zanima?')
            return vnesi_izbiro(izvajalci)


@prekinitev
def iskanje_izvajalca():
    """
    Poišče izvajalca in izpiše njegovo pesem.
    """
    izvajalec = poisci_izvajalca()
    izpisi_pesmi(izvajalec)

@prekinitev
def iskanje_drzav():
    '''Preveri, katere države so v določenem letu sodelovale na Evroviziji.'''
    leto = input('Katero leto te zanima? ')
    drzave = list(Drzava.katere_drzave(leto))
    for ime_drzave in drzave:
        print(*ime_drzave, sep = ", ")
        
@prekinitev
def preglej_drzavo():
    '''Za vsako vnešeno državo izpiše vse podatke o njenem nastopanju na tekmovanju'''
    ime_drzave = input('Katera država te zanima? ')
    podatki = Drzava.isci_drzavo(ime_drzave)
    for leto, ime_izvajalca, naslov_pesmi, mesto, tocke_v_finalu in podatki:
        print(f'leto: {leto}, izvajalec: {ime_izvajalca}, naslov pesmi: {naslov_pesmi}, {mesto}.mesto, točke v finalu: {tocke_v_finalu}')

    
@prekinitev
def najboljse_pesmi():
    """
    Izpiše najboljših 5 pesmi v letu, ki ga vnese uporabnik.
    """
    leto = input('Katero leto te zanima? ')
    pesmi = Pesem.najboljse_v_letu(leto)
    for naslov_pesmi, ime_izvajalca, ime_drzave, mesto, tocke_v_finalu, youtube_link in pesmi:
        print(f'naslov pesmi: {naslov_pesmi}, izvajalec: {ime_izvajalca}, država: {ime_drzave}, {mesto}. mesto, točke v finalu: {tocke_v_finalu}, poslušaj: {youtube_link}')


@prekinitev
def domov():
    """
    Pozdravi pred izhodom.
    """
    print('Adijo!')


class GlavniMeni(Meni):
    """
    Izbire v glavnem meniju.
    """
    ISKAL_IZVAJALCA = ('Iskal izvajalca', iskanje_izvajalca)
    POGLEDAL_DOBRE_PESMI = ('Pogledal dobre pesmi', najboljse_pesmi)
    PREVERIL_DRZAVE = ('Preveril države', iskanje_drzav)
    IZVEDEL = ('Izvedel vse o določeni državi', preglej_drzavo)
    SEL_DOMOV = ('Šel domov', domov)


@prekinitev
def glavni_meni():
    """
    Prikazuje glavni meni, dokler uporabnik ne izbere izhoda.
    """
    print('Pozdravljen v bazi Evrovizije!')
    while True:
        print('Kaj bi rad delal?')
        izbira = vnesi_izbiro(GlavniMeni)
        izbira.funkcija()
        if izbira == GlavniMeni.SEL_DOMOV:
            return


glavni_meni()