# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from bghw.partner import _
from zope import schema
from zope.interface import Interface
from plone.supermodel import model
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield import DictRow
from plone.app.textfield import RichText
from plone.indexer import indexer
from plone.autoform.directives import widget
from collective.z3cform.datagridfield import DictRow, DataGridFieldFactory
from z3c.form.browser.checkbox import CheckBoxFieldWidget
#from z3c.form.interfaces import IEditForm, IAddForm
from z3c.form import field
from geopy.geocoders import Nominatim
from zope.schema import ValidationError
from zope.interface import invariant, Invalid
#from plone.dexterity.browser import edit, add
from time import sleep
from plone import api as ploneapi

class keinPartner(ValidationError):
    u""" Bitte wählen Sie die Art des Netzwerkpartners aus. """

def validatePartner(value):
    if value:
        return True
    raise keinPartner

geolocator = Nominatim(user_agent="bghw.partner")

class IBghwPartnerLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""

uhrzeiten = SimpleVocabulary.fromItems((
    (u'--', u'-'),
    (u'6:00', 6),
    (u'7:00', 7),
    (u'8:00', 8),
    (u'9:00', 9),
    (u'10:00', 10),
    (u'11:00', 11),
    (u'12:00', 12),
    (u'13:00', 13),
    (u'14:00', 14),
    (u'15:00', 15),
    (u'16:00', 16),
    (u'17:00', 17),
    (u'18:00', 18),
    (u'19:00', 19),
    (u'20:00', 20)))

wochentage = SimpleVocabulary.fromItems((
    (u'Wochentag', 0),
    (u'Montag', 1),
    (u'Dienstag', 2),
    (u'Mittwoch', 3),
    (u'Donnerstag', 4),
    (u'Freitag', 5),
    (u'Samstag', 6),
    (u'Sonntag', 7),
    (u'Mo-Fr', 8),
    (u'Mo-So', 9)))

umkreise = SimpleVocabulary((
    SimpleTerm('alle','alle',u'alle anzeigen'),
    SimpleTerm(10,10,u'10 km'),
    SimpleTerm(20,20,u'20 km'),
    SimpleTerm(30,30,u'30 km'),
    SimpleTerm(50,50,u'50 km'),
    SimpleTerm(100,100,u'100 km'),
    SimpleTerm(150,150,u'150 km')))

standorte = SimpleVocabulary((
    SimpleTerm(u'', u'', u'Auswahl'),
    SimpleTerm(u'rdost', u'rdost', u'RD Ost'),
    SimpleTerm(u'rdsuedost', u'rdsuedost', u'RD Südost'),
    SimpleTerm(u'rdsuedwest', u'rdsuedwest', u'RD Südwest'),
    SimpleTerm(u'rdwest', u'rdwest', u'RD West'),
    SimpleTerm(u'rdnord', u'rdnord', u'RD Nord')))

spezialgebiete = SimpleVocabulary((
    SimpleTerm(u'', u'', u'Auswahl'),
    SimpleTerm(u'assessmentverfahren', u'assessmentverfahren', u'Assessmentverfahren zur Teilhabe am Arbeitsleben'),
    SimpleTerm(u'beraterbghw', u'beraterbghw', u'ärztliche Berater/innen der BGHW'),
    SimpleTerm(u'berufsfindung', u'berufsfindung', u'Eignungsuntersuchung, Berufsfindung und Arbeitserprobung'),
    SimpleTerm(u'handkompetenzzentrum', u'handkompetenzzentrum', u'Hand-Kompetenzzentrum'),
    SimpleTerm(u'heilverfahrenskontrollen', u'heilverfahrenskontrollen', u'Ärzte und Kliniken für Heilverfahrenskontrollen'),
    SimpleTerm(u'kfzhilfe', u'kfzhilfe', u'Leistungserbringer im Rahmen der KFZ-Hilfe'),
    SimpleTerm(u'neurologischereha', u'neurologischereha', u'neurologische Rehabilitation'),
    SimpleTerm(u'pflegeanbieter', u'pflegeanbieter', u'Pflegeanbieter'),
    SimpleTerm(u'pflegeeinrichtung', u'pflegeeinrichtung', u'Pflegeeinrichtung, SHT und Querschnitt'),
    SimpleTerm(u'privarbeitsvermittler', u'privarbeitsvermittler', u'Private Arbeitsvermittler'),
    SimpleTerm(u'prothesensprechstunde', u'prothesensprechstunde', u'Prothesensprechstunde'),
    SimpleTerm(u'psycheaertzlich', u'psycheartzlich', u'BGU / SAV-Zentrum Psyche ärztlich'),
    SimpleTerm(u'psychetherapeutisch', u'psychetherapeutisch', u'Psyche therapeutisch'),
    SimpleTerm(u'rehaplan', u'rehaplan', u'Reha-Plan Sprechstunde'),
    SimpleTerm(u'schmerz', u'schmerz', u'Schmerz'),
    SimpleTerm(u'schuhsprechstunde', u'schuhsprechstunde', u'Schuhsprechstunde'),
    SimpleTerm(u'teilhabeleistung', u'teilhabeleistung', u'Einrichtungen zur Durchführung qualifizierter Teilhabeleistungen'),
    SimpleTerm(u'wohnungshilfe', u'wohnungshilfe', u'Wohnungshilfe')))

