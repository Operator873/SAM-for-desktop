import requests
from requests_oauthlib import OAuth1
import json
import re


with open('wikis.txt') as file:
    WIKIS = json.load(file)

def xmit(site, creds, payload, method):  # This handles the post/get requests

    agent = {
        'User-Agent': 'Steward/Sysop Action Module v1.0.0 (Python3.7) contact@873gear.com',
    }

    if method == "post":
        return requests.post(site, headers=agent, data=payload, auth=creds).json()
    elif method == "get":
        return requests.get(site, headers=agent, params=payload, auth=creds).json()
    elif method == "authget":
        return requests.get(site, headers=agent, params=payload, auth=creds).json()
    else:
        return False


def getCSRF(site, creds, type):  # This handles fetching the appropriate token
    data = {}

    reqtoken = {
        'action': "query",
        'meta': "tokens",
        'format': "json",
        'type': type
    }

    token = xmit(site, creds, reqtoken, "get")

    # Check for errors and return csrf
    if 'error' in token:
        data['result'] = "Error"
        data['message'] = token['error']['info']
    else:
        data['result'] = "Success"
        data['token'] = token['query']['tokens']['%stoken' % type]

    return data


def spambot(SAM, values):
    response = {}

    creds = get_creds(SAM)

    try:
        api = WIKIS[values['project']]
    except Exception as e:
        response['status'] = "Failed"
        response['message'] = values['project'] + " is not known. Please add via AddApi on main menu."
        return response

    get_csrf = getCSRF(api, creds, 'csrf')
    if get_csrf['result'] == "Success":
        token = get_csrf['token']
    else:
        response['status'] = "Failed"
        response['message'] = get_csrf['message']
        return response

    if values['gs'] is True:
        reason = "Spambot ([[m:GS|Global sysop]] action) via SAM"
    else:
        reason = "Spambot via SAM"

    do_block = {
        "action": "block",
        "user": values['target'],
        "expiry": "never",
        "reason": reason,
        "token": token,
        "noemail": "",
        "nocreate": "",
        "reblock": "",
        "autoblock": "",
        "format": "json"
    }

    data = xmit(api, creds, do_block, 'post')

    if 'error' in data:
        response['status'] = "Error"
        response['message'] = data['error']['code'] + " " + data['error']['info']
        return response
    elif 'block' in data:
        response['status'] = "Success"
        response['message'] = data['block']['user'] + " was blocked until " + data['block'][
            'expiry'] + " with reason: " + data['block']['reason']
    else:
        response['status'] = "Unk"
        response['message'] = data

    return response


def block(SAM, values):
    response = {}

    creds = get_creds(SAM)

    try:
        api = WIKIS[values['project']]
    except Exception as e:
        response['status'] = "Failed"
        response['message'] = values['project'] + " is not known. Please add via AddApi on main menu."
        return response

    get_csrf = getCSRF(api, creds, 'csrf')
    if get_csrf['result'] == "Success":
        token = get_csrf['token']
    else:
        response['status'] = "Failed"
        response['message'] = get_csrf['message']
        return response

    if values['gs'] is True:
        reason = values['reason'] + " ([[m:GS|Global sysop]] action)"
    elif values['steward'] is True:
        reason = values['reason'] + " ([[m:Steward|Steward]] action)"
    else:
        reason = values['reason']

    do_block = {
        "action": "block",
        "user": values['target'],
        "expiry": adjust(values['duration']),
        "reason": reason,
        "token": token,
        "allowusertalk": "",
        "nocreate": "",
        "autoblock": "",
        "format": "json"
    }

    data = xmit(api, creds, do_block, 'post')

    if 'error' in data:
        response['status'] = "Error"
        response['message'] = data['error']['code'] + " " + data['error']['info']
        return response
    elif 'block' in data:
        response['status'] = "Success"
        response['message'] = data['block']['user'] + " was blocked until " + data['block']['expiry'] + " with reason: " + data['block']['reason']
    else:
        response['status'] = "Unk"
        response['message'] = data

    return response


