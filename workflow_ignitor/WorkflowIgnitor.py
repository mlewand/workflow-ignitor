
from workflow_ignitor.controller.IssueController import IssueController
from workflow_ignitor.Integration import Integration
from workflow_ignitor.Project import Project

class WorkflowIgnitor:
	
	def __init__( self ):
		self.issues = IssueController( self )
		'''
		List of Integration derived instances.
		'''
		self._integrations = list()
	
	def registerIntegration( self, IntegrationType ):
		
		if not issubclass( IntegrationType, Integration ):
			raise TypeError( 'Invalid IntegrationType, expected type to be Integration subclass.' )
		
		integration = IntegrationType( self )
		self._integrations.append( integration )
		integration.attach()
	
	def getIntegrations( self, baseType = None ):
		'''
		Returns registered integrations that implements given baseType.
		
		If baseType is None, it will return all the integrations.
		'''
		return tuple( filter( lambda x: baseType == None or isinstance( x, baseType ), self._integrations )  )
	
	def getProject( self ):
		'''
		Returns current project.
		'''
		import os
		
		# @TODO: fix me.
		# Hardcoded for testing purposes.
		proj = Project( 'workflow_ignitor', os.path.realpath( os.path.split( __file__ )[ 0 ] + os.sep + '..' ) )
		proj.setProperty( 'github.repo.name', 'foobar' )
		
		return proj
	
	
