#!/usr/bin/env python3

from os import times
from countdown_tddschn.utils import simple_countdown_notify, notify_options_dict
from countdown_tddschn.classes import NotifyOptions
import typer
from typer import Argument, Option
import daemon

app = typer.Typer()

DEFAULT_COUNTDOWN_LENGTH = 60 * 25
DEFAULT_COUNTDOWN_NOTIFY_INTERVAL = 60 * 5
DEFAULT_POMODORO_LENGTH = 60 * 25
DEFAULT_POMODORO_NOTIFY_INTERVAL = 60 * 5
DEFAULT_POMODORO_BREAK_LENGTH = 60 * 5


def length_option(l: int = DEFAULT_COUNTDOWN_LENGTH):
    return Option(l, '--length', '-l', help='Time to countdown in seconds')


def interval_option(i: int = DEFAULT_COUNTDOWN_NOTIFY_INTERVAL):
    return Option(i,
                  '--interval',
                  '-i',
                  help='Time between notifications in seconds')


def notify_option(n: NotifyOptions = NotifyOptions.say):
    return Option(n, '--notify', '-n', help='Notify options')


def break_length_option(l: int = DEFAULT_POMODORO_BREAK_LENGTH):
    return Option(l, '--break-length', '-bl', help='Time to break in seconds')


def is_break_option(b: bool = False):
    return Option(b, '--is-break', '-b', help='Is break?')


@app.command('c')
@app.command()
def countdown(length: int = length_option(),
              interval: int = interval_option(),
              notify: NotifyOptions = notify_option()):
    """Countdown with notify"""
    with daemon.DaemonContext():
        simple_countdown_notify(length, interval, notify_options_dict[notify])


@app.command('p')
@app.command('pomodoro')
def pomodoro_countdown(
        length: int = length_option(DEFAULT_POMODORO_LENGTH),
        interval: int = interval_option(DEFAULT_POMODORO_NOTIFY_INTERVAL),
        break_length: int = break_length_option(),
        is_break: bool = is_break_option(),
        notify: NotifyOptions = notify_option()):
    """Pomodoro with countdown and notify"""
    with daemon.DaemonContext():
        if is_break:
            simple_countdown_notify(
                break_length,
                interval,
                notify_options_dict[notify],
                times_up='Break is over, get back to work!')
        else:
            simple_countdown_notify(length,
                                    interval,
                                    notify_options_dict[notify],
                                    times_up='Go take a break. You eared it!')


if __name__ == "__main__":
    app()
