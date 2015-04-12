
import argparse

class CliHandler:
	
	def __init__( self, owner ):
		self.owner = owner
		self._actionMapping = {}
		self._createParser()
	
	def registerController( self, controller ):
		'''
		Checks desired action of given controller, and mapps it.
		'''
		
		if not controller.cliAction:
			raise ValueError( 'Registered controller must have non-empty cliAction' )
		
		self._actionMapping[ controller.cliAction ] = controller
	
	def parse( self, args ):
		'''
		Note that args parameter is expected to be in a form like in sys.argv. Meaning that first item is a program name, that will be stripped within this funciton.
		'''
		
		# Add all the actions registered by the controllers.
		self.parser.add_argument( 'action', help = 'an action', choices = self._actionMapping.keys() )
		
		try:
			controller = self._actionMapping[ args[ 1 ] ]
		except ( IndexError, KeyError ) as err:
			controller = None
			
		if not controller:
			self.parser.print_help()
			return False
		
		controller._registerCommands( self.parser )
		result = self.parser.parse_args( args[ 1 : ] )
		
		return controller, result
	
	def _createParser( self ):
		appLang = self.owner.lang[ 'app' ]
		self.parser = argparse.ArgumentParser( prog = appLang[ 'name' ], description = appLang[ 'descr' ] )
		self.parser.add_argument( '--project', '-p', help = appLang[ 'cli' ][ 'project' ], metavar = 'project' )
	