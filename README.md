bakshi
======

router configuration wizard



create python virutal environment:
----------------------------------

# project was originally "Expert Router Configurator" or "erc"
$env_name = erc

pip install virtualenvwrapper
echo "source /usr/local/bin/virtualenvwrapper.sh" > ~/.bash_rc
source ~/.bash_rc
mkvirtualenv $env_name

pip install django

# review package install status
lssitepackages

# verify version
python -c "import django; print(django.get_version())"

django-admin.py startproject django_project
cd django_project

python manage.py startapp ${env_name}_app 

python manage.py runserver 3000


reactivate python virtual environment:
------------------------------------

source ~/.virtualenvs/erc/bin/activate


Integrating Python and Expert System:
------------------------------------

We are using PyCLIPS a lib wrapper of CLIPS.

Refer to: http://pyclips.sourceforge.net/manual/pyclips-overview.html
 section 1.2.5 Using external functions in CLIPS

We use python-call to make callbacks to our python program, setting certain variables when a new message (question to the user or otherwise) or a new script command is triggered in the knowledge base


Running CLIPS in interactive mode with Django:
----------------------------------------------

Refer to: http://pyclips.sourceforge.net/manual/pyclips-overview.html
 section 2.1.2 Functions (Run[limit])

We use clips.run(1) to run the expert system until one(1) rule has been activated.
We check our variables to see if a new message, new script command, or both need to be preocessed.

++++++++++++++++++++++++++++++++++++++++++++++
LICENSE

This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/ or send a letter to:

Creative Commons, 444 Castro Street
Suite 900
Mountain View, California, 94041, USA.
++++++++++++++++++++++++++++++++++++++++++++++
