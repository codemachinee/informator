import datefinder
from datetime import datetime
from datetime import timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import pytz
tz_moscow = pytz.timezone('Europe/Moscow')


async def proverka_date(text):
    global tz_moscow
    list_date_now = [datetime.now(tz_moscow).day, datetime.now(tz_moscow).month, datetime.now(tz_moscow).hour,
                     datetime.now(tz_moscow).minute]
    try:
        matches = datefinder.find_dates(text, source=True)
        for match in matches:
            match = (match[1].replace(' ', '.23 ', 1))
            match = datetime.strptime(match, '%d.%m.%y %H:%M')
            list_date = [match.day, match.month, match.hour, match.minute]
            if list_date_now[1] < list_date[1]:
                return True
            elif list_date_now[1] == list_date[1]:
                if list_date_now[0] < list_date[0]:
                    return True
                elif list_date_now[0] == list_date[0]:
                    return 'equally'
                else:
                    return False
            else:
                return False
    except Exception:
        return None


async def return_date(text):
    global tz_moscow
    matches = datefinder.find_dates(text, source=True)
    for match in matches:
        match = (match[1].replace(' ', '.23 ', 1))
        match = datetime.strptime(match, '%d.%m.%y %H:%M')
        return match


async def unpin(bot, chat, message_id):
    try:
        await bot.unpin_chat_message(chat, message_id)
    except Exception:
        pass


async def post_delete(bot, message, message_text, chat, message_id, username):
    try:
        await bot.edit_message_text(f'<s>{message_text}\n<b>Автор - @{username}</b></s>', chat, message_id,
                                    parse_mode='HTML')
        id = (await bot.send_message(message.chat.id, '.')).message_id
        await bot.delete_message(message.chat.id, id)
        await bot.delete_message(message.chat.id, id - 1)
    except Exception:
        pass


async def delete_message(bot, chat, message_id):
    try:
        await bot.delete_message(chat, message_id)
    except Exception:
        pass

