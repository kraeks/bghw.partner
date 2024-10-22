from geopy.geocoders import Nominatim
from geopy.distance import vincenty
from zope.interface import Interface
from bghw.partner.interfaces import IPartnerSearch
from Products.CMFCore.utils import getToolByName
from plone.autoform.form import AutoExtensibleForm
from z3c.form import button, form

def getlatlong(address):
    geolocator = Nominatim()
    location = geolocator.geocode(address)
    return (location.latitude, location.longitude)
    
def getdistance(loc1, loc2):
    return vincenty(loc1, loc2).km



class PartnerSuche(AutoExtensibleForm, form.EditForm)):
    schema = IPartnerSearch
    ignoreContext = True

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @button.buttonAndHandler("Suchen")
    def handle_send(self):
        data, errors = self.extractData()
        if errors:
            return
        versichertencoordinates = getlatlong(data.get('ort'))
        pcat = self.portal_catalog
        brains = pcat(portal_type="Partner")
        myobj = brains[0].getObject()
        partner = '%s %s %s' %(myobj.strhnr, myobj.plz, myobj.ort)
        partnercoordinates = getlatlong(partner)
        distance = getdistance(partnercoordinates, versichertencoordinates)
