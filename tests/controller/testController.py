
from unittest.mock import Mock
from tests.BaseTestCase import BaseTestCase
from workflow_ignitor.controller.Controller import Controller

class testController( BaseTestCase ):
	
	def testProcess( self ):
		mock = Mock()
		mock.cliSubActions = [ 'foo' ]
		args = Mock()
		
		args.subAction = 'foo'
		
		Controller.process( mock, args )
		
		mock.actionFoo.assert_called_once_with( args )
	
	def testProcessInvalid( self ):
		# Unmapped subaction.
		mock = Mock()
		mock.cliSubActions = []
		args = Mock()
		
		args.subAction = 'foox'
		
		Controller.process( mock, args )
		
	
