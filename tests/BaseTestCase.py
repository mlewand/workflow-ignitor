
import os
import unittest

class BaseTestCase( unittest.TestCase ):
	
	def __assertFileExists( self, filePath, failMessage, fileShouldExists ):
		self.assertTrue( os.path.isfile( filePath ) == bool( fileShouldExists ), failMessage )
	
	def assertIsSubclass( self, testedObject, expectedType, msg ):
		'''
		Checks if given testedObject is instance of expectedType object.
		'''
		
		if not isinstance( expectedType, type ):
			raise TypeError( 'Invalid type for expectedType argument. Should be a type, {0} got instead.'.format( type( expectedType ) ) )
		
		msgArgs = ( type( testedObject ).__name__, expectedType.__name__, msg if len( msg ) else '' )
		
		self.assertTrue( isinstance( testedObject, expectedType  ), '{0} instance is not a subclass of {1} type. {2}'.format( *msgArgs ) )
	
	
if __name__ == '__main__':
	suite = unittest.TestSuite()
	suite.addTest( unittest.makeSuite( BaseTestCase ) )
	unittest.TextTestRunner( verbosity = 2 ).run( suite )