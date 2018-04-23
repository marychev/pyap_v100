    clone git@bitbucket.org:marychev/pyap_v1.0.0.git
    cd pyap_v1.0.0
    virtualenv --python=python3 venv
	source venv/bin/activate
	cd ~/projects/pyap_v1.0.0/pyap/
	pip install -r requirements.txt
	python manage.py collectstatic --noinput
	python manage.py makemigrations
	python manage.py migrate
	python manage.py runserver
	
#  Развертывание проекта 

`pyap_v1.0.0` - название проекта используется как пример


Скачать или клонировать себе проект ``git@bitbucket.org:marychev/pyap_v1.0.0.git``
Подготовка папок для проекта
    
    cd ~/projects
    mkdir pyap_v1.0.0
    cd pyap_v1.0.0
    
проверяем `ls`. Должны быть следующие директории 
* app 
* pyap 
* theme


Ставим виртуальное окружение. Активируем.

	virtualenv --python=python3 venv
	source venv/bin/activate


Устанавливаем Джанго и все необходимые зависимости. Входим в папку где лежит файл `manage.py`.
	
	 cd ~/projects/pyap_v1.0.0/pyap/
	 pip install -r requirements.txt


По умолчанию установливается база `SQLite` `pyap_v100` в проект 
	
	python manage.py collectstatic --noinput
	python manage.py makemigrations
	python manage.py migrate

Проект создан! Проверяем `python manage.py runserver`. 
Запускаем локальный сервер и переходим на страницу в `http://localhost:8000/`. 
	

[I]Заполним проект дефолтными данными

	python manage.py createsuperuser
 		name: `superuser`
 		emal: `superuser@mail.ru`
 		password: `pyap_81086`

 	# [!]Эти команды применить раза 2-3. Пока не прекратятся ошибки
  	python manage.py loaddata users/fixtures/init.json
  	python manage.py loaddata home/fixtures/init.json
    python manage.py loaddata site_info/fixtures/init.json
    python manage.py loaddata settings_template/fixtures/init.json
    python manage.py loaddata include_area/fixtures/init.json
    python manage.py loaddata advertising/fixtures/init.json
    python manage.py loaddata gallery/fixtures/init.json
    python manage.py loaddata catalog/fixtures/init.json
    python manage.py loaddata product/fixtures/init.json
    python manage.py loaddata page/fixtures/init.json
    python manage.py loaddata blog/fixtures/init.json
    
    python manage.py loaddata menu/fixtures/init.json
    python manage.py loaddata order/fixtures/init.json


Проверяем `python manage.py runserver`.


Создадим базу данных `xxx` и настроем `postgres` для проекта

	sudo apt-get update
	sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib 
	
	# Если нужен `postgis`
	# sudo apt-get install postgis gdal-bin	

	sudo -u postgres psql
	postgres=# 
		CREATE DATABASE xxx;
		CREATE USER xxx WITH PASSWORD 'xxx';
		ALTER ROLE xxx SET client_encoding TO 'utf8';
		ALTER ROLE xxx SET default_transaction_isolation TO 'read committed';
		ALTER ROLE xxx SET timezone TO 'UTC';
		GRANT ALL PRIVILEGES ON DATABASE xxx TO xxx;
		\q


Меняем настройку подключения к Базе в `~/projects/dervek.ru/pyap/pyap/settings.py`
```
...
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'xxx',
        'USER': 'xxx',
        'PASSWORD': 'xxx',
        'HOST': 'localhost',
        'PORT': '',
    }
}
...
```
	
	python manage.py migrate


[I]Заполним проект дефолтными данными
	
	# ... создаем суперпользователя и приминяем фикстуры ...


Проверяем `python manage.py runserver`.

# Если сервер


## GIT / BITBACKET 
	
	cd ~/projects/pyap_v1.0.0

	git config --global user.name "Mihail"
	git config --global user.email pyapmail@gmail.com
	git config --global core.pager 'less -r'

	git init
	git add *
	git commit -m 'Hello World!'
	
	# --settings
	git remote add origin git@bitbucket.org:marychev/pyap_v1.0.0.git
	git push -u origin master


#### TRY/EXCEPT 

1.`Error: That port is already in use.`
	
	fuser -k 8000/tcp 


# ----      ---- #
  --- [pYAp] --- 
# ----      ---- #



