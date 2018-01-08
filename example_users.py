''' CREATE TABLE IF NOT EXISTS users (
        userid   INTEGER PRIMARY KEY,
        username TEXT    UNIQUE NOT NULL,
        bcrypt   BLOB    NOT NULL
    );
'''
from sqlfunc import sqlinit, sqludf, sqlfunc, singlevalue, rowtodict

__database__ = ':memory:' # default

@sqludf
def bcrypt_hash(password):
    # call to library here
    return b'$2b$12$.OjbRwRejxw92C89sA6JkOVrhmQzGsjoyCf1ofIN9hUNdHFufb3ty'

@sqludf
def bcrypt_verify(password, bcrypthash):
    # call to library here
    return True

@sqlfunc
def add_user(username, password):
    ''' INSERT OR IGNORE INTO $$$ (username, bcrypthash)
        VALUES (:username, bcrypt_hash(:password));
    '''

@sqlfunc(post=lambda x: bool(list(x)))
def login(username, password):
    ''' SELECT 1 FROM users
        WHERE username=:username
          AND bcrypt_verify(:password, bcrypt);
    '''

sqlinit()
