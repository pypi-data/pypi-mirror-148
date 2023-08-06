import schedule
import time


def pyschedule(second = 0, minutes = 0, hour = 0, limit = 0, description = "", sleep_time = 1, initial_delay = 0):
    def pyschedule_decorator(func):
        def inner_func(*args, **kwargs):
            nonlocal minutes, second, hour
            print("Scheduling function : {}".format(func.__name__))
            start_time = time.time()
            minutes = str(minutes)
            second = str(second)
            while time.time() < start_time + initial_delay:
                time.sleep(sleep_time)
            func(*args, **kwargs)
            if len(minutes) <= 1:
                minutes = "0"+minutes
            if len(second) <= 1:
                second = "0"+second
            if hour == 0:
                if minutes == "00":
                    schedule.every(int(second)).seconds.do(func, *args, **kwargs)
                else:
                    schedule.every(int(minutes)).minute.at(":{}".format(second)).do(func, *args, **kwargs)
            else:
                if minutes == "00":
                    minutes = ""
                print(hour, minutes, second)
                schedule.every(hour).hours.at("{}:{}".format(minutes, second)).do(func, *args, **kwargs)

            while True:
                schedule.run_pending()
                time.sleep(sleep_time)
                if(limit != 0 and time.time() > (start_time + limit )):
                    print("Stopping the schedular since it crossed the specified limit : {} sec".format(limit))
                    break
        return inner_func
    return pyschedule_decorator

