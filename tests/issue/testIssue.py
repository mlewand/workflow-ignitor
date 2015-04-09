
from tests.BaseTestCase import BaseTestCase
from workflow_ignitor.issue.Issue import Issue

class testIssue( BaseTestCase ):
	
	def testConstructorPositional( self ):
		'''
		Tests constructor using only positional arguments.
		'''
		instance = Issue( 'foo', 'bar' )
		
		self.assertEqual( 'foo', instance.title, 'Invalid title' )
		self.assertEqual( 'bar', instance.descr, 'Invalid description' )
	
	def testConstructorKeywords( self ):
		'''
		Tests constructor using keyword arguments.
		'''
		instance = Issue( 'foo', descr = 'bar' )
		
		self.assertEqual( 'foo', instance.title, 'Invalid title' )
		self.assertEqual( 'bar', instance.descr, 'Invalid description' )
	
