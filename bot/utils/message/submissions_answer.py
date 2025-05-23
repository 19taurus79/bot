import logging
from aiogram.types import ReplyKeyboardRemove

from utils.db.submissions import get_submissions, quantity_under_orders
from aiogram.exceptions import TelegramBadRequest as err

from utils.db.submissions import get_submissions_delivery_status


async def submissions_answer(message, val):
    await message.answer(f"<strong>*****Заявки*****</strong>{chr(10)}{chr(10)}")
    b = []
    sub = await get_submissions(val)

    if len(sub) > 0:
        for i in range(len(sub)):
            if i == 0:
                b.append(
                    f"<b><u>{sub[i].get('product.product')}</u></b>{chr(10)}<i>{sub[i].get('manager')}</i>{chr(10)}{sub[i].get('client')} {sub[i].get('different')}{chr(10)}"
                )
            if i > 0:
                if sub[i - 1].get("product.product") != sub[i].get("product.product"):
                    b.append(
                        f"<b><u>{sub[i].get('product.product')}</u></b>{chr(10)}<i>{sub[i].get('manager')}</i>{chr(10)}{sub[i].get('client')} {sub[i].get('different')}{chr(10)}"
                    )
                if sub[i - 1].get("product.product") == sub[i].get("product.product"):
                    if sub[i - 1].get("manager") != sub[i].get("manager"):
                        b.append(
                            f"<i>{sub[i].get('manager')}</i>{chr(10)}{sub[i].get('client')} {sub[i].get('different')}{chr(10)}"
                        )
                    if sub[i - 1].get("manager") == sub[i].get("manager"):
                        b.append(
                            f"{sub[i].get('client')} {sub[i].get('different')} {chr(10)}"
                        )
        try:
            await message.answer("".join(b), reply_markup=ReplyKeyboardRemove())
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
    if len(sub) == 0:
        await message.answer("Заявок нет", reply_markup=ReplyKeyboardRemove())

async def submissions_delivery_status(message, manager):

    b = []
    sub = await get_submissions_delivery_status(manager)

    if len(sub) > 0:
        for i in range(len(sub)):
                b.append(
                    f"<i>{sub[i].get('client')}</i>{chr(10)}{sub[i].get('product.product')} {sub[i].get('different')}{chr(10)}{chr(10)}"
                )
        try:
            await message.answer(f"<strong>***** Заявки с семенами и статусом 'Ні до постачання' *****</strong>{chr(10)} У менеджера {manager}{chr(10)}")
            await message.answer("".join(b), reply_markup=ReplyKeyboardRemove())
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
    if len(sub) == 0:
        await message.answer("Заявок с таким статусом нет", reply_markup=ReplyKeyboardRemove())
