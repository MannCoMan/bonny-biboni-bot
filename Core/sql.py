import sqlite3 as sql
from Core.tools import logger

logger = logger("sql")


def create_connection(file):
    conn = None
    try:
        conn = sql.connect(file)
    except sql.Error as err:
        message = "SQL error: {}\n".format(err)
        logger.warning(message)
    return conn


def new_table(table):
    conn = create_connection("Data/servers.data")
    cursor = conn.cursor()

    sql = """
    CREATE TABLE IF NOT EXISTS {table} (
        gid INTEGER, lc TEXT, prefix TEXT,
        UNIQUE (gid)
    );
    """
    sql = sql.format(table=table)

    cursor.execute(sql)
    conn.commit()

    logger.info("Table was created")


def drop_table():
    conn = create_connection("Data/servers.data")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE guilds")
    conn.commit()

    logger.info("Table was dropped")


def insert(**kwargs):
    conn = create_connection("Data/servers.data")
    cursor = conn.cursor()

    sql = "INSERT OR IGNORE INTO guilds ({keys}) VALUES({values})".format(
        gid=kwargs["gid"],
        keys=", ".join(i for i in kwargs.keys()),
        values=", ".join("'{}'".format(i) for i in kwargs.values())
    )
    cursor.execute(sql)
    conn.commit()

    logger.info("Data was inserted in guild")


def update(gid, **kwargs):
    """
    Args:
        gid - guild id
        kwargs - columns to update

    >>> update(guildid, lc="en-US", prefix="newprefix")
    """

    conn = create_connection("Data/servers.data")
    cursor = conn.cursor()

    sql = "UPDATE guilds SET {} WHERE gid = {}".format(
        ", ".join("'{}'".format(i) for i in kwargs.items()),
        gid
    )
    cursor.execute(sql)
    conn.commit()

    logger.info("Data was updated in guild")


def get_guilds(**kwargs):
    """
    Args:
        filter (str) - sql filter for WHERE method
    Returns:
        list of guilds ([gid, "lc-LC", 0 or 1])

    >>> get_guilds(gid=guildID, lc="lc-LC")
    """

    conn = create_connection("Data/servers.data")
    cursor = conn.cursor()

    if kwargs:
        sql = "SELECT gid, lc, prefix FROM guilds WHERE {} ;".format(
            ", ".join("'{}'".format(i) for i in kwargs.items())
        )
    else:
        sql = "SELECT * FROM guilds ;"

    cursor.execute(sql)
    return cursor.fetchall()
