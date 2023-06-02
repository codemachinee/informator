import sqlite3
from datetime import datetime
import pytz
tz_moscow = pytz.timezone('Europe/Moscow')


class data_base:
    def __init__(self):
        self.base = sqlite3.connect('base.db')
        self.cur = self.base.cursor()
        self.base.execute(
            'CREATE TABLE IF NOT EXISTS {}(telegram_id PRIMARY KEY, username, message_id, message_text, date, pol_id)'.format(
                'data'))

    def find_user(self, message, message_id):
        r = self.cur.execute('SELECT message_id, message_text FROM data WHERE '
                             'telegram_id == ?', (message.chat.id,)).fetchone()
        if r:
            self.cur.execute('UPDATE data SET message_text == ?, message_id == ?, date == ?, pol_id == ? '
                             'WHERE telegram_id == ?',
                             (message.text, message_id, datetime.now(tz_moscow).day, None, message.chat.id))
            self.base.commit()
        else:
            self.cur.execute('INSERT INTO data VALUES(?, ?, ?, ?, ?, ?)', (message.chat.id, message.chat.username,
                                                                           message_id, message.text,
                                                                           datetime.now(tz_moscow).day, None))
            self.base.commit()

    def poll(self, message, pol_id):
        self.cur.execute('UPDATE data SET pol_id == ? WHERE telegram_id == ?',
                         (pol_id, message.chat.id))
        self.base.commit()

    def parse_any(self, message, type):
        r = self.cur.execute(f'SELECT {type} FROM data WHERE '
                             'telegram_id == ?', (message.chat.id,)).fetchone()
        return r[0]

# cur.execute('INSERT INTO data VALUES(?, ?, ?, ?)', ('127154291', '@hlop', '111', 'hih'))
# cur.execute('SELECT telegram_id FROM data').fetchall()
# base.commit()

#r = cur.execute('SELECT message_id, message_text FROM data WHERE telegram_id == ?', ('127154290', )).fetchone()
# if r:
#     print(r[0], r[1])
#
# else:
#     print('truble')

# cur.execute('UPDATE data SET message_text == ? WHERE message_id == ?', ('helo', '128'))
# base.commit()
