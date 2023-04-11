VENV=venv
export VENV
PYTHON=python3
export PYTHON
venv: $(VENV)/bin/activate

$(VENV)/bin/activate: requirements.txt
	test -d $(VENV) || $(PYTHON) -m venv $(VENV)
	. $(VENV)/bin/activate; pip3 install  --ignore-installed -Ur requirements.txt
	touch $(VENV)/bin/activate

init: venv
	. $(VENV)/bin/activate

test: init
	. $(VENV)/bin/activate ; $(PYTHON) manage.py test --pattern="*test*" 
	
run: venv
	. $(VENV)/bin/activate ; find -iname "*.pyc" -delete; $(PYTHON) manage.py migrate && $(PYTHON) manage.py runserver 0.0.0.0:8000

makemigrations: init
	. $(VENV)/bin/activate ; $(PYTHON) manage.py makemigrations

migrate: init
	. $(VENV)/bin/activate ; $(PYTHON) manage.py migrate

migrate_fake: init
	. $(VENV)/bin/activate ; $(PYTHON) manage.py migrate --fake; $(PYTHON) manage.py createcachetable

migrate_one_fake: init
	. $(VENV)/bin/activate ; $(PYTHON) manage.py migrate $(appname) ${migration_name} --fake createcachetable

migrate_reverse: init
	. $(VENV)/bin/activate ; $(PYTHON) manage.py migrate $(appname) ${migration_name}
	
#./run-make.sh migrate_reverse appname=app migration_name=0001_initial
	
execute: venv
	. $(VENV)/bin/activate; $(command)

createsuperuser: venv
	. $(VENV)/bin/activate; $(PYTHON) manage.py createsuperuser

collectstatic: init
	. $(VENV)/bin/activate ; $(PYTHON) manage.py collectstatic --noinput

clean:
	rm -rf $(VENV)
	find -iname "*.pyc" -delete

startapp: init
	. $(VENV)/bin/activate ; $(PYTHON) manage.py startapp $(appname)
#./run-make.sh startapp appname=machine_learning

dumpdata: init
	. $(VENV)/bin/activate ; $(PYTHON) manage.py dumpdata --exclude auditlog.logentry --exclude custom_logger --exclude auth.permission --exclude contenttypes --natural-foreign > db.json

loaddata: init
	. $(VENV)/bin/activate ; $(PYTHON) manage.py loaddata db.json

shell:init
	. $(VENV)/bin/activate ; $(PYTHON) manage.py shell



.PHONY: clean execute

