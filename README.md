# TNM Neural Network
# Network used to detect categories from text.

Uses:

 - [scikit-learn](http://scikit-learn.org/)
 - [Django](https://www.djangoproject.com/)
 - [Python 2.7+](https://www.python.org/)

## Getting Started
Make sure you have the following installed:

 - Python 2.7+
 - MongoDB 3.0+

Set MONGODB settings in line 83 of file tnm-neural/settings.py
Example:
```sh
_MONGODB_USER = 'tnm-neural'
_MONGODB_PASSWD = '123456'
_MONGODB_HOST = '127.0.0.1'
_MONGODB_NAME = 'classifier'
_MONGODB_DATABASE_HOST = \
    'mongodb://%s:%s@%s/%s' \
    % (_MONGODB_USER, _MONGODB_PASSWD, _MONGODB_HOST, _MONGODB_NAME)
```

You need to install scikit-learn and Django, I recommend using PIP for python
```sh
"If you already have a working installation of numpy and scipy, the easiest way to install scikit-learn is using pip"
pip install -U scikit-learn

pip install django
```

If you are in Windows I recommend installing the numpy and scipy binaries, then run the PIP command.

NumPY -> https://sourceforge.net/projects/numpy/files/
SciPY -> https://sourceforge.net/projects/scipy/files/

## Starting the server
To start the Django server located at `./` execute:
```sh
python manage.py runserver
```