
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import ChatMemberUpdatedFilter, MEMBER, KICKED
from aiogram.enums import ChatMemberStatus
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

user_cache = set()

@dp.chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER))
async def on_user_join(event: types.ChatMemberUpdated):
    user_id = event.from_user.id
    chat_id = event.chat.id

    if user_id in user_cache:
        return

    user_cache.add(user_id)

    markup = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="✅ Подтвердить", callback_data="verify")]]
    )
    msg = await bot.send_message(chat_id, f"Привет, {event.from_user.first_name}! Подтверди, что ты не бот.", reply_markup=markup)

    await asyncio.sleep(60)
    if user_id in user_cache:
        await bot.ban_chat_member(chat_id, user_id)
        await bot.delete_message(chat_id, msg.message_id)
        user_cache.remove(user_id)

@dp.callback_query(lambda call: call.data == "verify")
async def on_verify(call: types.CallbackQuery):
    user_id = call.from_user.id
    chat_id = call.message.chat.id

    if user_id in user_cache:
        user_cache.remove(user_id)
        await call.message.edit_text("✅ Вы прошли проверку!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
