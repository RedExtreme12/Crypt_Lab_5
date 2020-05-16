import os.path
import datetime


log_file_name = 'log.txt'
today = datetime.datetime.today()


def logger(filename):
    def decorator(func):
        def wrapped(*args, **kwargs):
            result = func(*args, **kwargs)
            if not os.path.exists(log_file_name):
                with open(filename, 'w') as f:
                    f.write(result + ' : ' + today.strftime("%Y-%m-%d-%H.%M.%S") + '\n')
            else:
                with open(filename, 'a') as f:
                    f.write(result + ' : ' + today.strftime("%Y-%m-%d-%H.%M.%S") + '\n')

            return result
        return wrapped
    return decorator
