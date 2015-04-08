
from tests.BaseTestCase import BaseTestCase
from workflow_ignitor.WorkflowIgnitor import WorkflowIgnitor
from workflow_ignitor.controller.IssueController import IssueController

class testWorkflowIgnitor( BaseTestCase ):
	
	def testConstructor( self ):
		
		instance = WorkflowIgnitor()
		self.assertIsInstance( instance.issues, IssueController )
