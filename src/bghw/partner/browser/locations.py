# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from Products.CMFCore.interfaces import IFolderish
from collective.beaker.interfaces import ISession
import jsonlib

class Locations(BrowserView):

    def __call__(self):
        locations = []
        session = ISession(self.request)
        if session.get('geodata'):
            locations = session.get('geodata')
        return jsonlib.write(locations)
