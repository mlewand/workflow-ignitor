
from unittest.mock import Mock
from tests.BaseTestCase import BaseTestCase
from workflow_ignitor.WorkflowIgnitor import WorkflowIgnitor
from workflow_ignitor.controller.IssueController import IssueController
from workflow_ignitor.Integration import Integration

class testWorkflowIgnitor( BaseTestCase ):
	
	def setUp( self ):
		self.mock = WorkflowIgnitor()
	
	def testConstructor( self ):
		instance = WorkflowIgnitor()
		self.assertIsInstance( instance.issues, IssueController )
	
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
	
