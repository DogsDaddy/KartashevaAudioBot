import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# Настройки бота
BOT_TOKEN = "7851065276:AAH5lGU8QO2rMM0UBX35yqDFz7AH5LgvABQ"
CHANNEL_ID = "-1002203758947"
WEB_APP_URL = "https://dogsdaddy.github.io/KartashevaAudioBot"

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Функция для команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    # Проверяем подписку
    user_id = update.effective_user.id
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        if member.status in ["member", "administrator", "creator"]:
            # Создаём кнопку для мини-приложения
            keyboard = [
                [InlineKeyboardButton("Открыть плеер", web_app={"url": WEB_APP_URL})]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                f"Привет, {user.first_name}! Ты подписан. Нажми кнопку, чтобы открыть плеер с аудиокнигами.",
                reply_markup=reply_markup,
            )
        else:
            await update.message.reply_text(
                "Ты не подписан на канал. Подпишись, чтобы получить доступ к аудиокнигам!"
            )
    except Exception as e:
        logger.error(f"Ошибка при проверке подписки: {e}")
        await update.message.reply_text(
            "Произошла ошибка. Попробуй позже или свяжись с поддержкой."
        )


# Основная функция
def main():
    # Создаём приложение
    application = Application.builder().token(BOT_TOKEN).build()

    # Добавляем обработчик команды
    application.add_handler(CommandHandler("start", start))

    # Запускаем бота
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
