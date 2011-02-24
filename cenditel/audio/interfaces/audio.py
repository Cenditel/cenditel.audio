from zope.interface import Interface
# -*- Additional Imports Here -*-
from plone.theme.interfaces import IDefaultPloneLayer


class Iaudio(Interface):
    """It's audio Streming using html5"""

    # -*- schema definition goes here -*-
class IaudioSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 skin layer 
       for this product."""