def hardblock(SAM, values):
    response = {}

    creds = get_creds(SAM)

    try:
        api = WIKIS[values['project']]
    except Exception as e:
        response['status'] = "Failed"
        response['message'] = values['project'] + " is not known. Please add via AddApi on main menu."
        return response

    get_csrf = getCSRF(api, creds, 'csrf')
    if get_csrf['result'] == "Success":
        token = get_csrf['token']
    else:
        response['status'] = "Failed"
        response['message'] = get_csrf['message']
        return response

    if values['gs'] is True:
        reason = values['reason'] + " ([[m:GS|Global sysop]] action)"
    elif values['steward'] is True:
        reason = values['reason'] + " ([[m:Steward|Steward]] action)"
    else:
        reason = values['reason']

    do_block = {
        "action": "block",
        "user": values['target'],
        "expiry": adjust(values['duration']),
        "reason": reason,
        "token": token,
        "noemail": "",
        "nocreate": "",
        "autoblock": "",
        "format": "json"
    }

    data = xmit(api, creds, do_block, 'post')

    if 'error' in data:
        response['status'] = "Error"
        response['message'] = data['error']['code'] + " " + data['error']['info']
        return response
    elif 'block' in data:
        response['status'] = "Success"
        response['message'] = data['block']['user'] + " was blocked until " + data['block'][
            'expiry'] + " with reason: " + data['block']['reason']
    else:
        response['status'] = "Unk"
        response['message'] = data

    return response


def lock(SAM, values):
    response = {}

    creds = get_creds(SAM)

    api = "https://meta.wikimedia.org/w/api.php"

    get_csrf = getCSRF(api, creds, 'setglobalaccountstatus')
    if get_csrf['result'] == "Success":
        token = get_csrf['token']
    else:
        response['status'] = "Failed"
        response['message'] = get_csrf['message']
        return response

    lockRequest = {
        "action": "setglobalaccountstatus",
        "format": "json",
        "user": values['target'],
        "locked": "lock",
        "reason": values['reason'],
        "token": token
    }

    lock = xmit(api, creds, lockRequest, "post")

    if 'error' in lock:
        response['status'] = "Failed"
        response['message'] = lock['error']['info']
    else:
        response['status'] = "Success"
        response['message'] = values['target'] + " locked."

    return response

def unlock(SAM, values):
    response = {}

    creds = get_creds(SAM)

    api = "https://meta.wikimedia.org/w/api.php"

    get_csrf = getCSRF(api, creds, 'setglobalaccountstatus')
    if get_csrf['result'] == "Success":
        token = get_csrf['token']
    else:
        response['status'] = "Failed"
        response['message'] = get_csrf['message']
        return response

    unlockRequest = {
        "action": "setglobalaccountstatus",
        "format": "json",
        "user": values['target'],
        "locked": "unlock",
        "reason": values['reason'],
        "token": token
    }

    lock = xmit(api, creds, unlockRequest, "post")

    if 'error' in lock:
        response['status'] = "Failed"
        response['message'] = lock['error']['info']
    else:
        response['status'] = "Success"
        response['message'] = values['target'] + " unlocked."


def gblock(values):
    pass


def massblock(values):
    # Is this needed?
    pass


def masslock(values):
    # Is this needed?
    pass


def massgblock(values):
    # Is this needed?
    pass


def addoauth(values):
    pass


def addapi(values):
    pass

def get_creds(SAM):

    AUTH = OAuth1(
        SAM['OAuth']['consumer_token'],
        SAM['OAuth']['consumer_secret'],
        SAM['OAuth']['access_token'],
        SAM['OAuth']['access_secret']
    )

    return AUTH


def adjust(duration):
    adjust = re.sub(r"([0-9]+([0-9]+)?)", r" \1 ", duration)
    adjusted = re.sub(' +', ' ', adjust).strip()

    return adjusted