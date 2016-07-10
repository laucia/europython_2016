import os
import time
from threading import current_thread

import requests


def application(env, start_response):
    start_response("200 OK", [("Content-Type","text/html")])
    start_time = time.time()

    calls = [
        long_network_call(i/8) for i in range(1,5)
    ]

    end_time = time.time()

    return [
        b"This call lasted %0.3f seconds with synchronous calls.\n" % (end_time - start_time)
    ]


def long_network_call(duration):
    thread_name = current_thread().name
    pid = os.getpid()
    print("pid: {} : thread_id: {} : start network call with duration {}".format(pid, thread_name, duration))
    requests.get('http://localhost:7001/?duration={}'.format(duration))
    print("pid: {} : thread_id: {} : end network call with duration {}".format(pid, thread_name, duration))
