
class Controller:
	
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
		Called when controller is finally attached to the main WorkflowIgnitor instance.
		'''
		self._registerCommands( self.owner.parser )
	
	def _registerCommands( self, argParser ):
		'''
		Called after the constructor to register controller commands in the CLI parser.
		'''
		pass
	
