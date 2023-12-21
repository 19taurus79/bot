from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.db.moved import get_line_of_business_sub
from utils.db.submissions import get_my_submissions, get_contract


async def submission_kb(sub_clients):
    builder = InlineKeyboardBuilder()
    for sub_client in sub_clients:
        data = sub_client[:20]
        builder.add(InlineKeyboardButton(text=f"{sub_client}", callback_data=f"{data}"))
        builder.adjust(1)
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
    contract_list = []
    for contract in contracts:
        if contract not in contract_list:
            contract_list.append(contract)
    builder = InlineKeyboardBuilder()
    if len(contracts) == 0:
        return None
    else:
        for contract in contract_list:
            contract = contract["contract_supplement"][23:34]
            builder.add(
                InlineKeyboardButton(text=f"{contract}", callback_data=f"{contract}")
            )
            builder.adjust(2)
        return builder.as_markup()
