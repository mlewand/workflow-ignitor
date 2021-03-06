
from unittest.mock import Mock, patch, call
from io import StringIO
import sys, os

from tests.BaseTestCase import BaseTestCase
from workflow_ignitor.controller.IssueController import IssueController

class testIssueController( BaseTestCase ):
	
	issuesLangDict = {
		"app": {
			"issues": {
				"cli": {
					"issuesAction": "Issues manipulation.",
					"issuesSubAction": "Subcommand to be performed.",
					"file": "File to be used as an issue source.",
					"stdin": "If set will read issue source form stdin."
				},
				"create": {
					"title": "Issue title: ",
					"descr": "Issue desription: "
				}
			}
		}
	}
	
	def setUp( self ):
		self.owner = Mock()
		self.mock = IssueController( self.owner )
	
	def testReportIssueFromText( self ):
		srcText = 'foobar'
		issueMock = Mock()
		textParserMock = Mock()
		textParserMock.parse = Mock( return_value = issueMock )
		
		self.mock._TextParser = Mock( return_value = textParserMock )
		self.mock._reportIssue = Mock()
		self.mock.reportIssueFromText( srcText )
		
		textParserMock.parse.assert_called_once_with( srcText )
		self.mock._reportIssue.assert_called_once_with( issueMock, self.owner.getProject() )
	
	def testActionCreate( self ):
		mock = Mock()
		mock.owner.lang = self.issuesLangDict
		args = Mock()
		IssueController.actionCreate( mock, args )
		mock._readCliLine.assert_has_calls( [ call( 'Issue title: ' ), call( 'Issue desription: ' ) ] )
		
	@patch( '__main__.sys.stdin', StringIO( 'foo\n\nbar' ) )
	def testActionCreateStdin( self ):
		'''
		Ensure that stdin input is taken by default.
		'''
		mock = Mock()
		mock.owner.lang = self.issuesLangDict
		args = Mock()
		args.stdin = True
		IssueController.actionCreate( mock, args )
		
		mock.reportIssueFromText.assert_called_once_with( 'foo\n\nbar' )
	
	@patch( '__main__.sys.stdin', StringIO( '' ) )
	def testActionCreateStdinEmpty( self ):
		mock = Mock()
		mock.owner.lang = self.issuesLangDict
		args = Mock()
		args.stdin = True
		self.assertRaisesRegex( RuntimeError, '^Empty buffer given to stdin. You\'re supposed to provide issue content with stdin\.$', IssueController.actionCreate, mock, args )
	
	@patch( '__main__.sys.stdin', StringIO( ' \t\n\t ' ) )
	def testActionCreateStdinWhitespace( self ):
		mock = Mock()
		mock.owner.lang = self.issuesLangDict
		args = Mock()
		args.stdin = True
		self.assertRaisesRegex( RuntimeError, '^Empty buffer given to stdin. You\'re supposed to provide issue content with stdin\.$', IssueController.actionCreate, mock, args )

	@patch( '__main__.sys.stdin' )
	def testActionCreateFromFile( self, stdinMock ):
		'''
		If --file arg is present then we should use file instead stdin.
		
		Note: I wasn't able to successfuly mock __main__.open method. Though it's well docummented: https://docs.python.org/3.3/library/unittest.mock.html#mock-open
		
		This is why I'm going to use real fixture files.
		
		It seems not to work here: Win7 Python 3.4.0 x64
		
		example code:
		
		>>>	with patch('__main__.open', mock_open(read_data='bibble'), create=True) as m:
		>>>		with open('foo') as h:
		>>>			result = h.read()
		Traceback (most recent call last):
			File "X:\dev\workflow-ignitor\tests\controller\testIssueController.py", line 74, in testActionCreateFromFile
				with open('foo') as h:
		FileNotFoundError: [Errno 2] No such file or directory: 'foo'
		'''
		
		mock = Mock()
		mock.owner.lang = self.issuesLangDict
		args = Mock()
		testBaseDir = os.path.split( os.path.realpath( __file__ ) )[ 0 ]
		args.file = os.sep.join( ( testBaseDir, '_fixtures', 'issueSource.md' ) )
			
		IssueController.actionCreate( mock, args )
		
		self.assertEqual( 0, stdinMock.readlines.call_count, 'stdin.readlines call count' )
		mock.reportIssueFromText.assert_called_once_with( 'Sample title\n\nSample description.' )

	@patch( '__main__.sys.stdin' )
	def testActionCreateFromEmptyFile( self, stdinMock ):
		'''
		For explaination why I didn't mocked read() method, see testActionCreateFromFile.
		
		This test ensures that proper exception is generated, when rovided file is empty.
		'''
		
		mock = Mock()
		mock.owner.lang = self.issuesLangDict
		args = Mock()
		testBaseDir = os.path.split( os.path.realpath( __file__ ) )[ 0 ]
		args.file = os.sep.join( ( testBaseDir, '_fixtures', 'emptyFile.md' ) )
	
		self.assertRaisesRegex( RuntimeError, '^The file is empty. You\'re supposed to provide issue content with stdin\.$', IssueController.actionCreate, mock, args )
	
	def testReportIssueWebbrowserOpen( self ):
		'''
		Web browser should be opened if issue is created and a proper config is set.
		'''
		
		issue = Mock()
		project = Mock()
		integrations = [ Mock(), Mock() ]
		self.owner.getIntegrations = Mock( return_value = integrations )
		self.owner.getConfig = Mock( return_value = True )
		
		self.mock._openBrowser = Mock()
		self.mock._reportIssue( issue, project )
		
		self.assertEqual( 2, self.mock._openBrowser.call_count, 'Invalid _openBrowser call count' )
	
	def testActionClose( self ):
		mock = Mock()
		args = Mock()
		pass
	
	def testActionCloseNoIdInArgs( self ):
		mock = Mock()
		args = Mock()
		args.id = None
		self.assertRaisesRegex( RuntimeError, '^No issue id provided.$', IssueController.actionClose, mock, args )
	
