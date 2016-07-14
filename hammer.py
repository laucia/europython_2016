import argparse
import time

import asyncio
from aiohttp import ClientSession


def parse_args():
    parser = argparse.ArgumentParser(
        description="Hammer a local server with requests",
    )
    parser.add_argument(
        "--port",
        dest="port",
        type=int,
        default=5000,
        help="local port",
    )
    parser.add_argument(
        "--nb_requests",
        dest="nb_requests",
        type=int,
        nargs="?",
        default=20,
        help="# of requests to hammer the server with",
    )
    parser.add_argument(
        "--max_concurrency",
        dest="max_concurrency",
        type=int,
        nargs="?",
        default=50,
        help="max number of concurrent requests on server",
    )
    return parser.parse_args()


async def fetch(sem, url):
    async with sem:
        async with ClientSession() as session:
            async with session.get(url) as response:
                return await response.read()


async def hammer(loop,  port, nb_requests, max_concurrency):
    """ Hammer a local port
        :param loop: asyncio loop instance
        :param port: local port that should be called
        :param nb_requests: total number of requests to emit
        :param max_concurrency: max number of concurrent requests
    """
    url = "http://localhost:{}/".format(port)
    tasks = []

    # Avoid hitting the connection limit
    sem = asyncio.Semaphore(max_concurrency)
    for i in range(nb_requests):
        task = asyncio.ensure_future(fetch(sem, url))
        tasks.append(task)

    responses = asyncio.gather(*tasks)
    await responses


if __name__ == "__main__":
    args = parse_args()
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(
        hammer(loop, args.port, args.nb_requests, args.max_concurrency)
    )
    start_time = time.time()
    loop.run_until_complete(future)
    end_time = time.time()
    print("We did {} requests in {:.3f}".format(
        args.nb_requests,
        end_time-start_time,
    ))
