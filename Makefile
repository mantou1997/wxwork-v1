env="dev"

freeze:
	pip freeze > requirements.txt
superuser:
	python manage.py createsuperuser
make:
	python manage.py makemigrations account
	python manage.py migrate
check_env:
	python manage.py check_env
use:
	python utils/env.py use --params $(env)
clean:
	rm -rf db.sqlite3
	rm -rf account/migrations
	rm -rf wxtags/migrations
