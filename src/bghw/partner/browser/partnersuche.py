from zope.interface import Interface
from uvc.api import api
from plone import api as ploneapi
from bghw.partner.interfaces import IPartnerSearch
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

    ignoreContent = False


    def update(self):
        self.formurl = self.context.absolute_url() + '/partnersearch'
        if not hasattr(self, 'partners'):
            self.partners = []

    @api.action('Suchen')
    def handle_search(self):
        data, errors = self.extractData()
        if errors:
            return
        brains = ploneapi.content.find(portal_typ='Partner', art=data.get('art'))
        self.partners = []
        for i in brains:
            entry = {}
            adresse = "%s, Deutschland" % data.get('plz')
            location = geolocator.geocode(adresse)
            location = (location.latitude, location.longitude)
            partner = (i.latitude, i.longitude)
            distance = great_circle(location, partner).km
            if data.get('distance'):
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
