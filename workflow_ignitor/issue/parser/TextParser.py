
from workflow_ignitor.issue.Issue import Issue

class MissingContentError( Exception ):
	'''
	Error thrown when content to be parsed has no content.
	'''
	
	def __init__( self ):
		super().__init__( 'Invalid content. Issue text should follow proper text schema.' )

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
		strippedSource = sourceText.strip()
		
		lines = sourceText.splitlines()
		
		if len( strippedSource ) == 0:
			raise MissingContentError()
		
		title, descr = lines[ 0 ], '\n'.join( lines[ 2 : ] )
		
		return self._IssueClass( title, descr )
	