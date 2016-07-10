import os
import time
from functools import partial
from threading import current_thread

import gevent
import requests
from gevent import monkey


# Monkey-patch.
monkey.patch_all(thread=False, select=False)


def application(env, start_response):
    start_response("200 OK", [("Content-Type","text/html")])
    start_time = time.time()

    jobs = [
        gevent.spawn(partial(long_network_call, i/8))
        for i in range(1,5)
    ]
    gevent.joinall(jobs)

    end_time = time.time()

    return [
        b"This lasted %0.3f seconds with async calls using gevent\n" % (end_time - start_time)
    ]


def long_network_call(duration):
    thread_name = current_thread().name
    pid = os.getpid()
    print("pid: {} : thread_id: {} : start network call with duration {}".format(pid, thread_name, duration))
    requests.get('http://localhost:7001/?duration={}'.format(duration))
    print("pid: {} : thread_id: {} : end network call with duration {}".format(pid, thread_name, duration))
