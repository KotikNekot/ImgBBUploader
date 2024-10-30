from imgbb import delete_image, upload_image
from config import TELEGRAM_TOKEN

from aiogram import Bot,Dispatcher,F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message,CallbackQuery,InlineKeyboardMarkup,InlineKeyboardButton

import asyncio

dp = Dispatcher()


@dp.message(F.photo)
async def upload_image_handler(message: Message) -> None:
    original_image_size = message.photo[-1]
    file = await message.bot.get_file(original_image_size.file_id)
    binary_image = await message.bot.download_file(file.file_path)

    image = await upload_image(binary_image)

    await message.answer(
        image.url,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Удалить", callback_data=f"delete:{image.delete_url}"),
                ]
            ]
        )
    )

@dp.callback_query(F.data.startswith("delete:"))
async def delete_image_handler(call: CallbackQuery):
    url = call.data.removeprefix("delete:")
    result = await delete_image(url)

    await call.answer(
        "Удалено." if result else "Не получилось!"
    )


async def main() -> None:
    bot = Bot(
        token=TELEGRAM_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
