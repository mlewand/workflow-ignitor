
import os

from workflow_ignitor.WorkflowIgnitor import WorkflowIgnitor
from workflow_ignitor.github.GitHubIntegration import GitHubIntegration

app = WorkflowIgnitor()
app.registerIntegration( GitHubIntegration )

issueText = '''Lorem ipsum

This is test issue.
'''

ret = app.issues.reportIssueFromText( issueText )

print( 'done' )