
from workflow_ignitor.controller.IssueController import IssueController
from workflow_ignitor.Integration import Integration

class WorkflowIgnitor:
	
	def __init__( self ):
		self.issues = IssueController( self )
		'''
		List of Integration derived instances.
		'''
		self._integrations = list()
	
	def registerIntegration( self, IntegrationType ):
		
		if not issubclass( IntegrationType, Integration ):
			raise TypeError( 'Invalid IntegrationType, expected type to be Integration subclass.' )
		
		integration = IntegrationType( self )
		self._integrations.append( integration )
		integration.attach()
