sqlfunc
=======

Clever stuff with SQL in __doc__

Features
--------

- In-memory database (Sqlite)
- Pre-process parameters
- Post-process returned data
- User definded functions

Example
-------

.. code:: python

    >>> from sqlfunc import sqlsetup, sqlfunc, singlevalue, rowtodict, sqludf
    >>>
    >>> sqlsetup('''
    ...     CREATE TABLE users (username TEXT UNIQUE NOT NULL, password TEXT NOT NULL);
    ... ''')
    >>> @sqlfunc()
    ... add_user(username=None, password=lambda pw: bcrypt(pw)):
    ...     ''' INSERT OR IGNORE INTO users (username, password)
    ...         VALUES (:username, :password);
    ...     '''
    ...
    >>> add_user('root', 'super secret 123')
    1
    >>> add_user('guest', 'guest')
    1
    >>> @sqlfunc(post=singlevalue)
    ... def number_of_users():
    ...     ''' SELECT count(*) FROM users;
    ...     '''
    ...
    >>> number_of_users()
    2
    >>> @sqlfunc(post=rowtodict)
    ... def list_users():
    ...     ''' SELECT username, coolness(username) as coolness FROM users;
    ...     '''
    ...
    >>> @sqludf
    ... def coolness(username):
    ...     if 'root' == username: return 99
    ...     return -1
    ...
    >>> list_users()
    [{'username': 'root', 'coolness': 99}, {'username': 'guest', 'coolness': -1}]
    >>> @sqlfunc(post=lambda row: verify(row[0]), onerror=False)
    ... def login(username=None, password=None):
    ...     ''' SELECT password FROM users WHERE password=:password;
    ...     '''
    ...
    >>> login('root', 'wrong password')
    False


This library is MIT licensed.
