# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from bghw.partner.testing import BGHW_PARTNER_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that bghw.partner is properly installed."""

    layer = BGHW_PARTNER_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if bghw.partner is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'bghw.partner'))

    def test_browserlayer(self):
        """Test that IBghwPartnerLayer is registered."""
        from bghw.partner.interfaces import (
            IBghwPartnerLayer)
        from plone.browserlayer import utils
        self.assertIn(IBghwPartnerLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = BGHW_PARTNER_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['bghw.partner'])

    def test_product_uninstalled(self):
        """Test if bghw.partner is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'bghw.partner'))

    def test_browserlayer_removed(self):
        """Test that IBghwPartnerLayer is removed."""
        from bghw.partner.interfaces import \
            IBghwPartnerLayer
        from plone.browserlayer import utils
        self.assertNotIn(IBghwPartnerLayer, utils.registered_layers())
