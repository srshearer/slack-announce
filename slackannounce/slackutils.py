#!/usr/bin/env python3
import json
import requests
from dataclasses import dataclass


@dataclass(frozen=True)
class TextColors:
    grey = "#d3d3d3"
    green = "good"
    orange = "warning"
    red = "danger"
    purple = "#764FA5"
    blue = "#439FE0"

    default = grey
    info = grey
    good = green
    warning = orange
    danger = red


class SlackException(Exception):
    """Custom exception for Slack related failures."""
    pass


class SlackSender(object):
    def __init__(
        self,
        webhook_url=None,
        channel=None,
        user=None,
        json_attachments=None,
        debug=False,
        dryrun=False,
    ):
        self.debug = debug
        self.dryrun = dryrun
        self.webhook_url = webhook_url
        self.json_attachments = json_attachments
        self.user = user
        self.channel = channel
        self.color = TextColors.info
        self._json_payload = None

    def set_simple_message(self, message, title=None, color=None, fallback=None):
        """Sets formatted json to use in sending a Slack notification using only
        a provided message.
        Requires:
            - str(message): The body text of the message
        Optional:
            - str(title): The title of the message
            - str(color): The color of the message
            - str(fallback): The fallback text. Same as title by default
        Returns:
            - json(self.json_attachments): The formatted json set in the object
        """

        if color is None:
            color = self.color

        if fallback is None:
            fallback = title or message

        self.json_attachments = {
            "fallback": fallback,
            "color": color,
            "text": message,
        }

        if title:
            self.json_attachments["title"] = title

        return self.json_attachments

    def send(self):
        """Send the Slack notification with the current json_attachments.
        This will update the debug state, channel, and webhook before sending.
        """
        if self.user is None:
            raise SlackException("Missing user")
        if self.webhook_url is None:
            raise SlackException("Missing webhook url")
        if self.json_attachments is None:
            raise SlackException("json_attachments not set")

        self._json_payload = {
            "channel": self.channel,
            "username": self.user,
            "attachments": [self.json_attachments],
        }

        if self.debug:
            print(f"json payload: {self._json_payload}")

        if self.dryrun:
            print("[Dry run. Not posting message.]")
            return

        response = requests.post(
            self.webhook_url,
            data=json.dumps(self._json_payload),
            headers={"Content-Type": "application/json"},
        )
        print(f"Result: [{response.status_code}] {response.text}")

        return response
