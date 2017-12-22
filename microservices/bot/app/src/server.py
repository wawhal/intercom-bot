from src import app
from flask import jsonify, request
from intercom.client import Client
from giphypop import translate
import requests
import json
import os
import urllib.request

adminId = os.environ['ADMIN_ID']
accessToken = os.environ['ACCESS_TOKEN']
intercom = Client(personal_access_token=accessToken)
dataUrl = "http://data.hasura/v1/query"
giphyApiKey = os.environ['GIPHY_API_KEY']

@app.route("/")
def main():
    return "Intercom bot is running"

@app.route("/bot", methods=['POST'])
def bot():
    KEY = str("secret")
    DATA = request.get_data()
    input = json.loads(DATA.decode())
    topic = input["topic"]
    convId = input["data"]["item"]["id"]
    userId = input["data"]["item"]["user"]["id"]
    msgTime = input["created_at"]
    assignee = input["data"]["item"]["assignee"]["type"]
    print (input)
    if((topic == "conversation.user.replied" or topic == "conversation.user.created") and assignee == "nobody_admin"):
        firstMsgTime = fetchMessageTime(convId)
        if (firstMsgTime == -1):
            storeToDb(convId, msgTime)

    if (topic == "conversation.admin.replied"):
        firstMsgTime = fetchMessageTime(convId)
        if (firstMsgTime > 0):
            print ("Unreplied Message")
            if ((msgTime - firstMsgTime) <= 200):
                print ("Replied under 200 seconds")
                gif = getGif()
                sendNoteWithImage(convId)
                updateAsReplied(convId)
    return "OK"

def storeToDb(convId, msgTime):
    headers = {
        "Content-type": "application/json",
        "X-Hasura-Role": "admin",
        "X-Hasura-User-Id":"1"
    }

    payload = {
        "type": "insert",
        "args": {
            "table": "intercom_messages",
            "objects": [
                {
                    "conversation_id": convId,
                    "time": msgTime,
                    "replied": False
                }
            ]
        }
    }

    r = requests.post(dataUrl, data=json.dumps(payload), headers=headers)
    print ("Hasura Insert Resp =====")
    print (r.json)
    print ("========================")
    respObj = r.json()


def fetchMessageTime(convId):
    headers = {
        "Content-type": "application/json",
        "X-Hasura-Role": "admin",
        "X-Hasura-User-Id": "1"
    }

    payload = {
        "type": "select",
        "args": {
            "table": "intercom_messages",
            "columns": [
                "time",
                "replied"
            ],
            "where": {
                "conversation_id": {
                    "$eq": convId
                }
            }
        }
    }

    r = requests.post(dataUrl, data=json.dumps(payload), headers=headers)
    respObj = r.json()
    if (len(respObj) == 0):
        return -1
    if (respObj[0]["replied"] == True):
        return -2
    return (respObj[0]["time"])


def updateAsReplied(convId):
    headers = {
        "Content-type": "application/json",
        "X-Hasura-Role": "admin",
        "X-Hasura-User-Id": "1"
    }

    payload = {
        "type": "update",
        "args": {
            "table": "intercom_messages",
            "where": {
                "conversation_id": convId,
            },
            "$set": {
                "replied": True
            }
        }
    }

    r = requests.post(dataUrl, data=json.dumps(payload), headers=headers)
    respObj = r.json()
    print (respObj)

def sendNoteWithImage(convId):
    url = "https://api.intercom.io/conversations/" + convId + "/reply"
    bearer = "Bearer " + accessToken
    headers = {
        "Authorization": bearer,
        "Content-type": "application/json",
        "Accept": "application/json"
    }
    gif = getGif()
    payload = {
        "body": "That was fast 👍" ,
        "type": "admin",
        "admin_id": adminId,
        "message_type": "note"
    }
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    respObj = r.json()
    print (respObj)

def getGif():
    text = "awesome"
    url = "http://api.giphy.com/v1/stickers/translate"
    r = requests.get(url=url, params = {"api_key": giphyApiKey, "s": text})
    respObj = r.json()
    print (respObj)
    gifUrl = respObj["data"]["embed_url"]
    return gifUrl
