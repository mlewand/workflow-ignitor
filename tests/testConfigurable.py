
from tests.BaseTestCase import BaseTestCase
from workflow_ignitor.Configurable import Configurable

class ConfigurableSubClass( Configurable ):
	pass

class Configurable( BaseTestCase ):
	
	def setUp( self ):
		self.mock = ConfigurableSubClass()
	
	def testConstructor( self ):
		instance = ConfigurableSubClass()
		self.assertIsInstance( instance._config, dict )
		
	def testSetConfig( self ):
		self.mock.setConfig( 'foo', 'bar' )
		props = self.mock._config
		
		self.assertTrue( 'foo' in props.keys(), 'foo is not in _config dictionary' )
		self.assertEqual( 'bar', props[ 'foo' ], 'Invalid _config.foo' )

	def testSetConfigNested( self ):
		
		self.mock.setConfig( 'foo.bar.baz', 'boom' )
		props = self.mock._config
		
		self.assertIn( 'bar', props[ 'foo' ].keys(), 'foo is not in _config.foo dictionary' )
		self.assertIn( 'baz', props[ 'foo' ][ 'bar' ].keys(), 'baz is not in _config.foo.bar dictionary' )
		self.assertEqual( 'boom', props[ 'foo' ][ 'bar' ][ 'baz' ], 'Invalid _config.foo.bar.baz' )
		
	def testGetConfigNested( self ):
		
		self.mock._config = {
			'abc': {
				'def': {
					'ghi': 'foobar'
				}
			}
		}
		self.assertEqual( 'foobar', self.mock.getConfig( 'abc.def.ghi' ), 'Invalid return value' )
		
	def testGetConfigInvalid( self ):
		
		self.mock._config = {}
		self.assertEqual( None, self.mock.getConfig( 'abc.def.ghi' ), 'Invalid return value' )
