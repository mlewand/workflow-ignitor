
class CliHandler:
	
	def __init__( self, owner ):
		self._actionMapping = {}
	
	def registerController( self, controller ):
		'''
		Checks desired action of given controller, and mapps it.
		'''
		
		if not controller.cliAction:
			raise ValueError( 'Registered controller must have non-empty cliAction' )
		
		self._actionMapping[ controller.cliAction ] = controller
	
	def parse( self, args ):
		pass
	