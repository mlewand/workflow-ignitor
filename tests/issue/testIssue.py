
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
		
	def testExists( self ):
		'''
		Tests constructor using keyword arguments.
		'''
		instance = Issue( 'foo', id = 11000 )
		self.assertTrue( instance.exists(), 'Invalid ret value' )
		
	def testExistsInvalid( self ):
		'''
		Tests constructor using keyword arguments.
		'''
		instance = Issue( 'foo' )
		self.assertFalse( instance.exists(), 'Invalid ret value' )
