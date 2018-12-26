# Slack Announce  
Tools for sending messages to a Slack channel via the Slack API. Created for my personal use.

## slackAnnounce.py  

*Description:*

This script is for sending notification messages to Slack via webhooks. Send arbitrary messages as your bot user, send expected downtime, or server up notifications.


Before this will work, you will need to do the following…
1. Get a Slack webhook url. _(More info at: https://api.slack.com/incoming-webhooks)_
2. Rename _slack_config_example.py_ –> _slack_config.py_
3. Add the following information to _slack_config.py_
    - Your Slack webhook url
    - Slack webhook url to send messages to yourself
    - The default username you want to send messages as
    - Slack channel to send messages to by default
    - Slack channel to send messages to when you are developing/testing/debugging
4. Verify that _.gitignore_ lists _*config.py_ as an ignored file and that slack_config.py will not be pushed to git. This should already be set up properly for you.
  

*Required arguments:*

`  -m, --message '<message>'` _Message to send to the channel._
- `'up'` _will send a pre-formatted message stating the server is back up. Default color: (good/green)_
- `'down <number> <time unit>'` _(ex.'down 20 min') will send a pre-formatted message that the server will be going down for maintenance for that amount of time. Default color: (warn/yellow)_
- Any other message will be sent as-is. Default color: (info/gray)
  
*Optional arguments:*

`  -h, --help`  _Show help message and exit_  
`  -c, --color <color>`  _Color for message. Color Options: gray/info (default), green/good, yellow/warn, red/danger, purple_  
`  -d, --debug`  _Enable debug mode. Send message to test channel and show json output in console._  
`  --dry`  _Enable dryrun mode. Message will not be sent._  
`  -r, --room <room>`  _Slack channel room to send the message to._  
`  -t, --title <title>`  _Set a message title._
