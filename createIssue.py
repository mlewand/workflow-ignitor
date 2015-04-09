
# This script will handle issue creation through CLI.
import sys, os
from workflow_ignitor.WorkflowIgnitor import WorkflowIgnitor
from workflow_ignitor.github.GitHubIntegration import GitHubIntegration

app = WorkflowIgnitor()
# Include GitHub integration.
app.registerIntegration( GitHubIntegration )

# Issue source text. First line is a title, and all the rest is the description.
# Issue text is taken from stdin.
stdInput = sys.stdin.readlines()
issueText = ''.join( stdInput ).strip()

if not issueText:
	raise RuntimeError( 'Empty buffer given to stdin. You\'re supposed to provide issue content with stdin.' )

# Reports the issue.
app.issues.reportIssueFromText( issueText )

print( 'Issue created successfuly!' )