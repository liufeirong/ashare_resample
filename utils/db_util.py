from sqlalchemy import create_engine
import tushare as ts
import pymysql
import asyncio
import aiomysql
import logging

engine = create_engine('mysql+pymysql://root:stock123@127.0.0.1/stock?charset=utf8')
conn = pymysql.connect(user='root', passwd='stock123', host='localhost', db='stock',charset='utf8')


def execute(sql):
    cur = conn.cursor()
    print(sql)
    status=cur.execute(sql)
    conn.commit()
    cur.close()


# @asyncio.coroutine
# def create_pool(loop, **kw):
#     logging.info('create database connection pool...')
#     global __pool
#     __pool = yield from aiomysql.create_pool(
#         host=kw.get('host', 'localhost'),
#         port=kw.get('port', 3306),
#         user=kw['root'],
#         password=kw['stock123'],
#         db=kw['stock'],
#         charset=kw.get('charset', 'utf8'),
#         autocommit=kw.get('autocommit', True),
#         maxsize=kw.get('maxsize', 10),
#         minsize=kw.get('minsize', 1),
#         loop=loop
#     )
#
#
# @asyncio.coroutine
# def select(sql, args, size=None):
#     logging.info(sql, args)
#     global __pool
#     with (yield from __pool) as conn:
#         cur = yield from conn.cursor(aiomysql.DictCursor)
#         yield from cur.execute(sql.replace('?', '%s'), args or ())
#         if size:
#             rs = yield from cur.fetchmany(size)
#         else:
#             rs = yield from cur.fetchall()
#         yield from cur.close()
#         logging.info('rows returned: %s' % len(rs))
#         return rs


