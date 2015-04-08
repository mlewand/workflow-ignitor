
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
		self.assertEqual( properties, instance._properties, 'Invalid properties dict' )
	
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
		
	
	def testSetProperty( self ):
		self.mock.setProperty( 'foo', 'bar' )
		props = self.mock._properties
		
		self.assertTrue( 'foo' in props.keys(), 'foo is not in _properties dictionary' )
		self.assertEqual( 'bar', props[ 'foo' ], 'Invalid _properties.foo' )

	def testSetPropertyNested( self ):
		
		self.mock.setProperty( 'foo.bar.baz', 'boom' )
		props = self.mock._properties
		
		self.assertIn( 'bar', props[ 'foo' ].keys(), 'foo is not in _properties.foo dictionary' )
		self.assertIn( 'baz', props[ 'foo' ][ 'bar' ].keys(), 'baz is not in _properties.foo.bar dictionary' )
		self.assertEqual( 'boom', props[ 'foo' ][ 'bar' ][ 'baz' ], 'Invalid _properties.foo.bar.baz' )
		
	def testGetPropertyNested( self ):
		
		self.mock._properties = {
			'abc': {
				'def': {
					'ghi': 'foobar'
				}
			}
		}
		self.assertEqual( 'foobar', self.mock.getProperty( 'abc.def.ghi' ), 'Invalid return value' )
		
	def testGetPropertyInvalid( self ):
		
		self.mock._properties = {}
		self.assertEqual( None, self.mock.getProperty( 'abc.def.ghi' ), 'Invalid return value' )
		
		
		
	
	
