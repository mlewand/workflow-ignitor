
# Controller

## Actions

Actions are "Controller subcommands". In CLI action will always follow controller name, e.g. `app.py issues create` - where `create` is an action.

Actions are simply a method in Controller class that starts with "action" prefix.

### Adding a New Action

To add a new action you need to register it in `subAction` list.

```python
class SampleController( Controller ):
	cliAction = 'sample'
	
	cliSubActions = [ 'handleX', 'handleY' ]
	
	def actionHandleY( self, args ):
		pass
	
	def actionHandleY( self, args ):
		pass
```
