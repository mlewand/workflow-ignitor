
import os.path

class Project:
	'''
	Class to represent the project.
	
	Currently we're strictly focused on project from a programmer POV, so it needs to be located within certian directory.
	'''
	
	def __init__( self, projectId, path, properties = None ):
		'''
		Constructor for Project.
		
		It will automatically check if path is valid and throw exception if it's invalid dir.
		'''
		self.id = projectId
		self.setPath( path )
		self._properties = properties or {}
	
	def setPath( self, path ):
		'''
		Path setter that will ensure that given directory does exists.
		'''
		
		if os.path.isdir( path ):
			self.path = path
		else:
			raise IOError( 'Project directory "{0}" not found.'.format( path ) )
	
	def setProperty( self, name, value ):
		'''
		Sets custom property to a given value.
		'''
		if not isinstance( name, str ):
			raise TypeError( 'Invalid type given for name. Expected {0}, while str was expected.'.format( type( name ) )  )
		
		parts = str( name ).split( '.' )
		
		curScope = self._properties
		
		for curPart in parts[ 0 : -1 ]:
			if not curPart in curScope.keys():
				curScope[ curPart ] = {}
			
			curScope = curScope[ curPart ]
		
		curScope[ parts[ -1 ] ] = value
	
	def getProperty( self, name ):
		
		parts = str( name ).split( '.' )
		
		curScope = self._properties
		
		for curPart in parts[ 0 : -1 ]:
			if not curPart in curScope.keys():
				return None
			else:
				curScope = curScope[ curPart ]
		
		return curScope[ parts[ -1 ] ]
	
	
	
