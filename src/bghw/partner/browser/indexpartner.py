from time import sleep
from zope.interface import Interface
from plone import api as ploneapi
from Products.Five.browser import BrowserView

counts = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600]

class reindexPartner(BrowserView):

    def __call__(self):
        brains = ploneapi.content.find(portal_type="Partner")
        count = 0
        for i in brains:
            sleep(1)
            obj = i.getObject()
            obj.reindexObject()
            if count in counts:
                sleep(30)
            count += 1
        return(f'Es wurden {count} Netzwerkpartner neu indexiert.')
