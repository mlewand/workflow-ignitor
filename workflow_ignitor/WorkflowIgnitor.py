
import os
import json

from workflow_ignitor.controller.IssueController import IssueController
from workflow_ignitor.Integration import Integration
from workflow_ignitor.Project import Project
from workflow_ignitor.Configurable import Configurable
from workflow_ignitor.CliHandler import CliHandler

class WorkflowIgnitor( Configurable ):
	
	'''
	Id of the current project.
	'''
	curProject = ''
	
	def __init__( self ):
		cfg = self._loadConfig()
		super().__init__( cfg )
		
		'''
		List of Integration derived instances.
		'''
		self._integrations = list()
		
		self._loadLang( cfg[ 'lang' ] if 'lang' in cfg.keys() else 'en' )
		self._registerCommandParser()
		self._loadControllers()
		
	def start( self, args ):
		self.curProject = self.getConfig( 'tmp.currentProject' )
		
		ret = self.cli.parse( args )
		
		if not ret:
			# If invalid CLI parameters were given, leave the app.
			# "Unix programs generally use 2 for command line syntax errors and 1 for all other kind of errors."
			# https://docs.python.org/2/library/sys.html#sys.exit
			exit( 2 )
		else:
			self._loadCliSettings( ret[ 1 ] )
			
			ret[ 0 ].process( ret[ 1 ] )
	
	def registerIntegration( self, IntegrationType ):
		
		if not issubclass( IntegrationType, Integration ):
			raise TypeError( 'Invalid IntegrationType, expected type to be Integration subclass.' )
		
		integration = IntegrationType( self )
		self._integrations.append( integration )
		integration.attach()
	
	def getIntegrations( self, baseType = None ):
		'''
		Returns registered integrations that implements given baseType.
		
		If baseType is None, it will return all the integrations.
		'''
		return tuple( filter( lambda x: baseType == None or isinstance( x, baseType ), self._integrations )  )
	
	def getProject( self ):
		'''
		Returns current project.
		'''
		curProj = self.curProject
		
		if not curProj:
			raise RuntimeError( 'Missing config: tmp.currentProject' )
		
		projConfig = self.getConfig( 'projects.' + curProj )
		
		return Project( curProj, projConfig[ 'path' ], config = projConfig )

	def _loadControllers( self ):
		self.issues = IssueController( self )
		self.issues.attach()
		self.cli.registerController( self.issues )

	def _loadConfig( self ):
		'''
		Loads local config from a JSON.
		'''
		
		jsonPath = os.sep.join( ( os.path.realpath( os.path.split( __file__ )[ 0 ] ), '..', 'config.json' ) )
		jsonContent = self._getFileContent( jsonPath )
		
		return json.loads( jsonContent )
	
	def _loadLang( self, langCode ):
		'''
		Loads language file with given code.
		'''
		
		fileName = langCode + '.json'
		jsonPath = os.sep.join( ( os.path.realpath( os.path.split( __file__ )[ 0 ] ), '..', 'lang', fileName ) )
		
		try:
			jsonContent = self._getFileContent( jsonPath )
			self.lang = json.loads( jsonContent )
		except FileNotFoundError as err:
			raise RuntimeError( 'Language file "{0}" not found. Check /lang file for available langs.'.format( fileName ) )
		
		return True

	def _loadCliSettings( self, args ):
		'''
		Checks CLI args for some global settings switches.
		'''
		
		if args.project:
			self.curProject = args.project
	
	def _getFileContent( self, filePath ):
		with open( filePath, 'r') as hFile:
			return hFile.read()
	
	def _registerCommandParser( self ):
		self.cli = CliHandler( self )
	
