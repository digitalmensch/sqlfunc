import example_users

example_users.add_user('root', 'password123')

x1 = example_users.login('root', 'secret')
print('x1', x1)
assert False == x1

x2 = example_users.login('root', 'password123')
print('x2', x2)
assert True == x2

x3 = example_users.list_users()
print('x3', x3)
assert len(x3) == 1
