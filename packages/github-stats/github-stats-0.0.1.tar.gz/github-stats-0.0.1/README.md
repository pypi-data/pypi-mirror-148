# Github Stats [![Python Versions](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/) [![GitHub](https://img.shields.io/github/license/saiyalamarty/gitstats.svg)](https://github.com/saiyalamarty/gitstats/blob/develop/LICENSE)

Command line tool to get number of PRs reviewed by a user.

## Usage
Use `--help` to see all options.
```
$ gitstats --help
Usage: gitstats [OPTIONS]

  This script will print the number of PRs reviewed by the user in the last
  two weeks.

Options:
  -t, --token TEXT     Github token
  -u, --username TEXT  Github username
  -o, --org TEXT       Github org
  -r, --repos TEXT     ',' separated github repos
  --help               Show this message and exit.
```

The script can by default attempts to read the options from the environment variables. Set the following environment variables:

* `GITHUB_TOKEN` - GitHub token
* `GITHUB_USERNAME` - GitHub username
* `GITHUB_ORGANIZATION` - GitHub organization
* `GITHUB_REPOS` - Comma separated list of GitHub repositories

If the environment variables are not set, the script will prompt for the values.

When the script is run, it will print the number of PRs reviewed by the user in the last two weeks.

```
$ gitstats
Repos ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2/2 • 0:00:06 0:00:00


╭───┬───────────┬─────────────────────────────────────────────────────────────────────┬───────╮
│   │ Repo      │ PR Title                                                            │ PR ID │
├───┼───────────┼─────────────────────────────────────────────────────────────────────┼───────┤
│ 0 │ gitrepo_1 │ Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiu │ 101   │
│ 1 │ gitrepo_2 │ Lorem ipsum dolor sit amet, consectetur adipiscing elit,            │ 100   │
╰───┴───────────┴─────────────────────────────────────────────────────────────────────┴───────╯

                                   PRs reviewed this week: 2


```
