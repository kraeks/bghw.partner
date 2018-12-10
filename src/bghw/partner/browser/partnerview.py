from zope.interface import Interface
from bghw.partner.interfaces import IPartner, spezialgebiete, kontaktarten
from uvc.api import api
from plone import api as ploneapi

api.templatedir('templates')

def getGlyph(value):
    glyphdict = {
        'telefon':'glyphicon glyphicon-phone-alt',
        'telefon_arbeit':'glyphicon glyphicon-earphone',
        'telefon_privat':'glyphicon glyphicon-earphone',
        'telefon_zentrale':'glyphicon glyphicon-earphone',
        'mobile':'glyphicon glyphicon-phone',
        'mobil':'glyphicon glyphicon-phone',
        'email':'glyphicon glyphicon-send',
        'fax_arbeit':'glyphicon glyphicon-print',
        'telefax':'glyphicon glyphicon-print',
        'fax_privat':'glyphicon glyphicon-print',
        'www':'glyphicon glyphicon-globe',
        'pager':'glyphicon glyphicon-flash',
        'andere':'glyphicon glyphicon-option-horizontal',
        }
    if value:
        return glyphdict.get(value)

class Partnerview(api.Page):
    api.context(IPartner)

    def update(self):
        self.art = ''
        if self.context.art:
            partnertitel = []
            for i in self.context.art:
                partnertitel.append(spezialgebiete.getTerm(i).title)
            self.art = ', '.join(partnertitel)
        titname = ''
        if self.context.ansprechpartner:
            titname = self.context.ansprechpartner[0]
        self.anschrift="""\
%s
%s
%s
%s %s
        """ %(self.context.title, titname, self.context.strhnr, self.context.plz, self.context.ort)
        self.kontaktinfos = []
        oldkontakt = [(u'telefon', u'Telefon'), (u'telefax', u'Telefax'), (u'mobil', u'Mobil'), (u'email', u'E-Mail'), (u'www', u'WWW')]
        for value,title in oldkontakt:
            if getattr(self.context, value, ''):
                wert = getattr(self.context, value)
                if value == 'www':
                    wert = '<a href="%s" target="_blank">%s</a>' %(wert, wert)
                if value == 'email':
                    wert = '<a href="mailto:%s">%s</a>' %(wert, wert)
                self.kontaktinfos.append((getGlyph(value), title, wert, ''))
        if self.context.kontaktinformationen:
            for i in self.context.kontaktinformationen:
                wert = i.get('kontaktadresse')
                if i.get('kontaktart') == 'www':
                    wert = '<a href="%s" target="_blank">%s</a>' %(wert, wert)
                if i.get('kontaktart') == 'email':
                    wert = '<a href="mailto:%s">%s</a>' %(wert, wert)
                self.kontaktinfos.append((getGlyph(i.get('kontaktart')), 
                                                   kontaktarten.getTerm(i.get('kontaktart')).title,
                                                   wert,
                                                   i.get('bemerkung')))
