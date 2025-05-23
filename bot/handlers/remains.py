import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from utils.db.get_products import get_products
from keyboards import kb
from aiogram.fsm.context import FSMContext

from keyboards.inline_kb import remains_type_kb, choosing_product
from utils.message.remains_answer import (
    remains_answer_summary,
    remains_answer_series,
    txt_choosing_product,
)
from utils.message.submissions_answer import submissions_answer

av_todo = ["без партии", "с партией"]


class CommandBot(StatesGroup):
    choosing_remains_type = State()
    choosing_remains_nomenclature = State()
    choosing_submission = State()
    show_submission = State()
    choosing_submissions_nomenclature = State()
    choosing_avstocks_nomenclature = State()


router = Router()


@router.message(Command("remains"))
async def remains(message: Message, state: FSMContext):
    logging.info(f"Пользователь {message.from_user.id} отправил команду {message.text}")
    await message.delete()
    await state.set_state(CommandBot.choosing_remains_type)
    kb = await remains_type_kb()

    await message.answer("В каком виде показать остатки ?", reply_markup=kb)


@router.callback_query(CommandBot.choosing_remains_type)
async def get_remains(
    callback: CallbackQuery,
    state: FSMContext,
):
    # logging.info(f"Пользователь {message.from_user.id} выбрал вариант {message.text}")
    await callback.answer()
    data = callback.data
    await state.update_data(chosen_remains_type=data)
    await callback.message.edit_text(
        "Введіть повне або часткове найменування номенклатури яка Вас цікавить :",
    )
    await state.set_state(CommandBot.choosing_remains_nomenclature)


@router.message(CommandBot.choosing_remains_nomenclature)
async def get_nomenclature(
    message: Message,
    state: FSMContext,
):
    logging.info(f"Пользователь {message.from_user.id} отправил запрос {message.text}")
    await state.update_data(chosen_nomenclature=message.text.capitalize())
    data = await state.get_data()
    remains_type = data.get("chosen_remains_type")
    nomenclature = data.get("chosen_nomenclature")
    kb = await choosing_product(nomenclature)
    product_text = await get_products(nomenclature)
    txt = await txt_choosing_product(product_text)
    txt = "".join(txt)
    if not txt.strip():
        response_message= "Извините, номенклатура по вашему запросу не найдена."
        await message.answer(text=response_message)
        await state.clear()
        return
    await message.answer(text=txt)
    if remains_type == "без партии":
        await remains_answer_summary(message, nomenclature)
    if remains_type == "с партией":
        await remains_answer_series(message, nomenclature)
    await message.answer(
        f"{chr(10)}Показать у кого заявки на эту номенклатуру ?",
        reply_markup=kb.make_row_keyboard(["Да", "Нет"]),
    )
    await state.set_state(CommandBot.show_submission)


@router.message(CommandBot.show_submission, F.text.in_(["Да", "Нет"]))
async def show_submission(message: Message, state: FSMContext):
    data = await state.get_data()
    nomenclature = data.get("chosen_nomenclature")
    if message.text == "Да":
        await submissions_answer(message, nomenclature)
    if message.text == "Нет":
        await message.answer("Ok", reply_markup=ReplyKeyboardRemove())
    await state.clear()
