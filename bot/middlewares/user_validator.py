from typing import Callable, Dict, Any, Awaitable
import logging
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

managers_id = {
    "Онищенко": 548019148,
    "Скирда": 392207160,
    "Цовма": 979678923,
    "Гаража": 5072996747,
    "Поливода": 811507369,
    "Шпак": 1779116530,
    "Гуржий": 819553841,
    "Онищенко рабочий": 1060393824,
    "Чех": 1600296306,
}
managers = managers_id.values()


def _is_manager(message: Message) -> bool:
    return message.from_user.id in managers


class ManagerValidatorMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if _is_manager(event):
            return await handler(event, data)
        else:
            await event.answer(
                "Вы не зарегистрированы. Можно ввести фамилию и обратитесь к"
                " разработчику открытия доступа."
            )
            logging.info(
                f"Пользователь {event.from_user.id} отправил команду {event.text}"
            )
