
from workflow_ignitor.controller.IssueController import IssueController

class WorkflowIgnitor:
	
	def __init__( self ):
		self.issues = IssueController( self )
