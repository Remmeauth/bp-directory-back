# Block producers directory back-end

Directory of block producers based around ``Remme Protocol``.

* [API](#api)
  * [Authentication](#authentication)
  * [User](#user)
  * [Block producer](#block-producer)
* [Development](#development)
* [Production](#production)

## API

### Authentication

* `POST | /authentication/token/obtaining/` - obtain `JWT token` for existing user by his email and password.

##### Request parameters 

| Arguments  | Type    | Required | Description    |
| :--------: | :-----: | :------: | -------------- |
| email      | String  | Yes      | User e-mail.   |
| password   | String  | Yes      | User password. |

```bash
$ curl -v -X POST -H "Content-Type: application/json" -d \
     '{"username_or_email":"dmytro.striletskyi@gmail.com","password":"dmytro.striletskyi.1337"}' \
      http://localhost:8000/authentication/token/obtaining/ | python -m json.tool
{
    "token": "eyJ0e....eyJ1c2VyX2....NzZ0sVpa5..."
}
```

* `POST | /authentication/token/refreshing/` - refresh `JWT token` for existing user by previously obtained token.

##### Request parameters 

| Arguments | Type   | Required | Description     |
| :-------: | :----: | :------: | --------------- |
| token     | String | Yes      | User JWT token. |

```bash
$ curl -v -X POST -H "Content-Type: application/json" -d '{"token":"eyJ0e....eyJ1c2VyX....NzZ..."}' \
      http://localhost:8000/authentication/token/refreshing/ | python -m json.tool
{
    "token": "eyJ0e....eyJ1c2VyX2....sOx4S9zpC..."
}
```

* `POST | /authentication/token/verification/` - check if `JWT token` token is valid.

##### Request parameters 

| Arguments | Type   | Required | Description     |
| :-------: | :----: | :------: | --------------- |
| token     | String | Yes      | User JWT token. |

```bash
$ curl -v -X POST -H "Content-Type: application/json" -d '{"token":"eyJ0e....eyJ1c2VyX2....sOx4S9zpC..."}' \
      http://localhost:8000/authentication/token/verification/ | python -m json.tool
{
    "token": "eyJ0e....eyJ1c2VyX2....sOx4S9zpC..."
}
```

Returns token and status code `200` if valid. Otherwise, it will return a `400` status code as well as an error 
identifying why the token was invalid.

### User

* `POST | /users/registration/` - register a user with email and password.

##### Request parameters 

| Arguments  | Type    | Required | Description    |
| :--------: | :-----: | :------: | -------------- |
| email      | String  | Yes      | User e-mail.   |
| password   | String  | Yes      | User password. |

```bash
$ curl -X POST -H "Content-Type: application/json" \
      -d '{"email":"dmytro.striletskyi@gmail.com","username":"dmytro.striletskyi","password":"dmytro.striletskyi.1337"}' \
      http://localhost:8000/users/registration/ | python -m json.tool
{
    "result": "User has been created."
}
```

##### Known errors

| Argument  | Level                      | Error message                                      | Status code |
| :-------: | :------------------------: | -------------------------------------------------- | :---------: |
|  -        | General execution          | User with specified e-mail address already exists. | 400         |
|  email    | Input arguments validation | This field is required.                            | 400         |
|  password | Input arguments validation | This field is required.                            | 400         |

* `GET | /users/` - get user from token.

##### Request parameters 

```bash
$ curl -H "Content-Type: application/json" \
      -H "Authorization: JWT eyJ0e....eyJ1c2VyX2....sOx4S9zpC..." \
      http://localhost:8000/users/ | python -m json.tool
{
    "result": {
        "email": "dmytro.striletskyi@gmail.com"
    }
}
```

* `DELETE | /users/{username}/` - delete user by username.

##### Request parameters 

| Arguments | Type   | Required | Description    |
| :-------: | :----: | :------: | -------------- |
| username  | String | Yes      | User username. |

```bash
$ curl -X DELETE -H "Content-Type: application/json" \
      -H "Authorization: JWT eyJ0e....eyJ1c2VyX2....sOx4S9zpC..." \
      http://localhost:8000/users/dmytro.striletskyi/ | python -m json.tool
{
    "result": "User has been deleted."
}
```

##### Known errors

| Argument | Level                      | Error message                                                       | Status code |
| :------: | :------------------------: | ------------------------------------------------------------------- | :---------: |
| username | Input arguments validation | User with specified username does not exists.                       | 400         |
| username | Input arguments validation | User has no authority to delete this account by specified username. | 400         |

* `POST | /users/email/` - change user e-mail by username.

##### Request parameters

| Arguments | Type   | Required | Description      |
| :-------: | :----: | :------: | ---------------- |
| username  | String | Yes      | User username.   |
| new_email | String | Yes      | New user e-mail. |

```bash
$ curl -X POST -d '{"new_email":"dmytro.striletskyi.1337@gmail.com"}' \
      -H "Content-Type: application/json" \
      -H "Authorization: JWT eyJ0e....eyJ1c2VyX2....sOx4S9zpC..." \
      http://localhost:8000/users/dmytro.striletskyi/email/ | python -m json.tool
{
    "result": "E-mail has been changed."
}
```

##### Known errors

| Argument  | Level                      | Error message                                 | Status code |
| :-------: | :------------------------: | --------------------------------------------- | :---------: |
| username  | Input arguments validation | User with specified username does not exists. | 400         |
| new_email | Input arguments validation | This field is required.                       | 400         |

* `POST | /users/password/` - change user password.

##### Request parameters

| Arguments    | Type   | Required | Description        |
| :----------: | :----: | :------: | ------------------ |
| old_password | String | Yes      | Old user password. |
| new_password | String | Yes      | New user password. |

```bash
$ curl -X POST -d '{"old_password":"dmytro.striletskyi.1337", "new_password":"dmytro.1337"}' \
      -H "Content-Type: application/json" \
      -H "Authorization: JWT eyJ0e....eyJ1c2VyX2....sOx4S9zpC..." \
      http://localhost:8000/users/dmytro.striletskyi/password/ | python -m json.tool
{
    "result": "Password has been changed."
}
```

##### Known errors

| Argument     | Level                      | Error message                                      | Status code |
| :----------: | :------------------------: | -------------------------------------------------- | :---------: |
| -            | General execution          | User with specified e-mail address does not exist. | 400         |
| -            | General execution          | The specified user password is incorrect.          | 400         |
| old_password | Input arguments validation | This field is required.                            | 400         |
| new_password | Input arguments validation | This field is required.                            | 400         |

* `POST | /users/password/recovery` - request password recovery for an existing user by his e-mail address. Send the recovery link to the e-mail address.

##### Request parameters

| Arguments | Type   | Required | Description  |
| :-------: | :----: | :------: | ------------ |
| email     | String | Yes      | User e-mail. |

```bash
$ curl -X POST -d '{"email":"dmytro.striletskyi@gmail.com"}' \
      -H "Content-Type: application/json" \
      http://localhost:8000/users/password/recovery | python -m json.tool
{
    "result": "Recovery link has been sent to the specified e-mail address."
}
```

##### Known errors

| Argument | Level                      | Error message                                      | Status code |
| :------: | :------------------------: | -------------------------------------------------- | :---------: |
| -        | General execution          | User with specified e-mail address does not exist. | 400         |
| email    | Input arguments validation | This field is required.                            | 400         |

* `POST | /users/password/recovery/{user_identifier}` - send a new password to an existing user who previously requested a password recovery.

##### Request parameters

| Arguments       | Type   | Required | Description      |
| :-------------: | :----: | :------: | ---------------- |
| user_identifier | String | Yes      | User identifier. |

```bash
$ curl -X POST -H "Content-Type: application/json" \
      http://localhost:8000/users/password/recovery/dd76b112f590494fb76e4954ee50961a/ | python -m json.tool
{
    "result": "New password has been sent to e-mail address."
}
```

| Argument | Level             | Error message                                              | Status code |
| :------: | :---------------: | ---------------------------------------------------------- | :---------: |
| -        | General execution | User with specified e-mail address does not exist.         | 400         |
| -        | General execution | Recovery password has been already sent to e-mail address. | 400         |

### Block producer

* `GET | /block-producers/{block_producer_identifier}/` - get block producer by its identifier.

##### Request parameters 

| Arguments                 | Type    | Required | Description                   |
| :-----------------------: | :-----: | :------: | ----------------------------- |
| block_producer_identifier | Integer | Yes      | Identifier of block producer. |

```bash
$ curl http://localhost:8000/block-producers/2/ -H "Content-Type: application/json" | python -m json.tool
{
    "result": {
        "facebook_url": "https://www.facebook.com/bpcanada",
        "full_description": "# About Us\n\nFounded by a team of serial tech entrepreneurs, block producer Canada is headquartered in Montreal, Canada and is backed by reputable Canadian financial players. We believe that BP.IO will fundamentally change our economic and social systems and as such we are deeply committed to contribute to the growth of the ecosystem.",
        "github_url": "https://github.com/bpcanada",
        "id": 2,
        "linkedin_url": "https://www.linkedin.com/in/bpcanada",
        "location": "San Francisco, USA",
        "logo_url": "",
        "medium_url": "https://medium.com/@bpcanada",
        "name": "Block producer Canada",
        "reddit_url": "https://reddit.com/@bpcanada",
        "short_description": "Leading Block Producer - founded by a team of serial tech entrepreneurs, headquartered in Canada",
        "slack_url": "https://slack.com/bpcanada",
        "status": "active",
        "steemit_url": "https://steemit.com/@bpcanada",
        "telegram_url": "https://t.me/bpcanada",
        "twitter_url": "https://twitter.com/bpcanada",
        "user": {
            "email": "tony.stark@gmail.com",
            "id": 2,
            "is_active": true,
            "is_staff": false,
            "is_superuser": false,
            "last_login": null,
            "username": "tony.stark"
        },
        "user_id": 2,
        "website_url": "https://bpcanada.com",
        "wikipedia_url": "https://wikipedia.com/bpcanada"
    }
}
```

##### Known errors

| Argument  | Level             | Error message                                            | Status code |
| :-------: | :---------------: | -------------------------------------------------------- | :---------: |
| -         | General execution | Block producer with specified identifier does not exist. | 400         |

* `GET | /block-producers/` - get all block producers.

```bash
$ curl http://localhost:8000/block-producers/ -H "Content-Type: application/json" | python -m json.tool
{
    "result": [
        {
            "facebook_url": "https://www.facebook.com/bpusa",
            "full_description": "# About Us\n\nFounded by a team of serial tech entrepreneurs, block producer USA is headquartered in San Francisco, USA and is backed by reputable American financial players. We believe that BP.IO will fundamentally change our economic and social systems and as such we are deeply committed to contribute to the growth of the ecosystem.",
            "github_url": "https://github.com/bpusa",
            "id": 3,
            "linkedin_url": "https://www.linkedin.com/in/bpusa",
            "location": "San Francisco, USA",
            "logo_url": "",
            "medium_url": "https://medium.com/@bpusa",
            "name": "Block producer USA",
            "reddit_url": "https://reddit.com/@bpusa",
            "short_description": "Leading Block Producer - founded by a team of serial tech entrepreneurs, headquartered in USA",
            "slack_url": "https://slack.com/bpusa",
            "status": "active",
            "steemit_url": "https://steemit.com/@bpusa",
            "telegram_url": "https://t.me/bpusa",
            "twitter_url": "https://twitter.com/bpusa",
            "user": {
                "email": "tony.stark@gmail.com",
                "id": 2,
                "is_active": true,
                "is_staff": false,
                "is_superuser": false,
                "last_login": null,
                "username": "tony.stark"
            },
            "user_id": 2,
            "website_url": "https://bpusa.com",
            "wikipedia_url": "https://wikipedia.com/bpusa"
        },
        ...
    ]
}
```

* `PUT | /block-producers/` - create a block producer.

##### Request parameters 

| Arguments         | Type   | Required | Description                                         |
| :---------------: | :----: | :------: | --------------------------------------------------- |
| name              | String | Yes      | Name of the block producer.                         |
| website_url       | String | Yes      | Reference to the block producer website.            |
| location          | String | No       | Location of the block producer.                     |
| short_description | String | Yes      | Short description about the block producer.         |
| full_description  | String | No       | Full detailed description about the block producer. |
| logo_url          | String | No       | Reference to the block producer logotype.           |
| linkedin_url      | String | No       | Reference to the Linkedin.                          |
| twitter_url       | String | No       | Reference to the Twitter.                           |
| medium_url        | String | No       | Reference to the Medium.                            |
| github_url        | String | No       | Reference to the GitHub.                            |
| facebook_url      | String | No       | Reference to the Facebook.                          |
| telegram_url      | String | No       | Reference to the Telegram.                          |
| reddit_url        | String | No       | Reference to the Reddit.                            |
| slack_url         | String | No       | Reference to the Slack.                             |
| steemit_url       | String | No       | Reference to the Steemit.                           |
| wikipedia_url     | String | No       | Reference to the Wikipedia.                         |

```bash
$ curl -X PUT http://localhost:8000/block-producers/ \
     -H "Content-Type: application/json" \
     -H "Authorization: JWT eyJ0e....eyJ1c2VyX2....sOx4S9zpC..." \
     -d $'{
  "name": "Block Producer USA",
  "website_url": "https://bpusa.com",
  "location": "San Francisco, USA",
  "short_description": "Leading Block Producer - founded by a team of serial tech entrepreneurs, headquartered in USA",
  "linkedin_url": "https://www.linkedin.com/in/bpusa"
}' | python -m json.tool
{
    "result": {
        "facebook_url": "",
        "full_description": "",
        "github_url": "",
        "id": 6,
        "linkedin_url": "https://www.linkedin.com/in/bpusa",
        "location": "San Francisco, USA",
        "logo_url": "",
        "medium_url": "",
        "name": "Block Producer USA",
        "reddit_url": "",
        "short_description": "Leading Block Producer - founded by a team of serial tech entrepreneurs, headquartered in USA",
        "slack_url": "",
        "steemit_url": "",
        "telegram_url": "",
        "twitter_url": "",
        "user": {
            "email": "dmytro.striletskyi@gmail.com",
            "id": 5,
            "is_active": true,
            "is_staff": false,
            "is_superuser": false,
            "last_login": null,
            "username": "dmytro.striletskyi"
        },
        "user_id": 5,
        "website_url": "https://bpusa.com",
        "wikipedia_url": ""
    }
}
```

##### Known errors

| Argument          | Level                      | Error message                                      | Status code |
| :---------------: | :------------------------: | -------------------------------------------------- | :---------: |
| -                 | General execution          | User with specified e-mail address does not exist. | 400         |
| name              | Input arguments validation | This field is required.                            | 400         |
| website_url       | Input arguments validation | This field is required.                            | 400         |
| short_description | Input arguments validation | This field is required.                            | 400         |

* `POST | /block-producers/{block_producer_identifier}/` - update block producer information.

##### Request parameters 

| Arguments                 | Type    | Required | Description                                         |
| :-----------------------: | :-----: | :------: | --------------------------------------------------- |
| block_producer_identifier | Integer | Yes      | Identifier of block producer.                       |
| name                      | String  | No       | Name of the block producer.                         |
| website_url               | String  | No       | Reference to the block producer website.            |
| location                  | String  | No       | Location of the block producer.                     |
| short_description         | String  | No       | Short description about the block producer.         |
| full_description          | String  | No       | Full detailed description about the block producer. |
| logo_url                  | String  | No       | Reference to the block producer logotype.           |
| linkedin_url              | String  | No       | Reference to the Linkedin.                          |
| twitter_url               | String  | No       | Reference to the Twitter.                           |
| medium_url                | String  | No       | Reference to the Medium.                            |
| github_url                | String  | No       | Reference to the GitHub.                            |
| facebook_url              | String  | No       | Reference to the Facebook.                          |
| telegram_url              | String  | No       | Reference to the Telegram.                          |
| reddit_url                | String  | No       | Reference to the Reddit.                            |
| slack_url                 | String  | No       | Reference to the Slack.                             |
| steemit_url               | String  | No       | Reference to the Steemit.                           |
| wikipedia_url             | String  | No       | Reference to the Wikipedia.                         |

```bash
$ curl -X POST http://localhost:8000/block-producers/2/ \
     -H "Content-Type: application/json" \
     -H "Authorization: JWT eyJ0e....eyJ1c2VyX2....sOx4S9zpC..." \
     -d $'{
  "name": "Block producer USA",
  "website_url": "https://bpusa.com",
  "location": "San Francisco, USA",
  "short_description": "Leading Block Producer - founded by a team of serial tech entrepreneurs, headquartered in USA",
  "full_description": "# About Us\\n\\nFounded by a team of serial tech entrepreneurs, block producer USA is headquartered in San Francisco, USA and is backed by reputable American financial players. We believe that BP.IO will fundamentally change our economic and social systems and as such we are deeply committed to contribute to the growth of the ecosystem.",
  "linkedin_url": "https://www.linkedin.com/in/bpusa"
}' | python -m json.tool
{
    "result": "Block producer has been updated."
}
```

##### Known errors

| Argument | Level             | Error message                                            | Status code |
| :------: | :---------------: | -------------------------------------------------------- | :---------: |
| -        | General execution | User with specified e-mail address does not exist.       | 400         |
| -        | General execution | Block producer with specified identifier does not exist. | 400         |

* `GET | /block-producers/search/?phrase=block%20producer%20usa` - search block producers by phrase.

##### Request parameters 

| Arguments | Type   | Required | Description                                         |
| :-------: | :----: | :------: | --------------------------------------------------- |
| phrase    | String | Yes      | Phrase by which you can search for block producers. |

```bash
$ curl http://localhost:8000/block-producers/search/?phrase=block%20producer%20usa \
     -H "Content-Type: application/json" | python -m json.tool
{
    "result": [
        {
            "facebook_url": "https://www.facebook.com/bpusa",
            "full_description": "# About Us\n\nFounded by a team of serial tech entrepreneurs, block producer USA is headquartered in San Francisco, USA and is backed by reputable American financial players. We believe that BP.IO will fundamentally change our economic and social systems and as such we are deeply committed to contribute to the growth of the ecosystem.",
            "github_url": "https://github.com/bpusa",
            "id": 3,
            "linkedin_url": "https://www.linkedin.com/in/bpusa",
            "location": "San Francisco, USA",
            "logo_url": "",
            "medium_url": "https://medium.com/@bpusa",
            "name": "Block producer USA",
            "reddit_url": "https://reddit.com/@bpusa",
            "short_description": "Leading Block Producer - founded by a team of serial tech entrepreneurs, headquartered in USA",
            "slack_url": "https://slack.com/bpusa",
            "steemit_url": "https://steemit.com/@bpusa",
            "telegram_url": "https://t.me/bpusa",
            "twitter_url": "https://twitter.com/bpusa",
            "user": {
                "email": "tony.stark@gmail.com",
                "id": 2,
                "is_active": true,
                "is_staff": false,
                "is_superuser": false,
                "last_login": null,
                "username": "tony.stark"
            },
            "user_id": 2,
            "website_url": "https://bpusa.com",
            "wikipedia_url": "https://wikipedia.com/bpusa"
        }
    ]
}
```

* `POST | /block-producers/{block_producer_identifier}/avatars/` - upload block producer avatar.

##### Request parameters 

| Arguments                 | Type    | Required | Description                   |
| :-----------------------: | :-----: | :------: | ----------------------------- |
| block_producer_identifier | Integer | Yes      | Identifier of block producer. |

```bash
$ curl -X POST http://localhost:8000/block-producers/2/avatars/ \
      -F "file=@/Users/dmytrostriletskyi/Desktop/default-user-logotype.png" \
      -H "Authorization: JWT eyJ0e....eyJ1c2VyX2....sOx4S9zpC..." | python -m json.tool
{
    "result": "Block producer avatar has been uploaded."
}
```

## Development

Clone the project with the following command:

```bash
$ git clone https://github.com/Remmeauth/block-producers-directory-back.git
$ cd block-producers-directory-back
```

The project requires the following environment variables:

```bash
export SENDGRID_API_KEY='PZqNQgmk9dJcw.yJ0eNzZ0sVpa5NzZ0sVpa5.eyJ1c2VyX2eyJ1c2VyX2'
```

Instead of default values above, request workable and real ones from [@dmytrostriletskyi](https://github.com/dmytrostriletskyi) or [@yelaginj](https://github.com/yelaginj).

To build the project, use the following command:

```bash
$ docker-compose -f docker-compose.develop.yml build
```

To run the project, use the following command. It will start the server and occupate current terminal session:

```bash
$ docker-compose -f docker-compose.develop.yml up
```

If you need to enter the bash of the container, use the following command:

```bash
$ docker exec -it block-producers-directory-back bash
```

Clean all containers with the following command:

```bash
$ docker rm $(docker ps -a -q) -f
```

Clean all images with the following command:

```bash
$ docker rmi $(docker images -q) -f
```

## Production

To build the project, use the following command:

```bash
$ docker build -t block-producers-directory-back . -f Dockerfile.production
```

To run the project, use the following command. It will start the server and occupate current terminal session:

```bash
$ docker run -p 8000:8000 -e PORT=8000 -e DEBUG=False -e SECRET_KEY=t5dcw2llz8eshqp \
      -e DATABASE_URL='sqlite:///db.sqlite3' -e ENVIRONMENT=REVIEW-APP \
      -v $PWD:/block-producers-directory-back \
      --name block-producers-directory-back block-producers-directory-back
```
