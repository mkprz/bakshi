# bakshi
A small-office/home-office router configuration wizard

## Dev Notes
### Windows Requirements
1. Python2.6 32-bit (*not 64-bit*)
2. PyClips **unofficial** for Python 2.6 from http://aosekai.net
3. Django (1.6 installed via pip)

### Linux (Debian) Requirements
1. Python 2 (2.6 or 2.7?)
2. Install ```python-dev``` from debian repositories
3. Use python to install pyclips
 ```
 tar xvzf pyclips.tar.gz
 cd pyclips
 python setup.py install
 ```
4. Django (1.6 installed via pip)

### verify devenv
#### commandline
```
python -c "import clips; import django; print(django.get_version())"
```

#### web server
```
python manage.py runserver 8080
```
then browse --> http://localhost:8080

#### models
1. add ```'erc_app'``` to INSTALLED_APPS in erc/erc/settings.py
2. and run the following
```
python manage.py validate
python manage.py sql erc_app
python manage.py syncdb
```

#### sandboxing
if all the above works fine, you can play with the APIs in the sandbox
```
python manage.py shell
```

### Notes on Integrating Django, Python, and the CLIPS Expert System
PyCLIPS is a lib wrapper of CLIPS.
[more info on pyclips: http://prezi.com/5-vp1anq-xu2/pyclips/]

Refer to: http://pyclips.sourceforge.net/manual/pyclips-overview.html
 section 1.2.5 Using external functions in CLIPS

Use pyclips' python-call to make callbacks to python,
setting certain variables when a new message (user query or otherwise)
or a new script command is triggered in the knowledge base

#### Running CLIPS in interactive mode with Django
Refer to: http://pyclips.sourceforge.net/manual/pyclips-overview.html
 section 2.1.2 Functions (Run[limit])

Use clips.run(1) to run the expert system until exactly one(1) rule has been activated.
Check your variables to see if a new message, new script command, or both need to be
processed.


# LICENSE
This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/ or send a letter to:

Creative Commons, 444 Castro Street
Suite 900
Mountain View, California, 94041, USA.
