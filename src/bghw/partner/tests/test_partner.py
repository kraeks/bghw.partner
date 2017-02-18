# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from bghw.partner.interfaces import IPartner
from bghw.partner.testing import BGHW_PARTNER_INTEGRATION_TESTING  # noqa
from zope.component import createObject
from zope.component import queryUtility

import unittest


class PartnerIntegrationTest(unittest.TestCase):

    layer = BGHW_PARTNER_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='Partner')
        schema = fti.lookupSchema()
        self.assertEqual(IPartner, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='Partner')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='Partner')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IPartner.providedBy(obj))

    def test_adding(self):
        obj = api.content.create(
            container=self.portal,
            type='Partner',
            id='Partner',
        )
        self.assertTrue(IPartner.providedBy(obj))
