import os

import redis
from rq import Queue, Worker, Connection

redis_url = os.getenv('REDIS_URL') or 'redis://localhost:6379'
listen = ['default']

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue,listen)))
        worker.work()