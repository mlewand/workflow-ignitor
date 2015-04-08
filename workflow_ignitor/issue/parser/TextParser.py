
from workflow_ignitor.issue.Issue import Issue

class TextParser:
	
	_IssueClass = Issue
	
	'''
	A helper class that will take care of converting plain text into an issue object.
	'''
	
	def parse( self, sourceText ):
		'''
		Parses given text and returns an Issue object.
		
		Note that parsed content will have Unix-style line endings despite platform.
		'''
		lines = sourceText.splitlines()
		
		title, descr = lines[ 0 ], '\n'.join( lines[ 2 : ] )
		
		return self._IssueClass( title, descr )
	