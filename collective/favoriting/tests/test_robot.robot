*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Test Setup  Open test browser
Test Teardown  Close all browsers

*** Test Cases ***

Create content and check history is working
    Go to homepage
    Page Should Not Contain    css=#document-action-favoriting_add
    Page Should Not Contain    css=#document-action-favoriting_rm
    Log in as site owner
    Page Should Contain Element    css=#document-action-favoriting_add
    Page Should Not Contain    css=#document-action-favoriting_rm
    Click Element    css=#document-action-favoriting_add
    Page Should Not Contain    css=#document-action-favoriting_add
    Page Should Contain Element    css=#document-action-favoriting_rm
