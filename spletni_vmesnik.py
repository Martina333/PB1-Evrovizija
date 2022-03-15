import bottle
from model import Pesem, Izvajalec, Drzava

@bottle.get('/najboljse/<leto:int>/')
def najboljse_pesmi(leto):
    return bottle.template(
        'najboljse_pesmi.html',
        leto=leto,
        pesmi=Pesem.najboljse_v_letu(leto)
    )

@bottle.get('/')
def zacetna_stran():
    return bottle.template(
        'zacetna_stran.html',
        leta=range(1956, 2020)
    )

@bottle.get('/isci/')
def isci():
    iskalni_niz = bottle.request.query['iskalni_niz']
    izvajalci = Izvajalec.poisci(iskalni_niz)
    return bottle.template(
        'izvajalci.html',
        iskalni_niz = iskalni_niz,
        izvajalec = izvajalci
    )


@bottle.get('/seznam/')
def iskanje_drzav():
    katero_leto = bottle.request.query['katero_leto']
    drzave = Drzava.katere_drzave(katero_leto)
    return bottle.template(
        'seznam_drzav.html',
        katero_leto=katero_leto,
        drzava=drzave
    )

@bottle.get('/preglej/')
def preglej_drzavo():
    ime = bottle.request.query['ime']
    info = Drzava.isci_drzavo(ime)
    return bottle.template(
        'informacije.html',
        ime=ime,
        nekaj=info
    )

bottle.run(debug=True, reloader=True)