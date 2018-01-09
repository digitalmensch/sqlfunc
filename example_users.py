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