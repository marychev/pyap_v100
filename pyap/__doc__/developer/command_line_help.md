# Данные проекта Premium37.ru


## SERVER
### ssh и данные для доступа
    логин: root/marychev
    пароль: qqy4bqme6f

    ssh root@95.213.236.77
    ssh marychev@95.213.236.77 

[sudo] password for marychev: 

    mmc81086

    ip address
    95.213.236.77
    Маска подсети
    255.255.255.0 
    Шлюз
    95.213.236.1


    email:
    marychevmihail3737@gmail.com

##### после внесения изменений на сервер выполнить команды

    source /home/marychev/premium37/premium37_venv/bin/activate && 
    cd premium37 &&
    python manage.py migrate && 
    python manage.py collectstatic && 
    sudo systemctl restart gunicorn



## DATABASE: POSTGRES

    user:  premium37
    pass: premium37_81086
    
    $ sudo su - postgres 
    $ psql

##### установить все привилегии для пользователя

    grant all privileges on database premium37 to premium37;


##### бэкап базы

    pg_dump -h localhost -U premium37 premium37 > /home/backups/premium37/20171112.sql
    
##### востановление базы (pass: premium37_81086)

    psql -h localhost -U premium37 -d premium37 -f /home/backups/premium37/premium37/20171112.sql



## SITE: PREMIUM37.RU

    admin: admin
    pass: P5a2t6r6o5n5
    admin: marychev
    pass: mmc81086
	
	
    
### MANAGE.PY: команду выполнять из папки где лежит файл ``manage.py`` "pyap/manage.py"

    pip install -r requirements.txt
    python manage.py migrate
    python manage.py makemigrations thumbnail
    

### fixtures
##### По умолчанию нужно хранить в папке fixtures, которую нужно создать внутри каждого приложения.

    python manage.py dumpdata --format=json myapp > myapp/fixtures/initial_data.json

##### Загрузка фикстуры из файла

    python manage.py loaddata myapp/fixtures/myfix.json

###### "выброшено" исключение IntegrityError.
###### исключить таблицы contenttypes и auth.permissions:

    python manage.py dumpdata --exclude auth.permission --exclude contenttypes > db.json


# ... admin panel
    python manage.py createsuperuser ``admin`` ``P5a2t6r6o5n5``
    
    [!]sudo fuser -k 8000 / tcp 
    Это должно уничтожить все процессы, связанные с портом 8000.


## БЕКПА САЙТА / ЗАПОЛНЕНИЕ САЙТА

#### Выгрузка данных json
       
    python manage.py dumpdata --format=json users > users/fixtures/init.json    
    python manage.py dumpdata --format=json site_info > site_info/fixtures/init.json
    python manage.py dumpdata --format=json settings_template > settings_template/fixtures/init.json
    python manage.py dumpdata --format=json include_area > include_area/fixtures/init.json
    python manage.py dumpdata --format=json advertising > advertising/fixtures/init.json
    python manage.py dumpdata --format=json home > home/fixtures/init.json
    python manage.py dumpdata --format=json gallery > gallery/fixtures/init.json
    python manage.py dumpdata --format=json catalog > catalog/fixtures/init.json
    python manage.py dumpdata --format=json product > product/fixtures/init.json
    python manage.py dumpdata --format=json page > page/fixtures/init.json
    python manage.py dumpdata --format=json blog > blog/fixtures/init.json
    
    python manage.py dumpdata --format=json menu > menu/fixtures/init.json
    python manage.py dumpdata --format=json order > order/fixtures/init.json


#### Загрузка данных json
    
    python manage.py loaddata users/fixtures/init.json
    python manage.py loaddata site_info/fixtures/init.json
    python manage.py loaddata settings_template/fixtures/init.json
    python manage.py loaddata include_area/fixtures/init.json
    python manage.py loaddata advertising/fixtures/init.json
    python manage.py loaddata home/fixtures/init.json
    python manage.py loaddata gallery/fixtures/init.json
    python manage.py loaddata catalog/fixtures/init.json
    python manage.py loaddata product/fixtures/init.json
    python manage.py loaddata page/fixtures/init.json
    python manage.py loaddata blog/fixtures/init.json
    
    python manage.py loaddata menu/fixtures/init.json
    python manage.py loaddata order/fixtures/init.json


