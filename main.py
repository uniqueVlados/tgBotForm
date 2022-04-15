from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton


TOKEN = "YOUR_TOKEN"

STATES = {"start": False, "ans": 1}

# MSG
HELP_INFO = "Нажимая на кнопку *Потребность*, вы заполняете гугл форму, где вы подробно описываете ваши потребности," \
            " инновационность продукта и дополнительную информацию, пожелания и тд.,после чего запрос берется в работу " \
            "нашими сотрудниками.\nНажимая на кнопку *Участие с партнером*, вы подтверждаете свою заинтересованность и " \
            "желание поучаствовать в запросах от наших партнеров. Вы будете перенаправлены на ссылку гугл-формы, где " \
            "сможете подробно изложить свою информацию о проекте, прикрепить презентацию и ссылку на ваш сайт, после" \
            " чего информация передается напрямую партнеру"

PARD_TEXT = "Просим вас заполнить нашу небольшую форму ниже чтобы предоставить проектам самую полную и достоверную" \
            " информацию о вашем запросе и вашей организации."

PARD_PROJECT_TEXT = "💼Кнопка *Партнер* - запрос от  компаний, заинтересованных во внедреннии технологических решений " \
                    "под свои запросы\n🚀Кнопка *Проект* - подача заявки на участие по запросу партнера или описание" \
                    " своих потребностей."

# BUTTONS
BUTTON_PARD = KeyboardButton('Партнёр🤝')
BUTTON_PROJECT = KeyboardButton('Проект📟')
BUTTON_PARD_LINK = InlineKeyboardButton(text="Перейти", url="https://docs.google.com/forms/d/e/1FAIpQLSeS"
                                                       "2PtNZzTTZxurwyZhW-8a8s-frw5WcL7ppFSZNOsPxcj0rw/viewform")
BUTTON_NEED = KeyboardButton('Потребность👋')
BUTTON_INFO = KeyboardButton(' ❓ ')
BUTTON_ANS = KeyboardButton('❓')
BUTTON_FRIEND = KeyboardButton('Участие с партнёром👥')
BUTTON_BACK = KeyboardButton('Назад⤴️')

BUTTON_NEED_LINK = InlineKeyboardButton(text="Перейти", url="https://docs.google.com/forms/d/e/1FAIpQLSeW7bDgdYa"
                                                            "tnQxgEwD1BRYi3DMsYAE4QJsrr0WKX2aCGXeDqg/viewform ")

BUTTON_ACTION_PARD_LINK = InlineKeyboardButton(text="Перейти", url="https://docs.google.com/forms/d/e/1FAIpQLSfxUNfl"
                                                                   "7pxOsvpwnrEYIqonK5cg2A8vUECtWl3um5wfwZXDUw/viewform ")

# KEYBOARDS
KB_START = ReplyKeyboardMarkup(resize_keyboard=True)
KB_START.add(BUTTON_PARD, BUTTON_PROJECT, BUTTON_INFO)

KB_LINK_PARD = InlineKeyboardMarkup(resize_keyboard=True)
KB_LINK_PARD.add(BUTTON_PARD_LINK)

KB_PARD = ReplyKeyboardMarkup(resize_keyboard=True)
KB_PARD.add(BUTTON_PARD, BUTTON_BACK)

KB_PROJECT = ReplyKeyboardMarkup(resize_keyboard=True)
KB_PROJECT.add(BUTTON_NEED, BUTTON_ANS, BUTTON_FRIEND, BUTTON_BACK)

KB_LINK_NEED = InlineKeyboardMarkup(resize_keyboard=True)
KB_LINK_NEED.add(BUTTON_NEED_LINK)

KB_LINK_ACTION_PARD = InlineKeyboardMarkup(resize_keyboard=True)
KB_LINK_ACTION_PARD.add(BUTTON_ACTION_PARD_LINK)


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_(message: types.Message):
    STATES["start"] = True
    await message.reply(f"Здравствуйте, {message.from_user.first_name}", reply_markup=KB_START)


@dp.message_handler(commands=['help'])
async def start_(message: types.Message):
    await message.reply(HELP_INFO, reply_markup=KB_PROJECT, parse_mode="Markdown")


@dp.message_handler()
async def info(message: types.Message):
    if message.text == "Партнёр🤝":
        STATES["btn_back"] = "PARD"
        await message.reply(PARD_TEXT, reply_markup=KB_PARD)
        await message.reply("⬇️ФОРМА ДЛЯ ЗАПОЛНЕНИЯ⬇️", reply_markup=KB_LINK_PARD)
    elif message.text == "Проект📟":
        STATES["btn_back"] = "PROJECT"
        await message.reply('Добрый день! Вы можете выбрать интересующий вас фичу. Если возникнут вопросы, нажмите “?”',
                            reply_markup=KB_PROJECT)
    elif message.text == "Потребность👋":
        await message.reply('⬇️Заполнить форму️⬇️',
                            reply_markup=KB_LINK_NEED)
    elif message.text == "Участие с партнёром👥":
        await message.reply('⬇️Заполнить форму️⬇️',
                            reply_markup=KB_LINK_ACTION_PARD)
    elif message.text == "Назад⤴️":
        STATES["ans"] = 1
        await message.reply(f"{message.from_user.first_name}, Вы снова в главном меню", reply_markup=KB_START)
    elif message.text == "❓" and STATES["ans"] == 1:
        STATES["ans"] = 2
        await message.reply(PARD_PROJECT_TEXT, reply_markup=KB_START, parse_mode="Markdown")
    elif message.text == "❓" and STATES["ans"] == 2:
        await message.reply(HELP_INFO, reply_markup=KB_PROJECT, parse_mode="Markdown")


if __name__ == '__main__':
    executor.start_polling(dp)