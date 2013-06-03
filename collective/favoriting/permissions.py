from AccessControl.SecurityInfo import ModuleSecurityInfo
from Products.CMFCore.permissions import setDefaultRoles

security = ModuleSecurityInfo('Products.CMFCore.permissions')

security.declarePublic('AddToFavorites')
AddToFavorites = 'collective.favoriting: Add'
setDefaultRoles(AddToFavorites, ('Member', 'Manager'))
