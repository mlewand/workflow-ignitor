
class Issue:
	'''
	Issue model.
	'''
	
	def __init__( self, title, descr = '', id = None ):
		'''
		Constructor for Issue.
		'''
		self.title = title
		self.descr = descr
		self.id = id
	
	def exists( self ):
		'''
		Tells if this issue exists (was registered).
		
		:type: bool
		'''
		
		return self.id != None
	
	
