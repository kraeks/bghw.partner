# -*- coding: utf-8 -*-
from zope.interface import Interface
from uvc.api import api
from plone import api as ploneapi
from bghw.partner.interfaces import IPartnerSearch, IPartnerWordSearch, spezialgebiete, kontaktarten
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from geopy.distance import great_circle
from operator import itemgetter

geolocator = Nominatim(user_agent="bghw.partner")

api.templatedir('templates')

def getGlyph(value):
    glyphdict = {
        'telefon':'glyphicon glyphicon-earphone',
        'telefon_arbeit':'glyphicon glyphicon-earphone',
        'telefon_privat':'glyphicon glyphicon-earphone',
        'telefon_zentrale':'glyphicon glyphicon-earphone',
        'mobile':'glyphicon glyphicon-phone',
        'mobil':'glyphicon glyphicon-phone',
        'email':'',
        'fax_arbeit':'glyphicon glyphicon-print',
        'telefax':'glyphicon glyphicon-print',
        'fax_privat':'glyphicon glyphicon-print',
        'www':'glyphicon glyphicon-globe',
        'pager':'glyphicon glyphicon-flash',
        'andere':'glyphicon glyphicon-option-horizontal',
        }
    if value:
        return glyphdict.get(value)

class PartnerSearch(api.Form):
    api.context(Interface)
    label = u'Suche in der Partnerdatenbank'
    fields = api.Fields(IPartnerSearch)
    fields['plz'].htmlAttributes['maxlength'] = 5
    fields['plz'].htmlAttributes['size'] = 6

    ignoreContent = False

    def update(self):
        #self.portal_type = ''
        self.message = ''
        self.headimage = ''
        if self.context.image:
            self.headimage = "%s/@@images/image/large" %self.context.absolute_url()
        self.formurl = self.context.absolute_url() + '/partnersearch'
        self.altformurl = self.context.absolute_url() + '/partnerwordsearch'
        if not hasattr(self, 'partners'):
            self.partners = []

    def createKontaktinfos(self, obj):
        kontaktinfos = []
        oldkontakt = [(u'telefon', u'Telefon'), (u'telefax', u'Telefax'), (u'mobil', u'Mobil'), (u'email', u'E-Mail')]
        for value,title in oldkontakt:
            if getattr(obj, value, ''):
                wert = getattr(obj, value)
                if value == 'email':
                    wert = '<a href="mailto:%s">%s</a>' %(wert, wert)
                kontaktinfos.append((getGlyph(value), title, wert, ''))
        if obj.kontaktinformationen:
            for i in obj.kontaktinformationen:
                wert = i.get('kontaktadresse')
                if i.get('kontaktart') == 'email':
                    wert = '<a href="mailto:%s">%s</a>' %(wert, wert)
                if i.get('kontaktart') != 'www':
                    kontaktinfos.append((getGlyph(i.get('kontaktart')),
                                                       kontaktarten.getTerm(i.get('kontaktart')).title,
                                                       wert,
                                                       i.get('bemerkung')))
        return kontaktinfos 

    @api.action('Suchen')
    def handle_search(self):
        data, errors = self.extractData()
        if errors:
            return
        brains = ploneapi.content.find(portal_typ='Partner', art=data.get('art'))
        self.partners = []
        adresse = "%s, Deutschland" % data.get('plz')
        location = geolocator.geocode(adresse, timeout=10)
        location = (location.latitude, location.longitude)
        for i in brains:
            entry = {}
            partner = (i.latitude, i.longitude)
            distance = great_circle(location, partner).km
            if data.get('umkreis') != 'alle':
                if distance <= data.get('umkreis'):
                    obj = i.getObject()
                    entry['title'] = obj.title
                    entry['id'] = obj.UID()
                    entry['url'] = obj.absolute_url()
                    entry['plz'] = obj.plz
                    entry['ort'] = obj.ort
                    entry['kontakt'] = self.createKontaktinfos(obj)
                    entry['distance'] = distance
                    entry['printdistance'] = int(round(distance))
                    entry['zusatzinfos'] = obj.zusatzinfos
                    self.partners.append(entry)
            else:
                obj = i.getObject()
                entry['title'] = obj.title
                entry['id'] = obj.UID()
                entry['url'] = obj.absolute_url()
                entry['plz'] = obj.plz
                entry['ort'] = obj.ort
                entry['kontakt'] = self.createKontaktinfos(obj)
                entry['distance'] = distance
                entry['printdistance'] = int(round(distance))
                entry['zusatzinfos'] = obj.zusatzinfos
                self.partners.append(entry)
        if self.partners:
            self.partners = sorted(self.partners, key=itemgetter('distance'))
        else:
            self.message = u'Leider konnten für Ihre Angaben keine Netzwerkpartner gefunden werden. Bitte ändern Sie gegebenenfalls Ihre Angaben\
                            und versuchen es dann erneut.'
            #ploneapi.portal.show_message(self.message, self.request, type="error")
            #return self.response.redirect(self.formurl)

