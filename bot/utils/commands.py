from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="Остатки", description="Вывести остатки"),
        BotCommand(command="Заявки", description="Вывести заявки"),
        BotCommand(command="Доступность", description="Вывести доступность"),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
