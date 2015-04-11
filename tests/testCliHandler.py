
from unittest.mock import Mock, patch
from tests.BaseTestCase import BaseTestCase
from workflow_ignitor.CliHandler import CliHandler

class CliHandlerMock( CliHandler ):
	_createParser = Mock()

class testCliHandler( BaseTestCase ):
	
	def setUp( self ):
		self.app = Mock()
	
	def testConstructor( self ):
		mock = CliHandlerMock( self.app )
		self.assertIsInstance( mock._actionMapping, dict )
		self.assertDictEqual( mock._actionMapping, {} )
		self.assertEqual( self.app, mock.owner, 'Invalid owner property' )
		self.assertEqual( mock._createParser(), mock.parser, 'Invalid praser' )
		
	
	def testRegisterController( self ):
		controller = Mock()
		controller.cliAction = 'foo'
		mock = Mock()
		mock._actionMapping = {}
		
		CliHandler.registerController( mock, controller )
		
		self.assertIn( 'foo', mock._actionMapping.keys(), 'Missing _actionMapping key' )
		self.assertEqual( mock._actionMapping[ 'foo' ], controller, 'Invalid _actionMapping.foo value' )
	
	def testRegisterControllerInvalid( self ):
		'''
		Ensure that exception is thrown if the controller has empty cliAction string.
		'''
		
		controller = Mock()
		controller.cliAction = ''
		mock = Mock()
		mock._actionMapping = {}
		
		self.assertRaisesRegex( ValueError, '^Registered controller must have non-empty cliAction$', CliHandler.registerController, mock, controller )
	
	def testCreateParser( self ):
		lang = {
			"app": {
				"name": "foo",
				"descr": "bar"
			}
		}
		mock = Mock()
		mock.owner.lang = lang
		parser = Mock()
		with patch( 'argparse.ArgumentParser', return_value = parser ) as argParserMock:
			CliHandler._createParser( mock )
			
			argParserMock.assert_called_once_with( prog = 'foo', description = 'bar' )
			self.assertEqual( parser, mock.parser, 'Invalid mock.parser value' )

