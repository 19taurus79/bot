import asyncio
import logging

# from middlewares import first_contact
from handlers import (
    echo,
    remains,
    submissions,
    av_stocks,
)

# from aiogram.client.session.aiohttp import ClientSession, AiohttpSession


from utils.commands import set_commands
from create_bot import bot, dp


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    # dp.message.outer_middleware(first_contact.FirstContactMiddleware())
    # await set_commands(bot)
    # dp.include_router(first_contact_handler.router)
    # dp.include_router(inline_kb_test.router)
    # dp.include_router(remains.router)
    dp.include_router(submissions.router)
    dp.include_router(remains.router)
    dp.include_router(av_stocks.router)
    dp.include_router(echo.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
