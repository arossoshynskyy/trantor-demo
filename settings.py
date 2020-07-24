from os import environ


EVENT_SOURCE=environ.get("EVENT_SOURCE", "trantor-demo-dev")
TRANTOR_EVENT_BUS=environ.get("TRANTOR_EVENT_BUS", "trantor-demo")
SLACK_API_TOKEN=environ.get("SLACK_API_TOKEN")
GITHUB_API_TOKEN=environ.get("GITHUB_API_TOKEN")