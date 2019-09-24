from Core.asql import runner
from Core.asql import new_table
from Core.asql import drop_table
from Core.asql import get_guilds
from Core.asql import insert
from Core.asql import update

from Core.tools import logs
from Core.constants import Const
import pprint


runner(new_table, "guilds", "gid", gid="INTEGER", lc="TEXT", prefix="TEXT")
# await runner(insert(gid=377018078501928991, lc='ru-RU', prefix='биба '))
# await runner(insert(gid=601836147722944524, lc='ru-RU', prefix='биба '))
# await runner(insert(gid=405285018454327296, lc='ru-RU', prefix='биба '))
# await runner(insert(gid=623397495921311774, lc='ru-RU', prefix='биба '))
# await runner(pprint.pprint(get_guilds()))
# await runner(drop_table())
