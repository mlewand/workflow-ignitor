
import sys

from workflow_ignitor.controller.Controller import Controller
from workflow_ignitor.issue.parser.TextParser import TextParser, MissingContentError
from workflow_ignitor.issue.IssueIntegration import IssueIntegration

class IssueController( Controller ):
	
	_TextParser = TextParser
	
	'''
	Value that this controller is going to be invoked with from CLI, e.g. for "issues" it's going to be reachable with: "app.py issues".
	
	This string is mandatory.
	'''
	cliAction = 'issues'
	
	def process( self, args ):
		'''
		Looks for args, and based on that executes proper logic.
		'''
		if args.subAction == 'create':
			self.actionCreate( args )
	
	def actionCreate( self, args ):
		'''
		Creates an issue.
		
		By default issue source is taken from stdin, but you can provide also a file source for it.
		'''
		
		issueText = ''
		errorPrefix = ''
		
		if not args.file:
			stdInput = sys.stdin.readlines()
			issueText = ''.join( stdInput )
			errorPrefix = 'Empty buffer given to stdin'
		else:
			with open( args.file, 'r' ) as hFile:
				issueText = ''.join( hFile.readlines() )
			errorPrefix = 'The file is empty'
		
		issueText = issueText.strip()
		
		if not issueText:
			raise RuntimeError( '{0}. You\'re supposed to provide issue content with stdin.'.format( errorPrefix ) )
		
		# Reports the issue.
		self.reportIssueFromText( issueText )
	
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
	
	def _registerCommands( self, argParser ):
		
		if not isinstance( self.owner.lang, dict ):
			return 
		
		cliLang = self.owner.lang[ 'app' ][ 'issues' ][ 'cli' ]
		
		argParser.add_argument( 'subAction', help = cliLang[ 'issuesSubAction' ], choices = [ 'create', 'close' ] )
		# Mutaly exclusive group, meaning that only one of the params can be set at a time.
		inputSwitchGroup = argParser.add_mutually_exclusive_group()
		inputSwitchGroup.add_argument( '--file', help = cliLang[ 'file' ], metavar = 'srcFile' )
		inputSwitchGroup.add_argument( '--stdin', help = cliLang[ 'stdin' ], action = 'store_true' )
	
	def _reportIssue( self, issue, project ):
		'''
		Reports issue to a given project.
		'''
		integrations = self.owner.getIntegrations( IssueIntegration )
		
		list( map( lambda x: x.createIssue( issue, project ), integrations ) )
	
