
from unittest.mock import Mock, patch
from tests.BaseTestCase import BaseTestCase
from workflow_ignitor.github.GitHubIntegration import GitHubIntegration

class testGitHubIntegration( BaseTestCase ):
	
	def setUp( self ):
		self.owner = Mock()
		self.mock = GitHubIntegration( self.owner )
	
	def testCreateIssue( self ):
		
		issue = Mock()
		issue.title = 'foo'
		issue.descr = 'bar'
		proj = Mock()
		self.mock._getRepo = Mock()
		
		self.mock.createIssue( issue, proj )
		
		self.mock._getRepo.assert_called_once_with( proj )
		self.mock._getRepo().create_issue.assert_called_once_with( 'foo', 'bar' )
		
	def testCreateIssueSetsId( self ):
		'''
		We need to make sure that new id is assigned to issue object.
		'''
		
		issue = Mock()
		createdIssueMock = Mock()
		createdIssueMock.id = 11033
		self.mock._getRepo = Mock()
		self.mock._getRepo().create_issue = Mock( return_value = createdIssueMock )
		
		self.mock.createIssue( issue, Mock() )
		
		self.assertEqual( 11033, issue.id, 'Issue id was not updated' )
	
	def testGetRepo( self ):
		proj = Mock()
		userMock = Mock()
		userMock.get_repo = Mock()
		# Return repo name in first getConfig call, but return None in second call (no organization).
		proj.getConfig = Mock( side_effect = [ 'foo', None ] )
		self.mock.github = Mock()
		self.mock.github.get_user = Mock( return_value = userMock )
		
		ret = self.mock._getRepo( proj )
		
		self.mock.github.get_user.assert_called_once_with()
		userMock.get_repo.assert_called_once_with( 'foo' )
		self.assertEqual( userMock.get_repo( 'foo' ), ret, 'Invalid return value' )
	
	def testGetRepoOrganization( self ):
		proj = Mock()
		orgMock = Mock()
		orgMock.get_repo = Mock()
		proj.getConfig = Mock( side_effect = [ 'foo', 'bar' ] )
		self.mock.github = Mock()
		self.mock.github.get_organization = Mock( return_value = orgMock )
		
		ret = self.mock._getRepo( proj )
		
		self.assertFalse( self.mock.github.get_user.called, 'get_user() should not be called' )
		self.mock.github.get_organization.assert_called_once_with( 'bar' )
		
		orgMock.get_repo.assert_called_once_with( 'foo' )
		self.assertEqual( orgMock.get_repo( 'foo' ), ret, 'Invalid return value' )
		
	
	def testGetRepoMissingName( self ):
		proj = Mock()
		proj.getConfig = Mock( return_value = None )
		
		self.assertRaisesRegex( RuntimeError, '^Missing config: github.repo.name$', self.mock._getRepo, proj )
	
	def testGetIssueUrl( self ):
	
		issue = Mock()
		issue.id = 202
		proj = Mock()
		proj.getConfig = Mock( side_effect = ( 'fooBAR', None ) )
		self.owner.getConfig = Mock( return_value = 'userName' )
		
		self.assertEqual( 'https://github.com/userName/fooBAR/issues/202', self.mock.getIssueUrl( issue, proj ), 'Invalid URL returned' )
		
		proj.getConfig.assert_any_call( 'github.repo.name' )
		proj.getConfig.assert_any_call( 'github.repo.organization' )
	
	def testGetIssueUrlOrganization( self ):
		
		issue = Mock()
		issue.id = 202
		proj = Mock()
		proj.getConfig = Mock( side_effect = ( 'fooBAR', 'coolOrganization' ) )
		
		self.assertEqual( 'https://github.com/coolOrganization/fooBAR/issues/202', self.mock.getIssueUrl( issue, proj ), 'Invalid URL returned' )
	
	def testGetIssueUrlNoId( self ):
		
		issue = Mock()
		issue.id = None
		proj = Mock()
		
		self.assertRaisesRegex( ValueError, '^Issue doesn\'t have an id.$', self.mock.getIssueUrl, issue, proj )
