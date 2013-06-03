*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Test Setup  Open test browser
Test Teardown  Close all browsers

*** Test Cases ***

Login and add home page to favorite
    Go to homepage
    Page Should Not Contain    css=#document-action-favoriting_add
    Page Should Not Contain    css=#document-action-favoriting_rm
    Log in as site owner
    Go to  ${PLONE_URL}/createObject?type_name=Document
    Input text  name=title  An edited page
    Click Button  Save
    Page Should Contain Element    css=#document-action-favoriting_add
    Page Should Not Contain    css=#document-action-favoriting_rm
    Click Element    css=#document-action-favoriting_add a
    Page Should Not Contain    css=#document-action-favoriting_add
    Page Should Contain Element    css=#document-action-favoriting_rm
    Go to  ${PLONE_URL}/@@favoriting_view
    Page Should Contain Element    css=table#favorites
    Table Row Should Contain    favorites  2  An edited page
