import logging
from utils.db.available_stock import get_available_stock
from aiogram.exceptions import TelegramBadRequest as err

from utils.db.available_stock import get_available_stock_analog_nomenclature_product, \
    get_available_stock_analog_nomenclature_substance


async def avail_stock_answer(message, val):
    await message.answer(f"<strong>*****Свободно на РУ*****</strong>{chr(10)}{chr(10)}")
    aval = await get_available_stock(val)
    b = []
    if len(aval) > 0:
        for i in range(len(aval)):
            if i == 0:
                b.append(
                    f"{chr(10)}<strong><u>{aval[i].get('product.product')}</u></strong>{chr(10)}{chr(10)}"
                    f"{aval[i].get('division')} {aval[i].get('available')}{chr(10)}"
                )
            if i > 0:
                if aval[i - 1].get("product.product") != aval[i].get("product.product"):
                    b.append(
                        f"{chr(10)}<strong><u>{aval[i].get('product.product')}</u></strong>{chr(10)}{chr(10)}"
                        f"{aval[i].get('division')} {aval[i].get('available')}{chr(10)}"
                    )
                if aval[i - 1].get("product.product") == aval[i].get("product.product"):
                    b.append(
                        f"{aval[i].get('division')} {aval[i].get('available')}{chr(10)}"
                    )
        try:
            await message.answer("".join(b))
            text = "".join(b)
            logging.info(f"Пользователь {message.from_user.id} получил ответ {text}")
        except err:
            await message.answer(
                f"Вероятно слишком длинное сообщение{chr(10)}"
                f"Попробуйте конкретизировать данные для поиска"
            )
            logging.info(
                f"Вероятно слишком длинное сообщение{chr(10)}"
                f"Попробуйте конкретизировать данные для поиска"
            )

    if len(aval) == 0:
        await message.answer("Остатков на других подразделениях нет")


async def analog_avail_stock_answer(message, val, analog_type):
    if analog_type == "По товару":
        aval = await get_available_stock_analog_nomenclature_product(val)
    if analog_type == "По веществу":
        aval = await get_available_stock_analog_nomenclature_substance(val)
    b = []
    if len(aval) > 0:
        await message.answer(
            f"<strong>*****Свободно на РУ с подбором по действующему веществу*****</strong>{chr(10)}{chr(10)}"
        )
        for i in range(len(aval)):
            if i == 0:
                b.append(
                    f"{chr(10)}<strong><u>{aval[i].get('product.product')}</u></strong>{chr(10)}{chr(10)}"
                    f"Действуещее вещество {aval[i].get('product.active_substance')}{chr(10)}"
                    f"{aval[i].get('division')} {aval[i].get('available')}{chr(10)}"
                )
            if i > 0:
                if aval[i - 1].get("product.product") != aval[i].get("product.product"):
                    b.append(
                        f"{chr(10)}<strong><u>{aval[i].get('product.product')}</u></strong>{chr(10)}{chr(10)}"
                        f"Действуещее вещество {aval[i].get('product.active_substance')}{chr(10)}"
                        f"{aval[i].get('division')} {aval[i].get('available')}{chr(10)}"
                    )
                if aval[i - 1].get("product.product") == aval[i].get("product.product"):
                    b.append(
                        f"{aval[i].get('division')} {aval[i].get('available')}{chr(10)}"
                    )
        try:
            await message.answer("".join(b))
            text = "".join(b)
            logging.info(f"Пользователь {message.from_user.id} получил ответ {text}")
        except err:
            await message.answer(
                f"Вероятно слишком длинное сообщение{chr(10)}"
                f"Попробуйте конкретизировать данные для поиска"
            )
            logging.info(
                f"Вероятно слишком длинное сообщение{chr(10)}"
                f"Попробуйте конкретизировать данные для поиска"
            )

    if len(aval) == 0:
        await message.answer(
            "По данному запросу ничего не найдено. Попробуйте изменить запрос или вид запроса."
        )
