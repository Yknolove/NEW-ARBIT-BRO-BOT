import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_webhook
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load environment variables from .env if present
load_dotenv()

# Environment variables
BOT_TOKEN    = os.getenv("BOT_TOKEN")
WEBHOOK_URL  = os.getenv("WEBHOOK_URL")  # https://…/webhook
WEBHOOK_PATH = "/webhook"
PORT         = int(os.environ.get("PORT", 8443))

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Main menu keyboard
def main_menu_keyboard():
    """Return persistent menu for the bottom of the chat."""
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("⚙️ Настройки", "📈 Калькулятор")
    kb.row("📜 История", "🔥 Топ-сделки")
    return kb

# Handlers
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.reply(
        "Привет! Я ArbitPRO-бот. Выберите действие:",
        reply_markup=main_menu_keyboard()
    )

@dp.message_handler(commands=["ping"])
async def cmd_ping(message: types.Message):
    await message.reply("pong")


# Handlers for persistent menu buttons
@dp.message_handler(lambda m: m.text == "⚙️ Настройки")
async def menu_settings(message: types.Message):
    await message.answer("Здесь будут настройки пользователя.")

@dp.message_handler(lambda m: m.text == "📈 Калькулятор")
async def menu_calculator(message: types.Message):
    await message.answer("Здесь калькулятор прибыли.")

@dp.message_handler(lambda m: m.text == "📜 История")
async def menu_history(message: types.Message):
    await message.answer("Здесь история сделок.")

@dp.message_handler(lambda m: m.text == "🔥 Топ-сделки")
async def menu_top_deals(message: types.Message):
    await message.answer("Архив топ-сделок дня.")

# Startup and shutdown
async def on_startup(_):
    logging.info("Setting webhook…")
    await bot.set_webhook(WEBHOOK_URL)
    logging.info(f"Webhook set to {WEBHOOK_URL}")

async def on_shutdown(_):
    logging.info("Deleting webhook…")
    await bot.delete_webhook()

if __name__ == "__main__":
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host="0.0.0.0",
        port=PORT,
    )




