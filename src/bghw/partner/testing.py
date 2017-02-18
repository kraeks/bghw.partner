# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import bghw.partner


class BghwPartnerLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=bghw.partner)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'bghw.partner:default')


BGHW_PARTNER_FIXTURE = BghwPartnerLayer()


BGHW_PARTNER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(BGHW_PARTNER_FIXTURE,),
    name='BghwPartnerLayer:IntegrationTesting'
)


BGHW_PARTNER_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(BGHW_PARTNER_FIXTURE,),
    name='BghwPartnerLayer:FunctionalTesting'
)


BGHW_PARTNER_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        BGHW_PARTNER_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='BghwPartnerLayer:AcceptanceTesting'
)
