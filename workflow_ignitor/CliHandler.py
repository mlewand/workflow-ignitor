
import argparse

class CliHandler:
	
	def __init__( self, owner ):
		self.owner = owner
		self._actionMapping = {}
		self.parser = self._createParser()
	
	def registerController( self, controller ):
		'''
		Checks desired action of given controller, and mapps it.
		'''
		
		if not controller.cliAction:
			raise ValueError( 'Registered controller must have non-empty cliAction' )
		
		self._actionMapping[ controller.cliAction ] = controller
	
	def parse( self, args ):
		pass
	
	def _createParser( self ):
		appLang = self.owner.lang[ 'app' ]
		self.parser = argparse.ArgumentParser( prog = appLang[ 'name' ], description = appLang[ 'descr' ] )
	