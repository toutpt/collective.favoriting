from plone.app.testing import *
import collective.favoriting


FIXTURE = PloneWithPackageLayer(
    zcml_filename="configure.zcml",
    zcml_package=collective.favoriting,
    additional_z2_products=[],
    gs_profile_id='collective.favoriting:default',
    name="collective.favoriting:FIXTURE"
)

INTEGRATION = IntegrationTesting(
    bases=(FIXTURE,), name="collective.favoriting:Integration"
)

FUNCTIONAL = FunctionalTesting(
    bases=(FIXTURE,), name="collective.favoriting:Functional"
)
