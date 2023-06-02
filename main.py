from aiogram import Bot, executor, Dispatcher, types
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ContentType, Message
from datetime import datetime, timedelta
import time
from keyboards import *
from paswords import *
from database import *
from functions import *
import pytz

tz_moscow = pytz.timezone('Europe/Moscow')

# token = lemonade
token = codemashine_test

bot = Bot(token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    text = State()
    message_id = State()
    change_message = State()


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    # await bot.delete_message(message.chat.id, message.message_id)
    await buttons(bot, message).start_buttons(text=f'Привет, {message.from_user.first_name}! Я помогу тебе собрать людей на '
                                                 f'покатушку. Все анонсы публикую в канале {group_id}, '
                                                 f'обязательно подпишись.')
    await bot.delete_message(message.chat.id, message.message_id)


@dp.callback_query_handler()
async def button_message(callback: types.CallbackQuery):
    if callback.data == 'new_race':
        kb2 = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        but1 = types.InlineKeyboardButton(text='Отмена')
        kb2.add(but1)
        # await bot.delete_message(callback.message.chat.id, callback.message.message_id)
        await bot.send_message(callback.message.chat.id, f'Ок, пиши подробно время и место. Пример: \n\nПарк Горького '
                                                         f'у Чайной\n17.05 10:10 (только так, да)\nЕду через Лужники, '
                                                         f'Воробьёвы в парк Победы\n\nЗдесь только текст - фото и '
                                                         f'видео в комментарии к записи в канал.', reply_markup=kb2)
        await bot.delete_message(callback.message.chat.id, callback.message.message_id)
        await Form.text.set()  # Устанавливаем состояние
    elif callback.data == 'spravka':
        # await buttons(bot, callback.message).only_race_button()
        await bot.edit_message_text(f'Читай пост по ссылке https://t.me/esk8ru/111', callback.message.chat.id,
                                    callback.message.message_id)
        await bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id,
                                            reply_markup=await buttons(bot, callback.message).only_race_button())
    elif callback.data == 'change_race':
        try:
            await bot.delete_message(callback.message.chat.id, callback.message.message_id + 1)
            if data_base().parse_any(callback.message, "pol_id"):
                await bot.delete_message(group_id, data_base().parse_any(callback.message, "pol_id"))
            await bot.edit_message_text(f'Ок, ниже текущий текст твоего объявления, пришли мне новый\n\n'
                                        f'{data_base().parse_any(callback.message, type="message_text")}',
                                        callback.message.chat.id, callback.message.message_id)
            await Form.message_id.set()
        except Exception:
            if data_base().parse_any(callback.message, "pol_id"):
                await bot.delete_message(group_id, data_base().parse_any(callback.message, "pol_id"))
            await bot.edit_message_text(f'Ок, ниже текущий текст твоего объявления, пришли мне новый\n\n'
                                        f'{data_base().parse_any(callback.message, type="message_text")}',
                                        callback.message.chat.id, callback.message.message_id)
            await Form.message_id.set()
    elif callback.data == 'cancel_race':
        try:
            await bot.delete_message(callback.message.chat.id, callback.message.message_id + 1)
            if data_base().parse_any(callback.message, "pol_id"):
                await bot.delete_message(group_id, data_base().parse_any(callback.message, "pol_id"))
            await bot.edit_message_text(f'❗️❕ Покатушка отменена', callback.message.chat.id,
                                        callback.message.message_id)
            await bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id,
                                                reply_markup=await buttons(bot, callback.message).only_race_button())
            await bot.edit_message_text(f'<s>{data_base().parse_any(callback.message, type="message_text")}</s>',
                                        group_id,
                                        data_base().parse_any(callback.message, type="message_id"), parse_mode='HTML')
            await unpin(bot, group_id, data_base().parse_any(callback.message, "message_id"))
            await bot.send_message(group_id, '❗️❕ Покатушка отменена',
                                   reply_to_message_id=data_base().parse_any(callback.message, type="message_id"))
        except Exception:
            if data_base().parse_any(callback.message, "pol_id"):
                await bot.delete_message(group_id, data_base().parse_any(callback.message, "pol_id"))
            await bot.edit_message_text(f'❗️❕ Покатушка отменена', callback.message.chat.id,
                                        callback.message.message_id)
            await bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id,
                                                reply_markup=await buttons(bot, callback.message).only_race_button())
            await bot.edit_message_text(f'<s>{data_base().parse_any(callback.message, type="message_text")}</s>',
                                        group_id,
                                        data_base().parse_any(callback.message, type="message_id"), parse_mode='HTML')
            await unpin(bot, group_id, data_base().parse_any(callback.message, "message_id"))
            await bot.send_message(group_id, '❗️❕ Покатушка отменена',
                                   reply_to_message_id=data_base().parse_any(callback.message, type="message_id"))
    elif callback.data == 'pin_post':
        try:
            delta = timedelta(minutes=2)
            td = datetime.now() + delta
            scheduler.add_job(unpin, 'date',
                              run_date=datetime(td.year, td.month, td.day, td.hour, td.minute, 0),
                              args=[bot, group_id, data_base().parse_any(callback.message, "message_id")],
                              id=f'unpin{data_base().parse_any(callback.message, "message_id")}')
            scheduler.start()
            await bot.answer_callback_query(callback.id,
                                            f'Покатушка была закреплена в канале на 12 часов.', show_alert=True)
            await bot.delete_message(callback.message.chat.id, callback.message.message_id)
            await bot.pin_chat_message(group_id, message_id=data_base().parse_any(callback.message, type="message_id"))
        except Exception:
            delta = timedelta(minutes=10)
            td = datetime.now() + delta
            scheduler.add_job(unpin, 'date',
                              run_date=datetime(td.year, td.month, td.day, td.hour, td.minute, 0),
                              args=[bot, group_id, data_base().parse_any(callback.message, "message_id")],
                              id=f'unpin{data_base().parse_any(callback.message, "message_id")}')
            scheduler.start()
            await bot.answer_callback_query(callback.id,
                                            f'Покатушка была закреплена в канале на 12 часов.', show_alert=True)
            await bot.pin_chat_message(group_id, message_id=data_base().parse_any(callback.message, type="message_id"))


