import time
from slackclient import SlackClient
import requests
import argparse
import config
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--message', default="hoge", type=str,  help='message')
    parser.add_argument('--app', default="hoge", type=str,  help='message')
    parser.add_argument('--endpoint', default="hoge", type=str,  help='message')
    parser.add_argument('--channel', default="hoge", type=str,  help='message')
    parser.add_argument('--token', default="hoge", type=str,  help='message')
    args = parser.parse_args()

    headers = {'Content-Type': 'application/json'}
    try:
        app = requests.get("{{}/app/{}".format(config.DOCKER_REPOGITORY, args.app)).json()
        requests.put("{}endpoints/{}".format(config.MARATHON_URL, args.endpoint), json={"version": app["version"]}, headers=headers)
    except:
        app = {"name": ""}
    sc = SlackClient(args.token)
    sc.rtm_connect()
    sc.rtm_send_message(channel=args.channel, message="{} デプロイしましたです〜".format(app["name"]))
