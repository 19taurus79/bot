import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards import kb
from aiogram.fsm.context import FSMContext
from utils.message.remains_answer import (
    remains_answer_summary,
    remains_answer_series,
    remains_answer_series_seeds,
)
from utils.message.submissions_answer import submissions_answer

av_todo = ["без партии", "с партией"]


class CommandBot(StatesGroup):
    choosing_remains_nomenclature_seeds = State()
    choosing_submission = State()
    show_submission_seeds = State()
    choosing_submissions_nomenclature = State()
    choosing_avstocks_nomenclature = State()


router = Router()


@router.message(Command("seeds"))
async def remains(message: Message, state: FSMContext):
    logging.info(f"Пользователь {message.from_user.id} отправил команду {message.text}")
    await message.delete()
    await message.answer("По каким семенам показать остатки с показателями ?:")
    await state.set_state(CommandBot.choosing_remains_nomenclature_seeds)


@router.message(CommandBot.choosing_remains_nomenclature_seeds)
async def get_nomenclature(message: Message, state: FSMContext):
    logging.info(f"Пользователь {message.from_user.id} отправил запрос {message.text}")
    await state.update_data(chosen_nomenclature_seeds=message.text.capitalize())
    data = await state.get_data()
    nomenclature = data.get("chosen_nomenclature_seeds")
    await remains_answer_series_seeds(message, nomenclature)
    await message.answer(
        f"{chr(10)}Показать у кого заявки на эту номенклатуру ?",
        reply_markup=kb.make_row_keyboard(["Да", "Нет"]),
    )
    await state.set_state(CommandBot.show_submission_seeds)


@router.message(CommandBot.show_submission_seeds, F.text.in_(["Да", "Нет"]))
async def show_submission(message: Message, state: FSMContext):
    data = await state.get_data()
    nomenclature = data.get("chosen_nomenclature_seeds")
    if message.text == "Да":
        await submissions_answer(message, nomenclature)
    if message.text == "Нет":
        await message.answer("Ok", reply_markup=ReplyKeyboardRemove())
    await state.clear()
