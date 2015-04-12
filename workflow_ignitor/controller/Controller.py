
class Controller:
	
	'''
	Value that this controller is going to be invoked with from CLI, e.g. for "issues" it's going to be reachable with: "app.py issues".
	
	This string is mandatory.
	'''
	cliAction = ''
	
	cliSubActions = []
	
	def __init__( self, owner ):
		'''
		Constructor for Controller.
		'''
		
		if 0:
			# IDE syntax helper.
			from workflow_ignitor.WorkflowIgnitor import WorkflowIgnitor
			self.owner = WorkflowIgnitor()
		
		self.owner = owner
	
	def process( self, args ):
		'''
		Looks for args, and based on that executes proper logic.
		'''
		
		if self.cliSubActions:
			action = 'action' + str( args.subAction ).capitalize()
			if self.cliSubActions and hasattr( self, action):
				getattr( self, action )( args )
	
	def attach( self ):
		'''
		Called when controller is finally attached to the main WorkflowIgnitor instance.
		'''
		pass
	
	def _registerCommands( self, argParser ):
		'''
		Called after the constructor to register controller commands in the CLI parser.
		'''
		pass
	
