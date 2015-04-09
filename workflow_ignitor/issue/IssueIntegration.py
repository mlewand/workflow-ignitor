
from workflow_ignitor.Integration import Integration

class IssueIntegration( Integration ):
	
	'''
	Interface for all issue-related integrations.
	
	Later on we should change it with event system. For the time being I'll implement it by interfaces, so it will be a little quicker.
	'''
	
	def createIssue( self, issue, project ):
		raise NotImplementedError()
