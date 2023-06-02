from datetime import *
import pytz
import datefinder
list_date = []
import sqlite3
data = '''Парк Горького у Чайной\n17.08 10:10\nЕду через Лужники, Воробьёвы в парк Победы'''
# matches = datefinder.find_dates(data, source=True)
# for match in matches:
#     match = (match[1].replace(' ', '.23 ', 1))
#     match = datetime.strptime(match, '%d.%m.%y %H:%M')
#     list_date.append(match.day)
#     list_date.append(match.month)
#     list_date.append(match.hour)
#     list_date.append(match.minute)
#     print(list_date)
#     print(list_date[0])
#     print(match)
#     break
tz_moscow = pytz.timezone('Europe/Moscow')
# print(f'{datetime.now(tz_moscow).day} {datetime.now(tz_moscow).month} {datetime.now(tz_moscow).hour}:'
#       f'{datetime.now(tz_moscow).hour}')
#print(datetime.now(tz_moscow), '%m/%d/%y %H:%M:%S')


# class data_base:
#     def __init__(self):
#         self.base = sqlite3.connect('base1.db')
#         self.cur = self.base.cursor()
#         self.base.execute(
#             'CREATE TABLE IF NOT EXISTS {}(telegram_id PRIMARY KEY, username, message_id, message_text, date, pol_id)'.format(
#                 'data'))
#         self.cur.execute('INSERT INTO data VALUES(?, ?, ?, ?, ?, ?)', (1234567, 'Игорь', 734536, 'привет как дела?',
#                                                                        f"{datetime.now(tz_moscow).day, datetime.now(tz_moscow).month}", None))
#         self.base.commit()
#
#     # def parse_text(self, type):
#     #     r = self.cur.execute(f'SELECT {type} FROM data WHERE '
#     #                          'telegram_id == ?', (127154290,)).fetchone()
#     #     print(r[0])
# print(data_base())
#
# delta = timedelta(minutes=5)
# td = datetime.now() + delta
# print(td)
# print(td.year, td.month, td.day, td.hour, td.minute)


def return_date(text):
    global tz_moscow
    matches = datefinder.find_dates(text, source=True)
    for match in matches:
        match = (match[1].replace(' ', '.23 ', 1))
        match = datetime.strptime(match, '%d.%m.%y %H:%M')
        delta = timedelta(minutes=1)
        print(match + delta)
        # list_date = [match.day, match.month, match.hour, match.minute]
        # return list_date


return_date(data)