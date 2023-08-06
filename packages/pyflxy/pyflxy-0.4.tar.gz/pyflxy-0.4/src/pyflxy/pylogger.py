import logging
import time

def pylog(original_func, fname = "", root_path = ""):
    path = ""
    if root_path != "":
        path = root_path
    if fname != '':
        path += "./" + fname
    else:
        path += "./" + "app.log"
    if path == "":
        path = "app"
    logging.basicConfig(filename="{}.log".format(path), level=logging.INFO)
    def wrapper_func(*args, **kwargs):
        logging.info("ran with args: {} kwars: {}".format(args, kwargs))
        return original_func(*args, **kwargs)
    return wrapper_func

#
# @my_logger
# class TESTME:
#
#     def __init__(self, func):
#         self.func = func
#
#     def __call__(self, *args, **kwargs):
#         return self.func