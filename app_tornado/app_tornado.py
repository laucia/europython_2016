import atexit
import functools
import os
import threading
import time
from concurrent.futures import Future

from tornado.httpclient import AsyncHTTPClient
from tornado.ioloop import IOLoop

_loop = IOLoop()

def _event_loop():
    _loop.make_current()
    _loop.start()

def setup():
    t = threading.Thread(
        target=_event_loop,
        name="TornadoReactor",
    )
    t.start()
    atexit.register(_loop.close)
setup()


def long_network_call(duration):
    http_client = AsyncHTTPClient(_loop)

    thread_name = threading.current_thread().name
    pid = os.getpid()
    print("pid: {} : thread_id: {} : start network call with duration {}".format(pid, thread_name, duration))

    # this uses the threadsafe loop.add_callback internally
    fetch_future = http_client.fetch(
        'http://localhost:7001/?duration={}'.format(duration)
    )

    result_future = Future()
    def callback(f):
        try:
            result_future.set_result(f.result())
        except BaseException as e:
            result_future.set_exception(e)
        print("pid: {} : thread_id: {} : end network call with duration {}".format(pid, thread_name, duration))

    fetch_future.add_done_callback(callback)

    return result_future


##############################################################################


def application(env, start_response):
    start_response("200 OK", [("Content-Type","text/html")])
    start_time = time.time()

    futures = [
        long_network_call(i/8) for i in range(1,5)
    ]
    # Let's do something heavy like ... waiting
    time.sleep(1)

    for future in futures:
        future.result()

    end_time = time.time()

    return [
        b"This call lasted %0.3f seconds with offloaded asynchronous calls.\n" % (end_time - start_time)
    ]
