import sqlite3
import inspect
import functools

################################################################################
#
################################################################################

class sqldb(object):

    def __init__(self, sql, database=':memory:'):
        self.__db = sqlite3.connect(database)
        self.__cur = self.__db.cursor()
        self.__cur.execute(sql)

    def sqludf(self, func):
        sig = inspect.signature(func)
        self.__db.create_function(func.__name__, len(sig.parameters), func)

    def sqlfunc(self, _func=None, post=None, single=False, default=None):
        def _decorator(func):
            sql = func.__doc__
            assert len(sql) >= 8 # 'SELECT 1'
            signature = inspect.signature(func)
            params = tuple(signature.parameters.keys())

            @functools.wraps(func)
            def _function(*args, **kwargs):
                bound = signature.bind(*args, **kwargs)
                bound.apply_defaults()
                mapping = dict(zip(params, bound.args))

                result = list(self.__cur.execute(sql, mapping))
                print(result)
                print('single', single)
                print('default', default)

                if single:
                    for row in result:
                        print('row', row)
                        return post(row) if post else row
                    else:
                        return default

                return map(post, result) if post else result


            return _function

        if _func is not None:
            return _decorator(_func)
        else:
            return _decorator

