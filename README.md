# basil

Some sort of collection of things. A tiny empire of links, if you will. 🌱


## Getting Started

Project consists of docker services, web and database, which can be run using docker-compose.

A `cmd` script is used for helpful shortcuts during development. But should not be used in production.


### Quick Start Method

1. Install [Docker](https://docs.docker.com/docker-for-mac/install/) and 
	[docker-compose](https://docs.docker.com/compose/install/).
1. Run `cmd quickstart`
1. Go to [localhost:8000](http://localhost:8000) to view!


### Detailed Start Method

1. Install [Docker](https://docs.docker.com/docker-for-mac/install/) and 
	[docker-compose](https://docs.docker.com/compose/install/).
1. Build docker iamges `docker-compose build`
1. Start containers `docker-compose up web`
1. Open new terminal shell
1. Run database migrations `docker-compose exec web manage.py migrate`
1. (optional) Run database restore with backup file `cmd restore database/untracked_backups/<backup_file>`
1. (optional) Create a user in database. Shortcut: `docker-compose exec web scripts/create_user.sh admin admin superuser` (note: you will want to delete this user before production)
1. Collect static files. `docker-compose exec web manage.py collectstatic --no-input`
1. Go to [localhost:8000](http://localhost:8000) to view!


### Project Structure 

* **database/** : contains Docker build for database
	* **untracked_backups/** : auto generated output for any backup files
	* **Dockerfile** : build script for db service
	* **healthcheck.sh** : script for health check on service
* **web/** : contains Docker build for web server
	* **basil/** : contains Django apps and static content
		* **common/** : shared modules for apps
		* **links/** : links app
		* **templates/** : static django templates
		* **static/** : custom css/js/images other static content
		* **untracked_collectstatic/** : auto generated output from django collectstatic command
	* **web/** : configuration
		* **settings/** : folder contains settings modules for each environment
		* **urls.py** : django url routing 
		* **asgi.py** : ASGI config
		* **wsgi.py** : WSGI config
	* **scripts/** : useful scripts for development, NOT FOR PRODUCTION
	* **bin/** : useful scripts for production, included in container PATH
	* **Dockerfile** : build script for web service
	* **requirements.txt** : version free requirements with description
	* **requirements_freeze.txt** : version fixed requirements	
* **.aliases** : add some helpful aliases for development
* **.env** : environment variables to be overwritten in each service environment
* **.gitignore** : git ignore for project
* **cmd** : bash script with helpful shortcuts for development
* **docker-compose.yml** : docker-compose config for services
* **LICENSE** : project license


