# PyAp - движок, с открытым исходным кодом для разработки веб-приложений, корпоративных сайтов.

Технологии: Python 3.x, Django<=1.11, Postgres*. 
Разработчикам - движок сократит много недель. 
Административная панель на русском. 

*Pyap* легко расширять, изменять бизнес логику. 

В качестве шаблона был взят бесплатный шаблон интернет магазина.

[Спасибо Bootstrap! и OBAJU E-COMMERCE TEMPLATE!](https://bootstrapious.com/p/obaju-e-commerce-template). 

 
--------------------------------------------------
### Быстрая установка и клонирование движка.

    git clone git@bitbucket.org:marychev/pyap_v100.git    
    cd pyap_v100
    virtualenv --python=python3 venv
    source venv/bin/activate
    
    cd pyap
    pip install -r requirements.txt
    python manage.py runserver 

[Смотрим](http://localhost:8000). 

-------------------------------------------------

# Подробная Установка.

`pyap_v100` - название проекта (заменить на название своего проекта)


Клонировать себе проект.
    
    git@bitbucket.org:marychev/pyap_v100.git
    cd pyap_v100
    
Проверяем `ls`. Должны быть следующие директории: 
- `app`
- `pyap` 
- `theme`



Ставим виртуальное окружение. Активируем.

	virtualenv --python=python3 venv
	source venv/bin/activate


Устанавливаем Джанго и все необходимые зависимости. Входим в папку где лежит файл `manage.py`.
	
	 cd pyap/
	 pip install -r requirements.txt


По умолчанию установливается база `SQLite` `pyap_v100` в проект с тестовыми данными и товарами.
Запускаем проект.
    
    python manage.py runserver
    
Переходим в браузер [localhost:8000](http://localhost:8000). 

## Проект развернут!
---------------------


### Дополнительно...
#### Очистить базу

Можно удалить файл, ``pyap_v100.sqlite``, чтоб полностью очистить базу даных и начать с `0`.
Затем выполнить эти команды.

	python manage.py collectstatic --noinput
	python manage.py makemigrations
	python manage.py migrate
	
Создаем суперпользователя, чтоб войти в админку.	
	
	python manage.py createsuperuser
 		name: `superuser`
 		emal: `superuser@mail.ru`
 		password: `karamba_888`


Проект создан! Проверяем `python manage.py runserver`. 
Запускаем локальный сервер и переходим на страницу в [localhost:8000](http://localhost:8000).  
	

### Заполнить проект текстовыми данными (фикстуры).

 	#[!] Эти команды применить раза 2/3. Если будут ошибки
 	
  	python manage.py loaddata users/fixtures/init.json
  	python manage.py loaddata home/fixtures/init.json
    python manage.py loaddata site_info/fixtures/init.json
    python manage.py loaddata settings_template/fixtures/init.json
    python manage.py loaddata include_area/fixtures/init.json
    python manage.py loaddata advertising/fixtures/init.json
    python manage.py loaddata gallery/fixtures/init.json
    python manage.py loaddata catalog/fixtures/init.json
    python manage.py loaddata page/fixtures/init.json
    python manage.py loaddata blog/fixtures/init.json
    python manage.py loaddata menu/fixtures/init.json
    python manage.py loaddata product/fixtures/init.json
    python manage.py loaddata order/fixtures/init.json
    


Проверяем `python manage.py runserver`.


## Настройка Postgres

Создадим базу данных `xxx` и настроем `postgres` для проекта.

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


Меняем настройку подключения к Базе в `pyap_v1.0.0/pyap/pyap/settings.py`
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


Создаем суперпользователя, чтоб войти в админку.	

	python manage.py createsuperuser
 		name: `superuser`
 		emal: `superuser@mail.ru`
 		password: `karamba_888`

Проверяем `python manage.py runserver`.



