import time


def pytimeit(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        end_time = time.time()
        # need to handle logger
        print("Time taken to run '{}' : {} seconds".format(func.__name__,(end_time - start_time)))
        return res
    return wrapper
