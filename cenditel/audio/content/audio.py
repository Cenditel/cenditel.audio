"""Definition of the audio content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.validation import V_REQUIRED
from Products.validation.config import validation

# -*- Message Factory Imported Here -*-
from cenditel.audio import audioMessageFactory as _

from cenditel.audio.interfaces import Iaudio
from cenditel.audio.config import PROJECTNAME
from cenditel.audio.validators import ContentTypeAudioValidator, TranscodeAudioValidator

# -*- FileSystemStorage Import here -*-
from iw.fss.FileSystemStorage import FileSystemStorage

audioSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    atapi.FileField(
        name='audio',
        widget=atapi.FileWidget(
            label=_(u"Audio"),
            description=_(u"The Audio file to be uploaded")
        ),
        required=True,
        searchable=True,
        storage=FileSystemStorage(),
        validators=(
            ('checkFileMaxSize',V_REQUIRED),
            (ContentTypeAudioValidator()),
            (TranscodeAudioValidator()),
        ),
    
    ),

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

audioSchema['title'].storage = atapi.AnnotationStorage()
audioSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(audioSchema, moveDiscussion=False)


class audio(base.ATCTContent):
    """It's audio Streming using html5"""
    implements(Iaudio)
    _at_rename_after_creation=True
    meta_type = "audio"
    schema = audioSchema
    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(audio, PROJECTNAME)
