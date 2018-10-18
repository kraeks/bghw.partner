from zope.interface import Interface
from uvc.api import api
from plone import api as ploneapi

class reindexPartner(api.Page):
    api.context(Interface)

    def render(self):
        brains = ploneapi.content.find(portal_type="Partner")
        count = 0
        for i in brains:
            obj = i.getObject()
            obj.reindexObject()
            count += 1
        return 'Es wurden %s Netzwerkpartner neu indexiert.' % count
