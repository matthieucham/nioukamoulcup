#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py flush --no-input
# zinnia special case
python manage.py makemigrations zinnia

python manage.py migrate
python manage.py collectstatic --noinput --clear

if [[ ! -f ".db_preloaded" ]]; then
  echo "Preloading data"
  #pg_restore --host $SQL_HOST --port $SQL_PORT --username "nioukamoulcupuser" --dbname "nioukamoulcup" --no-password  --verbose "nioukamoulcup.backup.2020-05-08.tar"
  python manage.py loaddata ligue1/fixtures/ligue12018.json
  touch ".db_preloaded"
fi

exec "$@"