@dp.message_handler(state=Form.text)  # Принимаем состояние
async def new_message(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:  # Устанавливаем состояние ожидания
            if message.text != 'Отмена':
                if await proverka_date(message.text) is True:
                    data['text'] = message.text
                    message_id = (await bot.send_message(group_id,
                                                         f'{data["text"]}\n<b>Автор - @{message.from_user.username}</b>',
                                                         parse_mode='HTML')).message_id
                    data['message_id'] = message_id
                    data_base().find_user(message, message_id)
                    await buttons(bot, message).only_before_post_button()
                    await buttons(bot, message).only_pin_button()
                    pol_id = (await bot.send_poll(group_id, question='Ты участвуешь?', options=['Да', 'Да, но опоздаю',
                                                                                      'Да, присоединюсь по маршруту',
                                                                                      'Думаю, напишу позже, Нет',
                                                                                      'Посмотреть результат'],
                                                  reply_to_message_id=data['message_id'])).message_id
                    data_base().poll(message, pol_id)
                    await posting_timer(bot, message)
                    await state.finish()
                elif await proverka_date(message.text) is None:
                    data['text'] = message.text
                    message_id = (await bot.send_message(group_id,
                                                         f'{data["text"]}\n<b>Автор - </b>'
                                                         f'<b>@{message.from_user.username}</b>',
                                                         parse_mode='HTML')).message_id
                    data['message_id'] = message_id
                    data_base().find_user(message, message_id)
                    await buttons(bot, message).only_before_post_button()
                    pol_id = (await bot.send_poll(group_id, question='Ты участвуешь?', options=['Да', 'Да, но опоздаю',
                                                                                                'Да, присоединюсь по маршруту',
                                                                                                'Думаю, напишу позже, Нет',
                                                                                                'Посмотреть результат'],
                                                  reply_to_message_id=data['message_id'])).message_id
                    data_base().poll(message, pol_id)
                    await state.finish()
                elif await proverka_date(message.text) == 'equally':
                    data['text'] = message.text
                    message_id = (await bot.send_message(group_id,
                                                         f'{data["text"]}\n<b>Автор - </b>'
                                                         f'<b>@{message.from_user.username}</b>',
                                                         parse_mode='HTML')).message_id
                    data['message_id'] = message_id
                    data_base().find_user(message, message_id)
                    await posting_timer(bot, message)
                    await buttons(bot, message).only_before_post_button()
                    pol_id = (await bot.send_poll(group_id, question='Ты участвуешь?', options=['Да', 'Да, но опоздаю',
                                                                                                'Да, присоединюсь по маршруту',
                                                                                                'Думаю, напишу позже, Нет',
                                                                                                'Посмотреть результат'],
                                                  reply_to_message_id=data['message_id'])).message_id
                    data_base().poll(message, pol_id)
                    await posting_timer(bot, message)
                    await state.finish()
                else:
                    await bot.delete_message(message.chat.id, message.message_id)
                    await bot.delete_message(message.chat.id, message.message_id - 1)
                    await buttons(bot, message).start_buttons(text='Ошибка. Неверная дата')
                    await state.finish()

            else:
                await bot.delete_message(message.chat.id, message.message_id)
                await bot.delete_message(message.chat.id, message.message_id - 1)
                await state.finish()
                await buttons(bot, message).start_buttons(text=f'Привет, {message.from_user.first_name}! Я помогу тебе собрать людей на '
                                                 f'покатушку. Все анонсы публикую в канале {group_id}, '
                                                 f'обязательно подпишись.')
    except Exception:
        #await bot.delete_message(message.chat.id, message.message_id)
        await state.finish()
        await buttons(bot, message).start_buttons(text=f'Привет, {message.from_user.first_name}! Я помогу тебе собрать людей на '
                                                 f'покатушку. Все анонсы публикую в канале {group_id}, '
                                                 f'обязательно подпишись.')


@dp.message_handler(state=Form.message_id)  # Принимаем состояние
async def new_message(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:  # Устанавливаем состояние ожидания
            if message.text != 'Отмена':
                data['text'] = message.text
                if await proverka_date(message.text) is True:
                    message_id = (await bot.edit_message_text(f'{data["text"]}\n\n'
                                                              f'<s>{data_base().parse_any(message, type="message_text")}</s>'
                                                              f'\n\n<b>Автор - '
                                                              f'@{message.from_user.username}</b>\n'
                                                              f'Обновлено - '
                                                              f'{datetime.now(tz_moscow).day}.{datetime.now(tz_moscow).month} '
                                                              f'{datetime.now(tz_moscow).hour}:{datetime.now(tz_moscow).minute}',
                                                              group_id,
                                                              data_base().parse_any(message, type="message_id", ),
                                                              parse_mode='HTML')).message_id
                    data['message_id'] = message_id
                    data_base().find_user(message, message_id)
                    await buttons(bot, message).only_before_post_button()
                    await buttons(bot, message).only_pin_button()
                    pol_id = (await bot.send_poll(group_id, question='Ты участвуешь?', options=['Да', 'Да, но опоздаю',
                                                                                                'Да, присоединюсь по маршруту',
                                                                                                'Думаю, напишу позже, Нет',
                                                                                                'Посмотреть результат'],
                                                  reply_to_message_id=data['message_id'])).message_id
                    data_base().poll(message, pol_id)
                    await posting_timer(bot, message)
                    await state.finish()
                elif await proverka_date(message.text) is None:
                    message_id = (await bot.edit_message_text(f'{data["text"]}\n\n'
                                                              f'<s>{data_base().parse_any(message, type="message_text")}</s>'
                                                              f'\n\n<b>Автор - '
                                                              f'@{message.from_user.username}</b>\n'
                                                              f'Обновлено - '
                                                              f'{datetime.now(tz_moscow).day}.{datetime.now(tz_moscow).month} '
                                                              f'{datetime.now(tz_moscow).hour}:{datetime.now(tz_moscow).minute}',
                                                              group_id,
                                                              data_base().parse_any(message, type="message_id", ),
                                                              parse_mode='HTML')).message_id
                    data['message_id'] = message_id
                    data_base().find_user(message, message_id)
                    await buttons(bot, message).only_before_post_button()
                    pol_id = (await bot.send_poll(group_id, question='Ты участвуешь?', options=['Да', 'Да, но опоздаю',
                                                                                                'Да, присоединюсь по маршруту',
                                                                                                'Думаю, напишу позже, Нет',
                                                                                                'Посмотреть результат'],
                                                  reply_to_message_id=data['message_id'])).message_id
                    data_base().poll(message, pol_id)
                    await state.finish()
                elif await proverka_date(message.text) == 'equally':
                    message_id = (await bot.edit_message_text(f'{data["text"]}\n\n'
                                                              f'<s>{data_base().parse_any(message, type="message_text")}</s>'
                                                              f'\n\n<b>Автор - '
                                                              f'@{message.from_user.username}</b>\n'
                                                              f'Обновлено - '
                                                              f'{datetime.now(tz_moscow).day}.{datetime.now(tz_moscow).month} '
                                                              f'{datetime.now(tz_moscow).hour}:{datetime.now(tz_moscow).minute}',
                                                              group_id,
                                                              data_base().parse_any(message, type="message_id", ),
                                                              parse_mode='HTML')).message_id
                    data['message_id'] = message_id
                    data_base().find_user(message, message_id)
                    await buttons(bot, message).only_before_post_button()
                    pol_id = (await bot.send_poll(group_id, question='Ты участвуешь?', options=['Да', 'Да, но опоздаю',
                                                                                                'Да, присоединюсь по маршруту',
                                                                                                'Думаю, напишу позже, Нет',
                                                                                                'Посмотреть результат'],
                                                  reply_to_message_id=data['message_id'])).message_id
                    data_base().poll(message, pol_id)
                    await posting_timer(bot, message)
                    await state.finish()
                else:
                    await bot.delete_message(message.chat.id, message.message_id)
                    await bot.delete_message(message.chat.id, message.message_id - 2)
                    await buttons(bot, message).data_error_button(text='Ошибка. Неверная дата')
                    await state.finish()

            else:
                await bot.delete_message(message.chat.id, message.message_id)
                await state.finish()
                await buttons(bot, message).start_buttons(text=f'Привет, {message.from_user.first_name}! Я помогу тебе собрать людей на '
                                                 f'покатушку. Все анонсы публикую в канале {group_id}, '
                                                 f'обязательно подпишись.')
    except Exception:
        await bot.delete_message(message.chat.id, message.message_id)
        await state.finish()
        await buttons(bot, message).start_buttons(text=f'Привет, {message.from_user.first_name}! Я помогу тебе собрать людей на '
                                                 f'покатушку. Все анонсы публикую в канале {group_id}, '
                                                 f'обязательно подпишись.')


@dp.message_handler(content_types='text')  # перехватчик текстовых сообщений
async def chek_message_category(m: types.Message):
    if m.text == 'Отмена':
        await buttons(bot, m).start_buttons(text=f'Привет, {m.from_user.first_name}! Я помогу тебе собрать людей на '
                                                 f'покатушку. Все анонсы публикую в канале {group_id}, '
                                                 f'обязательно подпишись.')


async def posting_timer(bot, message):
    delta = timedelta(minutes=2)
    message_text = data_base().parse_any(message, type="message_text")
    td = await return_date(message_text) + delta
    #td = datetime.now(tz_moscow) + delta
    scheduler.add_job(post_delete, 'date',
                      run_date=datetime(td.year, td.month, td.day, td.hour, td.minute, 0),
                      args=[bot, message, message_text,  group_id,
                            data_base().parse_any(message, "message_id"), data_base().parse_any(message, "username")],
                      id=f'{data_base().parse_any(message, "message_id")}', replace_existing=True)
    scheduler.print_jobs()
    if data_base().parse_any(message, "pol_id"):
        scheduler.add_job(delete_message, 'date',
                          run_date=datetime(td.year, td.month, td.day, td.hour, td.minute, 0),
                          args=[bot, group_id,
                                data_base().parse_any(message, "pol_id")],
                          id=f'pol{data_base().parse_any(message, "pol_id")}', replace_existing=True)


if __name__ == '__main__':
    scheduler = AsyncIOScheduler()
    scheduler.start()
    # scheduler.add_job(statistic().obnulenie, "cron", day_of_week='mon-sun', hour=0)
    # scheduler.add_job(statistic().obnulenie, "interval", hours=6)
    # scheduler.start()
    executor.start_polling(dp, skip_updates=True)
