import datetime
import json
import random

import jpholiday
import pytz
import requests

import functions_framework


@functions_framework.http
def main_http(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    request_json = request.get_json(silent=True)

    if request_json and 'action' in request_json:
        action = request_json['action']

        if action == "random":
            return random_int()

        if action == "baz":
            return execute("baz")

        if action == "qux":
            return execute("qux")

        return "unknown action: " + action

    return "no action"


def is_holiday(date):
    """
    Check whether a given date is a public holiday or weekend in Japan.
    Returns True if it is, False otherwise.
    """
    if jpholiday.is_holiday(date) or date.weekday() >= 5:
        return True
    else:
        return False


def execute(event):
    """
    Your custom implementation here.
    Code below is just an example
    """

    url = "https://example.com/do"

    now_utc = datetime.datetime.now(tz=pytz.UTC)

    if is_holiday(now_utc):
        return "Today is holiday"

    now_str = now_utc.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    payload = json.dumps({
        "foo": "bar",
        "time": now_str,
        "event": event
    })

    headers = {
        "hello": "world"
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response


def random_int():
    return str(random.randint(1, 7200))
