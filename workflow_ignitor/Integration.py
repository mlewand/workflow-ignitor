
class Integration:
	
	def __init__( self, owner ):
		'''
		Constructor for Controller.
		'''
		
		if 0:
			# IDE syntax helper.
			from workflow_ignitor.WorkflowIgnitor import WorkflowIgnitor
			self.owner = WorkflowIgnitor()
		
		self.owner = owner
	
	def attach( self ):
		'''
		Called when the integration is attached to the main app object.
		'''
		pass
