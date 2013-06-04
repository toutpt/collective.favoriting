import unittest2 as unittest
from collective.favoriting.tests import base
ACTION_IDS = ("favoriting_rm", "favoriting_add", "favoriting_view")


class TestSetup(base.IntegrationTestCase):
    """We tests the setup (install) of the addons. You should check all
    stuff in profile are well activated (browserlayer, js, content types, ...)
    """

    def test_default_profile_actions(self):
        document_actions = self.layer['portal'].portal_actions.document_actions
        actions = [
            action for action in document_actions.listActions()
            if action.visible and action.id in ACTION_IDS
        ]
        self.assertEqual(len(actions), 2)
        action_info = actions[0].getInfoData()[0]
        self.assertEqual(action_info['category'], 'document_actions')
        self.assertEqual(
            action_info['available'].text,
            'not:object/@@collective.favoriting/isin'
        )
        self.assertEqual(action_info['description'], u"")
        self.assertEqual(action_info['title'], u'Add to favorite')
        self.assertEqual(
            action_info['url'].text,
            u'string:$object_url/favoriting_add'
        )
        self.assertEqual(
            action_info['permissions'], ('collective.favoriting: Add',),
        )
        self.assertIsNone(action_info['link_target'])
        self.assertEqual(action_info['id'], 'favoriting_add')
        self.assertEqual(action_info['icon'], '')

        action_info = actions[1].getInfoData()[0]
        self.assertEqual(action_info['category'], 'document_actions')
        self.assertEqual(
            action_info['available'].text,
            'object/@@collective.favoriting/isin'
        )
        self.assertEqual(action_info['description'], u"")
        self.assertEqual(action_info['title'], u'Remove from favorite')
        self.assertEqual(
            action_info['url'].text,
            u'string:$object_url/favoriting_rm'
        )
        self.assertEqual(
            action_info['permissions'], ('collective.favoriting: Add',),
        )
        self.assertIsNone(action_info['link_target'])
        self.assertEqual(action_info['id'], 'favoriting_rm')
        self.assertEqual(action_info['icon'], '')

        user_actions = self.layer['portal'].portal_actions.user
        actions = [
            action for action in user_actions.listActions()
            if action.visible and action.id in ACTION_IDS
        ]
        self.assertEqual(len(actions), 1)
        action_info = actions[0].getInfoData()[0]
        self.assertEqual(action_info['category'], 'user')
        self.assertEqual(
            action_info['available'].text,
            "python:member is not None"
        )
        self.assertEqual(action_info['description'], u"")
        self.assertEqual(action_info['title'], u'My favorites')
        self.assertEqual(
            action_info['url'].text,
            u'string:${globals_view/navigationRootUrl}/@@favoriting_view'
        )
        self.assertEqual(
            action_info['permissions'], ('collective.favoriting: Add',),
        )
        self.assertIsNone(action_info['link_target'])
        self.assertEqual(action_info['id'], 'favoriting_view')
        self.assertEqual(action_info['icon'], '')

    def test_browserlayer(self):
        from plone.browserlayer import utils
        from collective.favoriting import layer
        self.assertIn(layer.Layer, utils.registered_layers())

    def test_catalog(self):
        catalog = self.layer['portal'].portal_catalog
        idx_fav = catalog._catalog.indexes['favoritedby']
        self.assertEqual(type(idx_fav).__name__, "KeywordIndex")
        self.assertEqual(idx_fav.indexed_attrs, ['favoritedby'])

    def test_upgrades(self):
        profile = 'collective.favoriting:default'
        setup = self.layer['portal'].portal_setup
        upgrades = setup.listUpgrades(profile, show_old=True)
        self.assertTrue(len(upgrades) > 0)
        for upgrade in upgrades:
            upgrade['step'].doStep(setup)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
