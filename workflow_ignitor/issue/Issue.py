
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
	
	
