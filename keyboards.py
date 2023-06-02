from aiogram import types
from paswords import *
from database import *


class buttons:  # класс для создания клавиатур различных категорий товаров

    def __init__(self, bot, message):
        self.bot = bot
        self.message = message

    async def start_buttons(self, text):
        kb0 = types.ReplyKeyboardRemove()
        kb1 = types.InlineKeyboardMarkup(row_width=1)
        but1 = types.InlineKeyboardButton(text='Справка', callback_data='spravka')
        but2 = types.InlineKeyboardButton(text='Добавить покатушку', callback_data='new_race')
        kb1.add(but1, but2)
        try:
            await self.bot.delete_message(self.message.chat.id, self.message.message_id - 1)
            await self.bot.send_message(self.message.chat.id, text, reply_markup=kb1)
        except Exception:
            await self.bot.send_message(self.message.chat.id, text, reply_markup=kb1)

    async def only_race_button(self):
        kb2 = types.InlineKeyboardMarkup(row_width=1)
        but1 = types.InlineKeyboardButton(text='Добавить покатушку', callback_data='new_race')
        kb2.add(but1)
        return kb2
        # await self.bot.send_message(self.message.chat.id, f'Читай пост по ссылке https://t.me/esk8ru/111', reply_markup=kb2)
        # await self.bot.edit_message_text(f'Читай пост по ссылке https://t.me/esk8ru/111', self.message.chat.id,
        #                                  self.message.message_id)
        # await self.bot.edit_message_reply_markup(self.message.chat.id, self.message.message_id, reply_markup=kb2)

    async def only_before_post_button(self):
        kb3 = types.InlineKeyboardMarkup(row_width=1)
        but1 = types.InlineKeyboardButton(text='Добавить покатушку', callback_data='new_race')
        but2 = types.InlineKeyboardButton(text='Изменить', callback_data='change_race')
        but3 = types.InlineKeyboardButton(text='Отменить', callback_data='cancel_race')
        kb3.add(but1, but2, but3)
        # await self.bot.send_message(self.message.chat.id, f'Читай пост по ссылке https://t.me/esk8ru/111', reply_markup=kb2)
        try:
            # await self.bot.delete_message(self.message.chat.id, self.message.message_id - 1)
            # await self.bot.delete_message(self.message.chat.id, self.message.message_id)
            await self.bot.send_message(self.message.chat.id, f'Покатушка добавлена. Ты можешь сделать отмену или '
                                                              f'изменить покатушку\n\nПосмотри ее '
                                                              f'<a href="{group_hrev}/{data_base().parse_any(self.message, type="message_id", )}">здесь</a>.', parse_mode='HTML', reply_markup=kb3)
            await self.bot.delete_message(self.message.chat.id, self.message.message_id - 1)
            await self.bot.delete_message(self.message.chat.id, self.message.message_id)
        except Exception:
            # await self.bot.delete_message(self.message.chat.id, self.message.message_id)
            await self.bot.send_message(self.message.chat.id, f'Покатушка добавлена. Ты можешь сделать отмену или '
                                                              f'изменить покатушку\n\nПосмотри ее '
                                                              f'<a href="{group_hrev}/{data_base().parse_any(self.message, type="message_id", )}">здесь</a>.', parse_mode='HTML', reply_markup=kb3)
            await self.bot.delete_message(self.message.chat.id, self.message.message_id)

    async def only_pin_button(self):
        kb4 = types.InlineKeyboardMarkup(row_width=1)
        but1 = types.InlineKeyboardButton(text='Закрепить', callback_data='pin_post')
        kb4.add(but1)
        await self.bot.send_message(self.message.chat.id, f'Ты можешь закрепить свою покатушку на 12 часов, '
                                                          f'чтобы напомнить о ней подписчикам. Сделать так можно '
                                                          f'всего 1 раз, используй эту возможность только если до '
                                                          f'покатушки ещё несколько дней',
                                    reply_markup=kb4)

    async def data_error_button(self, text=None):
        kb3 = types.InlineKeyboardMarkup(row_width=1)
        but1 = types.InlineKeyboardButton(text='Добавить покатушку', callback_data='new_race')
        but2 = types.InlineKeyboardButton(text='Изменить', callback_data='change_race')
        but3 = types.InlineKeyboardButton(text='Отменить', callback_data='cancel_race')
        kb3.add(but1, but2, but3)
        try:
            await self.bot.send_message(self.message.chat.id, text, reply_markup=kb3)
        except Exception:
            await self.bot.send_message(self.message.chat.id, text, reply_markup=kb3)
