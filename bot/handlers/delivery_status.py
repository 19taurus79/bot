from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from utils.message.submissions_answer import submissions_answer
from aiogram.fsm.state import StatesGroup, State
from handlers.remains import CommandBot
from aiogram.fsm.context import FSMContext
from handlers.remains import CommandBot
from middlewares.user_validator import managers_id

from utils.message.submissions_answer import submissions_delivery_status

router = Router()


@router.message(Command("delivery_status"))
async def delivery_status(message: Message):
    await message.delete()
    manager_id = message.from_user.id
    manager = next(ch for ch, code in managers_id.items() if code == manager_id)
    await submissions_delivery_status(message, manager)



@router.message(CommandBot.choosing_submissions_nomenclature)
async def submission_with_nomenclature(message: Message, state: FSMContext):
    nomenclature = message.text
    await submissions_answer(message, nomenclature)
    await state.clear()
