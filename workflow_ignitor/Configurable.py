
class Configurable:
	'''
	Abstract class that provides configuration getters / setters.
	'''
	
	def __init__( self, config = None ):
		self._config = config or {}
	
	def setConfig( self, name, value ):
		'''
		Sets custom property to a given value.
		'''
		if not isinstance( name, str ):
			raise TypeError( 'Invalid type given for name. Expected {0}, while str was expected.'.format( type( name ) )  )
		
		parts = str( name ).split( '.' )
		
		curScope = self._config
		
		for curPart in parts[ 0 : -1 ]:
			if not curPart in curScope.keys():
				curScope[ curPart ] = {}
			
			curScope = curScope[ curPart ]
		
		curScope[ parts[ -1 ] ] = value
	
	def getConfig( self, name ):
		
		parts = str( name ).split( '.' )
		
		curScope = self._config
		
		for curPart in parts[ 0 : -1 ]:
			if not curPart in curScope.keys():
				return None
			else:
				curScope = curScope[ curPart ]
		
		return curScope[ parts[ -1 ] ] if parts[ -1 ] in curScope else None