#                         ** --------------- **
#                             Tweechie v1.0
# ----------------------------------------------------------------------
#  /r/impshum wrote this file. As long as you retain this notice you can do
#    whatever you want with this stuff. If we meet some day, and you
#     think this stuff is worth it, you can buy me a beer in return.
#  ---------------------------------------------------------------------

import os
import sys
import json
import time
import mmap
import tweepy
import timeago
import datetime
from halo import Halo
import urllib.request
import dateutil.parser
from config import *


class Colour:
    Green, Red, White, Yellow = '\033[92m', '\033[91m', '\033[0m', '\033[93m'


print(Colour.Yellow + """
╔╦╗╦ ╦╔═╗╔═╗╔═╗╦ ╦╦╔═╗
 ║ ║║║║╣ ║╣ ║  ╠═╣║║╣
 ╩ ╚╩╝╚═╝╚═╝╚═╝╩ ╩╩╚═╝ 1.0
""")

print(Colour.White + 'Checking every {}'.format(int(sleep_timer)), 'seconds\n\nPress Ctrl + C to exit\n')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

dead_count = 0

script_dir = os.path.dirname(__file__)
history_file = 'data/history.txt'
history_path = os.path.join(script_dir, history_file)
preview_file = 'data/preview.jpg'
preview_path = os.path.join(script_dir, preview_file)

def empty_check():
    with open(history_path, 'r+') as f:
        p = f.read(1)
        if not p:
            f.write('-' + '\n')

def nope():
    time.sleep(sleep_timer)

if quiet_mode:
    try:
        spinner = Halo(text='Running', spinner='dots')
        spinner.start()
    except KeyboardInterrupt:
        spinner.stop()

def tweechy(twitch_user):
    with urllib.request.urlopen('https://api.twitch.tv/kraken/streams/' + twitch_user + '?client_id=' + twitch_client_id) as url:
        data = json.loads(url.read().decode())
        if data['stream']:
            if data['stream']['stream_type'] == 'live':
                t = data['stream']['created_at']
                o = t.encode()
                game = data['stream']['game']
                viewers = data['stream']['viewers']
                preview = data['stream']['preview']['large']
                name = data['stream']['channel']['display_name']
                url = data['stream']['channel']['url']

                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-7]
                then = datetime.datetime.strptime(t, "%Y-%m-%dT%H:%M:%SZ")
                started = timeago.format(then, now)

                with open(history_path, 'rb', 0) as f, mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as s, open(history_path, 'a') as fp:
                    if not s.find(o) != -1:
                        fp.write(t + '\n')

                        urllib.request.urlretrieve(preview, preview_path)

                        message = alert.format(
                            name, game, started, viewers, url)

                        if not quiet_mode:
                            print(Colour.Green + message + '\n')

                        if not test_mode:
                            api.update_with_media(preview_path, message)

                    else:
                        if not quiet_mode:
                            print(
                                Colour.Yellow + '{} started playing {} {}'.format(twitch_user, game, started))

        else:
            if not quiet_mode:
                print(Colour.Yellow + '{} is not playing anything'.format(twitch_user))

def main():
    while True:
        try:
            for twitch_user in twitch_users:
                tweechy(twitch_user)
                nope()
        except Exception as e:
            print(Colour.Red + '\n' + str(e))
            print(Colour.White + '\nExiting due to errors\n')
            sys.exit(1)

        except KeyboardInterrupt:
            print(Colour.White + '\nExiting\n')
            sys.exit(1)


if __name__ == '__main__':
    empty_check()
    main()
