
import os
from unittest.mock import Mock, patch
from tests.BaseTestCase import BaseTestCase
from workflow_ignitor.WorkflowIgnitor import WorkflowIgnitor
from workflow_ignitor.controller.IssueController import IssueController
from workflow_ignitor.Integration import Integration

class testWorkflowIgnitor( BaseTestCase ):
	
	def setUp( self ):
		self.mock = WorkflowIgnitor()
	
	def testConstructor( self ):
		class __WorkflowIgnitorSub( WorkflowIgnitor ):
			_loadConfig = Mock()
		
		instance = __WorkflowIgnitorSub()
		self.assertIsInstance( instance.issues, IssueController )
		instance._loadConfig.assert_called_once_with()
	
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
		
		jsonDictionary = { 'foo': 1 }
		self.mock._getFileContent = Mock( return_value = '<configMock>' )
		
		with patch( 'json.loads', return_value = jsonDictionary ) as jsonLoadStringMocked:
			ret = self.mock._loadConfig()
			
			self.assertEqual( 1, self.mock._getFileContent.call_count, '_getFileContent call count' )
			self.assertIsInstance( self.mock._getFileContent.call_args[ 0 ][ 0 ], str )
			self.assertTrue( self.mock._getFileContent.call_args[ 0 ][ 0 ].endswith( 'config.json' ) )
			
			jsonLoadStringMocked.assert_called_once_with( '<configMock>' )
			self.assertEqual( jsonDictionary, ret, 'Invalid return value' )
			
			
			self.assertIsInstance( ret, dict, 'Invalid type' )
	
	def testGetFileContent( self ):
		ret = self.mock._getFileContent( os.sep.join( ( os.path.dirname( __file__ ), '_fixtures', 'sample.json' ) ) )
		
		self.assertEqual( '{"sample":true}', ret )
	