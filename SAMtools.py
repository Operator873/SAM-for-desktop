import requests
from requests_oauthlib import OAuth1
import json
import re


with open('wikis.txt') as file:  # read in wikis
    WIKIS = json.load(file)

def xmit(site, creds, payload, method):  # This handles the post/get requests

    agent = {
        'User-Agent': 'Steward/Sysop Action Module v1.0.0 (Python3.7) contact@873gear.com',
    }

    if method == "post":
        return requests.post(site, headers=agent, data=payload, auth=creds).json()
    elif method == "get":
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


def spambot(SAM, values):  # Block a spambot quickly with few params
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
        reason = "Spambot ([[m:GS|Global sysop]] action)"
    else:
        reason = "Spambot"

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


def block(SAM, values):  # Execute a typical block
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


def hardblock(SAM, values):  # Execute a hard block
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


def lock(SAM, values):  # Lock the provided account
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


def unlock(SAM, values):  # Unlock the provided account
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

    return response


def gblock(SAM, values):  # Globally blocks the provided IP
    response = {}

    creds = get_creds(SAM)

    api = "https://meta.wikimedia.org/w/api.php"

    get_csrf = getCSRF(api, creds, 'csrf')
    if get_csrf['result'] == "Success":
        token = get_csrf['token']
    else:
        response['status'] = "Failed"
        response['message'] = get_csrf['message']
        return response

    block = {
        "action": "globalblock",
        "format": "json",
        "target": values['target'],
        "expiry": adjust(values['duration']),
        "reason": values['reason'],
        "alsolocal": True,
        "token": token
    }

    gblock = xmit(api, creds, block, "post")

    if 'error' in gblock:
        response['status'] = "Failed"
        response['message'] = gblock['error']['info']
    elif 'globalblock' in gblock:
        response['status'] = "Success"
        response['message'] = gblock['globalblock']['user'] + " was globally blocked until " + gblock['globalblock']['expiry']
    else:
        response['status'] = "Unk"
        response['message'] = gblock

    return response


def reblock(SAM, values):  # Modifies an existing block
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

    if values['notpa'] is True:

        do_block = {
            "action": "block",
            "user": values['target'],
            "expiry": adjust(values['duration']),
            "reason": reason,
            "token": token,
            "nocreate": "",
            "autoblock": "",
            "reblock":"",
            "format": "json"
        }
    else:
        do_block = {
            "action": "block",
            "user": values['target'],
            "expiry": adjust(values['duration']),
            "reason": reason,
            "token": token,
            "allowusertalk": "",
            "nocreate": "",
            "autoblock": "",
            "reblock": "",
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

def massblock(values):  # todo write or eliminate massblock
    # Is this needed?
    pass


def masslock(values):  # todo write or eliminate masslock
    # Is this needed?
    pass


def massgblock(values):  # todo write or eliminate massgblock
    # Is this needed?
    pass


def blockinfo(creds, values):  # Determines if an account or IP is currently blocked
    response = {}

    try:
        api = WIKIS[values['project']]
    except Exception as e:
        response['status'] = "Failed"
        response['message'] = values['project'] + " is not known. Please add via AddApi on main menu."
        return response

    query = {
        'action':"query",
        'format': "json",
        'list': "blocks",
        'bkusers': values['target']
    }

    data = xmit(api, creds, query, 'get')

    if len(data['query']['blocks']) > 0:
        response['status'] = "blocked"
        response['message'] = data['query']['blocks'][0]
        response['project'] = values['project']
    else:
        response['status'] = "notblocked"

    return response


def addapi(SAM, values):  # Adds a project/api to the wikis list
    response = {}

    try:
        api = WIKIS[values['project']]
    except:
        api = None

    if api is not None:
        response['status'] = "Failed"
        response['message'] = "Project already known. (" + api + ")"
    else:
        WIKIS[values['project']] = values['api']

        with open('wikis.txt', 'w') as wikis:
            wikis.write(json.dumps(WIKIS))

        response['status'] = "Success"
        response['message'] = values['project'] + " was added with api url: " + values['api']

    return response


def get_creds(SAM):  # Formats OAuth credentials for requests

    AUTH = OAuth1(
        SAM['OAuth']['consumer_token'],
        SAM['OAuth']['consumer_secret'],
        SAM['OAuth']['access_token'],
        SAM['OAuth']['access_secret']
    )

    return AUTH


def adjust(duration):  # Adjusts expiry format to allow for stupid and fat fingers
    adjust = re.sub(r"([0-9]+([0-9]+)?)", r" \1 ", duration)
    adjusted = re.sub(' +', ' ', adjust).strip()

    return adjusted