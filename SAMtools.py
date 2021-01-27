import sqlite3
import requests
import json
from requests_oauthlib import OAuth1


def xmit(site, creds, payload, method):  # This handles the post/get requests

    AUTH = OAuth1(creds[0], creds[1], creds[2], creds[3])

    if method == "post":
        return requests.post(site, data=payload, auth=AUTH).json()
    elif method == "get":
        return requests.get(site, params=payload, auth=AUTH).json()
    elif method == "authget":
        return connect.get(url, headers=agent, params=payload, auth=AUTH).json()
    else:
        return False


def getCSRF(site, creds, type):  # todo Adapt function for local use
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

def getCreds(name):  # todo Test for local use
    # Setup dbase connection
    db = sqlite3.connect('SAM.db')
    c = db.cursor()

    # Get user credentials and prepare api url for use
    creds = c.execute('''SELECT * from auth where account="%s";''' % name).fetchall()
    db.close()

    if creds is not None:
        return creds
    else:
        return None


def read_dbase(query):
    db = sqlite3.connect('SAM.db')
    c = db.cursor()

    data = c.execute(
        '''SELECT * FROM %s;''' % query
    ).fetchall()

    db.close()

    return data


def check_OAuth():  # todo Write the actual check_OAuth function

    if len(read_dbase('auth')) > 0:
        return True
    else:
        return False


def homewiki():  # Write the actual homewiki function
    return "simplewiki"


def spambot(values):
    work = {}
    if values['target'] != "Fail":
        work['status'] = "Success"
        work['message'] = values['target'] + " was blocked on " + values['project']
    else:
        work['status'] = "Fail"
        work['message'] = "The fail account was entered"

    return work


def lock(values):
    pass


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


def unlock(values):
    pass


def block(values):
    pass


def hardblock(values):
    pass


def addoauth(values):
    pass


def addapi(values):
    pass
