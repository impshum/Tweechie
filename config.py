# Get your Twitter keys from https://apps.twitter.com
consumer_key = 'XXXX'
consumer_secret = 'XXXX'
access_key = 'XXXX-XXXX'
access_secret = 'XXXX'


# Get your Twitch keys from https://dev.twitch.tv
twitch_client_id = 'XXXX'


# List of users to trigger alert
twitch_users = ['insert', 'user', 'names', 'here']


# Sleep time in seconds (30 queries per minute allowed / min 2 seconds)
sleep_timer = 30


# Alert message (KEEP TO THE FORMAT)
# Format = [LIVE STREAM] {USER} started playing {GAME} {@ HOURS AGO}. Join the action with {1234} others on Twitch at {LINK}
alert = "[LIVE STREAM] {} started playing {} {}. Join the action with {} others on Twitch at {}"


# Set to 0 to keep quiet (no output in terminal)
quiet_mode = 0


# Set to 0 to go live
test_mode = 1
