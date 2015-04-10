
from unittest.mock import Mock
from tests.BaseTestCase import BaseTestCase
from workflow_ignitor.CliHandler import CliHandler

class testCliHandler( BaseTestCase ):
	
	def setUp( self ):
		self.app = Mock()
	
	def testConstructor( self ):
		mock = CliHandler( self.app )
		self.assertIsInstance( mock._actionMapping, dict )
		self.assertDictEqual( mock._actionMapping, {} )
	
	def testRegisterController( self ):
		controller = Mock()
		controller.cliAction = 'foo'
		mock = Mock()
		mock._actionMapping = {}
		
		CliHandler.registerController( mock, controller )
		
		self.assertIn( 'foo', mock._actionMapping.keys(), 'Missing _actionMapping key' )
		self.assertEqual( mock._actionMapping[ 'foo' ], controller, 'Invalid _actionMapping.foo value' )
