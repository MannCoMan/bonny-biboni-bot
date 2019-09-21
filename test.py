from Core.sql import update, insert, get_guilds, new_table, drop_table
from Core.tools import logs
import pprint

<<<<<<< HEAD

new_table(table="guilds")
insert(gid=377018078501928991, lc='ru-RU', prefix='биба ')
insert(gid=601836147722944524, lc='ru-RU', prefix='биба ')
insert(gid=405285018454327296, lc='ru-RU', prefix='биба ')
pprint.pprint(get_guilds(gid=405285018454327296))
drop_table()
=======
# new_table(table="guilds")
# insert(gid=377018078501928991, lc='ru-RU', prefix='биба ')
# insert(gid=601836147722944524, lc='ru-RU', prefix='биба ')
# insert(gid=405285018454327296, lc='ru-RU', prefix='биба ')
pprint.pprint(get_guilds(gid=405285018454327296))
# drop_table()
>>>>>>> 9ad2324714667587996bd6fb0b7c52815107be92

