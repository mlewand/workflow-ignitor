
import os.path

from unittest.mock import Mock, patch
from tests.BaseTestCase import BaseTestCase
from workflow_ignitor.Project import Project

class _ProjectMock( Project ):
	def setPath( self, path ):
		'''
		Simplified setPath, without real path checking.
		'''
		self.path = path

class testProject( BaseTestCase ):
	
	def setUp( self ):
		self.mock = _ProjectMock( '', '' )
	
	def testConstructor( self ):
		class __ProjectSubclass( Project ):
			setPath = Mock()
		
		properties = {
			'a': 123,
			'b': 'c'
		}
		
		instance = __ProjectSubclass( 'a', 'b', properties )
		self.assertEqual( 'a', instance.id, 'Invalid project id' )
		instance.setPath.calledOnceWith( 'b' )
	
	def testSetPath( self ):
		class __ProjMockup:
			path = None
		
		# First patch os.path.isdir.
		with patch( 'os.path.isdir', return_value = True ) as mockedIsDir:
			mock = __ProjMockup()
			Project.setPath( mock, 'foo' )
			self.assertEqual( 'foo', mock.path, 'Invalid mock.path' )
	
	def testSetPathInvalid( self ):
		# First patch os.path.isdir.
		with patch( 'os.path.isdir', return_value = False ) as mockedIsDir:
			mock = object()
			self.assertRaisesRegex( IOError, '^Project directory "foo" not found\.$', Project.setPath, mock, 'foo' )
	
	
