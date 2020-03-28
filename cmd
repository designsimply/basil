#!env bash

PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

usage="usage: $(basename "$0") command [args]


This script helps with simple command shortcuts. You can add this to your 
path by running or adding the following to a rc file:


	export PATH=\"\$PATH:$PROJECT_DIR\"


docker helper commands 
	up   		Wrapper for docker-compose up
	run 		Wrapper for docker-compose run
	exec  		Wrapper for docker-compose exec
	quickstart	Build and initialize the project 	

web helper commands
	bash       	Start a bash shell in the server
	shell		Start a django shell
	manage.py	Run python manage.py <arguments> in a new container
	createuser 	Create a user. Args: username password [is_staff|is_superuser]
	deleteuser 	Delete a user. Args: username

postgres helper commands
	psql 		Start psql shell in a running container
	pg_scripts	Execute scripts in ./postgresql/scripts/
	pg_backup	Create a backup file of postgres data

"


# Commands here work within the context of this directory. This should 
# temporarily navigate you to the project dir during the script.
cd $PROJECT_DIR


# ---------------------------------------------------------------------------- #
# Take the input command

case "$1" in

# ---------------------------------------------------------------------------- #
# docker helper commands 
up)
	docker-compose up --remove-orphans --no-recreate ${@:2}
	exit 
	;;

run)
	docker-compose run --rm ${@:2}
	exit
	;;

exec)
	docker-compose exec ${@:2}
	exit 
	;;

quickstart):
	docker-compose build
	docker-compose run --rm web manage.py migrate
	echo 'WARNING: creating admin user. Should probably delete.'
	$PROJECT_DIR/script/dev/create_user.sh admin admin is_superuser
	docker-compose up
	exit 
	;;

# ---------------------------------------------------------------------------- #
# web helper commands

bash)
	docker-compose exec web bash
	exit
	;;


shell)
	docker-compose exec web python manage.py shell
	exit
	;;


manage.py)
	docker-compose exec web manage.py ${@:2} 2> /dev/null
	exitcode=$?
	if [[ $exitcode == 1 ]]
	then
		echo "No container web found, executing with 'run'"
		docker-compose run --rm web manage.py ${@:2}
	fi
	exit
	;;

createuser)
	$PROJECT_DIR/scripts/dev/create_user.sh ${@:2}
	exit
	;;

deleteuser)
	$PROJECT_DIR/scripts/dev/delete_user.sh ${@:2}
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


pg_backup)
	# TODO: parameterize path
	outdir_host=${PROJECT_DIR}'/postgres/untracked_backups'
 	outdir_docker='/mnt/backups'

	if [ ! -d "$outdir_host" ]; then
	  # Control will enter here if $DIRECTORY doesn't exist.
	  echo "Creating backup directory $outdir_host"
	  mkdir $outdir_host
	fi	

	# pgdump_2019-10-09T21:02:26.backup
	now=$(date +'%Y-%m-%dT%H:%M:%S')
	fn='pg_dump_'$now'.backup'
	echo "Backup file: $fn"

	fp=${outdir_docker}'/'${fn}
	echo "Backup filepath: $fp"

	psql_cmd='pg_dump -U $POSTGRES_USER -d $POSTGRES_DB > '$fp
	docker-compose exec postgres bash -c "$psql_cmd"

	exit
	;;

# ---------------------------------------------------------------------------- #
# defaults

*) printf "illegal option: $1\n\n" >&2
	echo "$usage" >&2
	exit 1
	;;

esac

echo "done!"
