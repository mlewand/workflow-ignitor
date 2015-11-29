
import sys
import os
import webbrowser

from github import Github
from github.InputFileContent import InputFileContent

from workflow_ignitor.controller.Controller import Controller

class GistController( Controller ):
	
	'''
	Value that this controller is going to be invoked with from CLI, e.g. for "issues" it's going to be reachable with: "app.py issues".
	
	This string is mandatory.
	'''
	cliAction = 'gists'
	
	cliSubActions = [ 'create' ]
	
	github = None
	
	readline = input
	
	def actionCreate( self, args ):
		'''
		Creates the gist.
		
		By default the content is taken from stdin, but you can provide also a file path.
		'''
		
		# Note: it looks like dict keys are does not matter.
		contentDict = {}
		isPublic = args.public == True
		
		if args.stdin == True:
			stdInput = sys.stdin.readlines()
			contentString = ''.join( stdInput[ 1 : ] )
			fileName = stdInput[ 0 ].strip()
			
			contentDict[ '0' ] = InputFileContent( contentString, fileName )
		elif args.files and len( args.files ):
			for offset, file in enumerate( args.files ):
				with open( file, 'r' ) as hFile:
					contentString = ''.join( hFile.readlines() )
					
				fileName = os.path.split( file )[ -1 ]
				contentDict[ str( offset ) ] = InputFileContent( contentString, fileName )
		else:
			fileName = self.readline( 'File name:' )
			contentString = self.readline( 'Content:' )
			
			contentDict[ '0' ] = InputFileContent( contentString, fileName )
		
		gist = self._getGithubUser().create_gist( isPublic, contentDict )
		
		# @todo: add a possibilty to open Gist in a browser or copy it's link to the clipboard.
	
	def _getGithubUser( self ):
		if not self.github:
			self.github = Github( self.owner.getConfig( 'github.token' ) )
		
		return self.github.get_user()
	
	def _registerCommands( self, argParser ):
		
		if not isinstance( self.owner.lang, dict ):
			return 
		
		cliLang = self.owner.lang[ 'app' ][ 'gists' ][ 'cli' ]
		
		argParser.add_argument( 'subAction', help = cliLang[ 'gistsSubAction' ], choices = self.cliSubActions )
		# Mutaly exclusive group, meaning that only one of the params can be set at a time.
		inputSwitchGroup = argParser.add_mutually_exclusive_group()
		inputSwitchGroup.add_argument( '--files', help = cliLang[ 'files' ], metavar = 'srcFile', nargs = '*' )
		inputSwitchGroup.add_argument( '--stdin', help = cliLang[ 'stdin' ], action = 'store_true' )
		argParser.add_argument( '--public', help = cliLang[ 'public' ], action = 'store_true' )
	
	def _openBrowser( self, url ):
		webbrowser.open_new_tab( url )
