
from unittest.mock import Mock, patch
from tests.BaseTestCase import BaseTestCase
from workflow_ignitor.github.GitHubIntegration import GitHubIntegration

class testGitHubIntegration( BaseTestCase ):
	
	def setUp( self ):
		self.owner = Mock()
		self.mock = GitHubIntegration( self.owner )
	
	def testCreateIssue( self ):
		
		githubMock = Mock()
		issue = Mock()
		issue.title = 'foo'
		issue.descr = 'bar'
		proj = Mock()
		proj.getConfig = Mock( return_value = 'repoName' )
		
		self.mock.github = githubMock
		self.mock.createIssue( issue, proj )
		
		proj.getConfig.assert_called_once_with( 'github.repo.name' )
		
		githubMock.get_user.assert_called_once_with()
		githubMock.get_user().get_repo.assert_called_once_with( 'repoName' )
		githubMock.get_user().get_repo().create_issue.assert_called_once_with( 'foo', 'bar' )
	
	def testCreateIssueInvalidProject( self ):
		
		issue = Mock()
		issue.title = 'foo'
		issue.descr = 'bar'
		proj = Mock()
		proj.getConfig = Mock( return_value = None )
		
		self.assertRaises( RuntimeError, self.mock.createIssue, issue, proj )
	

