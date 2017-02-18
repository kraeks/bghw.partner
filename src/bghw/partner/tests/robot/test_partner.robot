# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s bghw.partner -t test_partner.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src bghw.partner.testing.BGHW_PARTNER_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_partner.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a Partner
  Given a logged-in site administrator
    and an add partner form
   When I type 'My Partner' into the title field
    and I submit the form
   Then a partner with the title 'My Partner' has been created

Scenario: As a site administrator I can view a Partner
  Given a logged-in site administrator
    and a partner 'My Partner'
   When I go to the partner view
   Then I can see the partner title 'My Partner'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add partner form
  Go To  ${PLONE_URL}/++add++Partner

a partner 'My Partner'
  Create content  type=Partner  id=my-partner  title=My Partner


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.title  ${title}

I submit the form
  Click Button  Save

I go to the partner view
  Go To  ${PLONE_URL}/my-partner
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a partner with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the partner title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
