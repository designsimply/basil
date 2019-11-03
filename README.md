# basil
Some sort of collection of things. A tiny empire of links, if you will. 🌱


## Installation


1. Install [Docker](https://docs.docker.com/docker-for-mac/install/) and 
	[docker-compose](https://docs.docker.com/compose/install/).
1. run `docker-compose build` then `docker-compose up`.


## Database Management

When modifying the models you will need to run 

```
cmd manage makemigrations
```

To apply the migrations to the postgres database you run

```
cmd manage migrate
```