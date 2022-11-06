import time

def sec_to_timestamp(seconds):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(seconds))


