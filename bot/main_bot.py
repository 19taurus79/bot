import asyncio
import logging

from middlewares import user_validator
from handlers import (
    echo,
    remains,
    submissions,
    av_stocks,
    remains_seeds,
    analog_selection,
)


from create_bot import bot, dp
from aiogram.types import BotCommand


async def main():
    file_log = logging.FileHandler("log/Log.log")
    console_out = logging.StreamHandler()
    logging.basicConfig(
        handlers=(file_log, console_out),
        level=logging.INFO,
        datefmt="%m.%d.%Y %H:%M:%S",
        format="[%(asctime)s | %(levelname)s]: %(message)s",
    )
    await bot.set_my_commands(
        [
            BotCommand(command="/remains", description="Получить остатки"),
            BotCommand(command="/submissions", description="Получить заявки"),
            BotCommand(
                command="/avail_stock",
                description="Поиск свободных остатков по складам",
            ),
            BotCommand(command="/seeds", description="Остатки семян с показателями"),
            BotCommand(command="/analog", description="Подбор аналога"),
        ]
    )
    dp.message.outer_middleware(user_validator.ManagerValidatorMiddleware())
    # await set_commands(bot)
    # dp.include_router(first_contact_handler.router)
    dp.include_router(analog_selection.router)
    dp.include_router(remains_seeds.router)
    dp.include_router(submissions.router)
    dp.include_router(remains.router)
    dp.include_router(av_stocks.router)
    dp.include_router(echo.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
