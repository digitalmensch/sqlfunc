sqlfunc
=======

.. code:: python

    >>> from sqlfunc import sqlfunc, singlevalue, singlecolumn
    >>>
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
    >>> @sqlfunc(post=singlecolumn)
    ... def list_users():
    ...     ''' SELECT username FROM users;
    ...     '''
    ...
    >>> list_users()
    ['root', 'guest']
    >>> @sqlfunc(post=lambda row: verify(row[0]), onerror=False)
    ... def login(username=None, password=None):
    ...     ''' SELECT password FROM users WHERE password=:password;
    ...     '''
    ...
    >>> login('root', 'wrong password')
    False


This library is MIT licensed.
