# -*- coding: utf-8 -*-
# pylint: disable=broad-except

"""redis 数据类型例子
"""

__authors__ = ['"sue.chain" <sue.chain@gmail.com>']

import time
import redis
from concurrent.futures import ProcessPoolExecutor

r = redis.Redis()

def try_pipeline():
    start = time.time()
    with r.pipeline(transaction=False) as p:
        p.sadd('seta', 1).sadd('seta', 2).srem('seta', 2).lpush('lista', 1).lrange('lista', 0, -1)
        p.execute()
    print time.time() - start


def without_pipeline():
    start = time.time()
    r.sadd('seta', 1)
    r.sadd('seta', 2)
    r.srem('seta', 2)
    r.lpush('lista', 1)
    r.lrange('lista', 0, -1)
    print time.time() - start


def worker():
    while True:
        without_pipeline()

with ProcessPoolExecutor(max_workers=12) as pool:
    for _ in range(10):
        pool.submit(worker)
