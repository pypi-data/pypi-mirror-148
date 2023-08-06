import time


def timeit(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        end_time = time.time()
        # need to handle logger
        print("Time taken to run '{}' : {} seconds".format(func.__name__,(end_time - start_time)))
        return res
    return wrapper

@timeit
def add(a,b):
    time.sleep(10)
    return a+b

if __name__=="__main__":
    print(add(1,2))