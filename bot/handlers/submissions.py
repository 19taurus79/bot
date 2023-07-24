from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, ReplyKeyboardRemove
from utils.message.submissions_answer import submissions_answer
from aiogram.fsm.state import StatesGroup, State
from handlers.remains import CommandBot
from aiogram.fsm.context import FSMContext
from handlers.remains import CommandBot


router = Router()


@router.message(Command("submissions"))
async def submissions(message: Message, state: FSMContext):
    await message.answer("Укажите номенклатуру :", reply_markup=ReplyKeyboardRemove)
    await state.set_state(CommandBot.choosing_submissions_nomenclature)


@router.message(CommandBot.choosing_submissions_nomenclature)
async def submission_with_nomenclature(message: Message, state: FSMContext):
    nomenclature = message.text
    await submissions_answer(message, nomenclature)
    await state.clear()
