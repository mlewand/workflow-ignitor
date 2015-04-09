
# This sample will create an issue in your current project with a fixed, junk content.
from workflow_ignitor.WorkflowIgnitor import WorkflowIgnitor
from workflow_ignitor.github.GitHubIntegration import GitHubIntegration

app = WorkflowIgnitor()
# Include GitHub integration.
app.registerIntegration( GitHubIntegration )

# Issue source text. First line is a title, and all the rest is the description.
issueText = '''Lorem ipsum

This is test issue.
'''

print( 'This script will add junk issue to your current project. Type "y" to continue.' )
resp = input( '' )

if resp != 'y':
	print( 'Typed "{}", aborting.'.format( resp ) )
	exit()

# Reports the issue.
app.issues.reportIssueFromText( issueText )
