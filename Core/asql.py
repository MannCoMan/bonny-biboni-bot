import functools
import sqlite3
import aiosqlite
import asyncio

from Core.constants import Const
from Core.tools import logger


logger = logger(__name__)


async def new_table(file=None, table=None, *uniques, **kwargs):
    """
    Args:
          table (str)    - table name
          uniques (args) - unique value(-s)
          kwargs         - <column-name=TYPE>
    """
    if not file:
        file = Const.SQL_DEFAULT_FILE
    file = "Data/{}".format(file)

    if not table:
        raise ValueError("Parameter 'table' is None!")

    async with aiosqlite.connect("Data/users.data") as conn:
        unique = ""
        if uniques:
            unique = "UNIQUE ({uniques})".format(
                uniques=", ".join(uniques)
            )

        if not kwargs:
            raise KeyError("kwargs not found!")

        keys = ", ".join(
            "{} {}".format(key, typo) for (key, typo) in kwargs.items()
        )

        sql = "CREATE TABLE IF NOT EXISTS {table} ({keys}, {unique});"
        sql = sql.format(table=table, keys=keys, unique=unique)

        await conn.execute(sql)
        await conn.commit()


async def drop_table(file=None, table=None):
    if not file:
        file = Const.SQL_DEFAULT_FILE
    file = "Data/{}".format(file)

    if not table:
        raise ValueError("Parameter 'table' is None!")

    async with aiosqlite.connect(file) as conn:
        await conn.execute("DROP TABLE {table}".format(table=table))
        await conn.commit()


async def insert(file=None, **kwargs):

    if not file:
        file = Const.SQL_DEFAULT_FILE
    file = "Data/{}".format(file)

    async with aiosqlite.connect(file) as conn:
        keys = ", ".join(
            "{!s}".format(i) for i in kwargs.keys()
        )
    
        values = ", ".join(
            "{!r}".format(i) for i in kwargs.values()
        )
    
        sql = "INSERT OR IGNORE INTO guilds ({keys}) VALUES({values})".format(
            keys=keys,
            values=values
        )

        await conn.execute(sql)
        await conn.commit()


async def update(file=None, gid=None, **kwargs):
    """
    Args:
        gid - guild id
        kwargs - columns to update

    >>> update(guildid, lc="en-US", prefix="newprefix")
    """

    if not file:
        file = Const.SQL_DEFAULT_FILE
    file = "Data/{}".format(file)

    if not gid:
        raise ValueError("Parameter 'gid' is None!")

    async with aiosqlite.connect(file) as conn:
        items = ", ".join(
            "'{}'".format(i) for i in kwargs.items()
        )

        sql = "UPDATE guilds SET {gid} WHERE gid = {items} ;".format(
            gid=gid,
            items=items
        )

        await conn.execute(sql)
        await conn.commit()


async def get_guilds(file=None, **kwargs):
    """
    Args:
        filter (str) - sql filter for WHERE method
    Returns:
        list of guilds ([gid, "lc-LC", 0 or 1])

    >>> get_guilds(gid=guildID, lc="lc-LC")
    """

    if not file:
        file = Const.SQL_DEFAULT_FILE
    file = "Data/{}".format(file)

    async with aiosqlite.connect(file) as conn:
        if kwargs:
            items = ", ".join(
                "{!s}={!r}".format(key, val) for (key, val) in kwargs.items()
            )
    
            sql = "SELECT gid, lc, prefix FROM guilds WHERE {items} ;".format(
                items=items
            )
        sql = "SELECT * FROM guilds ;"

        cursor = await conn.execute(sql)
        return await cursor.fetchall()


async def runner(func, *args, **kwargs):
    loop = asyncio.get_event_loop()
    asyncio.run(functools.partial(func, *args, **kwargs))
