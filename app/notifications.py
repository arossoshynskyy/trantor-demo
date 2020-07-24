import os
import logging

import settings

from slack import WebClient
from github import Github

DEPLOYMENT_STATUS = {"COMPLETED": "SUCCEEDED", "ERRORED": "FAILED"}

slack_client = WebClient(token=settings.SLACK_API_TOKEN)
github_client = Github(settings.GITHUB_API_TOKEN)


def notify_deployment_success():
    notify_slack_tech_release(event)
    notify_slack_deployment_status(event)

def notify_deployment_failed():
    notify_slack_deployment_status()

def notify_slack_tech_release(event):
    repository = event["repository"]
    created_by = event["created_by"]
    commit_sha = event["commit_sha"]
    environment = event["environment"]

    commit = get_commit(repository, commit_sha)

    response = slack_client.chat_postMessage(
        channel="tech-release-notes",
        text=f"`{repository}` <@{created_by}> \n\n {commit.message}"
    )

def notify_slack_deployment_status(event):
    created_by = event["created_by"]
    commit_sha = event["commit_sha"]
    repository = event["repository"]
    status = event["status"]
    environment = event["environment"]

    response = slack_client.chat_postMessage(
        channel=f"@{created_by}",
        text=f"`{repository}` -> `{environment}` has *{DEPLOYMENT_STATUS[status]}*"
    )


def get_commit(repository, commit_sha):
    return github_client.get_repo(f"boughtbymany/{repository}").get_commit(commit_sha).commit
