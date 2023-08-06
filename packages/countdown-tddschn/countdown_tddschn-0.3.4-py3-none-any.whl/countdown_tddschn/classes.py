#!/usr/bin/env python3

from enum import Enum


class NotifyOptions(str, Enum):
    """Notify options"""
    say = 'say'
    pync = 'pync'
    none = 'none'
