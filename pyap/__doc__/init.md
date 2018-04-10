
### Install the Packages from the Ubuntu Repositories

	sudo apt-get update
	sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib 
	
	# if need postgis
	# sudo apt-get install postgis gdal-bin	

### Create the PostgreSQL Database and User

	sudo -u postgres psql

	postgres=# 
		CREATE DATABASE xxx;
		CREATE USER xxx WITH PASSWORD 'xxxxxxxxxxx';
		ALTER ROLE xxx SET client_encoding TO 'utf8';
		ALTER ROLE xxx SET default_transaction_isolation TO 'read committed';
		ALTER ROLE xxx SET timezone TO 'UTC';
		GRANT ALL PRIVILEGES ON DATABASE xxx TO xxx;


### upgrade pip and install the package by typing:

	sudo -H pip3 install --upgrade pip
	sudo -H pip3 install virtualenv

	python3 -m virtualenv ~/xxx/pyap/venv

	source pyap/venv/bin/activate

	pip install -r requirements.txt
    python manage.py makemigrations
    python manage.py migrate




