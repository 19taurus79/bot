import logging

from utils.db.remains import get_remains_series, get_summary_remains
from utils.db.submissions import quantity_under_orders
from aiogram.exceptions import TelegramBadRequest as err


async def remains_answer_series(message, val):
    await message.answer(f"<b>*****Отатки с партиями*****</b>{chr(10)}{chr(10)}")
    ans = await get_remains_series(val)
    under_orders = await quantity_under_orders(val)
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
        except err:
            await message.answer(
                f"Вероятно под Ваш критерий попало слишко много товаров{chr(10)}"
                f"Попробуйте конкретизировать данные для поиска"
            )
    if len(ans) == 0:
        await message.answer("Остатков нет")


async def remains_answer_summary(message, val):
    await message.answer(f"<b>*****Отатки*****</b>{chr(10)}{chr(10)}")
    ans = await get_summary_remains(val)
    under_orders = await quantity_under_orders(val)
    under_orders_dict = {}
    for i in under_orders:
        under_orders_dict[i.get("product.product")] = i.get("sum")
    a = []

    # for i in ans:
    #     get_prod = i.get('product.product')
    #     under = under_orders_dict.get(get_prod)
    #     if get_prod in under_orders_dict:
    #         print(f"{get_prod} под заявками {under}")
    #     if get_prod not in under_orders_dict:
    #         print(f"{get_prod} под заявками нет")

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
                a.append(
                    f"<strong><u>{ans[i].get('product.product')}{chr(10)}"
                    f"Бухгалтерия {ans[i].get('buh')} Склад {ans[i].get('skl')}{chr(10)}"
                    f"Под заявками {under_orders_dict.get(get_prod)}{chr(10)}"
                    f"Свободного на складе {ans[i].get('buh')-under_orders_dict.get(get_prod)}{chr(10)}{chr(10)}</u></strong>"
                )

        await message.answer("".join(a))
        text = "".join(a)
        logging.info(f"Пользователь {message.from_user.id} получил ответ {text}")
    if len(ans) == 0:
        await message.answer("Остатков нет")
