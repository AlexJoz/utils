import argparse
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from slacker import Slacker


class MyHandler(FileSystemEventHandler):
    def __init__(self, slack_channel):
        self.ch = slack_channel

    def on_created(self, event):
        # slack.chat.post_message('self.ch', event.src_path)
        slack.files.upload(event.src_path, channels=self.ch)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--token', help='api_token from slack')
    parser.add_argument('--ch', help='channel from slack')
    parser.add_argument('--path', help='directory to monitor')

    args = parser.parse_args()
    print('Monitoring directory {} \n Slack token {} \n Slack channel {}'.format(args.path, args.token, args.ch))
    slack = Slacker(args.token)

    event_handler = MyHandler(args.ch)
    observer = Observer()
    observer.schedule(event_handler, path=args.path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
