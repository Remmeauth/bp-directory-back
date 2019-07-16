# Block producers directory back-end

Directory of block producers based around ``Remme Protocol``.

* [Development](#development)

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
