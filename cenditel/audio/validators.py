#!/usr/bin/env python
from Products.validation.config import validation
try:
    from Products.validation.interfaces.IValidator import IValidator
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir))
    from interfaces.IValidator import IValidator
    del sys, os
#MaxSizeValidator Validator Imports
from Products.ATContentTypes.configuration import zconf
from Acquisition import aq_base
from DateTime import DateTime
from ZPublisher.HTTPRequest import FileUpload

#Utility control panel
from zope.component import getMultiAdapter
from zope.component import getUtility
from plone.registry.interfaces import IRegistry

#
from cenditel.transcodedeamon.interfaces import ITranscodeSetings
from cenditel.audio import audioMessageFactory as _

#
from zope.i18n import translate

#ContentType Validator Import
from Products.CMFCore.utils import getToolByName
from zope.interface import implements
from Products.validation.i18n import recursiveTranslate
from Products.validation.i18n import safe_unicode

ValidatorsList=[]


class EvilValidator:
    __implements__ = IValidator

    def __init__(self,
                 name,
                 title='Evil validator',
                 description='You will fail'):
        self.name = name
        self.title = title or name
        self.description = description

    def __call__(self, value, *args, **kwargs):
        instance = kwargs.get('instance', None)
        field    = kwargs.get('field', None)
        import pdb; pdb.set_trace()
        return('Moahahahaha - you FAIL!')

ValidatorsList.append(EvilValidator('evilness', title='', description=''))

class FileSizeValidator:
    """Tests if an upload, file or something supporting len() is smaller than a
       given max size value

    If it's a upload or file like thing it is using seek(0, 2) which means go
    to the end of the file and tell() to get the size in bytes otherwise it is
    trying to use len()

    The maxsize can be acquired from the kwargs in a call, a
    getMaxSizeFor(fieldname) on the instance, a maxsize attribute on the field
    or a given maxsize at validator initialization.
    """
    __implements__=IValidator

    def __init__(self, name, title='', description='', maxsize=0):
        self.name = name
        self.title = title or name
        self.description = description
        self.maxsize = maxsize
        
    def __call__(self, value, *args, **kwargs):
        instance = kwargs.get('instance', None)
        field    = kwargs.get('field', None)

        # get max size
        
        if kwargs.has_key('maxsize'):
            maxsize = kwargs.get('maxsize')
        elif hasattr(aq_base(instance), 'getMaxSizeFor'):
            maxsize = instance.getMaxSizeFor(field.getName())
        elif hasattr(field, 'maxsize'):
            maxsize = field.maxsize
        else:
            # set to given default value (default defaults to 0)
            registry = getUtility(IRegistry)
            settings = registry.forInterface(ITranscodeSetings)
            maxsize = settings.max_file_size
        if not maxsize:
            return True

        # calculate size
        elif (isinstance(value, FileUpload) or isinstance(value, file) or
              hasattr(aq_base(value), 'tell')):
            value.seek(0, 2) # eof
            size = value.tell()
            value.seek(0)
        else:
            try:
                size = len(value)
            except TypeError:
                size = 0
        size = float(size)
        sizeMB = (size / (1024 * 1024))

        if sizeMB > maxsize:
            msg = _("Validation failed(Uploaded data is too large: ${size}MB (max ${max}MB))",
                    mapping = {
                        'size' : safe_unicode("%.3f" % sizeMB),
                        'max' : safe_unicode("%.3f" % maxsize)
                        })
            return recursiveTranslate(msg, **kwargs)
        else:
            return True

ValidatorsList.append(FileSizeValidator('checkFileMaxSize',
                                     maxsize=zconf.ATFile.max_file_size))

class NameValidator:
    
    __implements__=IValidator
    
    def __init__(self, name='', title='', description=''):
        self.name=name
        self.title=title
        self.decription=description
    
    def __call__(self, value, *args, **kwargs):
        instance = kwargs.get('instance', None)
        field    = kwargs.get('field', None)
        
        
