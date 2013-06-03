from collective.favoriting.tests import base


class TestStorage(base.IntegrationTestCase):

    def setUp(self):
        from collective.favoriting import storage
        super(TestStorage, self).setUp()
        self.storage = storage.FavoritingManager(self.document, self.request)

    def test_call(self):
        self.assertEqual(self.storage(), self.storage)

    def test_update(self):
        self.assertIsNone(self.storage.catalog)
        self.assertIsNone(self.storage.membership)
        self.assertIsNone(self.storage.userid)
        self.assertIsNone(self.storage.storage)
        self.storage.update()
        self.assertIsNotNone(self.storage.catalog)
        self.assertIsNotNone(self.storage.membership)
        self.assertIsNotNone(self.storage.userid)
        self.assertIsNotNone(self.storage.storage)

    def test_add_and_get_and_rm(self):
        self.assertEqual(len(self.storage.get()), 0)
        self.assertTrue(not self.storage.isin())
        self.storage.add()
        self.assertEqual(len(self.storage.get()), 1)
        self.assertTrue(self.storage.isin())
        self.storage.rm()
        self.assertEqual(len(self.storage.get()), 0)
        self.assertTrue(not self.storage.isin())
