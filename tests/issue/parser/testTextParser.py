
import os
from unittest.mock import Mock

from tests.BaseTestCase import BaseTestCase
from workflow_ignitor.issue.parser.TextParser import TextParser, MissingContentError

def loadFixture( filePath ):
	with open( filePath, 'r' ) as hFile:
		return ''.join( hFile.readlines() )

class testTextParser( BaseTestCase ):
	
	fixtures = {}
	
	@classmethod
	def setUpClass( cls ):
		'''
		Loads fixture content from files and put it into `testTextParser.fixtures` dictionary.
		
		So file contents are stored as string, e.g. `testTextParser.fixtures[ 'standard' ]`.
		'''
		
		def importFixture( tcClass, fixtureName ):
			tcClass.fixtures[ fixtureName ] = loadFixture( os.sep.join( ( os.path.split( __file__ )[0], '_fixtures', fixtureName + '.txt' ) ) )
			
		importFixture( cls, 'simplest' )
		importFixture( cls, 'standard' )
		importFixture( cls, 'missingDescription' )
	
	def setUp( self ):
		self.mock = TextParser()
	
	def testParseSimplest( self ):
		expectedIssue = Mock()
		# Use a mock as an Issue class, so later on we can check what arguments it was called with.
		self.mock._IssueClass = Mock( return_value = expectedIssue )
		
		src = self.fixtures[ 'simplest' ]
		ret = self.mock.parse( src )
		
		self.assertEqual( expectedIssue, ret, 'Invalid return value' )
		self.mock._IssueClass.assert_called_once_with( 'Issue title', 'This is issue description.' )

	def testParseStandard( self ):
		expectedIssue = Mock()
		# Use a mock as an Issue class, so later on we can check what arguments it was called with.
		self.mock._IssueClass = Mock( return_value = expectedIssue )
		
		self.mock.parse( self.fixtures[ 'standard' ] )
		
		self.mock._IssueClass.assert_called_once_with( 'This is an issue', 'This is issue description.\n\nBelive it or not - often times it will be multiline!' )

	def testParseTitleOnly( self ):
		'''
		Ensure that nothing wrong happens if no descr is provided.
		'''
		expectedIssue = Mock()
		# Use a mock as an Issue class, so later on we can check what arguments it was called with.
		self.mock._IssueClass = Mock( return_value = expectedIssue )
		
		self.mock.parse( self.fixtures[ 'missingDescription' ] )
		
		self.mock._IssueClass.assert_called_once_with( 'Title only!', '' )
	
	def testParseThrowsErrorOnEmpty( self ):
		'''
		Ensure that parse throws exception if empty or whitespice-only string is provided.
		'''
		
		self.assertRaises( MissingContentError, self.mock.parse, '' )
		self.assertRaises( MissingContentError, self.mock.parse, ' ' )
		self.assertRaises( MissingContentError, self.mock.parse, '\n\n\n' )
