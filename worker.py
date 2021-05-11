import os

import redis
from rq import Worker, Queue, Connection

from vaxslot.scripts.db_imports_exports import initialize
from vaxslot.scripts.updateDB import updateDB

listen = ['high', 'default', 'low']

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        q = Queue(connection=conn)
        q.enqueue(initialize)
        q.enqueue(updateDB)
        worker.work()