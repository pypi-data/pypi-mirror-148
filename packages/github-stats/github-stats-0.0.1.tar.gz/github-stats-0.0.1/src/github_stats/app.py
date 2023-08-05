import datetime
from typing import List

import click
import pandas as pd
from github import Github
from github.PullRequest import PullRequest
from github.Repository import Repository
from rich import box
from rich.console import Console
from rich.table import Table

from github_stats import rich_utils

console = Console()


class GitStats:
    def __init__(self, token: str, user_name: str, org_name: str, repo_names: str) -> None:
        """
        Initializes the class

        Args:
            token: GitHub token
            user_name: GitHub username
        """
        self.g = Github(token)
        self.user = self.g.get_user(user_name)
        self.org_name = org_name
        self.repo_names = repo_names.replace(" ", "").split(",")

    def run(self):
        """
        Runs the program

        """

        stats = []

        # Getting the rich progress bar and the run id
        progress, run_id = rich_utils.get_rich_progress_and_run_id(self.repo_names)

        with progress:
            for repo in self.repo_names:
                prs_reviewed = self._get_review_count_per_repo(f"{self.org_name}/{repo}")
                for pr in prs_reviewed:
                    stats.append(
                        {
                            "Repo": repo,
                            "PR Title": pr.title,
                            "PR ID": pr.number,
                        }
                    )

                progress.update(run_id, advance=1)
                progress.refresh()

        stats = pd.DataFrame.from_records(stats)

        # Initiate a Table instance to be modified
        table = Table(show_header=True, header_style="bold magenta")

        # Modify the table instance to have the data from the DataFrame
        table = rich_utils.df_to_table(stats, table)

        # Update the style of the table
        table.box = box.ROUNDED
        table.caption = f"PRs reviewed this week: {len(stats)}"
        table.caption_style = "bold italic"

        console.print("\n", table, "\n")

    def _get_review_count_per_repo(self, repo_name: str) -> List[PullRequest]:
        """
        Returns a list of PRs reviewed by the user in the given repo

        Args:
            repo_name: The name of the repo to get the PRs from

        Returns: A list of PRs reviewed by the user in the given repo

        """
        repo = self.g.get_repo(repo_name)

        valid_pulls = self._get_valid_pulls(repo)

        prs_reviewed = []
        for pull in valid_pulls:
            for review in pull.get_reviews():
                if review.user == self.user:
                    prs_reviewed.append(pull)
                    break

        return prs_reviewed

    def _get_valid_pulls(self, repo: Repository) -> List[PullRequest]:
        """
        Returns a list of all PRs in a repo from the last two weeks that are not created by the user

        Args:
            repo: Repository object

        Returns: list of PRs

        """
        pulls = repo.get_pulls(state="all", sort="created", direction="desc")

        valid_pulls = [
            pull
            for pull in pulls
            if (
                pull.created_at >= datetime.datetime.now() - datetime.timedelta(days=14)
                and self.user not in pull.assignees
            )
        ]

        return valid_pulls


@click.command()
@click.option("-t", "--token", prompt="Github token", help="Github token", envvar="GITHUB_TOKEN")
@click.option("-u", "--username", prompt="Github username", help="Github username", envvar="GITHUB_USERNAME")
@click.option("-o", "--org", prompt="Github org", help="Github org", envvar="GITHUB_ORGANIZATION")
@click.option("-r", "--repos", prompt="Github repos", help="',' separated github repos", envvar="GITHUB_REPOS")
def main(token: str, username: str, org: str, repos: str):
    """
    This script will print the number of PRs reviewed by the user in the last two weeks.

    """

    gs = GitStats(token=token, user_name=username, org_name=org, repo_names=repos)
    gs.run()
