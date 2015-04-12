
from workflow_ignitor.Integration import Integration
from workflow_ignitor.issue.IssueIntegration import IssueIntegration

from github import Github

class GitHubIntegration( IssueIntegration ):
	
	def attach( self ):
		super().attach()
		
		self.githubToken = self.owner.getConfig( 'github.token' )
		self.github = Github( self.githubToken )
	
	def createIssue( self, issue, project ):
		
		githubRepo = project.getConfig( 'github.repo.name' )
		
		if not githubRepo:
			raise RuntimeError( 'Missing config: github.repo.name' )
		
		repo = self.github.get_user().get_repo( githubRepo )
		repo.create_issue( issue.title, issue.descr )
		
		print( '-- GitHubIntegration log: issue created' )
	
	def closeIssue( self, issue, project ):
		githubRepo = project.getConfig( 'github.repo.name' )
		
		if not githubRepo:
			raise RuntimeError( 'Missing config: github.repo.name' )
		
		repo = self.github.get_user().get_repo( githubRepo )
		issue = repo.get_issue( issue.id )
		issue.edit( state = 'closed' )
	
