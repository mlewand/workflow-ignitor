
from unittest.mock import Mock

from tests.BaseTestCase import BaseTestCase
from workflow_ignitor.controller.IssueController import IssueController

class testIssueController( BaseTestCase ):
	
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
