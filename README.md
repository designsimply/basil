# basil

Some sort of collection of things. A tiny empire of links, if you will. 🌱


## Getting Started

1. Install [Docker](https://docs.docker.com/docker-for-mac/install/) and 
	[docker-compose](https://docs.docker.com/compose/install/).
1. Build the docker images `docker-compose build`
1. Run the Django migrations for the database `docker-compose run --rm webserver manage.py migrate`
1. Create a user, can use this handy script `/webserver/scripts/create_user.sh me strongpassword`
1. Start the containers `docker-compose up` (or `cmd up`)
1. Go to [localhost:8000](http://localhost:8000) to view!
