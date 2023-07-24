from utils.db.available_stock import get_available_stock
from aiogram.exceptions import TelegramBadRequest as err


async def avail_stock_answer(message, val):
    await message.answer(f"<strong>*****Свободно на РУ*****</strong>{chr(10)}{chr(10)}")
    aval = await get_available_stock(val)
    b = []
    if len(aval) > 0:
        for i in range(len(aval)):
            if i == 0:
                # if aval[i].get("buying_season") is None:
                #     b.append(
                #         f"{chr(10)}<strong><u>{aval[i].get('product')}</u></strong>{chr(10)}{chr(10)}"
                #         f"{aval[i].get('division')} {aval[i].get('available')}{chr(10)}"
                #     )
                #
                # if aval[i].get("buying_season") is not None:
                #     b.append(
                #         f"{chr(10)}<strong><u>{aval[i].get('product')}</u></strong>{chr(10)}{chr(10)}"
                #         f"{aval[i].get('buying_season')}{chr(10)}"
                #         f"{aval[i].get('division')} {aval[i].get('available')}{chr(10)}"
                #     )
                b.append(
                    f"{chr(10)}<strong><u>{aval[i].get('product.product')}</u></strong>{chr(10)}{chr(10)}"
                    f"{aval[i].get('division')} {aval[i].get('available')}{chr(10)}"
                )
            if i > 0:
                if aval[i - 1].get("product.product") != aval[i].get("product.product"):
                    # if aval[i].get("buying_season") is None:
                    #     b.append(
                    #         f"{chr(10)}<strong><u>{aval[i].get('product')}</u></strong>{chr(10)}{chr(10)}"
                    #         f"{aval[i].get('division')} {aval[i].get('available')}{chr(10)}"
                    #     )
                    # if aval[i].get("buying_season") is not None:
                    #     b.append(
                    #         f"{chr(10)}<strong><u>{aval[i].get('product')}</u></strong>{chr(10)}{chr(10)}"
                    #         f"{aval[i].get('buying_season')}{chr(10)}"
                    #         f"{aval[i].get('division')} {aval[i].get('available')}{chr(10)}"
                    #     )
                    b.append(
                        f"{chr(10)}<strong><u>{aval[i].get('product.product')}</u></strong>{chr(10)}{chr(10)}"
                        f"{aval[i].get('division')} {aval[i].get('available')}{chr(10)}"
                    )
                if aval[i - 1].get("product.product") == aval[i].get("product.product"):
                    #             if aval[i].get("buying_season") is None:
                    #                 b.append(
                    #                     f"{aval[i].get('division')} {aval[i].get('available')}{chr(10)}"
                    #                 )
                    #             if aval[i].get("buying_season") is not None:
                    #                 b.append(
                    #                     f"{aval[i].get('buying_season')}{chr(10)}"
                    #                     f"{aval[i].get('division')} {aval[i].get('available')}"
                    #                 )
                    b.append(
                        f"{aval[i].get('division')} {aval[i].get('available')}{chr(10)}"
                    )
        try:
            await message.answer("".join(b))
        except err:
            await message.answer(
                f"Вероятно слишком длинное сообщение{chr(10)}"
                f"Попробуйте конкретизировать данные для поиска"
            )

    if len(aval) == 0:
        await message.answer("Остатков на других подразделениях нет")
