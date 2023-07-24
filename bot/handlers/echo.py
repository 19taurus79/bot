from aiogram import Router
from aiogram.types import (
    Message,
    KeyboardButton,
    WebAppInfo,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from utils.message import remains_answer, submissions_answer, aval_stock_answer
from keyboards import kb

router = Router()


@router.message()
async def echo(message: Message):
    val = message.text
    await remains_answer.remains_answer_summary(message, val)
    await remains_answer.remains_answer_series(message, val)
    await submissions_answer.submissions_answer(message, val)
    await aval_stock_answer.avail_stock_answer(message, val)
