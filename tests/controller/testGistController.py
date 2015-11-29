
from unittest.mock import Mock, patch, call
from io import StringIO
import sys, os

from tests.BaseTestCase import BaseTestCase
from workflow_ignitor.controller.GistController import GistController

class testGistController( BaseTestCase ):
	
	def setUp( self ):
		self.owner = Mock()
		self.mock = GistController( self.owner )
		self.mock.readline = Mock( return_value = 'foo' )
	
	def testActionCreate( self ):
		
		args = Mock()
		args.files = []
		self.mock._getGithubUser = Mock()
		self.mock.readline = Mock( side_effect = ( 'main.md', 'Hello world!' ) )
		self.mock.actionCreate( args )
		
		createGistMock = self.mock._getGithubUser().create_gist
		self.assertEqual( 1, createGistMock.call_count, 'Invalid user.create_gist call count' )
		
		callArgs = createGistMock.call_args[ 0 ]
		self.assertFalse( callArgs[ 0 ], 'Invalid first argument for create_gist' )
		self.assertIsInstance( callArgs[ 1 ], dict, 'Invalid type of second argument' )
		self.assertTupleEqual( ( '0', ), tuple( callArgs[ 1 ].keys() ) )
		
		self.assertEqual( 'main.md', callArgs[ 1 ][ '0' ]._InputFileContent__newName, 'Invalid gist file name' )
		self.assertEqual( 'Hello world!', callArgs[ 1 ][ '0' ]._InputFileContent__content, 'Invalid content' )
		
	def testActionCreateFiles( self ):
		
		args = Mock()
		testBaseDir = os.path.split( os.path.realpath( __file__ ) )[ 0 ]
		args.files = [
			os.sep.join( ( testBaseDir, '_fixtures', 'gistSource1.md' ) ),
			os.sep.join( ( testBaseDir, '_fixtures', 'gistSource2.md' ) )
		]
		self.mock._getGithubUser = Mock()
		self.mock.actionCreate( args )
		
		createGistMock = self.mock._getGithubUser().create_gist
		self.assertEqual( 1, createGistMock.call_count, 'Invalid user.create_gist call count' )
		
		callArgs = createGistMock.call_args[ 0 ]
		self.assertFalse( callArgs[ 0 ], 'Invalid first argument for create_gist' )
		self.assertIsInstance( callArgs[ 1 ], dict, 'Invalid type of second argument' )
		
		self.assertListEqual( [ '0', '1' ], sorted( list( callArgs[ 1 ].keys() ) ) )
		
		self.assertEqual( 'gistSource1.md', callArgs[ 1 ][ '0' ]._InputFileContent__newName, 'Invalid gist file name' )
		self.assertEqual( 'aaa', callArgs[ 1 ][ '0' ]._InputFileContent__content, 'Invalid content' )
		
		
		self.assertEqual( 'gistSource2.md', callArgs[ 1 ][ '1' ]._InputFileContent__newName, 'Invalid gist file name' )
		self.assertEqual( 'bbb\nbbb', callArgs[ 1 ][ '1' ]._InputFileContent__content, 'Invalid content' )
		
	def testActionCreatePublic( self ):
		
		args = Mock()
		args.public = True
		args.files = []
		self.mock._getGithubUser = Mock()
		self.mock.actionCreate( args )
		
		createGistMock = self.mock._getGithubUser().create_gist
		self.assertEqual( 1, createGistMock.call_count, 'Invalid user.create_gist call count' )
		
		callArgs = createGistMock.call_args[ 0 ]
		self.assertTrue( callArgs[ 0 ], 'Invalid first argument for create_gist' )
	
	@patch( '__main__.sys.stdin', StringIO( ' test.xml\t\n\t foo bar\nbaz' ) )
	def testActionCreateStdin( self ):
		
		args = Mock()
		args.stdin = True
		args.files = []
		self.mock._getGithubUser = Mock()
		self.mock.actionCreate( args )
		
		createGistMock = self.mock._getGithubUser().create_gist
		self.assertEqual( 1, createGistMock.call_count, 'Invalid user.create_gist call count' )
		
		callArgs = createGistMock.call_args[ 0 ]
		self.assertFalse( callArgs[ 0 ], 'Invalid first argument for create_gist' )
		self.assertIsInstance( callArgs[ 1 ], dict, 'Invalid type of second argument' )
		self.assertTupleEqual( ( '0', ), tuple( callArgs[ 1 ].keys() ) )
		
		self.assertEqual( 'test.xml', callArgs[ 1 ][ '0' ]._InputFileContent__newName, 'Invalid gist file name' )
		self.assertEqual( '\t foo bar\nbaz', callArgs[ 1 ][ '0' ]._InputFileContent__content, 'Invalid content' )
	