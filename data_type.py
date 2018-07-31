# -*- coding: utf-8 -*-
# pylint: disable=broad-except

"""redis 数据类型例子
"""

__authors__ = ['"sue.chain" <sue.chain@gmail.com>']

import redis

# start int
conn = redis.Redis()
print conn.delete('key')       # 尝试获取一个不存在的键将得到一个None值，终端不会显示这个值。
print conn.get('key')             # 尝试获取一个不存在的键将得到一个None值，终端不会显示这个值。
print conn.incr('key')            # 我们既可以对不存在的键执行自增操作，
#1                               # 也可以通过可选的参数来指定自增操作的增量。
print conn.incr('key', 15)        #
#16                              #
print conn.decr('key', 5)         # 和自增操作一样，
#11                              # 执行自减操作的函数也可以通过可选的参数来指定减量。
print conn.get('key')             # 在尝试获取一个键的时候，命令以字符串格式返回被存储的整数。
#'11'                            #
print conn.set('key', '13')       # 即使在设置键时输入的值为字符串，
#True                            # 但只要这个值可以被解释为整数，
print conn.incr('key')            # 我们就可以把它当作整数来处理。

# start string

print conn.delete('new-string-key')     # 将字符串'hello'追加到目前并不存在的'new-string-key'键里。
print conn.append('new-string-key', 'hello ')     # 将字符串'hello'追加到目前并不存在的'new-string-key'键里。
#6L                                              # APPEND命令在执行之后会返回字符串当前的长度。
print conn.append('new-string-key', 'world!')
#12L                                             #
print conn.substr('new-string-key', 3, 7)         # Redis的索引以0为开始，在进行范围访问时，范围的终点（endpoint）默认也包含在这个范围之内。
#'lo wo'                                         # 字符串'lo wo'位于字符串'hello world!'的中间。
print conn.setrange('new-string-key', 0, 'H')     # 对字符串执行范围设置操作。
#12                                              # SETRANGE命令在执行之后同样会返回字符串的当前总长度。
print conn.setrange('new-string-key', 6, 'W')
#12
print conn.get('new-string-key')                  # 查看字符串的当前值。
#'Hello World!'                                  # 前面执行的两个SETRANGE命令成功地将字母h和w从原来的小写改成了大写。
print conn.setrange('new-string-key', 11, ', how are you?')   # SETRANGE命令既可以用于替换字符串里已有的内容，又可以用于增长字符串。
#25
print conn.get('new-string-key')
#'Hello World, how are you?'                     # 前面执行的SETRANGE命令移除了字符串末尾的感叹号，并将更多字符追加到了字符串末尾。
print conn.setbit('another-key', 2, 1)            # 对超出字符串长度的二进制位进行设置时，超出的部分会被填充为空字节。
#0                                               # SETBIT命令会返回二进制位被设置之前的值。
print conn.setbit('another-key', 7, 1)            # 在对Redis存储的二进制位进行解释（interpret）时，
#0                                               # 请记住Redis存储的二进制位是按照偏移量从高到低排列的。
print conn.get('another-key')                     #
#'!'                                             # 通过将第2个二进制位以及第7个二进制位的值设置为1，键的值将变为‘!’，即字符33 。


# start list
conn.delete('list-key')
print conn.rpush('list-key', 'last')          # 在向列表推入元素时，
#1L                                          # 推入操作执行完毕之后会返回列表当前的长度。
print conn.lpush('list-key', 'first')         # 可以很容易地对列表的两端执行推入操作。
#2L
print conn.rpush('list-key', 'new last')
#3L
print conn.lrange('list-key', 0, -1)          # 从语义上来说，列表的左端为开头，右端为结尾。
#['first', 'last', 'new last']               #
print conn.lpop('list-key')                   # 通过重复地弹出列表左端的元素，
#'first'                                     # 可以按照从左到右的顺序来获取列表中的元素。
print conn.lpop('list-key')                   #
#'last'                                      #
print conn.lrange('list-key', 0, -1)
#['new last']
print conn.rpush('list-key', 'a', 'b', 'c')   # 可以同时推入多个元素。
#4L
print conn.lrange('list-key', 0, -1)
#['new last', 'a', 'b', 'c']
print conn.ltrim('list-key', 2, -1)           # 可以从列表的左端、右端或者左右两端删减任意数量的元素。
#True                                        #
print conn.lrange('list-key', 0, -1)          #
#['b', 'c']                                  #

