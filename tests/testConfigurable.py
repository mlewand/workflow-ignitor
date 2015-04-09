
from tests.BaseTestCase import BaseTestCase
from workflow_ignitor.Configurable import Configurable

class ConfigurableSubClass( Configurable ):
	pass

class Configurable( BaseTestCase ):
	
	def setUp( self ):
		self.mock = ConfigurableSubClass()
	
	def testConstructor( self ):
		instance = ConfigurableSubClass()
		self.assertIsInstance( instance._properties, dict )
		
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
