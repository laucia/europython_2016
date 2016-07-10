import asyncio
import os
import time
from threading import current_thread

from aiohttp import ClientSession


def application(env, start_response):
    start_response("200 OK", [("Content-Type","text/html")])
    start_time = time.time()

    loop = asyncio.get_event_loop()
    futures =  [
        asyncio.ensure_future(long_network_call(i/8))
        for i in range(1,5)
    ]
    loop.run_until_complete(asyncio.wait(futures))

    end_time = time.time()
    return [
        b"This lasted %0.3f seconds with async calls using asyncio\n" % (end_time - start_time)
    ]


async def long_network_call(duration):
    thread_name = current_thread().name
    pid = os.getpid()
    print("pid: {} : thread_id: {} : start network call with duration {}".format(pid, thread_name, duration))
    async with ClientSession() as session:
        async with session.get('http://localhost:7001/?duration={}'.format(duration)) as response:
            r = await response.read()
            print("pid: {} : thread_id: {} : end network call with duration {}".format(pid, thread_name, duration))
            return r