# start set
conn.delete('set-key')
print conn.sadd('set-key', 'a', 'b', 'c')         # SADD命令会将那些目前并不存在于集合里面的元素添加到集合里面，
#3                                               # 并返回被添加元素的数量。
print conn.srem('set-key', 'c', 'd')              # srem函数在元素被成功移除时返回True，
#True                                            # 移除失败时返回False；
print conn.srem('set-key', 'c', 'd')              # 注意这是Python客户端的一个bug，
#False                                           # 实际上Redis的SREM命令返回的是被移除元素的数量，而不是布尔值。
print conn.scard('set-key')                       # 查看集合包含的元素数量。
#2                                               #
print conn.smembers('set-key')                    # 获取集合包含的所有元素。
#set(['a', 'b'])                                 #
print conn.smove('set-key', 'set-key2', 'a')      # 可以很容易地将元素从一个集合移动到另一个集合。
#True                                            #
print conn.smove('set-key', 'set-key2', 'c')      # 在执行SMOVE命令时，
#False                                           # 如果用户想要移动的元素不存在于第一个集合里，
print conn.smembers('set-key2')                   # 那么移动操作就不会执行。
#set(['a'])                                      #


# start hash
conn.delete('hash-key')
print conn.hmset('hash-key', {'k1':'v1', 'k2':'v2', 'k3':'v3'})   # 使用HMSET命令可以一次将多个键值对添加到散列里面。
#True                                                            #
print conn.hmget('hash-key', ['k2', 'k3'])                        #  使用HMGET命令可以一次获取多个键的值。
#['v2', 'v3']                                                    #
print conn.hlen('hash-key')                                       # HLEN命令通常用于调试一个包含非常多键值对的散列。
#3                                                               #
print conn.hdel('hash-key', 'k1', 'k3')                           # HDEL命令在成功地移除了至少一个键值对时返回True，
#True                                                            # 因为HDEL命令已经可以同时删除多个键值对了，所以Redis没有实现HMDEL命令。

import pdb
pdb.set_trace()
# start zset
conn.delete('zset-key')
print conn.zadd('zset-key', 'a', 3, 'b', 2, 'c', 1)   # 在Python客户端执行ZADD命令需要先输入成员、后输入分值，
#3                                                   # 这跟Redis标准的先输入分值、后输入成员的做法正好相反。
print conn.zcard('zset-key')                          # 取得有序集合的大小可以让我们在某些情况下知道是否需要对有序集合进行修剪。
#3                                                   #
print conn.zincrby('zset-key', 'c', 3)                # 跟字符串和散列一样，
#4.0                                                 # 有序集合的成员也可以执行自增操作。
print conn.zscore('zset-key', 'b')                    # 获取单个成员的分值对于实现计数器或者排行榜之类的功能非常有用。
#2.0                                                 #
print conn.zrank('zset-key', 'c')                     # 获取指定成员的排名（排名以0为开始），
#2                                                   # 之后可以根据这个排名来决定ZRANGE的访问范围。
print conn.zcount('zset-key', 0, 3)                   # 对于某些任务来说，
#2L                                                  # 统计给定分值范围内的元素数量非常有用。
print conn.zrem('zset-key', 'b')                      # 从有序集合里面移除成员和添加成员一样容易。
#True                                                #
print conn.zrange('zset-key', 0, -1, withscores=True) # 在进行调试时，我们通常会使用ZRANGE取出有序集合里包含的所有元素，
[('a', 3.0), ('c', 4.0)]                            # 但是在实际用例中，通常一次只会取出一小部分元素。

