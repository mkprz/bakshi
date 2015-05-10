#WARNING
This readme is out of date. Django has been replaced with Pyramid. The Django source code has been preserved under src/django-root while the pyramid version lives next door at src/pyramid-root. The Pyramid version is a complete functioning version of this system while the Django version is not however, i have not yet tested building the dev-env (startenv.sh) and running the Pyramid application under this folder structure.

# bakshi
A small-office/home-office router configuration wizard

## Build Dev Environment
Run erc/startenv.sh to build 32bit python2.6 and pyclips from source.
The script will also create a virtualenv named "ev" and install the pyclips and django1.6 modules locally to the "ev" environment.

```
cd erc
./startenv.sh
```

## Dev Notes
I have not had luck using pyclips with 64bit python and many google searches will lead down the path to compiling pyclips with python2.7 but they often end-up buggy. Playing it safe here and sticking to 32bit python2.6. Using virtualenv to keep system default python in place and out of the way.


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
