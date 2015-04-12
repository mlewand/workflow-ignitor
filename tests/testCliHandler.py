
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
		mock._createParser.assert_called_once_with()
	
	def testParse( self ):
		mock = Mock()
		controllerMock = Mock()
		parsedArgs = Mock()
		mock._actionMapping = { 'foo': controllerMock }
		mock.parser.parse_args = Mock( return_value = parsedArgs )
		args = [ 'app.py', 'foo', 'bar' ]
		ret = CliHandler.parse( mock, args )
		mock.parser.parse_args.assert_called_once_with( [ 'foo', 'bar' ] )
		self.assertEqual( ( controllerMock, parsedArgs ), ret, 'Invalid return value' )
	
	def testParseToLittleArgs( self ):
		'''
		To few arguments given.
		'''
		mock = Mock()
		parser = mock.parser
		ret = CliHandler.parse( mock, [ 'app.py' ] )
		self.assertFalse( ret, 'Invalid return value' )
		parser.print_help.assert_called_once_with()
		self.assertEqual( 0, parser.parse_args.call_count, 'Invalid parser.parse_args call count' )
	
	def testParseUnknownController( self ):
		'''
		Unknown controller "bom". The only registered controller (action) is "foo".
		'''
		mock = Mock()
		parser = mock.parser
		mock._actionMapping = { 'foo': 'bar' }
		ret = CliHandler.parse( mock, [ 'app.py', 'bom' ] )
		self.assertFalse( ret, 'Invalid return value' )
		parser.print_help.assert_called_once_with()
		self.assertEqual( 0, parser.parse_args.call_count, 'Invalid parser.parse_args call count' )
	
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

