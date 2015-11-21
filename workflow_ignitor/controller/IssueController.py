
import sys
import webbrowser

from workflow_ignitor.controller.Controller import Controller
from workflow_ignitor.issue.parser.TextParser import TextParser, MissingContentError
from workflow_ignitor.issue.IssueIntegration import IssueIntegration
from workflow_ignitor.issue.Issue import Issue

class IssueController( Controller ):
	
	'''
	Value that this controller is going to be invoked with from CLI, e.g. for "issues" it's going to be reachable with: "app.py issues".
	
	This string is mandatory.
	'''
	cliAction = 'issues'
	
	cliSubActions = [ 'create', 'close' ]
	
	_TextParser = TextParser
	
	'''
	A mapping for builtin method, so we can mock it in tests.
	'''
	_readCliLine = input
	
	def actionCreate( self, args ):
		'''
		Creates an issue.
		
		By default issue source is taken from stdin, but you can provide also a file source for it.
		'''
		
		issueText = ''
		errorPrefix = ''
		lang = self.owner.lang[ 'app' ][ 'issues' ]
		
		if args.stdin == True:
			stdInput = sys.stdin.readlines()
			issueText = ''.join( stdInput )
			errorPrefix = 'Empty buffer given to stdin'
		elif args.file and isinstance( args.file, str ):
			with open( args.file, 'r' ) as hFile:
				issueText = ''.join( hFile.readlines() )
			errorPrefix = 'The file is empty'
		else:
			title = self._readCliLine( lang[ 'create' ][ 'title' ] )
			descr = self._readCliLine( lang[ 'create' ][ 'descr' ] )
			issueText = '{0}\n\n{1}'.format( title, descr )
		
		issueText = issueText.strip()
		
		if not issueText:
			raise RuntimeError( '{0}. You\'re supposed to provide issue content with stdin.'.format( errorPrefix ) )
		
		# Reports the issue.
		self.reportIssueFromText( issueText )
	
	def actionClose( self, args ):
		'''
		Closes the issue.
		'''
		issueId = args.id
		
		if issueId == None:
			raise RuntimeError( 'No issue id provided.' )
		
		project = self.owner.getProject()
		issue = self._getIssueById( issueId, project )
		integrations = self.owner.getIntegrations( IssueIntegration )
		list( map( lambda x: x.closeIssue( issue, project ), integrations ) )
	
	def reportIssueFromText( self, issueText ):
		'''
		Reports issue based on plain text provided as `issueText`.
		'''
		
		try:
			parser = self._TextParser()
			issue = parser.parse( issueText )
			self._reportIssue( issue, self.owner.getProject() )
		except MissingContentError as err:
			raise ValueError( str( err ) )
	
	def _getIssueById( self, issueId, project ):
		return Issue( '', id = issueId )
	
	def _registerCommands( self, argParser ):
		
		if not isinstance( self.owner.lang, dict ):
			return 
		
		cliLang = self.owner.lang[ 'app' ][ 'issues' ][ 'cli' ]
		
		argParser.add_argument( 'subAction', help = cliLang[ 'issuesSubAction' ], choices = self.cliSubActions )
		# Mutaly exclusive group, meaning that only one of the params can be set at a time.
		inputSwitchGroup = argParser.add_mutually_exclusive_group()
		inputSwitchGroup.add_argument( '--file', help = cliLang[ 'file' ], metavar = 'srcFile' )
		inputSwitchGroup.add_argument( '--stdin', help = cliLang[ 'stdin' ], action = 'store_true' )
		inputSwitchGroup.add_argument( '--id', help = cliLang[ 'id' ], type = int )
	
	def _reportIssue( self, issue, project ):
		'''
		Reports issue to a given project.
		'''
		integrations = self.owner.getIntegrations( IssueIntegration )
		openBrowserAfterCreation = self.owner.getConfig( 'app.issues.openAfterCreated' ) == True
		
		for integr in integrations:
			integr.createIssue( issue, project )
			
			if openBrowserAfterCreation and issue.id and integr.getIssueUrl( issue, project ):
				self._openBrowser( integr.getIssueUrl( issue, project ) )
	
	def _openBrowser( self, url ):
		webbrowser.open_new_tab( url )
