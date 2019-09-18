import sqlite3 as sql


def create_connection(file):
    conn = None
    try:
        conn = sql.connect(file)
    except sql.Error as e:
        print(e)
 
    return conn


def new_table():
    conn = create_connection("Data/servers.data")
    cursor = conn.cursor()
    
    sql = """
    CREATE TABLE guilds (
        gid INTEGER, lc TEXT, prefix TEXT
    )
    """
    cursor.execute(sql)
    conn.commit()


def insert(args):
    conn = create_connection("Data/servers.data")
    cursor = conn.cursor()

    sql = """
        INSERT INTO guilds VALUES (?,?,?)
    """
    cursor.execute(sql, args)
    conn.commit()


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
        ", ".join("='".join(i)+"'" for i in kwargs.items()),
        gid
    )
    cursor.execute(sql)
    conn.commit()


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
            ", ".join("='".join(i)+"'" for i in kwargs.items())
        )
    else:
        sql = "SELECT * FROM guilds ;"

    cursor.execute(sql)
    return cursor.fetchall()
