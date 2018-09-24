# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from bghw.partner import _
from zope import schema
from zope.interface import Interface
from plone.directives import form
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from plone.app.textfield import RichText
from plone.indexer import indexer
from collective.z3cform.datagridfield import DictRow, DataGridFieldFactory
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from geopy.geocoders import Nominatim

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
    SimpleTerm(0,0,u'Auswahl'),
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
    SimpleTerm(u'rehaplan', u'rehaplan', u'Reha-Plan Sprechstunde'),
    SimpleTerm(u'schuhsprechstunde', u'schuhsprechstunde', u'Schuhsprechstunde'),
    SimpleTerm(u'prothesensprechstunde', u'prothesensprechstunde', u'Prothesensprechstunde'),
    SimpleTerm(u'handkompetenzzentrum', u'handkompetenzzentrum', u'Hand-Kompetenzzentrum'),
    SimpleTerm(u'psycheaertzlich', u'psycheartzlich', u'BGU / SAV-Zentrum Psyche ärztlich'),
    SimpleTerm(u'psychetherapeutisch', u'psychetherapeutisch', u'Psyche therapeutisch'),
    SimpleTerm(u'schmerz', u'schmerz', u'Schmerz'),
    SimpleTerm(u'beraterbghw', u'beraterbghw', u'ärztliche Berater/innen der BGHW'),
    SimpleTerm(u'heilverfahrenskontrollen', u'heilverfahrenskontrollen', u'Ärzte und Kliniken für Heilverfahrenskontrollen'),
    SimpleTerm(u'assessmentverfahren', u'assessmentverfahren', u'Assessmentverfahren zur Teilhabe am Arbeitsleben'),
    SimpleTerm(u'berufsfindung', u'berufsfindung', u'Eignungsuntersuchung, Berufsfindung und Arbeitserprobung'),
    SimpleTerm(u'teilhabeleistung', u'teilhabeleistung', u'Einrichtungen zur Durchführung qualifizierter Teilhabeleistungen'),
    SimpleTerm(u'privarbeitsvermittler', u'privarbeitsvermittler', u'Private Arbeitsvermittler'),
    SimpleTerm(u'kfzhilfe', u'kfzhilfe', u'Leistungserbringer im Rahmen der KFZ-Hilfe'),
    SimpleTerm(u'pflegeanbieter', u'pflegeanbieter', u'Pflegeanbieter'),
    SimpleTerm(u'pflegeeinrichtung', u'pflegeeinrichtung', u'Pflegeeinrichtung, SHT und Querschnitt'),
    SimpleTerm(u'neurologischereha', u'neurologischereha', u'neurologische Rehabilitation'),
    SimpleTerm(u'wohnungshilfe', u'wohnungshilfe', u'Wohnungshilfe')))

class IPartnerSearch(Interface):

    plz = schema.TextLine(
        title=_(u'Postleitzahl der versicherten Person'),
        required=True
    )

    art = schema.Choice(
        title=_(u'Art des Netzwerkpartners'),
        vocabulary=spezialgebiete,
        required=True,
    )

    umkreis = schema.Choice(
        title=_(u'Angabe zur Umkreissuche'),
        vocabulary=umkreise,
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


class IPartner(Interface):

    title = schema.TextLine(
        title=_(u'Kurzname für den Netzwerkpartner'),
        description=_(u'Der Kurzname wird in allen Übersichten, Trefferlisten und\
                      in der Navigation angezeigt'),
        required=True,
    )

    description = schema.Text(
        title=_(u'Beschreibung'),
        description=_(u'Hier können Sie die Leistungen des Netzwerkpartners kurz\
                      beschreiben, z.B.: Spezialist im Bereich Schmerztherapie'),
        required=False,
    )

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

    www = schema.URI(
        title=_(u'Weblink/Homepage'),
        required=False,
    )

    telefon = schema.TextLine(
        title=_(u'Telefon'),
        required=True,
    )

    mobil = schema.TextLine(
        title=_(u'Mobiltelefon'),
        required=False,
    )

    telefax = schema.TextLine(
        title=_(u'Telefax'),
        required=False,
    )

    email = schema.TextLine(
        title=_(u'eMail Adresse'),
        required=True,
    )

    form.widget(art=CheckBoxFieldWidget)
    art = schema.List(
        title=_(u'Art des Netzwerkpartners'),
        value_type = schema.Choice(vocabulary=spezialgebiete),
        required=True,
    )

    ansprechpartner = schema.List(
        title=_(u'Feste Ansprechpartner'),
        description=u'Bitte nur einen Namen pro Zeile eintragen',
        value_type = schema.TextLine(),
        required=False,
    )

    oeffnungszeiten = schema.List(
        title=u'Liste der Öffnungszeiten und/oder Gesprächstermine',
        value_type = schema.TextLine(),
        required = False,
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
def latitudeIndexer(obj):
    if obj.strhnr:
        location = '%s, %s %s, Deutschland' %(obj.strhnr, obj.plz, obj.ort)
    else:
        location = '%s %s, Deutschland' %(obj.plz, obj.ort)
    try:
        latitude = geolocator.geocode(location).latitude
    except:
        latitude = ''
    return latitude

@indexer(IPartner)
def longitudeIndexer(obj):
    if obj.strhnr:
        location = '%s, %s %s, Deutschland' %(obj.strhnr, obj.plz, obj.ort)
    else:
        location = '%s %s, Deutschland' %(obj.plz, obj.ort)
    try:
        longitude = geolocator.geocode(location).longitude
    except:
        longitude = ''
    return longitude

