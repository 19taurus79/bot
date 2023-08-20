import logging

from utils.db.remains import (
    get_remains_series,
    get_summary_remains,
    get_remains_series_seeds,
    get_remains_analog_nomenclature_in_our_warehouse_product,
    get_remains_analog_nomenclature_in_our_warehouse_substance,
)
from utils.db.available_stock import get_available_stock_analog_nomenclature_product
from utils.db.submissions import quantity_under_orders
from aiogram.exceptions import TelegramBadRequest as err


async def remains_answer_series(message, val):
    await message.answer(f"<b>*****Остатки с партиями*****</b>{chr(10)}{chr(10)}")
    ans = await get_remains_series(val)
    a = []
    if len(ans) > 0:
        for i in range(len(ans)):
            if i == 0:
                a.append(
                    f"<strong><u>{ans[i].get('product.product')}</u></strong>{chr(10)}"
                    f"Партия {ans[i].get('nomenclature_series')} по бухгалтерии {ans[i].get('buh')} по складу {ans[i].get('skl')}{chr(10)}"
                )
            if i > 0:
                if ans[i - 1].get("product.product") != ans[i].get("product.product"):
                    a.append(
                        f"<strong><u>{ans[i].get('product.product')}</u></strong>{chr(10)}"
                        f"Партия {ans[i].get('nomenclature_series')} по бухгалтерии {ans[i].get('buh')} по складу {ans[i].get('skl')}{chr(10)}"
                    )
                if ans[i - 1].get("product.product") == ans[i].get("product.product"):
                    a.append(
                        f"Партия {ans[i].get('nomenclature_series')} по бухгалтерии {ans[i].get('buh')} по складу {ans[i].get('skl')}{chr(10)}"
                    )
        try:
            await message.answer("".join(a))
            text = "".join(a)
            logging.info(f"Пользователь {message.from_user.id} получил ответ {text}")
        except err:
            await message.answer(
                f"Вероятно под Ваш критерий попало слишко много товаров{chr(10)}"
                f"Попробуйте конкретизировать данные для поиска"
            )
    if len(ans) == 0:
        await message.answer("Остатков нет")


async def remains_answer_summary(message, val):
    await message.answer(f"<b>*****Остатки*****</b>{chr(10)}{chr(10)}")
    ans = await get_summary_remains(val)
    under_orders = await quantity_under_orders(val)
    under_orders_dict = {}
    for i in under_orders:
        under_orders_dict[i.get("product.product")] = i.get("sum")
    a = []

    if len(ans) > 0:
        # get_prod = ans[i].get("product.product")
        for i in range(len(ans)):
            get_prod = ans[i].get("product.product")
            if get_prod not in under_orders_dict:
                a.append(
                    f"<strong><u>{ans[i].get('product.product')}{chr(10)}"
                    f"Бухгалтерия {ans[i].get('buh')} Склад {ans[i].get('skl')}{chr(10)}"
                    f"Весь остаток свободен </u></strong>{chr(10)}{chr(10)}"
                )
            if get_prod in under_orders_dict:
                aval = ans[i].get("buh") - under_orders_dict.get(get_prod)
                if aval <= 0:
                    a.append(
                        f"<strong><u>{ans[i].get('product.product')}{chr(10)}"
                        f"Бухгалтерия {ans[i].get('buh')} Склад {ans[i].get('skl')}{chr(10)}"
                        f"Под заявками {under_orders_dict.get(get_prod)}{chr(10)}"
                        f"Свободного остатка на складе нет</u></strong>{chr(10)}{chr(10)}"
                    )
                if aval > 0:
                    a.append(
                        f"<strong><u>{ans[i].get('product.product')}{chr(10)}"
                        f"Бухгалтерия {ans[i].get('buh')} Склад {ans[i].get('skl')}{chr(10)}"
                        f"Под заявками {under_orders_dict.get(get_prod)}{chr(10)}"
                        f"Свободного на складе {ans[i].get('buh') - under_orders_dict.get(get_prod)}{chr(10)}{chr(10)}</u></strong>"
                    )

        await message.answer("".join(a))
        text = "".join(a)
        logging.info(f"Пользователь {message.from_user.id} получил ответ {text}")
    if len(ans) == 0:
        await message.answer("Остатков нет")


