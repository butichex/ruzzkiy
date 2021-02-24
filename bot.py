from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from config import TOKEN
from aiogram.utils import executor
from aiogram.types import (
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InlineQueryResultArticle,
    InputTextMessageContent,
)
from random import choice
from keyboards import *
import asyncio
import aiohttp
from data import __all_models
from data.models import *
from data.db_session import *
import time
import datetime


global_init("db/gamers.db")

users = {}
duels = {}
users_objects = {}
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


class singleGame:
    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username
        self.commands = {}
        self.words_number = 0
        self.wrong_answered_words_number = 0
        self.right_answered_words_number = 0
        self.is_first_word = True
        self.sended_inline_message_id = 0
        self.sended_inline_message_chat_id = 0
        self.sended_verdict_message_id = 0
        self.sended_verdict_message_chat_id = 0
        self.sended_introduction_message_id = 0
        self.sended_introduction_message_chat_id = 0
        self.skipped_answered_words_number = 0
        self.word_variations_keyboard = 0
        self.attempts_to_guess_number = 0
        self.commands_from_messages = {"🚪 Выйти из игры": self.quit_game}
        self.commands_from_inline_buttons = {"next_word": self.next_word}
        self.commands_type = {
            "from_messages": self.commands_from_messages,
            "from_inline_buttons": self.commands_from_inline_buttons,
        }

    async def quit_game(self):
        users[self.user_id] = User(self.user_id, self.username)
        await bot.send_message(
            self.user_id,
            text=f"Ты вышел из игры и вернулся в *главное меню*.",
            reply_markup=main_menu_keyboard,
            parse_mode="Markdown",
        )
        await bot.delete_message(
            chat_id=self.sended_introduction_message_chat_id,
            message_id=self.sended_introduction_message_id,
        )
        await bot.delete_message(
            chat_id=self.sended_inline_message_chat_id,
            message_id=self.sended_inline_message_id,
        )

    async def introduction(self):
        message = await bot.send_message(
            self.user_id,
            f"Ты начал играть в режим *ОДИНОЧНАЯ ИГРА*. \n\nТебе нужно ставить ударения в словах, нажимая на кнопки, находящиеся под словом. \n\nВперёд! ",
            reply_markup=single_game_menu_keybaord,
            parse_mode="Markdown",
        )
        self.sended_introduction_message_id = message.message_id
        self.sended_introduction_message_chat_id = message["chat"]["id"]
        await self.generate_word()

    async def generate_word(self):
        self.attempts_to_guess_number = 0
        sended_message_id = 0
        sended_message_chat_id = 0
        session = create_session()
        word_object = choice(session.query(Word).all())
        word_text = word_object.text
        word_structure = word_object.word_structure
        word_variations = []
        for i in range(len(word_text)):
            if word_structure[i] == "1":
                word = list(word_text)
                word[i] = word[i].upper()
                word_variations.append("".join(word))
        self.word_variations_keyboard = InlineKeyboardMarkup(row_width=2)
        for word in word_variations:
            word_variation_button = InlineKeyboardButton(word, callback_data=word)
            self.word_variations_keyboard.insert(word_variation_button)
        self.current_word = word_text
        if self.is_first_word:
            message = await bot.send_message(
                self.user_id,
                f"Поставьте ударение в слове *{word.upper()}*.",
                parse_mode="Markdown",
                reply_markup=self.word_variations_keyboard,
            )
            self.sended_inline_message_id = message.message_id
            self.sended_inline_message_chat_id = message["chat"]["id"]
            self.is_first_word = False
        else:
            message = await bot.edit_message_text(
                f"Поставьте ударение в слове {word.upper()}.",
                chat_id=self.sended_inline_message_chat_id,
                message_id=self.sended_inline_message_id,
                reply_markup=self.word_variations_keyboard,
            )
            self.sended_inline_message_id = message.message_id
            self.sended_inline_message_chat_id = message["chat"]["id"]

    async def stress_in_word_checker(self):
        attempts_to_guess_number = 0
        session = create_session()
        word_object = session.query(Word).filter(Word.text == self.current_word).first()
        word_accent_position = word_object.accent_position
        for i in range(len(self.command)):
            if self.command[i].isupper():
                if i == word_accent_position:
                    word_object.gamer_id = self.user_id
                    word_object.guesses_number += 1
                    await bot.answer_callback_query(
                        self.callback_query_id, text=f"👍 Правильно!",
                    )
                    self.right_answered_words_number += 1
                    await self.generate_word()
                else:
                    await bot.answer_callback_query(
                        self.callback_query_id,
                        text=f"👎 Неправильно! Попробуй ещё раз.",
                    )
                    self.attempts_to_guess_number += 1
                    if self.attempts_to_guess_number == 2:
                        self.word_variations_keyboard.add(
                            InlineKeyboardButton(
                                "Следующее слово ➡️", callback_data="next_word"
                            )
                        )
                        await bot.edit_message_reply_markup(
                            chat_id=self.sended_inline_message_chat_id,
                            message_id=self.sended_inline_message_id,
                            reply_markup=self.word_variations_keyboard,
                        )
                    self.wrong_answered_words_number += 1
                self.words_number += 1

    async def next_word(self):
        self.skipped_answered_words_number += 1
        await self.generate_word()

    async def commands_handler(
        self, command, source, callback_query_id=None, msg_id=None, query=None
    ):
        self.command = command
        self.source = source
        self.callback_query_id = callback_query_id
        self.query = query
        self.msg_id = msg_id
        try:
            await self.commands_type[source][command]()
        except KeyError:
            try:
                if command.lower() == self.current_word:
                    await self.stress_in_word_checker()
            except:
                await bot.send_message(
                    self.user_id,
                    f"Извини, но я не понимаю команды *{command}*. \n\nСписок доступных команд: {', '.join(list(key for key, value in self.commands_from_messages.items()))}",
                    parse_mode="Markdown",
                    reply_markup=single_game_menu_keybaord,
                )


