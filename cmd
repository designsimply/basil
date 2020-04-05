#!env bash

set -e

PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

usage="usage: $(basename "$0") command [args]


This script helps with simple command shortcuts. You can add this to your 
path by running or adding the following to a rc file:


	export PATH=\"\$PATH:$PROJECT_DIR\"


helper commands 
	
	alias 		Create useful aliases in your terminal

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
	backup		Create a backup file of postgres data. Usage: cmd pg_backup
	restore		Restore from backup. Usage: cmd pg_restore database/untracked_backups/<filename>

"


# Commands here work within the context of this directory. This should 
# temporarily navigate you to the project dir during the script.
cd $PROJECT_DIR


# ---------------------------------------------------------------------------- #
# Take the input command

case "$1" in

alias)
	source $PROJECT_DIR/.aliases
	echo "Created Aliases $PROJECT_DIR/.aliases"
	;;

# ---------------------------------------------------------------------------- #
# docker helper commands 
up)
	docker-compose up --remove-orphans --no-recreate ${@:2}
	;;

run)
	docker-compose run --rm ${@:2}
	;;

exec)
	docker-compose exec ${@:2}
	;;

quickstart):
	echo '----------------------------'
	echo 'Build Images'
	echo '----------------------------'
	docker-compose build

	echo '----------------------------'
	echo 'Start Images'
	echo '----------------------------'
	docker-compose up -d web
	# wait for started
	docker-compose exec web wait_for_database.sh

	echo '----------------------------'
	echo 'Run Migrations'
	echo '----------------------------'
	docker-compose exec web manage.py migrate

	echo '----------------------------'
	echo 'Create Admin User'
	echo '----------------------------'
	echo 'WARNING: creating admin user. Should probably delete.'
	docker-compose exec web bash -c 'scripts/create_user.sh admin admin superuser 2> /dev/null'

	echo '----------------------------'
	echo 'Restore Database'
	echo '----------------------------'
	echo 'INFORMATION ONLY'
	echo 'restore database using the following command if you have a backup'
	echo 'cmd restore database/untracked_backups/<filename>'

	echo '----------------------------'
	echo 'Collectstatic'
	echo '----------------------------'	
	docker-compose exec web manage.py collectstatic --no-input

	echo '----------------------------'
	echo 'Restart Images Attached'
	echo '----------------------------'	
	docker-compose stop web
	docker-compose up web

	;;

# ---------------------------------------------------------------------------- #
# web helper commands

bash)
	docker-compose exec web bash
	;;


shell)
	docker-compose exec web manage.py shell
	;;


manage.py)
	docker-compose exec web manage.py ${@:2} 2> /dev/null
	exitcode=$?
	if [[ $exitcode == 1 ]]
	then
		echo "No container web found, executing with 'run'"
		docker-compose run --rm web manage.py ${@:2}
	fi
	;;

createuser)
	docker-compose exec web scripts/create_user.sh ${@:2}
	;;

deleteuser)
	docker-compose exec web scripts/delete_user.sh ${@:2}
	;;

# ---------------------------------------------------------------------------- #
# postgres helper commands

psql)
    docker-compose exec db bash -c 'psql -U $POSTGRES_USER -d $POSTGRES_DB'
	;;


pg_scripts)
	echo 'NOT IMPLEMENTED'
	exit 1
	FILES=postgres/scripts/*
	for fp in $FILES
	do
		echo "Executing: $fp"

		fp_docker=/opt/scripts/$(basename $fp)    
		psql_cmd='psql -U $POSTGRES_USER -d $POSTGRES_DB -f '$fp_docker
	    docker-compose exec postgres bash -c "$psql_cmd"

	done		
	;;


backup)
	echo '-----------------------'
	echo 'Postgres Backup'
	echo '-----------------------'

	out_dir_host=${PROJECT_DIR}'/database/untracked_backups'
 	out_dir_guest='/mnt/backups'

	if [ ! -d "$out_dir_host" ]; then
	  # Control will enter here if $DIRECTORY doesn't exist.
	  echo "Creating backup directory $out_dir_host"
	  mkdir $out_dir_host
	fi	

	out_filename=$(basename $2)
	if [[ "$out_filename" == "" ]] # not provided
	then 
		# pgdump_2019-10-09T21:02:26.backup
		now=$(date +'%Y-%m-%dT%H:%M:%S')
		out_filename='pg_dump_'$now'.backup'
	fi
	echo "Backup file: $out_filename"

	out_filepath_guest=${out_dir_guest}/${out_filename}
	echo "Backup filepath: $out_filepath_guest"

	name='basil_db_1'
	started_db=false
	if [[ "$(docker ps -f "name=$name" --format '{{.Names}}')" == "" ]]
	then
		started_db=true
		docker-compose up -d db
	fi

	# https://mkyong.com/database/backup-restore-database-in-postgresql-pg_dumppg_restore/
	psql_cmd='pg_dump -U $POSTGRES_USER -d $POSTGRES_DB --clean --blobs --verbose --format=c --file='$out_filepath_guest	
	docker-compose exec db bash -c "$psql_cmd"

	if [[ $started_db ]]
	then
		docker-compose stop db
	fi
	;;

restore)
	echo '-----------------------'
	echo 'Postgres Restore'
	echo '-----------------------'

	in_dir_host=${PROJECT_DIR}'/database/untracked_backups'
	in_dir_guest='/mnt/backups'

	in_filepath_host=$2
	in_filename=$(basename $2)
	in_filepath_guest=${in_dir_guest}/$in_filename

	echo "Backup file: $in_filename"
	echo "Backup host location: $in_filepath_host"
	echo "Backup guest location: $in_filepath_guest"

	name='basil_db_1'
	started_db=false
	if [[ "$(docker ps -f "name=$name" --format '{{.Names}}')" == "" ]]
	then
		started_db=true
		docker-compose up -d db
	fi

	psql_cmd='pg_restore -U $POSTGRES_USER -d $POSTGRES_DB --verbose '$in_filepath_guest	
	docker-compose exec db bash -c "$psql_cmd"

	if [[ $started_db ]]
	then
		docker-compose stop db
	fi
	;;


# ---------------------------------------------------------------------------- #
# defaults

*) printf "illegal option: $1\n\n" >&2
	echo "$usage" >&2
	exit 1
	;;

esac
