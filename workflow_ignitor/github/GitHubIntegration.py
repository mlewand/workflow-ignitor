
from workflow_ignitor.Integration import Integration
from workflow_ignitor.issue.IssueIntegration import IssueIntegration

from github import Github

class GitHubIntegration( IssueIntegration ):
	
	def attach( self ):
		super().attach()
		
		import json
		
		# This part is totally hardcoded because it's already 1am. Later on I need to create a config in main app object.
		with open( 'config.json' ) as hFile:
			cfg = json.loads( hFile.read() )
			self.github = Github( cfg[ 'github.token' ] )
	
	def createIssue( self, issue, project ):
		
		githubRepo = project.getConfig( 'github.repo.name' )
		
		if not githubRepo:
			raise RuntimeError( 'Missing config: github.repo.name' )
		
		repo = self.github.get_user().get_repo( githubRepo )
		repo.create_issue( issue.title, issue.descr )
		
		print( '-- GitHubIntegration log: issue created' )
