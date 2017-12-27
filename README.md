# intercom-bot

## Introduction

This is a simple intercom bot that applauds your team members if they reply quickly. This project can also be used as a boilerplate if you want to make intercom bots. I is a fun bot to boost the support team enthusiasm on Intercom and encourage quick replies.

## How it works

Whenever a message is replied to under 5 minutes, the user gets an internal note saying that they did a fantastic job :-D

### Internal implementation

1. When a user sends a message, it is passed through this webhook by Intercom.
2. The webhook checks the presence of this conversation in the database. If it is present, no action is taken. If not, the conversation ID is inserted into the database along with the timestamp and the replied status.
3. When the team member replies to the conversation, the webhook checks the database if this conversation has been replied to. If it is, no action is taken.
4. If it is not replied to, the time difference is checked. If it is less than 5 minutes, an internal note is sent to that conversation applauding the team member.
5. The conversation is marked as replied in the database.
6. All the data operations are made using the Hasura Data API.

## Deployment Guide

To get the app running, follow these steps:

- Get the project.

```
$ hasura quickstart rishi/intercom-bot
```

- Add your intercom [access token](https://developers.intercom.com/v2.0/reference#personal-access-tokens-1) and [admin id](https://developers.intercom.com/v2.0/reference#viewing-the-current-admin) to secrets (so that you do not have to explicitly write them in your code).

```
$ hasura secret update chatbot.access.token <intercom_access_token>
$ hasura secret update chatbot.admin.id <intercom_admin_id>
```

- Create a [webhook](https://developers.intercom.com/v2.0/reference#webhooks-and-notifications) for your intercom workspace, enter the URL as `https://bot.<cluster-name>.hasura-app.io/bot` (run `hasura cluster status` to find your cluster name). Check all the subscription checkboxes.

- Finally, push the entire project to your cluster.

```
$ git add .
$ git commit -m "First commit"
$ git push hasura master
```

- Your intercom bot has been deployed. Whenever someone from your team replies to a lead within 200 seconds, they will be applauded :)

## How to modify it

This webhook is written in Python using the Flask framework. The source code lives in the `microservices/bot/app/src` directory. If you are familiar with Flask, you can jump right into it by modifying the `server.py` file.

If you are looking for any extra intercom features other than sending messages and sending notes, you might want to look at the intercom API reference.

## Support

If you happen to get stuck anywhere, please feel free to mail me at jaisontj@gmail.com. Also, if you find an error or a bug, you can report an issue [here](https;//github.com/wawhal/intercom-bot/issues)
