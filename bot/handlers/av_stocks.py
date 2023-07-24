from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from handlers.remains import CommandBot
from utils.message.aval_stock_answer import avail_stock_answer

router = Router()


@router.message(Command("avail_stock"))
async def av_stock(message: Message, state: FSMContext):
    await message.answer("Укажите номенклатуру :", reply_markup=ReplyKeyboardRemove)
    await state.set_state(CommandBot.choosing_avstocks_nomenclature)


@router.message(CommandBot.choosing_avstocks_nomenclature)
async def submission_with_nomenclature(message: Message, state: FSMContext):
    nomenclature = message.text
    await avail_stock_answer(message, nomenclature)
    await state.clear()
