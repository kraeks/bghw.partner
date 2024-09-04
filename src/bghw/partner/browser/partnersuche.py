# -*- coding: utf-8 -*-
import os
from zope.interface import Interface
from plone import api as ploneapi
from bghw.partner.interfaces import IPartnerSearch, IPartnerWordSearch, spezialgebiete, kontaktarten
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from geopy.distance import great_circle
from operator import itemgetter
from collective.beaker.interfaces import ISession
from plone.autoform.form import AutoExtensibleForm
from z3c.form import button, form
from zope.interface import Interface
import plone.z3cform.layout
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

module_dir = os.path.dirname(os.path.abspath(__file__))
module_dir = f'{module_dir}/templates/'
geolocator = Nominatim(user_agent="bghw.partner")

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

class PartnerSearch(AutoExtensibleForm, form.EditForm):
    schema = IPartnerSearch
    ignoreContext = True

    label = u'Suche in der Partnerdatenbank'
    description = u"Test"
    #fields = api.Fields(IPartnerSearch)
    #fields['plz'].htmlAttributes['maxlength'] = 5
    #fields['plz'].htmlAttributes['size'] = 6


    def get_image(self):
        if self.context.image:
            return "%s/@@images/image/large" %self.context.absolute_url()
        return ''

    def get_altformurl(self):
        return self.context.absolute_url() + '/partnerwordsearch'

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

    @button.buttonAndHandler("Suchen")
    def handle_search(self):
        data, errors = self.extractData()
        if errors:
            return
        brains = ploneapi.content.find(path='/inwiportal/inwi-rul/sonstige-dateien/netzwerkpartner', portal_typ='Partner', art=data.get('art'))
        self.partners = []
        adresse = "%s, Deutschland" % data.get('plz')
        if data.get('strhnr'):
            adresse = "%s, %s, Deutschland" % (data.get('strhnr'), data.get('plz'))
        location = geolocator.geocode(adresse, timeout=10)
        geolocations = []
        if location:
            location = (location.latitude, location.longitude)
            geolocation = {"title": "Adresse Kunde",
                       "lon": location[1],
                       "lat": location[0],
                       "color": '#555555'}
            geolocations = [geolocation]
        session = ISession(self.request)
        uids = []
        for i in brains:
            entry = {}
            partner = (i.latitude, i.longitude)
            distance = great_circle(location, partner).km
            if data.get('umkreis') != 'alle':
                if distance <= data.get('umkreis'):
                    try:
                        obj = i.getObject()
                    except:
                        continue
                    entry['title'] = obj.title
                    entry['id'] = obj.UID()
                    entry['url'] = obj.absolute_url()
                    entry['plz'] = obj.plz
                    entry['ort'] = obj.ort
                    entry['kontakt'] = self.createKontaktinfos(obj)
                    entry['distance'] = distance
                    entry['printdistance'] = int(round(distance))
                    entry['zusatzinfos'] = obj.zusatzinfos
                    if obj.UID() not in uids:
                        uids.append(obj.UID())
                        self.partners.append(entry)
                        geolocation = {"title": obj.title,
                            "lon": i.longitude,
                            "lat": i.latitude,
                            "color": '#004994'}
                        geolocations.append(geolocation)

            else:
                try:
                    obj = i.getObject()
                except:
                    continue
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
                if obj.UID() not in uids:
                    uids.append(obj.UID())
                    self.partners.append(entry)
                    geolocation = {"title": obj.title,
                        "lon": i.longitude,
                        "lat": i.latitude,
                        "color": '#004994'}
                    geolocations.append(geolocation)

        if self.partners:
            self.partners = sorted(self.partners, key=itemgetter('distance'))
        else:
            self.message = u'Leider konnten für Ihre Angaben keine Netzwerkpartner gefunden werden. Bitte ändern Sie gegebenenfalls Ihre Angaben\
                            und versuchen es dann erneut.'
            #ploneapi.portal.show_message(self.message, self.request, type="error")
            #return self.response.redirect(self.formurl)
        session['geodata'] = geolocations
        session.save()

partnertemplate = os.path.join(module_dir, 'partnersearch.pt')
partnersearchform = plone.z3cform.layout.wrap_form(PartnerSearch, index=ViewPageTemplateFile(partnertemplate))

class PartnerWordSearch(AutoExtensibleForm, form.EditForm):
    schema = IPartnerWordSearch
    ignoreContext = True

    label = u'Suche in der Partnerdatenbank'

    def get_image(self):
        if self.context.image:
            return "%s/@@images/image/large" %self.context.absolute_url()
        return ''

    def get_altformurl(self):
        return self.context.absolute_url()

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


    @button.buttonAndHandler("Suchen")
    def handle_search(self):
        data, errors = self.extractData()
        if errors:
            return
        if not data.get('art'):
            brains = ploneapi.content.find(portal_typ='Partner', partnersuche=data.get('begriff') + "*")
        else:
            brains = ploneapi.content.find(portal_typ='Partner', partnersuche=data.get('begriff') + "*", art=data.get('art'))
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
