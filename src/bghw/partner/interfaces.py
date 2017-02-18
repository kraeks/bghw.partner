# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from bghw.partner import _
from zope import schema
from zope.interface import Interface
from plone.directives import form
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from plone.app.textfield import RichText
from collective.z3cform.datagridfield import DictRow, DataGridFieldFactory

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
    SimpleTerm(u'berlin', u'berlin', u'Berlin'),
    SimpleTerm(u'bonn', u'bonn', u'Bonn'),
    SimpleTerm(u'mannheim', u'mannheim', u'Mannheim')))

spezialgebiete = SimpleVocabulary((
    SimpleTerm(u'rehaplan', u'rehaplan', u'Reha-Plan Sprechstunde'),
    SimpleTerm(u'schuhsprechstunde', u'schuhsprechstunde', u'Schuhsprechstunde'),
    SimpleTerm(u'prothesensprechstunde', u'prothesensprechstunde', u'Prothesensprechstunde'),
    SimpleTerm(u'handkompetenzzentrum', u'handkompetenzzentrum', u'Hand-Kompetenzzentrum'),
    SimpleTerm(u'heilverfahrenskontrollen', u'heilverfahrenskontrollen', u'Ärzte und Kliniken für Heilverfahrenskontrollen')))


class IPartnerSearch(Interface):

    ort = schema.TextLine(
        title=_(u'Wohnort der versicherten Person'),
        required=False
    )

    plz = schema.TextLine(
        title=_(u'Postleitzahl der versicherten Person'),
        required=False
    )

    name = schema.TextLine(
        title=_(u'Name des Netzwerkpartners'),
        required=False
    )

    art = schema.Choice(
        title=_(u'Art des Netzwerkpartners'),
        vocabulary=spezialgebiete,
        required=False,
    )

    umkreis = schema.Choice(
        title=_(u'Angabe zur Umkreissuche'),
        vocabulary=umkreise,
        required=False,
    )

    bghw = schema.Choice(
        title=_(u'Angabe zum BGHW-Standort'),
        vocabulary=standorte,
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

    name = schema.TextLine(
        title=_(u'Name/Institution'),
        description=_(u'Hier kann ein alternativer Name für die Einzelansicht des\
                      des Netzwerkpartners eingetragen werden.'),
        required=False,
    )

    ik = schema.TextLine(
        title=_(u'Institutionskennzeichen'),
        required=False,
    )

    plz = schema.TextLine(
        title=_(u'Postleitzahl'),
        required=True,
    )

    strhnr = schema.TextLine(
        title=_(u'Straße und Hausnummer'),
        required=False,
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

    telefax = schema.TextLine(
        title=_(u'Telefax'),
        required=False,
    )

    email = schema.TextLine(
        title=_(u'eMail Adresse'),
        required=True,
    )

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

    form.widget(termine=DataGridFieldFactory)
    termine = schema.List(
        title = u'Liste der Öffnungszeiten und/oder Gesprächstermine',
        description = u"Bitte erstellen Sie hier eine Tabelle mit den Öffnungszeiten\
                    und/oder Gesprächsterminen. Bei durchgehender Öffnung bearbeiten\
                    sie bitte nur die den Zeitabschnitt 1",
        value_type = DictRow(title=u'Termine', schema=IOeffnung),
        required = False,
    )

    durchgehend = schema.Bool(
        title = u'Tägliche und durchgehende Öffnung',
        description = u'Bitte klicken Sie hier bei täglicher und durchgehender Öffnung',
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
