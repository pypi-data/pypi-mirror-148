import logging
import os
import threading
import time
import uuid
from datetime import datetime
from typing import Optional

from firelog._event import Event
from firelog._ping import Ping

import requests

__EVENTS_COLLECTION = "events"
__PINGS_COLLECTION = "pings"
__FIRELOG_ENV_URL = "FIRELOG_URL"
__FIRELOG_ENV_SECRET = "FIRELOG_SECRET"

_database_url: Optional[str] = None
_secret: Optional[str] = None

_default_app: Optional[str] = None
_default_view: Optional[str] = None
_default_event_type: Optional[str] = None

async_enabled = False
disable_logging = False


def init(url: Optional[str] = None, secret: Optional[str] = None, is_async: bool = False) -> bool:
    global async_enabled
    async_enabled = is_async

    if url is None:
        url = os.getenv(__FIRELOG_ENV_URL)

    if secret is None:
        secret = os.getenv(__FIRELOG_ENV_SECRET)

    if secret is None:
        logging.warning("No secret provided -> firelog unauthorized mode")

    if url is None:
        global disable_logging
        disable_logging = True
        logging.warning("FireLog could not find credentials.")
        return False

    global _database_url, _secret
    _database_url = url
    _secret = secret

    return True


def set_defaults(app: Optional[str] = None, view: Optional[str] = None, event_type: Optional[str] = None):
    global _default_app, _default_view, _default_event_type
    _default_app = app
    _default_view = view
    _default_event_type = event_type


def log_event(event: Event):
    guid = str(uuid.uuid1())[:5]
    ts_str = event.timestamp.strftime("%Y-%m-%d-%H-%M-%S-%f")
    event_id = f"{ts_str}-{guid}"

    try:
        r = requests.put(
            f"{_database_url}/{__EVENTS_COLLECTION}/{event.app}/{event.view}/{event_id}.json?{_get_auth()}",
            json=event.to_json())

        if r.ok:
            return

        error = r.json()["error"]
        logging.warning(f"Could not send ping ({r.status_code}): {error}")
    except Exception as ex:
        logging.warning(f"Could not log event: {ex}")


def log_event_async(event: Event):
    threading.Thread(target=log_event, args=(event,)).start()


def log(app: Optional[str] = None, view: Optional[str] = None, event_type: Optional[str] = None,
        timestamp: Optional[datetime] = None, **params):
    if disable_logging:
        return

    if app is None:
        app = _default_app

    if view is None:
        view = _default_view

    if event_type is None:
        event_type = _default_event_type

    if async_enabled:
        log_event_async(Event(app, view, event_type, timestamp, **params))
    else:
        log_event(Event(app, view, event_type, timestamp, **params))


def send_ping(ping: Ping):
    if disable_logging:
        return

    try:
        r = requests.put(f"{_database_url}/{__PINGS_COLLECTION}/{ping.app}/{ping.view}.json?{_get_auth()}",
                         json=ping.to_json())

        if r.ok:
            return

        error = r.json()["error"]
        logging.warning(f"Could not send ping ({r.status_code}): {error}")
    except Exception as ex:
        logging.warning(f"Could not send ping: {ex}")


def start_pinging(interval: float = 60.0):
    def ping_loop():
        while True:
            ping = Ping(_default_app, _default_view)
            send_ping(ping)
            time.sleep(interval)

    threading.Thread(target=ping_loop, daemon=True).start()


def _get_auth() -> str:
    if _secret is not None:
        return f"auth={_secret}"
    else:
        return ""
