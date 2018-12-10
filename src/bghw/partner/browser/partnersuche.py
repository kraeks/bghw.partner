from zope.interface import Interface
from uvc.api import api
from plone import api as ploneapi
from bghw.partner.interfaces import IPartnerSearch, IPartnerWordSearch, spezialgebiete
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from geopy.distance import great_circle
from operator import itemgetter

geolocator = Nominatim(user_agent="bghw.partner")

api.templatedir('templates')

class PartnerSearch(api.Form):
    api.context(Interface)
    label = u'Suche in der Partnerdatenbank'
    fields = api.Fields(IPartnerSearch)
    fields['plz'].htmlAttributes['maxlength'] = 5
    fields['plz'].htmlAttributes['size'] = 6

    ignoreContent = False

    def update(self):
        self.formurl = self.context.absolute_url() + '/partnersearch'
        self.altformurl = self.context.absolute_url() + '/partnerwordsearch'
        if not hasattr(self, 'partners'):
            self.partners = []

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
                    entry['telefon'] = obj.telefon
                    entry['distance'] = distance
                    entry['printdistance'] = "%.2f" % distance
                    self.partners.append(entry)
            else:
                obj = i.getObject()
                entry['title'] = obj.title
                entry['id'] = obj.UID()
                entry['url'] = obj.absolute_url()
                entry['plz'] = obj.plz
                entry['ort'] = obj.ort
                entry['telefon'] = obj.telefon
                entry['distance'] = distance
                entry['printdistance'] = "%.2f" % distance
                self.partners.append(entry)
        if self.partners:
            self.partners = sorted(self.partners, key=itemgetter('distance'))

class PartnerWordSearch(api.Form):
    api.context(Interface)
    label = u'Suche in der Partnerdatenbank'
    fields = api.Fields(IPartnerWordSearch)

    ignoreContent = False

    def update(self):
        self.formurl = self.context.absolute_url() + '/partnerwordsearch'
        self.altformurl = self.context.absolute_url() + '/partnersearch'
        if not hasattr(self, 'partners'):
            self.partners = []

    @api.action('Suchen')
    def handle_search(self):
        data, errors = self.extractData()
        if errors:
            return
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
            entry['telefon'] = obj.telefon
            partnerarten = []
            for k in obj.art:
                partnerarten.append(spezialgebiete.getTerm(k).title)
            entry['partnerarten'] = ', '.join(partnerarten)
            self.partners.append(entry)
        if self.partners:
            self.partners = sorted(self.partners, key=itemgetter('plz'))
