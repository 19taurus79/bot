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
    remains_answer_analog_nomenclature,
)
from utils.message.submissions_answer import submissions_answer
from utils.message.aval_stock_answer import analog_avail_stock_answer


class CommandBot(StatesGroup):
    choosing_remains_nomenclature_seeds = State()
    choosing_submission = State()
    show_submission_seeds = State()
    choosing_submissions_nomenclature = State()
    choosing_avstocks_nomenclature = State()
    choosing_analog_nomenclature = State()
    choosing_analog_parametr = State()
    choosing_analog_warehouse = State()


router = Router()
by_what_parameter = ["По товару", "По веществу"]
by_what_warehouse = ["У нас на складе", "По всем складам"]


@router.message(Command("analog"))
async def remains(message: Message, state: FSMContext):
    logging.info(f"Пользователь {message.from_user.id} отправил команду {message.text}")
    await message.delete()
    await message.answer(
        "В каком виде искать аналог? :",
        reply_markup=kb.make_row_keyboard(by_what_parameter),
    )
    await state.set_state(CommandBot.choosing_analog_parametr)


@router.message(CommandBot.choosing_analog_parametr, F.text.in_(by_what_parameter))
async def get_remains(message: Message, state: FSMContext):
    logging.info(f"Пользователь {message.from_user.id} выбрал вариант {message.text}")
    await state.update_data(chosen_analog_type=message.text)
    await message.answer(
        "Где искать? :", reply_markup=kb.make_row_keyboard(by_what_warehouse)
    )
    await state.set_state(CommandBot.choosing_analog_warehouse)


@router.message(CommandBot.choosing_analog_warehouse, F.text.in_(by_what_warehouse))
async def get_remains(message: Message, state: FSMContext):
    data = await state.get_data()
    analog_type = data.get("chosen_analog_type")
    if analog_type == "По товару":
        text = "Укажите номенклатуру :"
    if analog_type == "По веществу":
        text = "Укажите действуещее вещество :"
    logging.info(f"Пользователь {message.from_user.id} выбрал вариант {message.text}")
    await state.update_data(chosen_analog_warehouse=message.text)
    await message.answer(f"{text}", reply_markup=ReplyKeyboardRemove)
    await state.set_state(CommandBot.choosing_analog_nomenclature)


@router.message(CommandBot.choosing_analog_nomenclature)
async def get_nomenclature(message: Message, state: FSMContext):
    logging.info(f"Пользователь {message.from_user.id} отправил запрос {message.text}")
    await state.update_data(chosen_analog_nomenclature=message.text.capitalize())
    data = await state.get_data()
    nomenclature = data.get("chosen_analog_nomenclature")
    analog_type = data.get("chosen_analog_type")
    warehouse = data.get("chosen_analog_warehouse")
    if warehouse == "У нас на складе":
        await remains_answer_analog_nomenclature(message, nomenclature, analog_type)
    if warehouse == "По всем складам":
        await analog_avail_stock_answer(message, nomenclature, analog_type)

    await state.clear()
