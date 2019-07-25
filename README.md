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
     '{"email":"dmytro.striletskyi@gmail.com","password":"dmytro.striletskyi.1337"}' \
      http://localhost:8000/authentication/token/obtaining/ | python -m json.tool
{
    "token": "eyJ0e....eyJ1c2VyX2....NzZ0sVpa5..."
}
```   

* `POST | /authentication/token/refreshing/` - refresh `JWT token` for existing user by previously obtained token.

```bash
$ curl -v -X POST -H "Content-Type: application/json" -d '{"token":"eyJ0e....eyJ1c2VyX....NzZ..."}' \
      http://localhost:8000/authentication/token/refreshing/ | python -m json.tool
{
    "token": "eyJ0e....eyJ1c2VyX2....sOx4S9zpC..."
}
```

* `POST | /authentication/token/verification/` - check if `JWT token` token is valid.

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

* `POST | /auth/registration/` - register a user with email and password.

##### Request parameters 

| Arguments  | Type    | Required | Description    |
| :--------: | :-----: | :------: | -------------- |
| email      | String  | Yes      | User e-mail.   |
| password   | String  | Yes      | User password. |

```bash
$ curl -X POST -H "Content-Type: application/json" -d '{"email":"dmytro.striletskyi@gmail.com","password":"dmytro.striletskyi.1337"}' \
      http://localhost:8000/user/registration/ | python -m json.tool
{
    "message": "User has been created.",
    "status_code": 200
}
```

##### Known errors

| Argument  | Level                      | Error message                                      | Status code |
| :-------: | :------------------------: | -------------------------------------------------- | :---------: |
|  -        | General execution          | User with specified e-mail address already exists. | 400         |
|  email    | Input arguments validation | This field is required.                            | 400         |
|  password | Input arguments validation | This field is required.                            | 400         |

* `POST | /user/password/` - change user password.

##### Request parameters

| Arguments    | Type   | Required | Description        |
| :----------: | :----: | :------: | ------------------ |
| old_password | String | Yes      | Old user password. |
| new_password | String | Yes      | New user password. |

```bash
$ curl -X POST -d '{"old_password":"dmytro.striletskyi.1337", "new_password":"dmytro.1337"}' \
      -H "Content-Type: application/json" \
      -H "Authorization: JWT eyJ0e....eyJ1c2VyX2....sOx4S9zpC..." \
      http://localhost:8000/user/password/ | python -m json.tool
{
    "message": "Password has been changed.",
    "status_code": 200
}
```

##### Known errors

| Argument     | Level                      | Error message                                      | Status code |
| :----------: | :------------------------: | -------------------------------------------------- | :---------: |
| -            | General execution          | User with specified e-mail address does not exist. | 400         |
| -            | General execution          | The specified user password is incorrect.          | 400         |
| old_password | Input arguments validation | This field is required.                            | 400         |
| new_password | Input arguments validation | This field is required.                            | 400         |

* `POST | /user/password/recovery` - request password recovery for an existing user by his e-mail address. Send the recovery link to the e-mail address.

##### Request parameters

| Arguments | Type   | Required | Description  |
| :-------: | :----: | :------: | ------------ |
| email     | String | Yes      | User e-mail. |

```bash
$ curl -X POST -d '{"email":"dmytro.striletskyi@gmail.com"}' \
      -H "Content-Type: application/json" \
      http://localhost:8000/user/password/recovery | python -m json.tool
{
    "message": "Recovery link has been sent to the specified e-mail address.",
    "status_code": 200
}
```

##### Known errors

| Argument | Level                      | Error message                                      | Status code |
| :------: | :------------------------: | -------------------------------------------------- | :---------: |
| -        | General execution          | User with specified e-mail address does not exist. | 400         |
| email    | Input arguments validation | This field is required.                            | 400         |

* `POST | /user/password/recovery/{user_identifier}` - send a new password to an existing user who previously requested a password recovery.

##### Request parameters

| Arguments       | Type   | Required | Description      |
| :-------------: | :----: | :------: | ---------------- |
| user_identifier | String | Yes      | User identifier. |

```bash
$ curl -X POST -H "Content-Type: application/json" \
      http://localhost:8000/user/password/recovery/dd76b112f590494fb76e4954ee50961a/ | python -m json.tool
{
    "message": "New password has been sent to e-mail address.",
    "status_code": 200
}
```

| Argument | Level             | Error message                                              | Status code |
| :------: | :---------------: | ---------------------------------------------------------- | :---------: |
| -        | General execution | User with specified e-mail address does not exist.         | 400         |
| -        | General execution | Recovery password has been already sent to e-mail address. | 400         |

### Block producer

* `GET | /block-producers/collection/` - get block producers.

```bash
$ curl http://localhost:8000/block-producers/collection/ -H "Content-Type: application/json" | python -m json.tool
{
    "result": [
        {
            "facebook_url": "https://www.facebook.com/bpcanada",
            "full_description": "# About Us\n\nFounded by a team of serial tech entrepreneurs, block producer Canada is headquartered in Montreal, Canada and is backed by reputable Canadian financial players. We believe that BP.IO will fundamentally change our economic and social systems and as such we are deeply committed to contribute to the growth of the ecosystem.",
            "github_url": "https://github.com/bpcanada",
            "id": 1,
            "linkedin_url": "https://www.linkedin.com/in/bpcanada",
            "location": "Berlin, Germany",
            "logo_url": "",
            "medium_url": "https://medium.com/@bpcanada",
            "name": "Block producer Canada",
            "reddit_url": "https://reddit.com/@bpcanada",
            "short_description": "Leading Block Producer - founded by a team of serial tech entrepreneurs, headquartered in Canada",
            "slack_url": "https://slack.com/bpcanada",
            "steemit_url": "https://steemit.com/@bpcanada",
            "telegram_url": "https://t.me/bpcanada",
            "twitter_url": "https://twitter.com/bpcanada",
            "user_id": 1,
            "website_url": "https://bpcanada.com",
            "wikipedia_url": "https://wikipedia.com/bpcanada"
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
    "message": "Block producer has been created.",
    "status_code": 200
}
```

##### Known errors

| Argument          | Level                      | Error message                                      | Status code |
| :---------------: | :------------------------: | -------------------------------------------------- | :---------: |
| -                 | General execution          | User with specified e-mail address does not exist. | 400         |
| name              | Input arguments validation | This field is required.                            | 400         |
| website_url       | Input arguments validation | This field is required.                            | 400         |
| short_description | Input arguments validation | This field is required.                            | 400         |

* `POST | /block-producers/{block_producer_identifier}/like/` - to like or unlike block producer.

##### Request parameters 

| Arguments                 | Type    | Required | Description                   |
| :-----------------------: | :-----: | :------: | ----------------------------- |
| block_producer_identifier | Integer | Yes      | Identifier of block producer. |

```bash
$ curl -X POST \
      -H "Content-Type: application/json" \
      -H "Authorization: JWT eyJ0e....eyJ1c2VyX2....sOx4S9zpC..." \
      http://localhost:8000/block-producers/2/like/ | python -m json.tool
{
    "message": "Block producer liking has been handled.",
    "status_code": 200
}
```

##### Known errors

| Argument  | Level             | Error message                                            | Status code |
| :-------: | :---------------: | -------------------------------------------------------- | :---------: |
| -         | General execution | User with specified e-mail address does not exist.       | 400         |
| -         | General execution | Block producer with specified identifier does not exist. | 400         |

* `POST | /block-producers/{block_producer_identifier}/comment/` - to comment a block producer.

##### Request parameters 

| Arguments                 | Type    | Required | Description                      |
| :-----------------------: | :-----: | :------: | -------------------------------- |
| block_producer_identifier | Integer | Yes      | Identifier of block producer.    |
| text                      | String  | Yes      | Comment text. Max length is 200. |

```bash
$ curl -X PUT -d '{"text":"Great block producer!"}' \
      -H "Content-Type: application/json" \
      -H "Authorization: JWT eyJ0e....eyJ1c2VyX2....sOx4S9zpC..." \
      http://localhost:8000/block-producers/2/comment/ | python -m json.tool
{
    "message": "Block producer has been commented.",
    "status_code": 200
}
```

##### Known errors

| Argument  | Level                      | Error message                                               | Status code |
| :-------: | :------------------------: | ----------------------------------------------------------- | :---------: |
| -         | General execution          | User with specified e-mail address does not exist.          | 400         |
| -         | General execution          | Block producer with specified identifier does not exist.    | 400         |
| -         | Input arguments validation | This field is required.                                     | 400         |
| -         | Input arguments validation | Ensure this value has at most 200 characters (it has more). | 400         |

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