try: # Plone 4 and higher
    import plone.app.upgrade
    USE_BBB_VALIDATORS = False
except ImportError: # BBB Plone 3
    USE_BBB_VALIDATORS = True

class ContentTypeAudioValidator:
    """Validates a file to be of one of the given content-types

    This code was taken from Raptus AG <dev at raptus com> in
    http://pypi.python.org/pypi/Products.ContentTypeValidator/2.0b3
    Only was implement the use of plone.app.registry to indicate which content types
    are allowed using a control panel
    """
    if USE_BBB_VALIDATORS: 
        __implements__ = (IValidator,)
    else:
        implements(IValidator)
    name = 'ContentTypeValidator'

    def __init__(self):
        pass
             
        
    def __call__(self, value, *args, **kw):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ITranscodeSetings)
        valid_content_types = settings.audio_valid_content_types
        content_type=""
        #import pdb; pdb.set_trace()
        content_types=tuple(valid_content_types.split())
        error = translate(_('contenttype_error', 
                            default=u"File has to be of one of the following content-types '${types}'.", 
                            mapping={'types': ', '.join(content_types)}), context=kw['instance'].REQUEST)
        if value and not value == 'DELETE_FILE':
            try:
                if kw['REQUEST'].form.get('%s_delete' % kw['field'].getName(), None) == 'delete':
                    return 1
                if kw['REQUEST'].form.get('%s_delete' % kw['field'].getName(), None) == 'nochange':
                    type = kw['field'].getContentType(kw['instance'])
                else:
                    mimetypes = getToolByName(kw['instance'], 'mimetypes_registry')
                    type = mimetypes.lookupExtension(value.filename.lower())
                    if type is None:
                        type = mimetypes.globFilename(value.filename)
                    try:
                        type = type.mimetypes[0]
                    except: # wasn't able to parse mimetype
                        type = None
                if not type in content_types:
                    return error
            except:
                return error
        return 1


class TranscodeAudioValidator:
    """
    Validates if a user could upload a file if the transcode is not started
    """
    __implements__=IValidator
    
    def __init__(self, name='', title='', description=''):
        self.name=name
        self.title=title
        self.decription=description
    
    def __call__(self, value, *args, **kw):
        
        instance = kw.get('instance', None)
        field    = kw.get('field', None)
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ITranscodeSetings)
        transcode_status = settings.transcode_switch
        valid_types=('audio/ogg', 'audio/x-theora+ogg', 'application/ogg')
        error = translate(_('contenttype_error_transcode_service', 
                            default=_(u"We sorry but in this moment, the transcode is out of service. To load your file must to be one of the following content-types '${types}'."), 
                            mapping={'types': ', '.join(valid_types)}), context=kw['instance'].REQUEST)

        if value and not value == 'DELETE_FILE':
            try:
                if kw['REQUEST'].form.get('%s_delete' % kw['field'].getName(), None) == 'delete':
                    return 1
                if kw['REQUEST'].form.get('%s_delete' % kw['field'].getName(), None) == 'nochange':
                    type = kw['field'].getContentType(kw['instance'])
                else:
                    my_mime_types = getToolByName(kw['instance'], 'mimetypes_registry')
                    type = my_mime_types.lookupExtension(value.filename.lower())
                    #pdb.set_trace()
                    if type is None:
                        type = my_mime_types.globFilename(value.filename)
                    try:
                        file_type = type.my_mime_types[0]
                    except: # wasn't able to parse mimetype
                        try:
                            file_type=str(type)
                        except:
                            file_type = None
                        if file_type in valid_types:
                            return 1
                        elif ((file_type not in valid_types) or (file_type in valid_types)) and (transcode_status == True):
                            return 1
                        elif file_type not in valid_types and transcode_status == False:
                            return error
            except:
                return error
        return 1
            
ValidatorsList.append(TranscodeAudioValidator('MyTranscodeValidator', title='', description=''))

for validator in ValidatorsList:
    validation.register(validator)
