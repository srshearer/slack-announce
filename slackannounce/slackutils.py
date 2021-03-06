#!/usr/bin/env python3
import json
import requests
from dataclasses import dataclass


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

        if not color:
            color = self.color

        if not fallback:
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
        if not self.user:
            raise SlackException("Missing user")
        if not self.webhook_url:
            raise SlackException("Missing webhook url")
        if not self.json_attachments:
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


@dataclass
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
    warn = orange
    warning = orange
    orange = orange
    danger = red
    red = red
    purple = purple


def text_color(requested_color):
    """Takes a color alias (str) and returns the color value if available"""

    print(
        "WARNING: This funtion is deprecated and will be removed soon! "
        "Please use TextColors dataclass instead of text_color() function!"
    )

    text_color_dict = {
        "default": TextColors.grey,
        "info": TextColors.grey,
        "good": TextColors.green,
        "green": TextColors.green,
        "warn": TextColors.orange,
        "orange": TextColors.orange,
        "danger": TextColors.red,
        "red": TextColors.red,
        "purple": TextColors.purple,
        "blue": TextColors.blue,
    }

    if requested_color.lower() in map(str.lower, text_color_dict):
        return_color = text_color_dict[requested_color]
    else:
        print(f"ERROR - Invalid color: {requested_color}")
        print(f"Available colors: {list(text_color_dict)}")
        return_color = text_color_dict["default"]
        print(f"Returning default color: {return_color}")

    return return_color
