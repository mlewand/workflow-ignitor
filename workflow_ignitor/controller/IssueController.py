
from workflow_ignitor.controller.Controller import Controller
from workflow_ignitor.issue.parser.TextParser import TextParser, MissingContentError
from workflow_ignitor.issue.IssueIntegration import IssueIntegration

class IssueController( Controller ):
	
	_TextParser = TextParser
	
	def process( self, args ):
		'''
		Looks for args, and based on that executes proper logic.
		'''
		
		pass
	
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
	
	def _reportIssue( self, issue, project ):
		'''
		Reports issue to a given project.
		'''
		integrations = self.owner.getIntegrations( IssueIntegration )
		
		list( map( lambda x: x.createIssue( issue, project ), integrations ) )
	
