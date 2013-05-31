from zope import interface
from zope import schema
from zope.annotation import factory
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.interfaces.base import IBaseObject


class IFavoritingManager(interface.Interface):
    """The main component API"""

    context = schema.Object(title=u"Context")
    request = schema.Object(title=u"Request")

    def get():
        """Return the list of all content favorited by the current user"""

    def add():
        """add the current context to the favorites of the current user"""

    def rm():
        """Remove the current context from the favorites."""

    def isIn():
        """Return True if the current context is in the favorites of the
        current user"""


class IFavoritingStorage(interface.Interface):
    """a list of all user who have favoriting this object"""
    favoritedby = schema.List(
        title=u"Favorited by",
        value_type=schema.TextLine(title=u"User ID")
    )


class ArchetypesFavoritingStorage(object):
    interface.implements(IFavoritingStorage)
    adapts(IBaseObject)
    def __init__(self):
        """
        Note that the annotation implementation does not expect any arguments
        to its `__init__`. Otherwise it's basically an adapter.
        """
        self.favoritedby = []


ArchetypesFavoritingStorageFactory = factory(ArchetypesFavoritingStorage)


class FavoritingManager(BrowserView):
    """implementation of IFavoriting using annotation + portal_catalog"""
    interface.implements(IFavoritingManager)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.userid = None
        self.membership = None
        self.catalog = None
        self.favorites = []
        self.storage = None

    def update(self):
        context = self.context
        if self.catalog is None:
            self.catalog = getToolByName(context, 'portal_catalog')
        if self.membership is None:
            self.membership = getToolByName(context, 'portal_membership')
        if self.userid is None:
            user = self.portal_membership.getAuthenticatedMember()
            if user:
                self.userid = user.getId()
        if self.storage is None:
            self.storage = IFavoritingStorage(self.context)

    def get(self):
        self.update()
        query = {"favoritedby": self.userid}
        favorites = self.catalog(**query)
        return favorites

    def add(self):
        self.update()
        self.storage.favoritedby.append(self.userid)

    def rm(self):
        self.update()
        self.storage.favoritedby.pop(self.userid)

    def isIn(self):
        self.update()
        return self.userid in self.storage.favoritedby
