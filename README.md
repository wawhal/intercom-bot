# intercom-bot

This is a simple intercom bot that applauds your team members if they reply quickly. This project can also be used as a boilerplate if you want to make intercom bots.

## Prerequisites

1. Intercom workspace
2. [hasura CLI tool](https://docs.hasura.io/0.15/manual/install-hasura-cli.html)

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

- Your intercom bot has been deployed. Whenever someone from your team replies to a lead within 200 seconds, he will be applauded :) 
