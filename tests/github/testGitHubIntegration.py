
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
	
