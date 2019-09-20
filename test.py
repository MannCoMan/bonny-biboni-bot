from Core.sql import update, insert, get_guilds, new_table, drop_table
from Core.tools import logs
import pprint

new_table()

insert(gid=377018078501928991, lc='ru-RU', prefix='биба ')
insert(gid=601836147722944524, lc='ru-RU', prefix='биба ')
insert(gid=405285018454327296, lc='ru-RU', prefix='биба ')

pprint.pprint(get_guilds())
drop_table()


# @logs(name="sql", message="Test")
# def test():
#     print("Hello")