class PartnerWordSearch(api.Form):
    api.context(Interface)
    label = u'Suche in der Partnerdatenbank'
    fields = api.Fields(IPartnerWordSearch)

    ignoreContent = False

    def update(self):
        self.message = ''
        self.headimage = ''
        if self.context.image:
            self.headimage = "%s/@@images/image/large" %self.context.absolute_url()
        self.formurl = self.context.absolute_url() + '/partnerwordsearch'
        self.altformurl = self.context.absolute_url() + '/partnersearch'
        if not hasattr(self, 'partners'):
            self.partners = []

    def createKontaktinfos(self, obj):
        kontaktinfos = []
        oldkontakt = [(u'telefon', u'Telefon'), (u'telefax', u'Telefax'), (u'mobil', u'Mobil'), (u'email', u'E-Mail')]
        for value,title in oldkontakt:
            if getattr(obj, value, ''):
                wert = getattr(obj, value)
                if value == 'email':
                    wert = '<a href="mailto:%s">%s</a>' %(wert, wert)
                kontaktinfos.append((getGlyph(value), title, wert, ''))
        if obj.kontaktinformationen:
            for i in obj.kontaktinformationen:
                wert = i.get('kontaktadresse')
                if i.get('kontaktart') == 'email':
                    wert = '<a href="mailto:%s">%s</a>' %(wert, wert)
                if i.get('kontaktart') != 'www':
                    kontaktinfos.append((getGlyph(i.get('kontaktart')),
                                                       kontaktarten.getTerm(i.get('kontaktart')).title,
                                                       wert,
                                                       i.get('bemerkung')))
        return kontaktinfos


    @api.action('Suchen')
    def handle_search(self):
        data, errors = self.extractData()
        if errors:
            return
        if not data.get('art'):
            brains = ploneapi.content.find(portal_typ='Partner', partnersuche=data.get('begriff'))
        else:
            brains = ploneapi.content.find(portal_typ='Partner', partnersuche=data.get('begriff'), art=data.get('art'))
        self.partners = []
        for i in brains:
            entry = {}
            obj = i.getObject()
            entry['title'] = obj.title
            entry['id'] = obj.UID()
            entry['url'] = obj.absolute_url()
            entry['plz'] = obj.plz
            entry['ort'] = obj.ort
            entry['kontakt'] = self.createKontaktinfos(obj)
            partnerarten = []
            for k in obj.art:
                partnerarten.append(spezialgebiete.getTerm(k).title)
            entry['partnerarten'] = ', '.join(partnerarten)
            self.partners.append(entry)
        if self.partners:
            self.partners = sorted(self.partners, key=itemgetter('plz'))
        else:
            self.message = u'Leider konnten für Ihre Angaben keine Netzwerkpartner gefunden werden. Bitte ändern Sie gegebenenfalls Ihre Angaben und\
                           versuchen es dann erneut.'
            #ploneapi.portal.show_message(self.message, self.request, type="error")
            #return self.response.redirect(self.formurl)
