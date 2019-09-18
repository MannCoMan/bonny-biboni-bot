from Core.sql import update, insert, get_guilds, new_table

new_table()
insert(('377018078501928991', 'ru-RU', 'биба '))
insert(('601836147722944524', 'ru-RU', 'биба '))
insert(('405285018454327296', 'ru-RU', 'биба '))
print(get_guilds())