async def remains_answer_series_seeds(message, val):
    await message.answer(
        f"<b>*****Отатки семян с показателями*****</b>{chr(10)}{chr(10)}"
    )
    ans = await get_remains_series_seeds(val)
    a = []
    if len(ans) > 0:
        for i in range(len(ans)):
            if i == 0:
                a.append(
                    f"<strong><u>{ans[i].get('product.product')}</u></strong>{chr(10)}"
                    f"Партия {ans[i].get('nomenclature_series')} по бухгалтерии {ans[i].get('buh')} по складу {ans[i].get('skl')}{chr(10)}"
                    f"Год урожая {ans[i].get('crop_year')}{chr(10)}"
                    f"Страна происхождения {ans[i].get('origin_country')}{chr(10)}"
                    f"Всхожесть {ans[i].get('germination')}{chr(10)}"
                    f"Масса тысячи {ans[i].get('mtn')}{chr(10)}"
                    f"Вес мешка {ans[i].get('weight')}{chr(10)}"
                )
            if i > 0:
                if ans[i - 1].get("product.product") != ans[i].get("product.product"):
                    a.append(
                        f"<strong><u>{ans[i].get('product.product')}</u></strong>{chr(10)}"
                        f"Партия {ans[i].get('nomenclature_series')} по бухгалтерии {ans[i].get('buh')} по складу {ans[i].get('skl')}{chr(10)}"
                        f"Год урожая {ans[i].get('crop_year')}{chr(10)}"
                        f"Страна происхождения {ans[i].get('origin_country')}{chr(10)}"
                        f"Всхожесть {ans[i].get('germination')}{chr(10)}"
                        f"Масса тысячи {ans[i].get('mtn')}{chr(10)}"
                        f"Вес мешка {ans[i].get('weight')}{chr(10)}"
                    )
                if ans[i - 1].get("product.product") == ans[i].get("product.product"):
                    a.append(
                        f"Партия {ans[i].get('nomenclature_series')} по бухгалтерии {ans[i].get('buh')} по складу {ans[i].get('skl')}{chr(10)}"
                        f"Год урожая {ans[i].get('crop_year')}{chr(10)}"
                        f"Страна происхождения {ans[i].get('origin_country')}{chr(10)}"
                        f"Всхожесть {ans[i].get('germination')}{chr(10)}"
                        f"Масса тысячи {ans[i].get('mtn')}{chr(10)}"
                        f"Вес мешка {ans[i].get('weight')}{chr(10)}"
                    )
        try:
            await message.answer("".join(a))
        except err:
            await message.answer(
                f"Вероятно под Ваш критерий попало слишко много товаров{chr(10)}"
                f"Попробуйте конкретизировать данные для поиска"
            )
    if len(ans) == 0:
        await message.answer("Остатков нет")


async def remains_answer_analog_nomenclature(message, val, analog_type):
    if analog_type == "По товару":
        ans = await get_remains_analog_nomenclature_in_our_warehouse_product(val)
    if analog_type == "По веществу":
        ans = await get_remains_analog_nomenclature_in_our_warehouse_substance(val)
    a = []
    if len(ans) > 0:
        for i in range(len(ans)):
            if i == 0:
                a.append(
                    f"<strong><u>{ans[i].get('product.product')}</u></strong>{chr(10)}"
                    f"Действуещее вещество {ans[i].get('active_substance')} по бухгалтерии {ans[i].get('buh')} по складу {ans[i].get('skl')}{chr(10)}"
                )
            if i > 0:
                if ans[i - 1].get("product.product") != ans[i].get("product.product"):
                    a.append(
                        f"<strong><u>{ans[i].get('product.product')}</u></strong>{chr(10)}"
                        f"Действуещее вещество {ans[i].get('active_substance')} по бухгалтерии {ans[i].get('buh')} по складу {ans[i].get('skl')}{chr(10)}"
                    )
                if ans[i - 1].get("product.product") == ans[i].get("product.product"):
                    a.append(
                        f"Действуещее вещество {ans[i].get('active_substance')} по бухгалтерии {ans[i].get('buh')} по складу {ans[i].get('skl')}{chr(10)}"
                    )
        await message.answer(
            f"<b>*****Отатки товара с подбором по действующему веществу*****</b>{chr(10)}{chr(10)}"
        )
        try:
            await message.answer("".join(a))
        except err:
            await message.answer(
                f"Вероятно под Ваш критерий попало слишко много товаров{chr(10)}"
                f"Попробуйте конкретизировать данные для поиска"
            )
    if len(ans) == 0:
        await message.answer(
            "По данному запросу ничего не найдено. Попробуйте изменить запрос или вид запроса."
        )
