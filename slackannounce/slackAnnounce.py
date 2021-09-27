#!/usr/bin/env python3
import sys
import os.path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import argparse
from slackannounce import config
from slackannounce import slackutils


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Send messages to slack channel. Capable of sending custom "
        "messages, maintenance up/down messages."
    )
    parser.add_argument(
        "-c",
        "--color",
        dest="color",
        metavar="<color>",
        default=None,
        required=False,
        action="store",
        help="The color for message. Options: info (default), "
        "green/good, orange/warn, red/danger, purple",
    )
    parser.add_argument(
        "-d",
        "--debug",
        dest="debug",
        default=False,
        required=False,
        action="store_true",
        help="Enable debug mode. Send message to test channel.",
    )
    parser.add_argument(
        "--dry",
        dest="dryrun",
        default=False,
        required=False,
        action="store_true",
        help="Enable dryrun mode. Message will not be sent.",
    )
    parser.add_argument(
        "-m",
        "--message",
        dest="message",
        metavar="<message>",
        default=None,
        required=True,
        action="store",
        help="The message to send to the channel.",
    )
    parser.add_argument(
        "-r",
        "--channel",
        dest="channel",
        metavar="<channel>",
        default=None,
        required=False,
        action="store",
        help="Slack channel room to send the message to.",
    )
    parser.add_argument(
        "-t",
        "--title",
        dest="title",
        metavar="<title>",
        default=None,
        required=False,
        action="store",
        help="Set a message title.",
    )
    return parser.parse_args()


def set_message(args, **kwargs):
    _message = args.message or kwargs.get("message") or None
    _title = args.title or kwargs.get("title") or None
    _color = args.color or kwargs.get("color") or None

    if args.message is None:
        raise slackutils.SlackException(f"No message given: {args}")

    if args.message.startswith("up"):
        title = "Announcement: Server is up"
        message = "The server is back up!"
        color = slackutils.TextColors.good
    elif args.message.startswith("down "):
        downtime = " ".join(args.message.split(" ")[1:])
        title = "Announcement: Server going down"
        message = (
            "The server is going down for maintenance.\n"
            f"Exepected downtime is about {downtime}."
        )
        color = slackutils.TextColors.warning
    elif _message.startswith("serverupdate"):
        _m_list = _message.split(" ")
        software = _m_list[1]
        title = f"{software} Update Available"
        message = " ".join(_m_list[2:]).replace("\\n", "\n")
        color = slackutils.TextColors.blue
    else:
        title = args.title or config.DEFAULT_TITLE
        message = args.message
        color = args.color or slackutils.TextColors.info

    json_attachments = {
        "fallback": title,
        "color": color,
        "title": title,
        "text": message,
    }

    return json_attachments


def set_channel_and_webhook_url(args):
    if args.dryrun:
        args.debug = True

    if args.channel == "me":
        channel = None
        webhook_url = config.SLACK_WEBHOOK_URL_ME
    elif args.debug:
        channel = config.DEBUG_SLACK_ROOM
        webhook_url = config.SLACK_WEBHOOK_URL
    else:
        channel = config.DEFAULT_SLACK_ROOM
        webhook_url = config.SLACK_WEBHOOK_URL

    if channel is not None and not channel.startswith("#"):
        channel = "#" + channel

    return channel, webhook_url


def send_slack_message(args):
    json = set_message(args)
    channel, webhook_url = set_channel_and_webhook_url(args)
    slack = slackutils.SlackSender(
        webhook_url=webhook_url,
        channel=channel,
        user=config.DEFAULT_SLACK_USER,
        json_attachments=json,
        debug=args.debug,
        dryrun=args.dryrun,
    )
    slack.send()


def main():
    args = parse_arguments()
    send_slack_message(args)


if __name__ == "__main__":
    main()
