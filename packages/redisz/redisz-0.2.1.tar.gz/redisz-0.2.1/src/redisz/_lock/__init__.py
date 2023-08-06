import math
import time
import uuid

import redis.exceptions
from .. import get_redis


def acquire_lock(lockname, acquire_timeout=10, lock_timeout=10):
    """
    描述:
        获取锁
        Redis的事务是通过MULTI和EXEC命令实现的，以确保一个客户端在不被其他客户端打断的情况下执行操作命令，当一个事务执行完毕时，才会处理其他客户端的命令
        Python客户端以流水线(pipeline)的方式实现的事务，一次将所有命令都发送给Redis，同时还要配合WATCH命令，以确保执行EXEC之前，操作的键值没有被修改
        这是一种"乐观锁"，不会阻止其他客户端对数据的修改，而是WATCH到数据变化后，会取消EXEC操作，并以重试的方式再次检查操作条件是否满足，再决定后续的操作
        请注意，WATCH必须和EXEC配合使用才有意义，单纯的WATCH是不起作用的
        这种WATCH方式，在有多个客户端操作相同数据时，可能会造成大量的重试，而且编码也比较麻烦
        所以提供了acquire_lock/release_lock方法实现分布式锁
        1.获取锁
            -如果成功返回锁的标识符，并且设置过期时间，以避免客户端异常退出锁一直被占用问题
            -如果锁已经存在，则等待acquire_timeout，如果在等待的时间内没有获取到，则返回False
            -如果锁已经存在，但是没有设置过期时间，则设置过期时间为lock_timeout，以避免锁一直不可用的问题
        2.释放锁
            -通过标识符判断当前的锁是否已经发生变化，如果没有变化，则将锁删除，如果有变化则返回False

    参数:
        lockname:string -锁的名称，可以有多个锁
        acquire_timeout:int -请求等待时间，默认10秒
        lock_timeout:int -锁的过期时间，超时自动移除锁

    返回:
        identifier:string|bool -如果获取成功，返回锁对应的标识符，如果获取失败，返回False

    示例:
        def lock_test():
            locked = acquire_lock('a-lock')
            if locked is False:
                return False

            r = redisz.get_redis()
            pipe = r.pipeline(True)
            try:
                pipe.set('a', 1)
                pipe.set('b', 2)
                pipe.execute()
            finally:
                release_lock('a-lock', locked)

    """
    r = get_redis()
    identifier = str(uuid.uuid4())  # 释放锁时检查
    lockname = _gen_lock_name(lockname)
    lock_timeout = int(math.ceil(lock_timeout))  # 整数
    end = time.time() + acquire_timeout

    while time.time() < end:
        if r.setnx(lockname, identifier):  # 如果lockname不存在，设置lockname&过期时间，并返回identifier
            r.expire(lockname, lock_timeout)
            return identifier
        elif r.ttl(lockname) == -1:  # 如果lockname没有设置到期时间，则设置超时时间，避免一直lock
            r.expire(lockname, lock_timeout)
        time.sleep(0.01)
    return False


def release_lock(lockname, identifier):
    """
    描述:
        释放锁

    参数:
        lockname:string -要释放锁的名称
        identifier:string -要释放锁的标识符

    返回:
        result:bool -如果释放成功返回True，否则返回False

    示例:
        # 请参考 acquire_lock
    """
    pipe = get_redis().pipeline(True)
    lockname = _gen_lock_name(lockname)
    while True:
        try:
            pipe.watch(lockname)  # 通过watch确保lockname没有被改变过
            if pipe.get(lockname) == identifier:  # 判断锁标识符是否发生变化
                pipe.multi()
                pipe.delete(lockname)
                pipe.execute()  # execute中会调用unwatch
                return True  # 释放成功
            pipe.unwatch()
            break
        except redis.exceptions.WatchError:
            pass

    return False  # 失去了锁


def _gen_lock_name(lockname):
    return 'redisz-lock:' + lockname
