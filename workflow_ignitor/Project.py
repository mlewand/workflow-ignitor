
import os.path

from workflow_ignitor.Configurable import Configurable

class Project( Configurable ):
	'''
	Class to represent the project.
	
	Currently we're strictly focused on project from a programmer POV, so it needs to be located within certian directory.
	'''
	
	def __init__( self, projectId, path, config = None ):
		'''
		Constructor for Project.
		
		It will automatically check if path is valid and throw exception if it's invalid dir.
		'''
		self.id = projectId
		self.setPath( path )
		
		super().__init__( config )
	
	def setPath( self, path ):
		'''
		Path setter that will ensure that given directory does exists.
		'''
		
		if os.path.isdir( path ):
			self.path = path
		else:
			raise IOError( 'Project directory "{0}" not found.'.format( path ) )
	
	
