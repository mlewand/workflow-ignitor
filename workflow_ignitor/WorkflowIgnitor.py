
import os
import json
import argparse

from workflow_ignitor.controller.IssueController import IssueController
from workflow_ignitor.Integration import Integration
from workflow_ignitor.Project import Project
from workflow_ignitor.Configurable import Configurable

class WorkflowIgnitor( Configurable ):
	
	def __init__( self ):
		self.issues = IssueController( self )
		'''
		List of Integration derived instances.
		'''
		self._integrations = list()
		
		cfg = self._loadConfig()
		super().__init__( cfg )
		
	def start( self, args ):
		pass
	
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
		# @TODO: fix me.
		# Hardcoded for testing purposes. It should automatically detect current project.
		curProj = self.getConfig( 'tmp.currentProject' )
		
		if not curProj:
			raise RuntimeError( 'Missing config: tmp.currentProject' )
		
		projConfig = self.getConfig( 'projects.' + curProj )
		
		return Project( curProj, projConfig[ 'path' ], config = projConfig )

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
		jsonPath = os.sep.join( ( os.path.realpath( os.path.split( __file__ )[ 0 ] ), '..', fileName ) )
		
		try:
			jsonContent = self._getFileContent( jsonPath )
			self.lang = json.loads( jsonContent )
		except FileNotFoundError as err:
			raise RuntimeError( 'Language file "{0}" not found. Check /lang file for available langs.'.format( fileName ) )
		
		return True
	
	def _getFileContent( self, filePath ):
		with open( filePath, 'r') as hFile:
			return hFile.read()
	
	def _registerCommandParser( self ):
		self.parser = argparse.ArgumentParser( prog = 'Workflow Ignitor' )
	
	
