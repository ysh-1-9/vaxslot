import os

import redis
from rq import Worker, Queue, Connection

from vaxslot.scripts.automator import automate

listen = ['high', 'default', 'low']

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        s = Queue(connection=conn)
        s.enqueue(automate,job_timeout=-1)
        # q.enqueue(automate)
        worker.work()