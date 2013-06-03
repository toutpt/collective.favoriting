import unittest2 as unittest
from zope import interface
from Products.statusmessages.interfaces import IStatusMessage
from collective.favoriting.tests import base


class TestViews(base.IntegrationTestCase):

    def setUp(self):
        from collective.favoriting.browser import favoriting_view as view
        from collective.favoriting.layer import Layer
        super(TestViews, self).setUp()
        interface.directlyProvides(self.request, Layer)
        self.add_view = view.Add(self.document, self.request)
        self.rm_view = view.Rm(self.document, self.request)
        self.isin_view = view.Isin(self.document, self.request)

    def test_add(self):
        res = self.add_view()
        self.assertTrue(res is None)
        status = IStatusMessage(self.request)
        messages = status.showStatusMessages()
        message = messages[0]
        self.assertEqual(len(messages), 1)
        self.assertEqual(message.message, u'Added to favorite')
        response = self.request.response
        doc_url = self.document.absolute_url()
        self.assertEqual(response.status, 302)
        self.assertEqual(response.getHeader('location'), doc_url)

    def test_rm(self):
        self.add_view()
        res = self.rm_view()
        self.assertTrue(res is None)
        status = IStatusMessage(self.request)
        messages = status.showStatusMessages()
        message = messages[1]
        self.assertEqual(len(messages), 2)
        self.assertEqual(message.message, u'Removed from favorite')
        response = self.request.response
        doc_url = self.document.absolute_url()
        self.assertEqual(response.status, 302)
        self.assertEqual(response.getHeader('location'), doc_url)

    def test_isin(self):
        self.assertTrue(not self.isin_view())
        self.add_view()
        self.assertTrue(self.isin_view())
