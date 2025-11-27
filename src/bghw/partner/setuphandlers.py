# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer
from Products.CMFCore.utils import getToolByName

@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller"""
        return [
            'bghw.partner:uninstall',
        ]


def post_install(context):
    """Post install script"""
    typesTool = getToolByName(context, 'portal_types')
    typefolder = typesTool['Folder']
    viewlist = typefolder.getProperty('view_methods', d=None)
    if 'partnersearch' not in viewlist:
        viewlist = viewlist + ('partnersearch',)
    typefolder.manage_changeProperties(view_methods = viewlist)

def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
