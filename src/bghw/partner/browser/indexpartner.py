from time import sleep
from zope.interface import Interface
from uvc.api import api
from plone import api as ploneapi

counts = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600]

class reindexPartner(api.Page):
    api.context(Interface)

    def render(self):
        brains = ploneapi.content.find(portal_type="Partner")
        count = 0
        for i in brains:
            obj = i.getObject()
            obj.reindexObject()
            if count in counts:
                sleep(60)
            count += 1
        return 'Es wurden %s Netzwerkpartner neu indexiert.' % count
