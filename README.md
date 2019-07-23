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

### Block producer

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

## Development

Clone the project with the following command:

```bash
$ git clone https://github.com/Remmeauth/block-producers-directory-back.git
$ cd block-producers-directory-back
```

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