class User:
    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username
        self.sended_invite_message_time = 0
        self.commands_from_messages = {
            "/start": self.start,
            "⚙️ Изменить настройки": self.set_settings,
            "👤 Одиночная игра": self.start_singlegame,
            "⚔️ Дуэль": self.checking_invitation_can_be_send,
        }
        self.commands_from_inline_buttons = {
            "accept": self.accept_multigame_invite,
            "deny": self.deny_nultigame_invite,
        }
        self.commands_from_inline_queries = {
            "дуэль": self.checking_invitation_can_be_send
        }
        self.commands_type = {
            "from_messages": self.commands_from_messages,
            "from_inline_buttons": self.commands_from_inline_buttons,
            "from_inline_queries": self.commands_from_inline_queries,
        }

    async def accept_multigame_invite(self):
        await bot.send_message(
            self.user_id,
            "Возможность принимать приглашения находится всё ещё в разработке.",
            parse_mode="Markdown",
        )

    async def deny_nultigame_invite(self):
        await bot.send_message(
            self.user_id,
            "Возможность принимать приглашения находится всё ещё в разработке.",
            parse_mode="Markdown",
        )

    async def start_multigame(self, first_user_id, second_user_id):
        pass

    async def checking_invitation_can_be_send(self):
        await self.send_invitation()

    async def send_invitation(self):
        results = []
        game_invite_keyboard = InlineKeyboardMarkup()
        game_invite_accept_button = InlineKeyboardButton(
            "✔️ Принять", callback_data=f"{self.user_id}_accept"
        )
        game_invite_deny_button = InlineKeyboardButton(
            "⭕ Отклонить", callback_data=f"{self.user_id}_deny"
        )
        game_invite_keyboard.insert(game_invite_accept_button)
        game_invite_keyboard.insert(game_invite_deny_button)
        duels[self.user_id] = time.time()
        single_msg = InlineQueryResultArticle(
            id="1",
            title="⚔️ Дуэль",
            description="Нажми, чтобы отправить приглашение.",
            input_message_content=InputTextMessageContent(
                message_text=f"ПРИГЛАШЕНИЕ: \n\nПользователь @{self.username} приглашает тебя сыграть в ⚔️ Дуэль в @ruzzkiy_bot. \n\nСкорее принимай приглашение!"
            ),
            reply_markup=game_invite_keyboard,
        )
        results.append(single_msg)
        await bot.answer_inline_query(self.msg_id, results)
        self.sended_invite_message_time = time.time()

    async def back_to_main_menu(self, results=None):
        pass

    async def start(self):
        session = create_session()
        new_gamer = Gamer(id=self.user_id)
        session.add(new_gamer)
        await bot.send_message(
            self.user_id,
            "Привет! \n Это бот, который научит тебя ставить правильное ударение в более 250 словах. \n\n Выбери один из игровых режимов, указанных на клавиатуре.",
            parse_mode="Markdown",
            reply_markup=main_menu_keyboard,
        )

    async def set_settings(self):
        await bot.send_message(
            self.user_id,
            "Выбери вид отображения ударной позиции в слове.",
            parse_mode="Markdown",
            reply_markup=main_menu_keyboard,
        )

    async def start_multigame(self, first_user_id, second_user_id, msg_id=None):
        print(1)

    async def start_singlegame(self):
        game_object = singleGame(self.user_id, self.username)
        users[self.user_id] = game_object
        await game_object.introduction()

    async def commands_handler(
        self, command, source, callback_query_id=None, msg_id=None
    ):
        self.command = command
        self.source = source
        self.callback_query_id = callback_query_id
        self.msg_id = msg_id
        try:
            await self.commands_type[source][command]()
        except KeyError:
            try:
                if command.split("_")[1] == "accept" or command.split("_")[1] == "deny":
                    await self.commands_from_inline_buttons[command.split("_")[1]]()
            except:
                await bot.send_message(
                    self.user_id,
                    f"Извини, но я не понимаю команды *{command}*. \n\nСписок доступных команд: {', '.join(list(key for key, value in self.commands_from_messages.items()))}",
                    parse_mode="Markdown",
                    reply_markup=main_menu_keyboard,
                )


async def get_user_object(msg):
    user_id = msg.from_user.id
    username = msg.from_user.username
    if user_id in users.keys():
        return users[user_id]
    users[user_id] = User(user_id=user_id, username=username)
    return users[user_id]


@dp.message_handler()
async def commands_from_messages_handler(msg):
    print(msg)
    user_object = await get_user_object(msg)
    await user_object.commands_handler(
        command=msg.text, msg_id=msg.message_id, source="from_messages"
    )


@dp.inline_handler(lambda query: len(query.query) == 5)
async def commands_from_inline_queries_handler(query):
    print(query)
    user_object = await get_user_object(query)
    await user_object.commands_handler(
        command=query.query, msg_id=query.id, source="from_inline_queries"
    )


@dp.callback_query_handler()
async def commands_from_inline_buttons_handler(msg):
    user_object = await get_user_object(msg)
    print(msg)
    await user_object.commands_handler(
        command=msg.data, callback_query_id=msg.id, source="from_inline_buttons"
    )


@dp.message_handler(content_types=["contact"])
async def get_contact(msg):
    user_object = await get_user_object(msg)
    await user_object.auth(msg.contact.phone_number)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