kontaktarten = SimpleVocabulary((
    SimpleTerm(u'telefon_arbeit', u'telefon_arbeit', u'Telefon Arbeit'),
    SimpleTerm(u'telefon_privat', u'telefon_privat', u'Telefon Privat'),
    SimpleTerm(u'telefon_zentrale', u'telefon_zentrale', u'Telefon Zentrale'),
    SimpleTerm(u'mobil', u'mobil', u'Mobiltelefon'),
    SimpleTerm(u'fax_arbeit', u'fax_arbeit', u'Telefax Arbeit'),
    SimpleTerm(u'fax_privat', u'fax_privat', u'Telefax Privat'),
    SimpleTerm(u'pager', u'pager', u'pager'),
    SimpleTerm(u'andere', u'andere', u'Andere'),
    SimpleTerm(u'email', u'email', u'E-Mail'),
    SimpleTerm(u'www', u'www', u'WWW'),
    ))

class IKontaktOptions(model.Schema):
    kontaktart = schema.Choice(title=u"Kontaktart",
                               source=kontaktarten,
                               required=True)
    kontaktadresse = schema.TextLine(title=u'Nummer, Adresse, Konto',
                                     required=True)
    bemerkung = schema.TextLine(title=u'Bemerkung',
                                required=False)


class IPartnerSearch(Interface):

    plz = schema.TextLine(
        title=_(u'Postleitzahl'),
        required=True,
    )

    strhnr = schema.TextLine(
        title=_(u'Strasse und Hausnummer des Kunden'),
        required=False
    )
   

    umkreis = schema.Choice(
        title=_(u'Angabe zur Umkreissuche'),
        vocabulary=umkreise,
        required=True,
    )

    art = schema.Choice(
        title=_(u'Art des Netzwerkpartners'),
        vocabulary=spezialgebiete,
        required=True,
        constraint = validatePartner
    )

    umkreis = schema.Choice(
        title=_(u'Angabe zur Umkreissuche'),
        vocabulary=umkreise,
        required=True,
    )

    @invariant
    def validateGeoData(data):
        if data.strhnr is not None and data.plz is not None:
            location = '%s, %s, Deutschland' %(data.strhnr, data.plz)
            latlong = geolocator.geocode(location, addressdetails=True, timeout=10)
            if not latlong:
                raise NoGeoLocation(u"Für diese Adresse kann keine Geolocation ermittelt werden.")

class IPartnerWordSearch(Interface):

    begriff = schema.TextLine(
        title=_(u'Suchbegriff'),
        required=True,
    )

    art = schema.Choice(
        title=_(u'Art des Netzwerkpartners'),
        vocabulary=spezialgebiete,
        required=False,
    )

class IOeffnung(Interface):

    wochentag = schema.Choice(
        title=u"Wochentag(e)",
        vocabulary=wochentage,
        required = True,
    )

    uhrzeit1von=schema.Choice(
        title=u"Zeit-1 von",
        vocabulary=uhrzeiten,
        required = True,
    )

    uhrzeit1bis = schema.Choice(
        title=u"Zeit-1 bis",
        vocabulary=uhrzeiten,
        required=True,
    )

    uhrzeit2von=schema.Choice(
        title=u"Zeit-2 von",
        vocabulary=uhrzeiten,
        required=False,
    )

    uhrzeit2bis = schema.Choice(
        title=u"Zeit-i2 bis",
        vocabulary=uhrzeiten,
        required=False,
    )

class NoGeoLocation(Invalid):
    __doc__ = u"Die Adressangabe ist nicht gültig."

