import logging

from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
from middlewares.user_validator import managers_id

from keyboards.inline_kb import submission_kb, line_of_business_kb, contract_kb
from utils.db.moved import get_products_from_number
from utils.db.submissions import get_my_submissions
from utils.message.my_moved_product import moved_product_answer

router = Router()


class MySubmission(StatesGroup):
    select_client = State()
    select_contract = State()
    select_line_of_business = State()


@router.message(Command("my_sub"))
async def my_sub(message: Message, state: FSMContext):
    manager_id = message.from_user.id
    # manager_id = 651394664
    manager = next(ch for ch, code in managers_id.items() if code == manager_id)
    # manager = "Чех Олександр Вікторович"
    await state.update_data({"manager": manager})
    data = await get_my_submissions(manager)
    await message.delete()
    clients = []
    for client in data:
        if client["client"] not in clients:
            clients.append(client["client"])
    clients.sort()
    await state.set_state(MySubmission.select_client)
    kb = await submission_kb(clients)
    await message.answer(text="Укажите клиента", reply_markup=kb)


@router.callback_query(MySubmission.select_client)
async def my_client(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = callback.data
    await state.update_data({"client": data})
    kb = await line_of_business_kb(client=data)
    await callback.message.answer(
        "По какому виду деятельности выбрать заявки ?", reply_markup=kb
    )
    await state.set_state(MySubmission.select_line_of_business)


@router.callback_query(MySubmission.select_line_of_business)
async def line_of_business(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = callback.data
    state_data = await state.get_data()
    manager = state_data.get("manager")
    client = state_data.get("client")
    await state.update_data({"line_of_bus": data})
    kb = await contract_kb(manager=manager, client=client, l_o_b=data)
    if kb is None:
        await callback.message.edit_text(
            "Заявок соответствующих выбранным параметрам нет", reply_markup=kb
        )
    else:
        await callback.message.edit_text("Укажите какая заявка", reply_markup=kb)
    await state.set_state(MySubmission.select_contract)


@router.callback_query(MySubmission.select_contract)
async def contract(callback: CallbackQuery, state: FSMContext):
    data = callback.data
    moved_products = await get_products_from_number(data)
    if not moved_products:
        await callback.message.edit_text(
            f"По заявке {data} информации о перемещении товара нет", reply_markup=None
        )
    await moved_product_answer(callback=callback, data=moved_products)
    await state.set_state(MySubmission.select_client)
