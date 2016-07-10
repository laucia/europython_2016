import gevent
import urllib.parse


def application(env, start_response):
    start_response("200 OK", [("Content-Type","text/html")])

    query_arg = urllib.parse.parse_qs(env["QUERY_STRING"])
    wait_time = float(query_arg.get("duration", (5,))[0])

    gevent.sleep(wait_time)

    return [b"Waited %d" % wait_time]
