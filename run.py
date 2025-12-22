import asyncio
import os
import signal
import json
import time

from server import protocol

WORKING_DIR = os.path.dirname(os.path.abspath(__file__))

def init_log():
    global logging_file
    import sys, time, os
    from twisted.python import log
    from twisted.python.logfile import DailyLogFile

    log_file = os.path.join(WORKING_DIR, "logs", "log.txt")
    try:
        os.makedirs(os.path.dirname(log_file))
    except OSError:
        pass
    logging_file = DailyLogFile(log_file, '.')
    log.addObserver(log.FileLogObserver(logging_file).emit)
    log.startLogging(sys.stdout)
    log.msg('AoS Server started on %s' % time.strftime('%c'))
    log.startLogging(sys.stdout) # force twisted logging

init_log()

with open("config.json") as f:
    config = json.load(f)

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

loop = asyncio.get_event_loop()
# Bad idea?
loop.time = time.perf_counter
loop._clock_resolution = time.get_clock_info('perf_counter').resolution
loop.set_debug(True)

server = protocol.ServerProtocol(config, loop=loop)

try:
    # aioconsole debugging stuff :)
    loop.console.locals['server'] = loop.console.locals['protocol'] = server
except AttributeError:
    pass

try:
    loop.add_signal_handler(signal.SIGINT, server.stop)
    loop.add_signal_handler(signal.SIGTERM, server.stop)
except NotImplementedError:
    pass

try:
    loop.run_until_complete(server.run())
finally:
    server.stop()
    loop.close()
