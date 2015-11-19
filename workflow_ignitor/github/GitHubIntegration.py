
from workflow_ignitor.Integration import Integration
from workflow_ignitor.issue.IssueIntegration import IssueIntegration

from github import Github

class GitHubIntegration( IssueIntegration ):
	
	def attach( self ):
		super().attach()
		
		self.githubToken = self.owner.getConfig( 'github.token' )
		self.github = Github( self.githubToken )
	
	def createIssue( self, issue, project ):
		repo = self._getRepo( project )
		repo.create_issue( issue.title, issue.descr )
		
		print( '-- GitHubIntegration log: issue created' )
	
	def closeIssue( self, issue, project ):
		repo = self._getRepo( project )
		issue = repo.get_issue( issue.id )
		issue.edit( state = 'closed' )
		
	def _getRepo( self, project ):
		'''
		Returns a proper repository object based on given project.
		
		:param project: :class:`workflow_ignitor.Projcet`
		:type: :class:`github.Repository.Repository` or None
		'''
		repoName = project.getConfig( 'github.repo.name' )
		organization = project.getConfig( 'github.repo.organization' )
		
		if not repoName:
			raise RuntimeError( 'Missing config: github.repo.name' )
		
		repoHost = self.github.get_organization( organization ) if organization else self.github.get_user()
		
		return repoHost.get_repo( repoName )
	
	def getIssueUrl( self, issue, project ):
		'''
		Returns an issue URL.
		
		:param issue: :class:`workflow_ignitor.issue.Issue`
		:param project: :class:`workflow_ignitor.Projcet`
		:type: str
		'''
		if issue.id == None:
			raise ValueError( 'Issue doesn\'t have an id.' )
		
		projectName = project.getConfig( 'github.repo.name' )
		organization = project.getConfig( 'github.repo.organization' )
		repoOwner = organization if organization else 'mlewand'
		
		return 'https://github.com/{1}/{2}/issues/{0.id}'.format( issue, repoOwner, projectName )
