
# Workflow Ignitor

This repo contains small app that will help me with project creation. Often times I'm creating tiny app / script to handle particular task, it would be cool to create whole project backend (local repo, online repo, IDE project) with just a single CLI command.

## Requirements

* Python3
* [PyGithub](https://github.com/PyGithub/PyGithub)

## Installation

```
git clone https://github.com/mlewand/workflow-ignitor.git workflow-ignitor
cd workflow-ignitor
pip install PyGithub
```

See also [Initial configuration section](#initial-configuration).

## Initial configuration

At the begining most likely you'll need to set your configuration. You need to set your projects, as based on their metadata app will know what repository should be used, etc.

For that create `config.json` based on `config.json.dist` file and:
* [Add necessary projects](#change-current-project).
* [Set current project](#change-current-project).
* Provide your GitHub token and user name if you want to integrate with it.

## Usage

### Adding a Project

You add a project by... manually adding it to `config.json` (Hell, yeah)!

### Changing Current Project

As of now current project is determined based on `config.json`. Open `config.json` and set `currentProject.tmp` to the key of your project in `projects` object. E.g.

This might be overridden by `--project` CLI option.

```json
{
	"tmp": {
		"currentProject": "foo_project"
	},
	"projects": {
		"foo_project": {
			"path": "/dev/foobar",
			"github": {
				"repo": {
					"name": "foobar"
				}
			}
		},
		
		"workflow_ignitor": {
			"path": "/dev/workflow_ignitor",
			"github": {
				"repo": {
					"name": "workflow-ignitor"
				}
			}
		}
	}
}
```

### Issue Creation

Issue creation by default takes source text from stdin (you might also provide issue source text as a file with `--file` option). Source text for issue is expected to have following format:

```
<issue title>

<issue description>
```

**Warning: it will automatically create this issue in your current project on github!**

```
python3 cli.py issues create
```

Enter title / descr and send a EOF character (`CTRL+D` at *nix and `CTRL+Z` on Windows).