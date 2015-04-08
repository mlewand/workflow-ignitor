
from workflow_ignitor.controller.Controller import Controller
from workflow_ignitor.issue.parser.TextParser import TextParser, MissingContentError

class IssueController( Controller ):
	
	_TextParser = TextParser
	
	def reportIssueFromText( self, issueText ):
		'''
		Reports issue based on plain text provided as `issueText`.
		'''
		
		try:
			parser = self._TextParser()
			issue = parser.parse( issueText )
			self._reportIssue( issue, None )
		except MissingContentError as err:
			raise ValueError( str( err ) )
	
	def _reportIssue( self, issue, project ):
		'''
		Reports issue to a given project.
		'''
		
		pass
	
