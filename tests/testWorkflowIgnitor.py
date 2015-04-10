
import os
from unittest.mock import Mock, patch
from tests.BaseTestCase import BaseTestCase
from workflow_ignitor.WorkflowIgnitor import WorkflowIgnitor
from workflow_ignitor.controller.IssueController import IssueController
from workflow_ignitor.Integration import Integration

class WorkflowIgnitorMock( WorkflowIgnitor ):
	'''
	Mocked WorkflowIgnitor class, that will work on fixtures rather than real IO resources.
	'''
	def __init__( self, *args, **kwargs ):
		# Mocking essential methods.
		self._loadConfig = Mock( return_value = self._getMockConfig() )
		self._loadLang = Mock()
		self._registerCommandParser = Mock()
		self._loadControllers = Mock()
		
		self.lang = {}
		self.parser = Mock()
		
		super().__init__( *args, **kwargs )
	
	def _getMockConfig( self ):
		return {}

class testWorkflowIgnitor( BaseTestCase ):
	
	def setUp( self ):
		self.mock = WorkflowIgnitorMock()
	
	def testConstructor( self ):
		instance = WorkflowIgnitorMock()
		instance._loadControllers.assert_called_once_with()
		instance._loadConfig.assert_called_once_with()
		# Since no lang is in config, app should load en lang.
		instance._loadLang.assert_called_once_with( 'en' )
		instance._registerCommandParser.assert_called_once_with()
		
	def testConstructorCustomLang( self ):
		class __WorkflowIgnitorSub( WorkflowIgnitorMock ):
			def _getMockConfig( self ):
				return { 'lang': 'nl' }
		
		instance = __WorkflowIgnitorSub()
		instance._loadLang.assert_called_once_with( 'nl' )
	
	def testRegisterIntegration( self ):
		class _IntegrationSubtype( Integration ):
			attach = Mock()
		
		IntegrationType = _IntegrationSubtype
		self.mock.registerIntegration( IntegrationType )
		
		self.assertEqual( 1, len( self.mock._integrations ), 'Invalid _integrations lenght' )
		self.assertIsInstance( self.mock._integrations[ 0 ], IntegrationType )
		
		self.mock._integrations[ 0 ].attach.assert_called_once_with()
	
	def testRegisterIntegrationInvalid( self ):
		class _BadIntegrationType:
			pass
		
		self.assertRaises( TypeError, self.mock.registerIntegration, _BadIntegrationType )
	
	def testGetIntegrations( self ):
		allIntegrations = ( 1, 'a', 2, dict() )
		self.mock._integrations = allIntegrations
		ret = self.mock.getIntegrations()
		
	def testGetIntegrationsFiltering( self ):
		allIntegrations = ( 1, 'a', 2, dict() )
		self.mock._integrations = allIntegrations
		ret = self.mock.getIntegrations( int )
		self.assertEqual( 2, len( ret ), 'Invalid ret lenght' )
		self.assertTupleEqual( ( 1, 2 ), ret, 'Invalid ret value' )
	
	def testLoadConfig( self ):
		import json
		mock = Mock()
		
		jsonDictionary = { 'foo': 1 }
		mock._getFileContent = Mock( return_value = '<configMock>' )
		
		with patch( 'json.loads', return_value = jsonDictionary ) as jsonLoadStringMocked:
			ret = WorkflowIgnitor._loadConfig( mock )
			
			self.assertEqual( 1, mock._getFileContent.call_count, '_getFileContent call count' )
			self.assertIsInstance( mock._getFileContent.call_args[ 0 ][ 0 ], str )
			self.assertTrue( mock._getFileContent.call_args[ 0 ][ 0 ].endswith( 'config.json' ) )
			
			jsonLoadStringMocked.assert_called_once_with( '<configMock>' )
			self.assertEqual( jsonDictionary, ret, 'Invalid return value' )
			
			
			self.assertIsInstance( ret, dict, 'Invalid type' )
	
	def testGetFileContent( self ):
		ret = self.mock._getFileContent( os.sep.join( ( os.path.dirname( __file__ ), '_fixtures', 'sample.json' ) ) )
		
		self.assertEqual( '{"sample":true}', ret )
	
	def testLoadLang( self ):
		mock = Mock()
		
		l11nDict = {}
		mockedGetFileContent = Mock( return_value = 'localizedContent' )
		mock._getFileContent = mockedGetFileContent
		
		with patch( 'json.loads', return_value = l11nDict ) as jsonLoadStringMocked:
			ret = WorkflowIgnitor._loadLang( mock, 'foob' )
			
			self.assertEqual( 1, mockedGetFileContent.call_count, 'Invalid _getFileContent call count' )
			# Checking argument given to _getFileContent.
			firstArg = mockedGetFileContent.call_args[ 0 ][ 0 ]
			self.assertIsInstance( firstArg, str, 'Invalid first arg type' )
			self.assertTrue( firstArg.endswith( 'foob.json' ), '_getFileContent arg 0 ("{0}") does not end with foob.json'.format( firstArg ) )
			
			jsonLoadStringMocked.assert_called_once_with( 'localizedContent' )
			
			self.assertEqual( l11nDict, mock.lang, 'Invalid dictionary' )
			
			self.assertTrue( ret, 'Invalid ret value' )
	
	def testLoadLangMissing( self ):
		mock = Mock()
		
		l11nDict = {}
		mockedGetFileContent = Mock( side_effect = FileNotFoundError( 'foo' ) )
		mock._getFileContent = mockedGetFileContent
		self.assertRaisesRegex( RuntimeError, '^Language file \"foo\.json\" not found\. Check \/lang file for available langs\.$', WorkflowIgnitor._loadLang, mock, 'foo' )
	
	def testLoadControllers( self ):
		mock = Mock()
		WorkflowIgnitor._loadControllers( mock )
		self.assertIsInstance( mock.issues, IssueController )
	
	def testRegisterCommandParser( self ):
		lang = {
			"app": {
				"name": "foo",
				"descr": "bar"
			}
		}
		mock = Mock()
		mock.lang = lang
		parser = Mock()
		with patch( 'argparse.ArgumentParser', return_value = parser ) as argParserMock:
			WorkflowIgnitor._registerCommandParser( mock )
			
			argParserMock.assert_called_once_with( prog = 'foo', description = 'bar' )
			self.assertEqual( parser, mock.parser, 'Invalid mock.parser value' )
