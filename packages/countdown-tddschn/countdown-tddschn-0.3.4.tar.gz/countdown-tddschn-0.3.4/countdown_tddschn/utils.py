#!/usr/bin/env python3

from cmath import e
from email import message
from typing import Any, Callable
from pync import notify  # type: ignore
import time
from .classes import NotifyOptions
from . import logger


def call_args_in_subprocess(args: list[str]):
    """call args in subprocess"""
    import subprocess
    subprocess.run(args)


def say(text: str):
    """speak text with macos say"""
    import subprocess
    from shutil import which
    for tts_command in ['say', 'espeak']:
        if which(tts_command):
            try:
                subprocess.run([tts_command], input=text.encode())
            except Exception as e:
                logger.error(f'Failed to run {tts_command} <<< "{e}"')
                logger.exception(e)
            break
    # subprocess.run(['say', text])


def pync_notify(message: str, title: str = 'Countdown'):
    """notify with pync"""
    notify(message, title=title)


def no_notify():
    """no notify"""
    pass


notify_options_dict = {
    NotifyOptions.say: say,
    NotifyOptions.pync: pync_notify,
    NotifyOptions.none: no_notify
}


def simple_countdown_notify(length: int,
                            interval: int,
                            notify: Callable[[str], Any] = say,
                            times_up: str = 'Time is up!'):
    """notify user with notify every interval seconds"""
    for i in range(length, 0, -interval):
        # notify(f"{i} seconds left")

        # notify user the remaining minutes

        notify(f'{i // 60} minutes left')
        time.sleep(interval)
    notify(times_up)