class IPartner(Interface):

    title = schema.TextLine(
        title=_(u'Kurzname für den Netzwerkpartner'),
        description=_(u'Der Kurzname wird in allen Übersichten, Trefferlisten und\
                      in der Navigation angezeigt'),
        required=True,
    )

    art = schema.List(
        title=_(u'Art des Netzwerkpartners'),
        value_type = schema.Choice(vocabulary=spezialgebiete),
        required=True,
    )
    widget(art=CheckBoxFieldWidget)

    ik = schema.TextLine(
        title=_(u'Institutionskennzeichen'),
        required=False,
    )

    strhnr = schema.TextLine(
        title=_(u'Straße und Hausnummer'),
        required=False,
    )

    plz = schema.TextLine(
        title=_(u'Postleitzahl'),
        required=True,
    )

    ort = schema.TextLine(
        title=_(u'Ort'),
        required=True,
    )

    kontaktinformationen = schema.List(title=u"Kontaktinformationen",
                                       description=u"Bitte tragen Sie hier die Kontaktinformationen zum Netzwerkpartner ein.",
                                       value_type=DictRow(title=u"Kontaktliste", schema=IKontaktOptions),
                                       required=False)
    widget(kontaktinformationen=DataGridFieldFactory)

    oeffnungszeiten = schema.List(
        title=u'Liste der Öffnungszeiten und/oder Gesprächstermine',
        value_type = schema.TextLine(),
        required = False,
    )

    zusatzinfos = schema.List(
        title=u"Zusatzinformationen zum Netzwerkpartner",
        description=u"Informationen zu Fachgebieten, Fremdsprachenkenntnissen, etc. (1 Eintrag pro Zeile).",
        value_type = schema.TextLine(),
        required = False,
    )

    ansprechpartner = schema.List(
        title=_(u'Feste Ansprechpartner'),
        description=u'Bitte nur einen Namen pro Zeile eintragen',
        value_type = schema.TextLine(),
        required=False,
    )

    bghwansprechpartner = schema.List(
        title=_(u'BGHW Ansprechpartner'),
        description=u'Bitte nur einen Namen pro Zeile eintragen',
        value_type = schema.TextLine(),
        required=False,
    )

    bemerkungen = RichText(
        title=_(u'Bemerkungen'),
        required=False,
    )

    #@invariant
    #def validateGeoData(data):
    #    if data.strhnr is not None and data.plz is not None and data.ort is not None:
    #        location = '%s, Deutschland' %(data.plz)
    #        latlong = geolocator.geocode(location, addressdetails=True, timeout=10)
    #        if not latlong:
    #            location = '%s, %s, Deutschland' %(data.strhnr, data.ort)
    #            latlong = geolocator.geocode(location, addressdetails=True, timeout=10)
    #        if not latlong:
    #            raise NoGeoLocation(u"Für diese Adresse kann keine Geolocation ermittelt werden.")
    #        plz = latlong.raw['address']['postcode']
    #        meldung = u'Für Ihre Adresse wurde eine Geolocation mit der PLZ: %s ermittelt. Diese stimmt nicht mit der angegebenen PLZ überein.' % plz
    #        if plz != data.plz:
    #            raise NoGeoLocation(meldung)
            

class IPartnerOrdner(Interface):

    title = schema.TextLine(
        title=_(u'Title'),
        required=True,
    )

    description = schema.Text(
        title=_(u'Description'),
        required=False,
    )

@indexer(IPartner)
def suchbegriffIndexer(obj):
    wordlist = []
    wordlist += obj.title.split(' ')
    wordlist += obj.strhnr.split(' ')[:-1]
    wordlist += obj.ort.split(' ')
    if obj.ansprechpartner:
        for i in obj.ansprechpartner:
            draftlist = i.split(' ')
            if 'Frau' in draftlist:
                draftlist.remove('Frau')
            if 'Herr' in draftlist:
                draftlist.remove('Herr')
            if 'Dr.' in draftlist:
                draftlist.remove('Dr.')
            if 'Prof.' in draftlist:
                draftlist.remove('Prof.')
            wordlist += draftlist
    if obj.zusatzinfos:
        wordlist += obj.zusatzinfos
    if obj.bemerkungen:
        wordlist += obj.bemerkungen.raw.split(' ')
    if not wordlist:
        return ""
    suchstring = u' '.join(wordlist)
    print(suchstring)
    return suchstring

@indexer(IPartner)
def latitudeIndexer(obj):
    #Ein bereits indexiertes Objekt indexieren wir nicht erneut
    objuid = obj.UID()
    brains = ploneapi.content.find(UID=objuid)
    if brains:
        brain = brains[0]
        if brain.latitude:
            return brain.latitude
    ####
    location = '%s, Deutschland' %(obj.plz)
    latlong = geolocator.geocode(location, addressdetails=True, timeout=10)
    if not latlong:
        location = '%s, %s, Deutschland' %(obj.strhnr, obj.ort)
        latlong = geolocator.geocode(location, addressdetails=True, timeout=10)
    if not latlong:
        return
    sleep(1)
    print(latlong.latitude)
    return latlong.latitude

@indexer(IPartner)
def longitudeIndexer(obj):
    #Ein bereits indexiertes Objekt indexieren wir nicht erneut
    objuid = obj.UID()
    brains = ploneapi.content.find(UID=objuid)
    if brains:
        brain = brains[0]
        if brain.longitude:
            return brain.longitude
    ###
    location = '%s, Deutschland' %(obj.plz)
    latlong = geolocator.geocode(location, addressdetails=True, timeout=10)
    if not latlong:
        location = '%s, %s, Deutschland' %(obj.strhnr, obj.ort)
        latlong = geolocator.geocode(location, addressdetails=True, timeout=10)
    if not latlong:
        return
    sleep(1)
    print(latlong.longitude)
    return latlong.longitude

