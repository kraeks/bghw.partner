# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from Products.CMFCore.interfaces import IFolderish
from collective.beaker.interfaces import ISession
import json

class Locations(BrowserView):

    def __call__(self):
        locations = []
        session = ISession(self.request)
        if session.get('geodata'):
            locations = session.get('geodata')
        return json.dumps(locations)
