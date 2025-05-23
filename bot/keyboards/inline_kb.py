from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.get_products import get_products
from remove_words import remove_words_until_uppercase
from utils.db.moved import get_line_of_business_sub
from utils.db.submissions import get_my_submissions, get_contract


async def submission_kb(sub_clients):
    builder = InlineKeyboardBuilder()
    for sub_client in sub_clients:
        data = sub_client["client"]
        builder.add(InlineKeyboardButton(text=f"{data}", callback_data=f"{data}"))
        builder.adjust(1)
    return builder.as_markup()


async def remains_type_kb():
    av_todo = ["без партии", "с партией"]
    builder = InlineKeyboardBuilder()
    for i in av_todo:
        builder.add(InlineKeyboardButton(text=f"{i}", callback_data=f"{i}"))
        builder.adjust(2)
    return builder.as_markup()


async def line_of_business_kb(client):
    builder = InlineKeyboardBuilder()
    # business = [
    #     "ЗЗР",
    #     "Власне виробництво насіння",
    #     "Позакореневi добрива",
    #     "Насіння",
    #     "Міндобрива (основні)",
    # ]
    business = await get_line_of_business_sub(client)
    # business.sort()
    for line in business:
        builder.add(
            InlineKeyboardButton(
                text=f"{line['line_of_business']}",
                callback_data=f"{line['line_of_business']}",
            )
        )
        builder.adjust(2)
    return builder.as_markup()


async def contract_kb(manager, client, l_o_b):
    contracts = await get_contract(manager=manager, client=client, l_o_b=l_o_b)
    # contract_list = []
    # for contract in contracts:
    #     if contract not in contract_list:
    #         contract_list.append(contract)
    builder = InlineKeyboardBuilder()
    if len(contracts) == 0:
        return None
    else:
        for contract in contracts:
            contract = contract["contract_supplement"]
            builder.add(
                InlineKeyboardButton(text=f"{contract}", callback_data=f"{contract}")
            )
            builder.adjust(2)
        return builder.as_markup()


async def choosing_product(product):
    builder = InlineKeyboardBuilder()
    products = await get_products(product)
    for product in range(len(products)):
        builder.add(InlineKeyboardButton(text=f"{product}", callback_data=f"{product}"))
        builder.adjust(3)
    return builder.as_markup()
