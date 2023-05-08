# -*- coding: utf-8 -*-
import transaction
from time import sleep
from plone import api
from Products.Five.browser import BrowserView


class PartnerIndex(BrowserView):
    """Temporary Script to Index new Netzwerkpartner"""

    def __call__(self):
        brains = api.content.find(portal_type="Partner")
        print "Gesamte Partner objekte zu indixieren %s:" % (len(brains))
        counter_partner = 0
        for i in brains:
            sleep(1)
            obj = i.getObject()
            obj.reindexObject()
            transaction.commit()
            sleep(40)
            counter_partner += 1
            print '%s Netzwerkpartner wurden indexiert' % counter_partner
        return 'Fertig - Es wurden %s Netzwerkpartner neu indexiert.' % counter_partner
