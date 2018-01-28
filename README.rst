sqlfunc
=======

Clever stuff with SQL in __doc__

.. image:: https://snyk.io/test/github/digitalmensch/sqlfunc/badge.svg
   :target: https://snyk.io/test/github/digitalmensch/sqlfunc

.. image:: https://travis-ci.org/digitalmensch/sqlfunc.svg?branch=master
   :target: https://travis-ci.org/digitalmensch/sqlfunc

.. image:: https://coveralls.io/repos/github/digitalmensch/sqlfunc/badge.svg?branch=master
   :target: https://coveralls.io/github/digitalmensch/sqlfunc?branch=master

Features
--------

- In-memory or file-backed database (Sqlite)
- Post-process returned data
- User definded functions

Example
-------

Given this:

.. code:: python
        
    ''' CREATE TABLE IF NOT EXISTS users (
            userid   INTEGER PRIMARY KEY,
            username TEXT    UNIQUE NOT NULL,
            bcrypt   BLOB    NOT NULL
        );
    '''
    from sqlfunc import sqldb
    db = sqldb(__doc__, database=':memory:') # this is the default

    @db.sqludf
    def bcrypt_hash(password):
        # call to library here
        return b'$2b$12$.OjbRwRejxw92C89sA6JkOVrhmQzGsjoyCf1ofIN9hUNdHFufb3ty'

    @db.sqludf
    def bcrypt_verify(password, bcrypthash):
        # call to library here
        return 'password123' == password

    @db.sqlfunc
    def add_user(username, password):
        ''' INSERT OR IGNORE INTO users (username, bcrypt)
            VALUES (:username, bcrypt_hash(:password));
        '''

    @db.sqlfunc(post=bool, single=True, default=False)
    def login(username, password):
        ''' SELECT 1 FROM users
            WHERE username=:username
              AND bcrypt_verify(:password, bcrypt);
        '''

    @db.sqlfunc
    def list_users():
       ''' SELECT userid, username FROM users;
       '''

You can now do this:

.. code:: python

    >>> import example_users
    >>> example_users.add_user('root', 'password123')
    >>> example_users.login('root', 'secret')
    False
    >>> example_users.login('root', 'password123')
    True
    >>> example_users.list_users()
    ['root']

This library is MIT licensed.
