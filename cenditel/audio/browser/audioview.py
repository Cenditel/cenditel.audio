from zope.interface import implements, Interface
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
###################
#python imports
import urlparse
import os
#############
from Acquisition import aq_inner
from zope.component import getMultiAdapter
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
#utility control panel imports
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from Acquisition import interfaces
#Products Imports
from cenditel.audio import audioMessageFactory as _
from cenditel.transcodedeamon.convert import MFN as MFNI
from cenditel.transcodedeamon.convert import newtrans_init_
from cenditel.transcodedeamon.convert import MTD as MTDI
from cenditel.transcodedeamon.convert import ServiceList
##########################################
#Options Imports
from cenditel.transcodedeamon.interfaces import ITranscodeSetings


class IaudioView(Interface):
    """
    audio view interface
    """

    def test():
        """ test method"""


class audioView(BrowserView):
    """
    audio browser view
    """
    implements(IaudioView)


    def __init__(self, context, request):
        self.context = context
        self.request = request
	self.MyTitle = ""
	self.MyTitleWhitOutSpace = ""
	self.filename = ""
	self.newfilename = ""
	self.filenamesaved= ""
	self.folderfile = ""
	self.StatusOfFile = ""
	self.filesize = ""
	self.SERVER = ""
	self.folderfileOGG=""
	self.PathOfFile=""
	self.STORAGE=""
	self.AbsoluteServerPath=""
	self.newfiletranscoded=""
	self.Error=False

    def RemoveSlash(self, path):
	reverse=path[::-1]
	newpath=""
	if reverse[0]=='/':
	    for x in path[:-1]:
		newpath=newpath+x
	    return newpath
	else:
	    return path

    def PlayingAudioType(self):
	#import pdb; pdb.set_trace()
	registry = getUtility(IRegistry)
	settings = registry.forInterface(ITranscodeSetings)
	self.SERVER = self.RemoveSlash(settings.adress_of_streaming_server)
	PARAMETRES_TRANSCODE = settings.ffmpeg_parameters_audio_line
	self.STORAGE = self.RemoveSlash(settings.mount_point_fss)
	self.MyTitle = self.context.Title()
        idaudio=self.context.getId()
	"""
	virtualobject=self.context.getAudio()
	self.filenamesaved=virtualobject.filename
	"""
	self.MyTitleWhitOutSpace = MFNI.TitleDeleteSpace(self.MyTitle) 
	self.filename = MFNI.DeleteSpaceinNameOfFolderFile(self.MyTitleWhitOutSpace)  
	url = self.context.absolute_url()
	self.PathOfFile = MFNI.ReturnPathOfFile(url)
	self.filenamesaved = MFNI.ReturnFileNameOfFileSaved(self.STORAGE, self.PathOfFile)
	if self.filenamesaved.haskey('ErrorBol')
	if self.filenamesaved['ErrorBol']
	print "IT IS THE NAME OF THE FILE SAVED " + self.filenamesaved
        #import pdb; pdb.set_trace()
	self.MyTitleWhitOutSpace = MFNI.DeleteSpaceinNameOfFolderFile(self.MyTitleWhitOutSpace)
	newtrans_init_(self.STORAGE, self.PathOfFile, self.filenamesaved, PARAMETRES_TRANSCODE, idaudio)
	self.folderfileOGG=MTDI.newname(self.PathOfFile+'/' + self.filenamesaved)
	self.AbsoluteServerPath = self.SERVER + MTDI.nginxpath(self.folderfileOGG)
	self.newfiletranscoded=MTDI.nginxpath(self.STORAGE+self.folderfileOGG)
	self.StatusOfFile = ServiceList.available(idaudio,self.newfiletranscoded)
	print "El STATUS OF FILE IN THE VIEW "+ str(self.StatusOfFile)
        if self.StatusOfFile == True:
	    self.newfilename=MTDI.newname(self.filenamesaved)
	else:
	    self.newfilename=_('The file is not ready yet, please contact site administration')
	return 


    def ErrorSituation(self):
	import pdb; pdb.set_trace()
	if self.Error==False:
	    return False
	else:
	    return True


    def GETFileSize(self):
        try:
	    self.filesize = MFNI.ReturnFileSizeOfFileInHardDrive(self.newfiletranscoded)
	    thefilesize = self.filesize
	    return thefilesize
	except OSError:
	    self.Error=True
	    self.ErrorSituation()
	    return "0 kb"

    def GETAdressOfAudioFromApache(self):
	
	TheFilePath = self.AbsoluteServerPath
	return TheFilePath

    def GETStatusOfFile(self):
	
	TheStatus = self.StatusOfFile
	str(TheStatus)
	return TheStatus
	

    def GETNewNameAudio(self):
	TheNewName = self.newfilename
	return TheNewName

    def GETfolderfile(self):
	
	TheFolderFile = self.AbsoluteServerPath 
	return TheFolderFile 

    
    def GETMyTitle(self):
	
	MyTitleWhitOutSpace  = self.MyTitleWhitOutSpace
	return MyTitleWhitOutSpace

    def ExternalMethodforURL(self):
	return self.context.absolute_url()


    def URLElement(self):
	url = self.context.absolute_url()
	self.PathOfFile = MFNI.ReturnPathOfFile(url)
	return self.PathOfFile

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

