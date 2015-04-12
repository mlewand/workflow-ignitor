#!/usr/bin/env python3

import sys

from workflow_ignitor.WorkflowIgnitor import WorkflowIgnitor
# Currently we need to attach integrations manually.
from workflow_ignitor.github.GitHubIntegration import GitHubIntegration

app = WorkflowIgnitor()
# Include GitHub integration.
app.registerIntegration( GitHubIntegration )

# Start the app.
app.start( sys.argv )
