#!env bash

usage="usage: $(basename "$0") <command> 


This script helps with simple command shortcuts

general helper commands 
	link_me		Link this cmd to /usr/local/bin/cmd

docker helper commands 
	up          Wrapper for docker-compose up

webserver helper commands
	bash       	Start a bash shell in the server
	shell		Start a django shell
	manage		Run python manage.py <arguments> in a new container

postgres helper commands
	psql 		Start psql shell in a running container
	pg_scripts	Execute scripts in ./postgresql/scripts/

"

# ---------------------------------------------------------------------------- #
# Take the input command

case "$1" in

# ---------------------------------------------------------------------------- #
# docker helper commands 
link_me)
	# get path to this file
	DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
	cmd_source=${DIR}/cmd 

	# get path to directory
	if [ -z ${VIRTUAL_ENV+x} ]; 
		then 
			echo "Not in virtualenv"; 
			exit;
	fi
	echo ${VIRTUAL_ENV};
	bin_path=${VIRTUAL_ENV}/bin;
	cmd_destination=${bin_path}/cmd
	
	ln -s $cmd_source $cmd_destination

	echo "created symlink $cmd_destination to point at $cmd_source"
	exit
	;;

# ---------------------------------------------------------------------------- #
# docker helper commands 
up)
	docker-compose up
	exit 
	;;

# ---------------------------------------------------------------------------- #
# webserver helper commands

bash)
	docker-compose exec webserver bash
	exit
	;;


shell)
	docker-compose exec webserver python manage.py shell
	exit
	;;


manage)
	docker-compose run webserver python manage.py ${@:2}
	exit
	;;

# ---------------------------------------------------------------------------- #
# postgres helper commands

psql)
    docker-compose exec postgres bash -c 'psql -U $POSTGRES_USER -d $POSTGRES_DB'
    exit	    
	;;


pg_scripts)
	FILES=postgres/scripts/*
	for fp in $FILES
	do
		echo "Executing: $fp"

		fp_docker=/opt/scripts/$(basename $fp)    
		psql_cmd='psql -U $POSTGRES_USER -d $POSTGRES_DB -f '$fp_docker
	    docker-compose exec postgres bash -c "$psql_cmd"

	done		
	exit
	;;


# ---------------------------------------------------------------------------- #
# defaults

*) printf "illegal option: $1\n\n" >&2
	echo "$usage" >&2
	exit 1
	;;

esac
